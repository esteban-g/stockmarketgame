from openbb_terminal.sdk import openbb
import streamlit as st
import datetime
import pandas as pd
import pandas.io.sql as sqlio


import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_modal import Modal
from configparser import ConfigParser
import psycopg2
import streamlit.components.v1 as components
from utils.investigamedb import *
from Investigame import *

# Candlestick code from 
# https://medium.com/@dannygrovesn7/using-streamlit-and-plotly-to-create-interactive-candlestick-charts-a2a764ad0d8e

ma1=10
ma2=30
days_to_plot=120
newportfolio=''
currentCurrency=''
if 'portf' not in st.session_state:
    st.session_state.portf = ''
if 'currency' not in st.session_state:
    st.session_state.currency = ''
if 'all_portfolios' not in st.session_state:
    st.session_state.all_portfolios = []
if 'name_portfolios' not in st.session_state:
    st.session_state.name_portfolios = []
if 'current_symbol' not in st.session_state:
    st.session_state.current_symbol = ''
if 'current_csv_portfolio' not in st.session_state:
    st.session_state.current_csv_portfolio = []
if 'current_selected_portfolio' not in st.session_state:
    st.session_state.current_selected_portfolio = []
if 'PP' not in st.session_state:
    st.session_state.PP = None






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



########################
# WEB CONTENT
st.set_page_config(layout="wide")
st.title('🌍 Goals')



if 'username' not in st.session_state:
        
    st.sidebar.warning(
    "Please log in")
    # st.success("Done!")
    # st.write('Please log in')
    
    with st.sidebar:
   
        login_modal = Modal("Log-in",'divlogin',20,500)
        login_button = st.button("Log in")
        

        if login_button:
            login_modal.open()

        if login_modal.is_open():
            with login_modal.container():

                with st.form("login_form"):

                    username= st.text_input(label="Username", value="")
                    

                    password= st.text_input(label="Password", value="")
                    
                                
                    submittedlogin = st.form_submit_button("Verify")
                    if submittedlogin:
                        # st.write("slider")
                        # st.write("slider", slider_val, "checkbox", checkbox_val)
                        # insertPortfolio(newportfolio,currentCurrency)
                        if validateUser(username,password):
                            st.session_state.username = username
                            st.session_state.password = password
                            st.write('Welcome')
                            print('username',username)
                            
                            
                            login_modal.close()
                        else:
                            st.write('Try again')
else:                            
    add_selectbox = st.sidebar.text(
                                st.session_state.username
                            )


col1, col2 = st.columns(2)

with col1:
    st.subheader('Your portfolios')
    getAllProfolios()    
    st.dataframe(st.session_state.all_portfolios)


with col2:
    st.subheader('Actions')
    
    modal = Modal("Setup your portfolio",'div',20,500)
    open_modal = st.button("Create a new Portfolio")
    st.button("Share Portfolio")
    st.button("Delete a Portfolio")
    csvportfolio = st.button("CSV/Excel Portfolio ")

   




components.html(
    """
    <script type='text/javascript' src='https://www.botlibre.com/scripts/sdk.js'></script>
    <script type='text/javascript' src='https://www.botlibre.com/scripts/game-sdk.js'></script>
    <script type='text/javascript'>
    SDK.applicationId = "6837138020863704473";
    SDK.backlinkURL = "http://www.botlibre.com/login?affiliate=ferzepognu";
    SDK.lang = "en";
    var sdk = new SDKConnection();
    var web = new WebChatbotListener();
    web.connection = sdk;
    web.instance = "46665546";
    web.instanceName = "Alice clone1";
    web.prefix = "botplatform";
    web.caption = "Chat Now";
    web.boxLocation = "bottom-right";
    web.color = "#009900";
    web.background = "#fff";
    web.css = "https://www.botlibre.com/css/chatlog.css";
    web.gameSDKcss = "https://www.botlibre.com/css/game-sdk.css"; 
    web.buttoncss ="https://www.botlibre.com/css/blue_round_button.css"; 
    web.version = 8.5;
    web.bubble = true;
    web.backlink = true;
    web.showMenubar = true;
    web.showBoxmax = true;
    web.showSendImage = true;
    web.showChooseLanguage = true;
    web.avatar = true;
    web.chatLog = true;
    web.popupURL = "https://www.botlibre.com/chat?&id=46665546&embedded=true&chatLog=true&facebookLogin=false&application=6837138020863704473&bubble=true&menubar=true&chooseLanguage=true&sendImage=true&background=%23fff&prompt=You+say&send=&css=https://www.botlibre.com/css/chatlog.css&language=en";
    web.createBox();
    </script>

    """,
    height=600,
)