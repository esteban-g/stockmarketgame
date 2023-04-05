
import streamlit as st
import datetime
import time
import pandas as pd
import pandas.io.sql as sqlio
from numpy.random import randint

from openbb_terminal.sdk import openbb
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_modal import Modal
from configparser import ConfigParser
import psycopg2
import streamlit.components.v1 as components
from utils.investigamedb import *
from utils.login import *
from streamlit_cookies_manager import EncryptedCookieManager



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
if 'current_asset' not in st.session_state:
    st.session_state.current_asset = ''
if 'current_csv_portfolio' not in st.session_state:
    st.session_state.current_csv_portfolio = []
if 'current_selected_portfolio' not in st.session_state:
    st.session_state.current_selected_portfolio = []
if 'PP' not in st.session_state:
    st.session_state.PP = None




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



############################################
# WEB CONTENT
# st.set_page_config(layout="wide")

st.set_page_config(page_title='🌍 InvestiGame', page_icon='📈', layout='wide')
st.title('🌍 Portfolio Management')


# st.dataframe(indices)  # Same as st.write(df)

###############################
# LOGIN AND SESSION MANAGEMENT


if 'username' not in st.session_state:
    loginprocedure()
    # st.sidebar.warning(
    # "Please log in")

    
    # with st.sidebar:
   
    #     login_modal = Modal("Log-in",'divlogin',20,500)
    #     login_button = st.button("Log in")
        

    #     if login_button:
    #         login_modal.open()

    #     if login_modal.is_open():
    #         with login_modal.container():

    #             with st.form("login_form"):

    #                 username= st.text_input(label="Username", value="")
                    

    #                 password= st.text_input(label="Password", value="")
                    
                                
    #                 submittedlogin = st.form_submit_button("Verify")
    #                 if submittedlogin:

    #                     if validateUser(username,password):
    #                         st.session_state.username = username
    #                         st.session_state.password = password
    #                         st.write('Welcome')
    #                         print('username',username)
                            
                            
    #                         login_modal.close()
    #                     else:
    #                         st.write('Try again')
else:                            
    add_selectbox = st.sidebar.text(
                                st.session_state.username
                            )
    

#TODO CHANGE THE FOLLOWING FOR THOSE ASSETS IN THE PORTFOLIO
indices= pd.DataFrame(openbb.economy.indices())            
col1, col2, col3,col4, col5 = st.columns(5,gap="small")


#TODO I DIDNT FIND HOW TO CREATE COLUMNS  ITERATIVELY/DYNAMICALLY
col1.metric(indices[indices.columns[0]][0], indices[indices.columns[1]][0], indices[indices.columns[2]][0])

col2.metric(indices[indices.columns[0]][1], indices[indices.columns[1]][1], indices[indices.columns[2]][1])

col3.metric(indices[indices.columns[0]][2], indices[indices.columns[1]][2], indices[indices.
columns[2]][2])

col4.metric(indices[indices.columns[0]][3], indices[indices.columns[1]][3], indices[indices.columns[2]][3])

col5.metric(indices[indices.columns[0]][4], indices[indices.columns[1]][4], indices[indices.columns[2]][4])




col1, col2 = st.columns(2)

with col1:
    st.subheader('Your portfolios')
    getAllProfolios()    
    st.dataframe(st.session_state.all_portfolios)


with col2:
    st.subheader('Actions')
    modal = Modal("Setup your portfolio",'divportf',20,500)
    open_modal = st.button("Create a new Portfolio")
    st.button("Share Portfolio")
    st.button("Delete a Portfolio")
    csvportfolio = st.button("CSV/Excel Portfolio ")
    testbuttonvar = st.button("Test")

    # if testbuttonvar:
        # insertUser('Esteban','estebang','123')

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

# st.markdown("**:blue[Select a portfolio to be updated]**")

if 'username' in st.session_state:
    # st.sidebar.warning(
    # "Please log in")

    # with st.sidebar:

    #     login_modal = Modal("Log-in",'divlogin',20,500)
    #     login_button = st.button("Log in")
        

    #     if login_button:
    #         login_modal.open()

    #     if login_modal.is_open():
    #         with login_modal.container():

    #             with st.form("login_form"):

    #                 username= st.text_input(label="Username", value="")
                    

    #                 password= st.text_input(label="Password", value="")
                    
                                
    #                 submittedlogin = st.form_submit_button("Verify")
    #                 if submittedlogin:
    #                     if validateUser(username,password):
    #                         st.session_state.username = username
    #                         st.session_state.password = password
    #                         st.write('Welcome')
    #                         print('username',username)
                            
                            
    #                         login_modal.close()
    #                     else:
    #                         st.write('Try again')

# else:                            
    add_selectbox = st.sidebar.text(st.session_state.username)
    col3, col4 = st.columns(2)

    with col3:

        portfoliolist = sqlio.read_sql_query("SELECT name FROM portfolio", connecto())
        portfoliooption = st.selectbox('Your current portfolio:',portfoliolist)
        st.session_state.current_selected_portfolio = portfoliooption

        # print(portfoliolist.head())

        # getNameProfolios()
        # print(st.session_state.name_portfolios)
        # st.session_state.portf= st.selectbox(c)
        st.subheader(st.session_state.portf)
        st.subheader(st.session_state.current_selected_portfolio)

    

        allAssets =  getAllAssetsProfolios(st.session_state.current_selected_portfolio,st.session_state.username) 
        assetslist = sqlio.read_sql_query("SELECT symbol FROM public.assets WHERE id_portfolio=( SELECT id FROM public.portfolio WHERE  name = '"+st.session_state.current_selected_portfolio+"' AND idusers = (SELECT id FROM public.users WHERE username = '"+st.session_state.username+"'))", connecto())
        pdasstslist = pd.DataFrame(assetslist)       

        assestsframe = st.dataframe(assetslist)



    with col4:
        asset = st.text_input('➕ Add assets to your portfolio to get relevant data and news',help ='It can be for example NOK, MSFT, HEXA-B.ST or the name of the company', placeholder ='e.g. NOK, MSFT, HEXA-B.ST')

        if asset:
            assetsdata = openbb.stocks.load(asset)
            assetsscreener = pd.DataFrame(openbb.stocks.ca.screener([asset]))       

            # assetscomparison = pd.DataFrame(openbb.stocks.ca.balance([asset], timeframe = '2021'))
            finnhubkey = open('finnhub.txt').readline()
            openbb.keys.finnhub(key = finnhubkey, persist = True)
            assetsnews = pd.DataFrame(openbb.stocks.ba.cnews(asset))
            

            if len(assetsdata)>0:
                
                addSymbol=st.button('➕ Add')
                
                assetsname = assetsscreener['Company'].iloc[0]
                st.subheader(assetsname)
                # st.dataframe(assetsscreener) ORIGINAL
                # st.dataframe(pdasstslist)


            
                
                if addSymbol: 
                    
                    insertRelevantAsset(assetsname,asset,st.session_state.current_selected_portfolio,st.session_state.username)
                    
                    #TODO AQUI TOCA AGREGAR/ACTUALIZAR LA LINEA QUE EL USUARIO ACABA DE METER
                    # assestsframe.add_rows(assetsname)
                    newasset = {'symbol': assetsname}
                    pdasstslist.append(newasset, ignore_index = True)
                    
                    
                    



                df = assetsdata.reset_index()
                df.columns = [x.title() for x in df.columns]

                df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
                df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
                df = df[-days_to_plot:]

                #

                # Display the plotly chart on the dashboard
                st.plotly_chart(
                    get_candlestick_plot(df, ma1, ma2, asset),
                    width=0, height=0,
                    use_container_width = True,
                )

                
                st.subheader('Last news about '+assetsname)


                    # \
                    # .hide(subset=[0, 2, 4], axis=0) \
                    # .hide(subset=[0, 2, 4], axis=1)
                st.dataframe(assetsnews.loc[:,["headline","summary", "url"]])
            
                # st.subheader('openbb.stocks.dd.customer')
                # st.dataframe(openbb.stocks.dd.customer(asset))
                
                pd.set_option('display.max_columns', None)
                
                # st.subheader('openbb.stocks.options.info')
                # data = openbb.stocks.options.info(asset)
                # new_data = pd.DataFrame.from_dict(data, orient='index')

                # new_data = new_data.reset_index(level=0)
                # new_data.columns=['Heading','Value']

                # AgGrid(new_data, height=300)
            else:
                st.write('No Data Found for '+asset)


homeTab, discoveryTab, indicesTab = st.tabs(["Portfolio", "Analysis", "Indices"])

 
with homeTab:
    st.dataframe(st.session_state.current_csv_portfolio)
        
    # ticker = st.text_input('Add assets to your portfolio to get relevant data and news')

    # if ticker:
    #     data = openbb.stocks.load(ticker)

    #     if len(data)>0:

    #         df = data.reset_index()
    #         df.columns = [x.title() for x in df.columns]

    #         df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
    #         df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
    #         df = df[-days_to_plot:]

    #         #

    #         # Display the plotly chart on the dashboard
    #         st.plotly_chart(
    #             get_candlestick_plot(df, ma1, ma2, ticker),
    #             width=0, height=0,
    #             use_container_width = True,
    #         )

            
    #         st.subheader('Revenue, Net income and Net margin of '+ticker)
    #         st.dataframe(openbb.stocks.dd.supplier(ticker))

        
    #         # st.subheader('openbb.stocks.dd.customer')
    #         # st.dataframe(openbb.stocks.dd.customer(ticker))
            
    #         pd.set_option('display.max_columns', None)
            
    #         # st.subheader('openbb.stocks.options.info')
    #         # data = openbb.stocks.options.info(ticker)
    #         # new_data = pd.DataFrame.from_dict(data, orient='index')

    #         # new_data = new_data.reset_index(level=0)
    #         # new_data.columns=['Heading','Value']

    #         # AgGrid(new_data, height=300)
    #     else:
    #         st.write('No Data Found for '+ticker)

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
    st.subheader('Companies with the highest positive change ("gainers")')
    gainers = openbb.stocks.disc.gainers()
    st.dataframe(gainers)

    st.subheader('Companies with the highest negative change ("losers")')
    losers = openbb.stocks.disc.losers()
    st.dataframe(losers)

    st.subheader('Tech Companies')
    gtech = openbb.stocks.disc.gtech()
    st.dataframe(gtech)

    st.subheader('Penny stocks')
    st.write("Penny stocks are stocks that trade for less than $5 per share1. They are often considered high risk but can potentially offer high rewards")
    hotpenny = openbb.stocks.disc.hotpenny()
    st.dataframe(hotpenny)

with indicesTab:

    st.subheader('Stock market indices')
    

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