import streamlit as st
from configparser import ConfigParser
import psycopg2
import streamlit.components.v1 as components
from datetime import datetime



# CONFIG
def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db



def connecto():
    """ Returns a connection to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def disconnecto(conn):
    """ disconnects a connection to the PostgreSQL database server """
    try:     
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        conn.close()
        print('Database connection closed.')


############################
# PORTFOLIO TABLE OPERATIONS

def insertPortfolio(name,currency):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('Inserting query:')
        cur.execute("INSERT INTO portfolio(name,currency) VALUES ('"+name+"','"+currency+"')")

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
        conn.commit()

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')





def getAllProfolios():
    """ Get Porfolios from the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT name, currency FROM portfolio')
        st.session_state.all_portfolios = cur.fetchall()

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')      

def getNameProfolios():
    """ Get Porfolios from the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT name FROM portfolio')
        st.session_state.name_portfolios = cur.fetchall()

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')      



########################
# USERS TABLE OPERATIONS

def insertUser(name,username,password):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('Inserting query:',name+username+password)
        cur.execute("INSERT INTO users(name,username, password) VALUES ('"+name+"','"+username+"','"+password+"')")

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
        conn.commit()

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')            


def validateUser(username,password):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('Checking query:',username+password)
        cur.execute("SELECT username FROM users WHERE username ='"+username+"' AND password ='"+password+"'")
        isvalid = bool(cur.rowcount)
        # if isvalid:
        #     st.write('EXIST!!!!!!!!!!!!!!!!!!!')
        # else:
        #     st.write(' NOOOOOOOO EXIST!!!!!!!!!!!!!!!!!!!')
        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
        conn.commit()

	# close the communication with the PostgreSQL
        cur.close()
        return isvalid
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')   
            return isvalid

def getAllUsers():
    """ Get Porfolios from the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('')
        st.session_state.all_portfolios = cur.fetchall()

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')  



###########################
#  ASSETS MANAGEMENT 
def insertRelevantAsset(name, symbol,portfolioname,username):
    """ Connect to the PostgreSQL database server """
    conn = None
    dt = datetime.now()

    # getting the timestamp
    ts = datetime.timestamp(dt)
    now = datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')

    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
        
        # search the idportfolio based on the portfolio name and yser
        cur.execute("SELECT id FROM public.portfolio WHERE name = '"+portfolioname+"' AND idusers = (SELECT id FROM public.users WHERE username = '"+username+"' LIMIT 1) LIMIT 1")
        allids = cur.fetchall()
        idport= allids[0][0]

        
        cur.execute("INSERT INTO assets(symbol,name,timestamp,id_portfolio) VALUES ('"+symbol+"','"+name+"','"+timestamp+"',"+str(idport)+")")
        


	# execute a statement            
        # cur.execute("INSERT INTO assets(symbol,name,timestamp,id_portfolio) VALUES ('"+symbol+"','"+name+"',"+ts+","+idportfolio+")")

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
        conn.commit()

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')            

def getAllAssetsProfolios(portfolioname,username):
    """ Get Porfolios from the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        print('PostgreSQL database version:')
        
        # search the idportfolio based on the portfolio name and yser
        cur.execute("SELECT symbol FROM public.assets WHERE id_portfolio=( SELECT id FROM public.portfolio WHERE  name = '"+portfolioname+"' AND idusers = (SELECT id FROM public.users WHERE username = '"+username+"'))")                    

        allassets = cur.fetchall()

        # display the PostgreSQL database server version
        # db_version = cur.fetchone()
        # print(db_version)
       
	# close the communication with the PostgreSQL
        cur.close()
        return allassets
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')    