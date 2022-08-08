import time
start = time.perf_counter()
import psycopg2
import os, sys
import csv
import json
import ast
import configparser
import pandas as pd
import datetime as dt
import concurrent.futures
from functools import partial
from bs4 import BeautifulSoup
from multiprocessing import Pool, freeze_support, Process
from datetime import datetime, date, timedelta
from psycopg2.extras import Json
from psycopg2 import sql



# telethon imports
from telethon import client, errors
from telethon.tl.types import UserStatusOnline, UserStatusOffline, ContactStatus, ChannelParticipantsSearch, InputPeerEmpty, PeerUser, PeerChat, PeerChannel
from telethon.tl.functions.channels import GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.sync import TelegramClient


# ____ local imports _____
from Config import payload, cred


# __________Pandas Settings____________
pd.options.display.max_columns = None           
# pd.options.display.max_rows = None              
pd.options.display.max_colwidth = 20            
pd.options.display.width = 2000

#  __________________ LONG IN GLOBALS __________________

def get_api_values(name):              
	api_id = cred[name]['API_ID']
	api_hash = cred[name]['API_HASH']
	phone = cred[name]['phone']
	return api_id, api_hash, phone

## _____________________________ DATAFRAME __________________________________________________________

def get_channel_names(url):
	channel_name = url.split('/')[3]
	return channel_name


def get_links():
	'''
	Gets a csv file of the targets (dataframe) from Input folder, 
	then returns a list of links and slugs
	'''
	links = pd.read_csv('Input/telegram_links_input.csv')   	
	slugs = list(links['Slug'])
	links = list(links['Telegram links'])
	return  links, slugs   


def member_count(channel_full_info, link, yesterday_df, slug):

	'''
	This is core task of this project, it's job is to mainly get two things:
		1. all of the members of channel(X)
		2. all the online members of channel(X)

		[but also some extra info, such as ]
		3. channel_username, 
		4. channel_id,  
		5. photo_date, 
		6. total_messages, 
		7. messages_today
		
		[then it adds data we already have]
		8. link, 
		9. slug,  

	Finally it returns a dataframe of the data.
	'''
	member_count = channel_full_info.full_chat.participants_count
	online_count = channel_full_info.full_chat.online_count
	channel_username = channel_full_info.chats[0].username
	channel_slug = slug
	channel_id = channel_full_info.full_chat.id
	timestamp = datetime.today().replace(hour = 0, microsecond = 0, second = 0, minute = 0).strftime("%Y.%m.%d")
	try:
		photo_date = channel_full_info.full_chat.chat_photo.date
		photo_date = photo_date.strftime("%Y.%m.%d")
	except AttributeError:
		print("'PhotoEmpty' object has no attribute 'date'")
		photo_date=""
	read_outbox = channel_full_info.full_chat.read_outbox_max_id    
	read_inbox = channel_full_info.full_chat.read_inbox_max_id      # Maybe Not nessasary
	unread_count = channel_full_info.full_chat.unread_count         # Maybe Not nessasary
	total_messages = read_outbox + read_inbox + unread_count        # Maybe Not nessasary
	if yesterday_df.empty:
		messages_today = 0
	else:
		messages_today = total_messages - int(yesterday_df['total_messages'])
	channel_info = pd.DataFrame([channel_username, slug,  channel_id,  member_count,  
								  online_count, link, photo_date, total_messages, messages_today],  
								index = ['channel_username','slug','channel_id','member_count',
										 'online_count', 'link', 'possible_creation_date','total_messages', 'messages_today'],
								columns = [timestamp]).T
	return channel_info, timestamp, channel_username


#  _________________________________ YESTEDAY SECTION _________________________________
'''
Yesterday section: 
	This section gets all the nessasary data from yesterdays scrape.
	it's primarily used to calculate changes in messages. 
'''

def Yesterday_str(yesterday):
	yesterday_str = str(yesterday).replace(" ","-")
	return yesterday_str

def Yesterday_datetime():
	yesterday = datetime.today().replace(hour=0, microsecond = 0, second = 0, minute = 0) - timedelta(days = 1)
	yesterday = yesterday.strftime("%Y.%m.%d")
	return yesterday


def Yesterday_ids(links):
	yesterday_ids = [link.split('/')[3] for link in links]
	return yesterday_ids


def get_yesterdays(df_old, yesterday):
	yesterdate = pd.DataFrame(index=[yesterday])
	df_old.index = pd.DatetimeIndex(df_old.index)
	df_old.index = df_old.index.strftime("%Y.%m.%d")
	if len(df_old)==1:
		print(" yesterday_df = df_old")
		yesterday_df = df_old
	else:
		print("     else has occored in get_yesterdays")
		try:
			print("         yesterday_df = df_old.loc[yesterdate.index]")
			yesterday_df = df_old.loc[yesterdate.index]
		except:
			print("         Error, needs to change df_old index, fixing issue")
			df_old.index = df_old.index.strftime("%Y.%m.%d")
			yesterday_df = df_old.loc[yesterdate.index]
	return yesterday_df


def Yesterday():
	yesterday = date.today() - timedelta(days=1)
	yesterday.strftime("%d.%m.%Y")
	return yesterday

# |____________________________________________________________________________________|




# _____________________________________________ POSTGRES _________________________________________________

# ______________________________________ PREP ____________________________________

def parse_config():
	dbname = payload['dbname']
	host = payload['host']
	user = payload['user']
	password = payload['password']
	tablename = payload['tablename']
	return dbname, host, user, password, tablename

dbname, host, user, password, tablename =  parse_config()

def get_connection():
	return psycopg2.connect(
		dbname = payload['dbname'], 
		host = payload['host'], 
		user = payload['user'], 
		password = payload['password'])

def get_cursor(conn):
	return conn.cursor()

def create_table(conn):
	curr = conn.cursor()
	create_table = """CREATE TABLE {} ( id VARCHAR PRIMARY KEY, 
										json_col VARCHAR        );""".format(tablename)
	curr.execute(create_table)
	conn.commit()

# |____________________________________________________________________________________|


# _______________________________ SAVE DATA TO POSTGRES _______________________________

'''
SAVE DATA TO POSTGRES:
	Collections of functions nessasary to save the data collected to the postgress database. 
'''

def check_index(df, df_name):
	if isinstance(df.index, pd.core.indexes.range.RangeIndex):
		print(f"    	{df_name} has incorrect index; set_index(['timestamp']), fixing issue")
		try:
			df.set_index(['timestamp'], inplace = True)
		except KeyError: 
			print("         	Error: None of ['timestamp'] are in the columns")
			print(df)
			print("*"*70)
	return df

def get_old_data(channel):
	conn = get_connection()
	curr = conn.cursor()
	curr.execute(f"SELECT * from {tablename} WHERE id = {'%s'};",(channel,))
	data = curr.fetchall()
	try:
		data = data[0][1]
		data = ast.literal_eval(data)
		df_old = pd.DataFrame.from_dict([data])
		df = pd.DataFrame()
		for i in df_old:
			d = df_old[i][0]
			d = pd.DataFrame.from_dict([d])
			df = pd.concat([df, d], axis = 0) 
		df.set_index(df_old.columns, inplace = True)
		df_old = df.T
		df_old = check_index(df_old, 'df_old')
	except IndexError:
		print(f"    database found no older data for {channel}")
		df_old = pd.DataFrame()  
	return df_old

def make_dict_out(df_old, df_new):
	if df_old.iloc[0].name == df_new.index:
		print("df_old.index = df_new.index")
		df_out = df_new
	else: 
		df_out = pd.concat([df_old, df_new], axis = 0)
	df_out = check_index(df_out, 'df_out')
	df_out.index = df_out.index.astype(str)
	dict_out = df_out.to_dict()

	return df_out, dict_out


def database_upload(curr, tablename, id, dict_obj, df_out):
	conn = get_connection()
	curr = get_cursor(conn)
	curr.execute(f'''
		DELETE FROM {tablename} WHERE id = %s 
		''', (id,))

	
	curr.execute(f'''
		INSERT INTO
			{tablename}(id, json_col) 
		VALUES
			('{id}', %s)
		''', [Json(dict_obj)])
	print("DATAFRAME OUTPUT:")
	print(df_out)
	print()
	conn.commit()
	curr.close()

# |____________________________________________________________________________________|



##  _____________________________________ MULTI PROCESSING _______________________________________

def worker_base(jobs = [], slugs = [], *args, name):
	'''
	the base function for the workers. 
	'''   
	s = 0.1
	api_id, api_hash, phone = get_api_values(name)   
	client = TelegramClient(phone, api_id, api_hash)
	client.connect()
	conn = get_connection()
	curr = get_cursor(conn)
	print(f"Worker: {name} --> api_hash: {api_hash}, api_id: {api_id}")
	yesterday = Yesterday_datetime()


	for link, slug in zip(jobs, slugs):
		channel_name = get_channel_names(link)
		print()
		print("_"*50)
		print(f"  Currently Scraping: {channel_name}")
		conn = get_connection()
		curr = get_cursor(conn)
		time.sleep(s)
		df_old = get_old_data(channel_name)
		try:
			print(f"    database did find yesterday's data for {channel_name}")
			yesterday_df = get_yesterdays(df_old, yesterday)
		except:
			print(f"    database found no yesterday's data for {channel_name}")
			yesterday_df = pd.DataFrame()
		print(f'		| Downloading:	"{channel_name}" |,	then sleep for {s}s.')

		'''
		Gets current data, then tries to save it to database. 

		'''
		try:
			try:

				try:
					channel_full_info = client(GetFullChannelRequest(channel_name))

				except ValueError:
					print(f'        Error: {link} is a bad link, adding to blacklist')
					badlink = pd.DataFrame([link])
					badlink.to_csv('Input/blacklist.csv', mode='a', header=False)

			except errors.rpcerrorlist.AuthKeyUnregisteredError:
				print(f'        Error: The key is not registered in the system, for account: {name}, when handling link: {link}')
				break
		except TypeError:
			print("        TypeError: Cannot cast InputPeerUser to any kind of InputChannel.")		

		df_new, timestamp, channel_username = member_count(channel_full_info, link, yesterday_df, slug)

		if df_old.empty:
			df_out = df_new
		else:
			df_out, dict_out = make_dict_out(df_old, df_new)
		print()
		print("OLD INPUT DATA:")
		print(df_old)
		print()
		print("NEW INPUT DATA:")
		print(df_new)
		print()

		try:     
			database_upload(curr, tablename, id = channel_username, dict_obj = dict_out, df_out=df_out)  
			curr.close()
			conn.commit()
			conn.close()
			print(f'		| Sucsess:	"{channel_name}"	was successfully uploaded to database.	')
			print()
		except psycopg2.errors.UniqueViolation:
			print(f'		| Upload aborted: Todays data for	"{channel_name}"	already exists.	')      
			conn.rollback() 


def gen_workers():
	'''
	generates worker functions (worker_base) based on len(api_keys)
	'''                      
	workers = [partial(worker_base, name = k) for k in cred]                          # <-- TEST  
	return workers


def session_creator(total_jobs, num_workers, JPWS, slugs):
	'''
	2 step process:
		1. session_jobs  ==> total_jobs divided by (len workers * workload pr worker):
		2. work_jobs     ==> the jobs in each session divided by all the workers / split by workload 
	'''
	session_jobs = [total_jobs[i:i+(num_workers*JPWS)] for i in range(0, len(total_jobs), (num_workers*JPWS))]
	work_jobs = [[S[i:i+JPWS] for i in range(0, len(S), JPWS)] for S in session_jobs]

	session_slugs = [slugs[i:i+(num_workers*JPWS)] for i in range(0, len(slugs), (num_workers*JPWS))]
	work_slugs = [[S[i:i+JPWS] for i in range(0, len(S), JPWS)] for S in session_slugs]

	return work_jobs, work_slugs

## |______________________________________________________________________________________________|


# # _____________________________________________ MAIN _________________________________________________

def main(i, session, slug_session):
	'''
	the main function for multi processing 
	'''
	workers = gen_workers()
	with concurrent.futures.ProcessPoolExecutor() as executor:
		results = [executor.submit(W, S, slugs) for W, S, slugs in zip(workers, session, slug_session, )]
	for f  in concurrent.futures.as_completed(results):
		print(f.result())


if __name__ == '__main__':
	print("="*91)
	print("|											  |")
	print("|				STARTING SCRAPING PROCESS				  |")
	print("|											  |")
	print("="*91)	

	s = 900             # sleep time inbetween sessions
	num_workers = 39    # number of workers
	JPWS = 50           # number of Jobs per worker for each session
	dbname, host, user, password, tablename =  parse_config()
	'''
	Checks if a table already exsist, if not, it will create one.
	'''
	conn = get_connection()
	curr = get_cursor(conn)
	try:
		create_table(conn)
	except (Exception, psycopg2.DataError) as error:
		print(error)
		conn = get_connection()    
	links, slugs = get_links()
	sessions, nested_slugs = session_creator(links, num_workers, JPWS, slugs)
	for i, session in enumerate(sessions):
		print(f"________ STARTING SESSION {i} ________")
		main(i, session, nested_slugs[i])
		print("_" * 80)
		print("				NOTIFICATION")
		print(f"	Session {i} has finished")
		print(f'	Finished in {round((time.perf_counter() - start), 2)} second(s)')
		print(f"	NOTE: The program will sleep for {round((s/60),2)} minutes before next session")
		print("_" * 80)
		time.sleep(s)
	print()
	print()
	print("="*91)
	print("|					NOTIFICATION					  |")
	print("|				The Whole Scraping has FINISHED				  |")
	print(f"|				   Finished in {round(time.perf_counter() - start, 2)} second(s)				  |")
	print("="*91)	