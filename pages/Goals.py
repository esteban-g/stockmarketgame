from openbb_terminal.sdk import openbb
import streamlit as st
import datetime
import pandas as pd
import pandas.io.sql as sqlio

from st_aggrid import AgGrid
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_modal import Modal
from configparser import ConfigParser
import psycopg2
import streamlit.components.v1 as components


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


def get_candlestick_plot(
        df: pd.DataFrame,
        ma1: int,
        ma2: int,
        ticker: str
):
    '''
    Create the candlestick chart with two moving avgs + a plot of the volume
    Parameters
    ----------
    df : pd.DataFrame
        The price dataframe
    ma1 : int
        The length of the first moving average (days)
    ma2 : int
        The length of the second moving average (days)
    ticker : str
        The ticker we are plotting (for the title).
    '''
    
    fig = make_subplots(
        rows = 2,
        cols = 1,
        shared_xaxes = True,
        vertical_spacing = 0.1,
        subplot_titles = (f'{ticker} Stock Price', 'Volume Chart'),
        row_width = [0.3, 0.7]
    )
    
    fig.add_trace(
        go.Candlestick(
            x = df['Date'],
            open = df['Open'], 
            high = df['High'],
            low = df['Low'],
            close = df['Close'],
            name = 'Candlestick chart'
        ),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['Date'], y = df[f'{ma1}_ma'], name = f'{ma1} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Line(x = df['Date'], y = df[f'{ma2}_ma'], name = f'{ma2} SMA'),
        row = 1,
        col = 1,
    )
    
    fig.add_trace(
        go.Bar(x = df['Date'], y = df['Volume'], name = 'Volume'),
        row = 2,
        col = 1,
    )
    
    fig['layout']['xaxis2']['title'] = 'Date'
    fig['layout']['yaxis']['title'] = 'Price'
    fig['layout']['yaxis2']['title'] = 'Volume'
    
    fig.update_xaxes(
        rangebreaks = [{'bounds': ['sat', 'mon']}],
        rangeslider_visible = False,
    )
    
    return fig
    
def loadFilePortfolio(portfolio):    
    file_path=''
    if portfolio == 'tea':
        file_path = 'holdings1.xlsx'
    elif portfolio == 'sdfg': 
        file_path = 'holdings2.xlsx'
    elif portfolio == 'NewPortf': 
        file_path = 'holdings3.xlsx'        
    elif portfolio == 'tes': 
        file_path = 'holdings4.xlsx'        
    else:
        file_path = 'holdings_example.xlsx'         
    print('>>>>>>>>>>>>>>>>>>>>>>0')
    print(file_path)
    print('>>>>>>>>>>>>>>>>>>>>>>1')
    P = openbb.portfolio.load(
        transactions_file_path = file_path
    )    
    print('>>>>>>>>>>>>>>>>>>>>>>2')
    tickers = P.tickers_list
    print('TICKERS:', tickers)
    returns = openbb.portfolio.dret(P)
    returns.rename(columns = {'portfolio': 'Portfolio % Returns', 'benchmark': 'Benchmark % Returns'}, inplace = True)
    returns.index = returns.index.rename('Date')
    print(returns.tail(5))
    outputporfolio = openbb.portfolio.show(P)
    # st.button('Add')
    # st.button('Update')
    # st.dataframe(outputporfolio)
    st.session_state.current_csv_portfolio= outputporfolio
    st.session_state.PP = P

st.set_page_config(layout="wide")


st.subheader('PORTFOLIO MANAGEMENT')
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

    if csvportfolio:
        loadFilePortfolio(st.session_state.current_selected_portfolio)

    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():

            with st.form("my_form"):

                st.subheader('Create your portfolio')
                newportfolio= st.text_input(label=" New Portfolio Name", value="")
                st.session_state.portf = newportfolio
                data = pd.DataFrame(openbb.economy.currencies())            
                currentCurrency= st.selectbox(  'Portfolio Currency', data)
                st.session_state.currency = currentCurrency

                            
                submitted = st.form_submit_button("Submit")
                if submitted:
                    # st.write("slider")
                    # st.write("slider", slider_val, "checkbox", checkbox_val)
                    insertPortfolio(newportfolio,currentCurrency)

                    modal.close()






 
# if newportfolio == "":
#     st.subheader('There are no portfolios')
# else:
#     st.subheader(newportfolio)

# Session State also supports attribute based syntax


# if st.session_state.portf=='':
#     st.markdown("**:red[Select a portfolio to update or create a new one]**")

st.markdown("**:blue[Select a portfolio to be updated]**")

portfoliolist = sqlio.read_sql_query("SELECT name FROM portfolio", connecto())
portfoliooption = st.selectbox('Your current portfolio:',portfoliolist)
st.session_state.current_selected_portfolio = portfoliooption
# print(portfoliolist.head())

# getNameProfolios()
# print(st.session_state.name_portfolios)
# st.session_state.portf= st.selectbox(c)
st.subheader(st.session_state.portf)

homeTab, discoveryTab, indicesTab = st.tabs(["Home", "Discovery", "Indices"])

 
with homeTab:
    st.dataframe(st.session_state.current_csv_portfolio)
        
    ticker = st.text_input('Add symbols to get relevant data and news')

    if ticker:
        data = openbb.stocks.load(ticker)

        if len(data)>0:

            df = data.reset_index()
            df.columns = [x.title() for x in df.columns]

            df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
            df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
            df = df[-days_to_plot:]

            #

            # Display the plotly chart on the dashboard
            st.plotly_chart(
                get_candlestick_plot(df, ma1, ma2, ticker),
                width=0, height=0,
                use_container_width = True,
            )

            
            st.subheader('Revenue, Net income and Net margin of '+ticker)
            st.dataframe(openbb.stocks.dd.supplier(ticker))

        
            # st.subheader('openbb.stocks.dd.customer')
            # st.dataframe(openbb.stocks.dd.customer(ticker))
            
            pd.set_option('display.max_columns', None)
            
            # st.subheader('openbb.stocks.options.info')
            # data = openbb.stocks.options.info(ticker)
            # new_data = pd.DataFrame.from_dict(data, orient='index')

            # new_data = new_data.reset_index(level=0)
            # new_data.columns=['Heading','Value']

            # AgGrid(new_data, height=300)
        else:
            st.write('No Data Found for '+ticker)

    # THE ANALYSIS OF THE PORTFOLIO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    
    # if st.session_state.PP is not None:
        # print(openbb.portfolio.summary(st.session_state.PP))
        # daframe = pd.DataFrame
        # # topop = output = openbb.portfolio.holdp(st.session_state.PP)
        # daframe = openbb.portfolio.holdp(st.session_state.PP)
        # fig = go.Figure(data=[go.Candlestick(x=daframe['Date'],
        #         open=daframe['AAPL.Open'],
        #         high=daframe['AAPL.High'],
        #         low=daframe['AAPL.Low'],
        #         close=daframe['AAPL.Close'])])

        # fig.show()
        # print('# THE ANALYSIS OF THE PORTFOLIO',daframe.head())
            # df = topop.reset_index()
            # df.columns = [x.title() for x in df.columns]

            # df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
            # df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
            # df = df[-days_to_plot:]

        # st.dataframe(topop)
        # fig = go.Figure(data=[go.Candlestick(x=topop[1],
        #         open=topop['AAPL.Open'], high=topop['AAPL.High'],
        #         low=topop['AAPL.Low'], close=topop['AAPL.Close'])
        #              ])

        # fig.update_layout(xaxis_rangeslider_visible=False)
        # fig.show()
            #

            # Display the plotly chart on the dashboard
    # openbb.portfolio.summary prints a table of risk metrics, comparing the portfolio against the benchmark.


with discoveryTab:
    st.subheader('openbb.stocks.disc.gainers')
    gainers = openbb.stocks.disc.gainers()
    st.dataframe(gainers)

    st.subheader('openbb.stocks.disc.losers')
    losers = openbb.stocks.disc.losers()
    st.dataframe(losers)

    st.subheader('openbb.stocks.disc.gtech')
    gtech = openbb.stocks.disc.gtech()
    st.dataframe(gtech)

    st.subheader('openbb.stocks.disc.hotpenny')
    hotpenny = openbb.stocks.disc.hotpenny()
    st.dataframe(hotpenny)

with indicesTab:

    st.subheader('Stock market indices')
    col1, col2, col3,col4, col5 = st.columns(5,gap="small")
    indices= pd.DataFrame(openbb.economy.indices())            


    col1.metric('indices[indices.columns[0]]', "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")
    col4.metric("Wind", "9 mph", "-8%")
    col5.metric("Humidity", "86%", "4%")

    st.dataframe(indices)  # Same as st.write(df)



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