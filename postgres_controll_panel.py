'''
Psycopg2 – Insert dictionary as JSON
'''

# __________________________ PREP _____________________________
import psycopg2
from psycopg2.extras import Json
import pandas as pd
import json
import ast
import pprint
''' lcoal import '''
from Config import payload
print(payload)


def parse_config():
    dbname = payload['dbname']
    host = payload['host']
    user = payload['user']
    password = payload['password']
    tablename = payload['tablename']
    return dbname, host, user, password, tablename

def get_connection():
    return psycopg2.connect(
        dbname = dbname, 
        host = host, 
        user = user, 
        password = password)

def get_cursor(conn):
    # returns cursor
    return conn.cursor()

def create_table(conn):
    curr = conn.cursor()
    table = 'daily_monitor'
    create_table = """CREATE TABLE {} (id VARCHAR PRIMARY KEY, 
                                       json_col VARCHAR,)
                                       ;""".format(table)
    curr.execute(create_table)
    conn.commit()

def try_create_table(conn):
    try:
        create_table(conn)
    except (Exception, psycopg2.DataError) as error:
        print(error)
        conn = get_connection()


##  __________________________________ METHOD 1 __________________________________
    # '''
    #     Method 1: 
    #         Setting up a PostgreSQL Database and Table:
    # '''
    # # __________________________ imports __________________________

    # import json



    # # __________________________ insert data ______________________
    # def dict_to_json(value: dict):

    #     # CONVERT DICT TO A JSON STRING AND RETURN
    #     return json.dumps(value)

    # def insert_value(id: str, json_col: str, conn):

    #     # CREATE A CURSOR USING THE CONNECTION OBJECT
    #     curr = conn.cursor()

    #     # EXECUTE THE INSERT QUERY
    #     curr.execute(f'''
    #         INSERT INTO
    #             json_table(id, json_col)
    #         VALUES
    #             ('{id}', '{json_col}')
    #     ''')

    #     # COMMIT THE ABOVE REQUESTS
    #     conn.commit()

    #     # CLOSE THE CONNECTION
    #     conn.close()

    # def main():

    #     # CREATE A PSYCOPG2 CONNECTION
    #     conn = get_connection()

    #     #TRY CREATING TABLE
    #     try_create_table(conn)

    #     # CREATE A PYTHON DICT OBJECT FOR JSON COL
    #     dict_obj = {
    #         "name": "John Smith",
    #         "skill": "Python",
    #         "experience": 2
    #     }

    #     # CONVERT DICT OBJECT TO JSON STRING
    #     json_obj = dict_to_json(value=dict_obj)

    #     # INSERT VALUES IN THE DATABASE TABLE
    #     insert_value(id='JSON002', json_col=json_obj,
    #                 conn=conn)

    # if __name__ == '__main__':
    #     dbname, host, user, password =  parse_config()
    #     main()
## |______________________________________________________________________________|


##  __________________________________ METHOD 2 __________________________________
'''
Method 2: 
    Using the psycopg2 Json adaptation:
'''

from psycopg2.extras import Json

# # __________________________ insert data ____________________

def insert_data(curr, id, dict_obj):
    print("_"*50)
    print()
    print()
    print(dict_obj)
    print()
    print()
    print("_"*50)
    _, _, _, _, tablename =  parse_config()
    curr.execute(f'''
        INSERT INTO
            {tablename}(id, json_col) 
        VALUES
            ('{id}', %s)
    ''', [Json(dict_obj)])    

def insert():
    conn = get_connection()
    curr = get_cursor(conn)
    manual_insert = manualInsertList()
    ids = [i['channel_username'] for i in manual_insert]
    dict_objs = manualInsertList()
    print(f'currently inserting the channels: {ids}')

    ''' EXECUTE THE INSERT QUERY '''
    for id, dict_obj in zip(ids, dict_objs):
        insert_data(curr, id, dict_obj)
  
    ''' COMMIT & CLOSE '''
    curr.close()
    conn.commit()
    conn.close()


# ## |______________________________________________________________________________|

# ##  _______________________________ FETCHING DATA _______________________________


def fetch_data(curr):  
    search_list = searchList()
    search_list = (str(search_list)[1:-1])
    _, _, _, _, tablename =  parse_config()
    if search_list:
        print(f'currently fetching the channels: {search_list}:')
        print("_"*100)
        curr.execute(f"SELECT * from {tablename} WHERE id in ({search_list});") # gets spesific
    elif not search_list:
        curr.execute(f"SELECT * FROM {tablename};") # gets all         
    else:
        print()
        print('''Unknow debug error: 
                The if statemant checking if the list "yesterday_ids" is empty, 
                returned that the list was neither.''')
        print()
    data = curr.fetchall()
    # data = data[0][1]
    df = pd.DataFrame(columns = ['channel_username','slug','channel_id','member_count',
                                 'online_count', 'link', 'possible_creation_date','total_messages', 'messages_today'])
    for row in data:
        d = ast.literal_eval(row[1])
        new_row = pd.DataFrame.from_dict([d])
        df = pd.concat([df, new_row], axis = 0)
    print()
    print('FETCHED DATA AS JSON:')   
    pprint.pprint([ast.literal_eval(i[1]) for i in data])
    print()
    print('FETCHED DATA AS DATAFRAME:')   
    print(df)
    print()
    print("_"*100)


def fetch():
    conn = get_connection()
    curr = conn.cursor()
    fetch_data(curr)
    curr.close()
    conn.commit()
    conn.close()

## |______________________________________________________________________________|

##  _________________________ PURGE TABLE ________________________
def purge_table(curr):
    print("________ !!! WARNING !!! ________")
    print(f'''   you are about to delete ALL the of the current data stored in {tablename}, 
                please make sure to make a backup before proceeding.''')
    print()
    warning = input(f"are you sure you want to purge {tablename}? (y/n): ")
    
    if warning == 'y':
        print(f"purging: {tablename}")
        curr.execute(f"truncate daily_monitor;")
        print(f"The data in {tablename} was purged")

    elif warning == 'Y':
        print(f"purging: {tablename}")
        curr.execute(f"truncate daily_monitor;")
        print(f"The data in {tablename} was purged")
    
    elif warning == 'n':
        print(f"Aborting the purge of {tablename}, the data will not be deleted.")

    elif warning =='N':
        print(f"Aborting the purge of {tablename}, the data will not be deleted.")
    
    else:
        print('''invalied input, please type "y" for yes, or "n" for no, 
                or press "ctrl+c" to close the program.''')
        purge()

def purge():
    conn = get_connection()
    curr = conn.cursor()
    purge_table(curr)
    curr.close()
    conn.commit()
    conn.close()

## |___________________________________________________________________|

def manualInsertList():
    '''
    List of dictionary objects, used for manuell inserts, used by insert()
    '''
    manual_insert = [
                     {   'timestamp':'2022.04.09', 
                         'channel_title':'Etherium Classic', 
                         'channel_username':'ethclassic', 
                         'channel_id':23456789, 
                         'member_count':7000,
                         'online_count':700, 
                         'link':'https//t.me/ethclassic', 
                         'possible_creation_date':'2016.09.13', 
                         'total_messages':482002, 
                         'messages_today':0,                     }, 

                     {   'timestamp':'2022.04.09', 
                         'channel_title':'FTX something something', 
                         'channel_username':'FTX_Official', 
                         'channel_id':23456789, 
                         'member_count':76000,
                         'online_count':7600, 
                         'link':'https//t.me/ethclassic', 
                         'possible_creation_date':'2016.09.13', 
                         'total_messages':690000, 
                         'messages_today':0,                     },
                                                                    ]
    return manual_insert

def searchList():
    '''
    List of channels, used for spesific seaches, used by fetch()
    '''
    # search_list = [ 'RuffChain', 'UniMexNetwork', ]
    search_list = []
    return search_list


if __name__ == '__main__':
    dbname, host, user, password, tablename =  parse_config()

    ''' choose which action you want to do next:'''
    fetch()
    # purge()
    # insert()
    

'''
QUICK USER MANUAL:
    Before usage, remember to update payload in the config file (Config.py), so that the code can accsess the database.
    
    The database admin has three options on the controll panel:
        1. purge()   
        2. insert()  
        3. fetch()   

    purge():
        deletes ALL the data in the database, be WARNED.

    insert():
        ..mainly used for testing and while building the code. 
        manually inserts data from a list of dictionaries named "manual_insert". 
        you'll find the list in the function right above "manualInsert()",
        to change the list, change the values (on the right side of ":") inside the dict "{}", 
        remember to use commas.
        remember to use "" or '' for texts and dates, and do NOT use "" or '' for numbers. 

    fetch():
        simply fetches the data from the database and displays them for you as a dataframe. 
        By default it fetches all of the channels from the database,

        if the user wants to check out one or more specific channles;
        go to the function "searchList()" above and replace the list "search_list" 
        from this (default):
            search_list = []        
        to this (spesific search):
            search_list = [ 'RuffChain', 'UniMexNetwork', ]
        remember to use commas and "" or ''

    HOW TO USE: 
    To use a function simply remove the "#" character before the code to activate it, 
    everything with "#" infront of it will be igrored by the machine. e.g.:
        
        fetch()
        # purge()
        # insert()
            now you have chosen the fetch option.

        # fetch()
        purge()
        # insert()
            now you have chosen the purge option.
'''