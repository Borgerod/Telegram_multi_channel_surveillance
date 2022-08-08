'''
Config
Postgres & Scraper Configuration file, containing: 

	____ Postgres ____
	- payload 

	____ Scraper ____ 	
	- cred 

	____ Common ____ 	
	- proxies


information:
	"payload" = Postgres connection credentials (password, user, host, dbname)
	
	"cred"	  = Login credentials for the telegram scraper, 
				(it logs into a telegram account and uses it to accsess the data).

	"proxies" = There are three different proxies, 
				"proxies" is the common proxy and is the default,
				use "p_proxies" and "s_proxies" if you wish to use different proxies.
				Warning: switching proxies will require some edits of the code. 
'''



# __________________________ POSTGRES __________________________

''' Payload: 
		Replace "payload" with the correct user- and database information for PostgreSQL.'''
payload = {	'dbname'   : 'Telegram_data',
			'host' 	   : 'localhost',
			'user'	   : 'postgres',
        	'password' : 'Orikkel1991',
        	'tablename': 'daily_monitor',  }

'''
example on how it should look like: 
	payload = {	'dbname'   : 'Telegram_data',
				'host' 	   : 'localhost',
				'user'	   : 'postgres',
	        	'password' : 'Password123',
	        	'tablename': 'daily_monitor',  }
'''




# ___ Config Alternatives: Postgres ____
'''
	# Alternative for Payload:
		User and payload as seperate dicts.
	db_payload = { 'dbname'   : 'Telegram_test',
				   'host' 	  : 'localhost',	 } 

	User =	 	 { 'user'	  : 'postgres',
	 		 	   'password' : 'password',   }

		Warning: This does require you to make 
			 	 some small edits to the code.  
'''
'''
				# [Will probobly be removed]
	# Alternative for postgress config; Nested dict:
		# Payload for postgres (password, user, host, dbname) & proxies in one. 

	postgres = {'payload' : { 'dbname'   : 'Telegram_test',
							  'host' 	 : 'localhost',
							  'user'	 : 'postgres',
					       	  'password' : 'password',  			  },

				'proxies' : { 'http'  	 : 'http://10.10.1.10:3128', 
					          'https' 	 : 'https://10.10.1.11:1080', 
					          'ftp'   	 : 'ftp://10.10.1.10:3128',   } }

		# Warning: This does require you to make 
		# 	 	 some small edits to the code.  
'''



# __________________________ SCRAPER __________________________

# Cred 
cred =  { # 'crypto1': {'API_HASH': '2837f41e5ffcbbf08e94c80f3b655497',
		          #    'API_ID': '15416290',
		          #    'App_title': 'register - crypto1',
		          #    'First_name': 'Crypto',
		          #    'Last_name': 'One',
			      #    'Sim_number': '639752920137',
			      #    'phone': '+INSERT_NUMBER'},

		 'crypto10': {'API_HASH': '97a93c17e3a76da2c781e6515b737cff',
		              'API_ID': '12411872',
		              'App_title': 'register - crypto10',
		              'First_name': 'Crypto',
		              'Last_name': 'Ten',
		              'Sim_number': '639752921244', 
		              'phone': '+INSERT_NUMBER'},

		 'crypto11': {'API_HASH': 'fbbe5c9161ddf4d67ae57120f77bb2d2',
		              'API_ID': '12846058',
		              'App_title': 'register - crypto11',
		              'First_name': 'Crypto',
		              'Last_name': 'Eleven',
		              'Sim_number': '639752921245',
		               'phone': '+INSERT_NUMBER'},

		 'crypto12': {'API_HASH': 'bffb9a79b112d8a2a8ca9587d729f3d8',
		              'API_ID': '15085032',
		              'App_title': 'register - crypto12',
		              'First_name': 'Crypto',
		              'Last_name': 'Twelve',
		              'Sim_number': '639752915076', 
		              'phone': '+INSERT_NUMBER'},

		 'crypto13': {'API_HASH': '110a2f345d10dccc0548be5e08da74ab',
		              'API_ID': '17084808',
		              'App_title': 'register - crypto13',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirteen',
		              'Sim_number': '639752920141',
		               'phone': '+INSERT_NUMBER'},

		 'crypto14': {'API_HASH': '1df9794e2ba7713ff7b1b0dad1cca93a',
		              'API_ID': '19445170',
		              'App_title': 'register - crypto14',
		              'First_name': 'Crypto',
		              'Last_name': 'Fourteen',
		              'Sim_number': '639752920128',
		               'phone': '+INSERT_NUMBER'},

		 'crypto15': {'API_HASH': 'e1b97df4023f6c99acb4c92383f1ba8e',
		              'API_ID': '12911280',
		              'App_title': 'register - crypto15',
		              'First_name': 'Crypto',
		              'Last_name': 'Fifteen',
		              'Sim_number': '639752920126',
		               'phone': '+INSERT_NUMBER'},

		 'crypto16': {'API_HASH': '715d947a4361d7fc07e3aa22389b7c93',
		              'API_ID': '17577024',
		              'App_title': 'register - crypto16',
		              'First_name': 'Crypto',
		              'Last_name': 'Sixteen',
		              'Sim_number': '639752920150',
		               'phone': '+INSERT_NUMBER'},

		 'crypto17': {'API_HASH': 'de667a331f39cfd51871749e8d613225',
		              'API_ID': '14746298',
		              'App_title': 'register - crypto17',
		              'First_name': 'Crypto',
		              'Last_name': 'Seventeen',
		              'Sim_number': '639752920145',
		               'phone': '+INSERT_NUMBER'},

		 'crypto18': {'API_HASH': '06284ff7458d8bfc91b777c727a36a9e',
		              'API_ID': '15516553',
		              'App_title': 'register - crypto18',
		              'First_name': 'Crypto',
		              'Last_name': 'Eighteen',
		              'Sim_number': '639752920132',
		               'phone': '+INSERT_NUMBER'},

		 'crypto19': {'API_HASH': '2766eb25011cf3b54427e56c2faed51a',
		              'API_ID': '17744802',
		              'App_title': 'register - crypto19',
		              'First_name': 'Crypto',
		              'Last_name': 'Nineteen',
		              'Sim_number': '639752920136',
		               'phone': '+INSERT_NUMBER'},

		 'crypto2': {'API_HASH': '37d436114ba7e75489803c45d22da7f7',
		             'API_ID': '10943886',
		             'App_title': 'register - crypto2',
		             'First_name': 'Crypto',
		             'Last_name': 'Two',
		             'Sim_number': '639752921248',
		              'phone': '+INSERT_NUMBER'},

		 'crypto20': {'API_HASH': '1fcf847d8ade9efce9fe8924908e801a',
		              'API_ID': '17480306',
		              'App_title': 'register - crypto20',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty',
		              'Sim_number': '639752914991',
		               'phone': '+INSERT_NUMBER'},

		 'crypto21': {'API_HASH': 'b26f92e2efa0991e1a0a42d9d75c2cba',
		              'API_ID': '14975337',
		              'App_title': 'register - crypto21',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-one',
		              'Sim_number': '639455937521',
		               'phone': '+INSERT_NUMBER'},

		 'crypto22': {'API_HASH': '72c6dbefa52a897db9638373925f4b09',
		              'API_ID': '17167780',
		              'App_title': 'register - crypto22',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-two',
		              'Sim_number': '639455937522',
		               'phone': '+INSERT_NUMBER'},

		 'crypto23': {'API_HASH': '06b167b33dced2cc5ccbd059507a74a2',
		              'API_ID': '11949238',
		              'App_title': 'register - crypto23',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-three',
		              'Sim_number': '639455937524',
		               'phone': '+INSERT_NUMBER'},

		 'crypto24': {'API_HASH': 'c4e527a85c1ca7ff5000cd20d890af05',
		              'API_ID': '17770837',
		              'App_title': 'register - crypto24',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-four',
		              'Sim_number': '639455937525',
		               'phone': '+INSERT_NUMBER'},

		 'crypto25': {'API_HASH': '6af84477fb70cf24d6bc00d6f3428ddc',
		              'API_ID': '15355592',
		              'App_title': 'register - crypto25',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-five',
		              'Sim_number': '639761160026',
		               'phone': '+INSERT_NUMBER'},

		 'crypto26': {'API_HASH': '447fe1f9cfb7f118dde9d219e8c0a28f',
		              'API_ID': '13664247',
		              'App_title': 'register - crypto26',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-six',
		              'Sim_number': '639455937518',
		               'phone': '+INSERT_NUMBER'},

		 'crypto27': {'API_HASH': 'dcfda02696ed103c4300d8f06fd5ec9b',
		              'API_ID': '13039270',
		              'App_title': 'register - crypto27',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-seven',
		              'Sim_number': '639455937519',
		               'phone': '+INSERT_NUMBER'},

		 'crypto28': {'API_HASH': '4701c5f23c1dff38514b2383bac1c386',
		              'API_ID': '15492542',
		              'App_title': 'register - crypto28',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-eight',
		              'Sim_number': '639455937520',
		               'phone': '+INSERT_NUMBER'},

		 'crypto29': {'API_HASH': '662c6ee37e2f7d1bfe9d2cd73951b815',
		              'API_ID': '17586647',
		              'App_title': 'register - crypto29',
		              'First_name': 'Crypto',
		              'Last_name': 'Twenty-nine',
		              'Sim_number': '639455937546',
		               'phone': '+INSERT_NUMBER'},

		 'crypto3': {'API_HASH': '5014c38981492541d593e45b22f9506a',
		             'API_ID': '13972273',
		             'App_title': 'register - crypto3',
		             'First_name': 'Crypto',
		             'Last_name': 'Three',
		             'Sim_number': '639752921253',
		              'phone': '+INSERT_NUMBER'},

		 'crypto30': {'API_HASH': 'fe0e3e91d4d6140b30e98128ec92e4df',
		              'API_ID': '10262371',
		              'App_title': 'register - crypto30',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty',
		              'Sim_number': '639455937543',
		               'phone': '+INSERT_NUMBER'},

		 'crypto31': {'API_HASH': 'd1427c6a6215a323e677a2df8215d3ae',
		              'API_ID': '17478863',
		              'App_title': 'register - crypto31',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-one',
		              'Sim_number': '639455937506',
		               'phone': '+INSERT_NUMBER'},

		 'crypto32': {'API_HASH': '782adadba09f8bf680cabc2e199735e7',
		              'API_ID': '13088897',
		              'App_title': 'register - crypto32',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-two',
		              'Sim_number': '639455937507',
		               'phone': '+INSERT_NUMBER'},

		 'crypto33': {'API_HASH': '2f5161f199d9a489673cd8c2a0e2a751',
		              'API_ID': '14181617',
		              'App_title': 'register - crypto33',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-three',
		              'Sim_number': '639455937510',
		               'phone': '+INSERT_NUMBER'},

		 'crypto34': {'API_HASH': 'ece2f7e144be40e3269171fd79cfb079',
		              'API_ID': '12300099',
		              'App_title': 'register - crypto34',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-four',
		              'Sim_number': '639455937511',
		               'phone': '+INSERT_NUMBER'},

		 'crypto35': {'API_HASH': '08518c2cfac798cde94c8d70bcbbee0c',
		              'API_ID': '11976168',
		              'App_title': 'register - crypto35',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-five',
		              'Sim_number': '639455937530',
		               'phone': '+INSERT_NUMBER'},

		 'crypto36': {'API_HASH': '9cd2ae576038ec10455c4485353832f3',
		              'API_ID': '11301359',
		              'App_title': 'register - crypto36',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-six',
		              'Sim_number': '639455937415',
		               'phone': '+INSERT_NUMBER'},

		 'crypto37': {'API_HASH': '3d3ba1c7a4b4d8e77c76ca6ae75868ce',
		              'API_ID': '18282240',
		              'App_title': 'register - crypto37',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-seven',
		              'Sim_number': '639455937416',
		               'phone': '+INSERT_NUMBER'},

		 # 'crypto38': {'API_HASH': '88a0bfcfda7acecf4db0849b24794c60',
		 #              'API_ID': '16217997',
		 #              'App_title': 'register - crypto38',
		 #              'First_name': 'Crypto',
		 #              'Last_name': 'Thirty-eight',
		 #              'Sim_number': '639455937418',
		 #				'phone': '+INSERT_NUMBER'},

		 'crypto39': {'API_HASH': '365401d9277e49f6cb5427bdbffc6132',
		              'API_ID': '10220001',
		              'App_title': 'register - crypto39',
		              'First_name': 'Crypto',
		              'Last_name': 'Thirty-nine',
		              'Sim_number': '639455937419',
		               'phone': '+INSERT_NUMBER'},

		 'crypto4': {'API_HASH': '2fbc9a928b8bef38b024813f642a590a',
		             'API_ID': '15218219',
		             'App_title': 'register - crypto4',
		             'First_name': 'Crypto',
		             'Last_name': 'Four',
		             'Sim_number': '639752921251',
		              'phone': '+INSERT_NUMBER'},

		 'crypto40': {'API_HASH': '51da34896b016d7eaf3b6a7ac4ad6b02',
		              'API_ID': '10831695',
		              'App_title': 'register - crypto40',
		              'First_name': 'Crypto',
		              'Last_name': 'Forty',
		              'Sim_number': '639455937420',
		               'phone': '+INSERT_NUMBER'},

		 'crypto5': {'API_HASH': '933010cf7a185620f1e87daf6435e418',
		             'API_ID': '16036184',
		             'App_title': 'register - crypto5',
		             'First_name': 'Crypto',
		             'Last_name': 'Five',
		             'Sim_number': '639752921255',
		              'phone': '+INSERT_NUMBER'},

		 'crypto6': {'API_HASH': 'd55496a1db34c360cd78b2ffa2e0cc63',
		             'API_ID': '17372892',
		             'App_title': 'register - crypto6',
		             'First_name': 'Crypto',
		             'Last_name': 'Six',
		             'Sim_number': '639752921257',
		              'phone': '+INSERT_NUMBER'},

		 'crypto7': {'API_HASH': '272df30018684674d004b4a168f09ca3',
		             'API_ID': '19574393',
		             'App_title': 'register - crypto7',
		             'First_name': 'Crypto',
		             'Last_name': 'Seven',
		             'Sim_number': '639752915091',
		              'phone': '+INSERT_NUMBER'},

		 'crypto8': {'API_HASH': 'e1b27649a69907dae5cde991f2355032',
		             'API_ID': '18019323',
		             'App_title': 'register - crypto8',
		             'First_name': 'Crypto',
		             'Last_name': 'Eight',
		             'Sim_number': '639752921239',
		              'phone': '+INSERT_NUMBER'},

		 'crypto9': {'API_HASH': 'f7bcbb5710d6a231cea4e62657d8640f',
		             'API_ID': '16884665',
		             'App_title': 'register - crypto9',
		             'First_name': 'Crypto',
		             'Last_name': 'Nine',
		             'Sim_number': '639752921241',
		             'phone': '+INSERT_NUMBER'},					 	}





# aiogram_key={'HTTP_API':'5201057835:AAH8-4234ttvtvsect54ctyw-hinPM'}


# ___ Config Alternatives: Postgres ____
'''
	# Alternatives for Cred
	cred = [ 'id' 	 : '11111',
			 'phone' : '+4799337661',
			 'hash'  : 'fu3487fh3nf98381399n9r43244432', ]

	cred = [  
			[ 'id'    , '11111' ],
			[ 'phone' , '44234324243' ],
			[ 'hash'  , 'fu3487fh3nf98381399n9r43244432' ],						
		   ]

	Warning: This does require you to make some small edits to the code. 
'''
'''
				[Will probobly be removed]
	Alternative for scraper config; Nested dict:
		Payload for postgres (password, user, host, dbname) & proxies in one. 

	scraper = { 'cred' 	  : { 'id' 	  : '11111',
			    		   	  'phone' : '3288282828',
	    				      'hash'  : 'fu3487fh3nf98381399n9r43244432', },

	    		'proxies' : { 'http'  : 'http://10.10.1.10:3128', 
	    		              'https' : 'https://10.10.1.11:1080', 
	    		              'ftp'   : 'ftp://10.10.1.10:3128',   			 } }
		# Warning: This does require you to make 
		# 	 	 some small edits to the code.  
'''


# __________________________ COMMON __________________________

# Proxies
proxies = { 'http'  : 'http://10.10.1.10:3128', 
            'https' : 'https://10.10.1.11:1080', 
            'ftp'   : 'ftp://10.10.1.10:3128',   }
