import streamlit as st 
from openbb_terminal.sdk import openbb

import pandas as pd
import os
from streamlit_modal import Modal
import streamlit.components.v1 as components
import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt



from PIL import Image
import pandas as pd
from st_aggrid import AgGrid



import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

from plotly.subplots import make_subplots



#def main():

st.set_page_config(layout="wide")
st.title('A stocks market game - evaluating risk in decision-making')

st.write('''Make a portfolio decision given a specific scenario ''')

def color_negative_red(val):
     if type(val) != 'str':
          color = 'green' if val >0 else 'red'
          return f'color: {color}'

     
# Candlestick code from 
# https://medium.com/@dannygrovesn7/using-streamlit-and-plotly-to-create-interactive-candlestick-charts-a2a764ad0d8e

ma1=10
ma2=30
days_to_plot=30

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

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("./style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

# icon("search")
# selected = st.text_input("", "Search...")
# button_clicked = st.button("OK")

with st.container():
    
     # st.write("This is inside the container")
     # image = Image.open('./msft_stocks.png')
     # st.image(image, caption='Sotck')
     
    # t = "<div>Hello there my <span class='highlight blue'>name <span class='bold'>yo</span> </span> is <span class='highlight red'>Fanilo <span class='bold'>Name</span></span></div>"
    backgroundInfo = "<div><span class='highlight blue'> <strong>Background information:</strong> First, consider your current portfolio (see pie plot). The Tesla Inc (TSLA) stock price is rising this week (see 1 month data). News about Tesla are positive (see key news last month). </span></div><br>"
    st.markdown(backgroundInfo, unsafe_allow_html=True)
    
    question1 = "<div><span class='highlight greenquestion'> Your current porfolio has   </span></div><br>"
    st.markdown(question1, unsafe_allow_html=True)

    st.write("Portfolio asset allocation")
    plt.rcParams['font.size'] = 7.0
    labels = 'Short-term', 'Stocks', 'Bonds'
    sizes = [30, 20, 50]
    explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
    #fig1, ax1 = plt.subplots(figsize=(1, 1))
    fig1, ax1 = plt.subplots(figsize=(10, 2))      
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%')
    # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(fig1)
    df = px.data.tips()
    fig = px.pie(df, values='tip', names='day')
    fig.show()
    




    ticker = 'TSLA'
    datastocks = openbb.stocks.load(ticker)

    if len(datastocks)>0:
        
        df = datastocks.reset_index()
        df.columns = [x.title() for x in df.columns]

        df[f'{ma1}_ma'] = df['Close'].rolling(ma1).mean()
        df[f'{ma2}_ma'] = df['Close'].rolling(ma2).mean()
        df = df[-days_to_plot:]

        # Display the plotly chart on the dashboard
        st.plotly_chart(
            get_candlestick_plot(df, ma1, ma2, ticker),
            width=0, height=0,
            use_container_width = True,
        )

        col1, col2 = st.columns(2)

        with col1:
            st.subheader('openbb.stocks.dd.supplier')
            st.dataframe(openbb.stocks.dd.supplier(ticker))

        with col2:
            st.subheader('openbb.stocks.dd.customer')
            st.dataframe(openbb.stocks.dd.customer(ticker))
        
        pd.set_option('display.max_columns', None)



col1, col2 = st.columns([3, 1])


with col1:

     st.subheader('START THE GAME')
     modal = Modal("Game",'div',20,900)
     open_modal = st.button("Open")
     if open_modal:
          modal.open()

     if modal.is_open():
          with modal.container():

               st.write("Portfolio asset allocation")
               plt.rcParams['font.size'] = 7.0
               
               labels = 'Short-term', 'Stocks', 'Bonds'
               sizes = [30, 20, 50]
               explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
               fig1, ax1 = plt.subplots(figsize=(1, 1))
               
               
               ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%')
               # ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.0f%%', shadow=True, startangle=90)
               ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

               html_string = '''
               <h1>HTML string in RED</h1>

               <script language="javascript">
               document.querySelector("h1").style.color = "red";
               </script>
               '''
               components.html(html_string)

               st.pyplot(fig1)
               st.write("Some fancy text")
               value = st.checkbox("Check me")
               st.write(f"Checkbox checked: {value}")


     st.button('Start game')

     st.subheader('MY CURRENT PORTFOLIO')
     st.button('Update portfolio')

          # data2 = openbb.stocks.load("Public_Equity_Orderbook.xlsx")    
     print('##### oooooooooooo ########## ooooooooooo')
     # pythonfile = 'Public_Equity_Orderbook.xlsx'

     # print('Get current working directory : ', os.getcwd())
     # fileportfolio =  os.path.abspath(pythonfile)
     # print("Path of the file..", fileportfolio)    
     # p = openbb.portfolio.load(fileportfolio)
     # output = openbb.portfolio.show(p)
     # st.dataframe(output)




with col2:
     # row1, row2 = st.rows() #columns([3, 1])
     st.subheader('NEWS')
     data = openbb.economy.usbonds()
     data[data.columns[1]] = data[data.columns[1]].apply(pd.to_numeric)
     data[data.columns[2]] = data[data.columns[2]].apply(pd.to_numeric)
     data[data.columns[3]] = data[data.columns[3]].apply(pd.to_numeric)

     columns = data.columns[3]

     st.dataframe(data.style.applymap(color_negative_red, subset=[columns]))

     data = openbb.economy.currencies()
     data[['Chng']] = data[['Chng']].apply(pd.to_numeric)
     st.dataframe(data.style.applymap(color_negative_red, subset=['Chng']))




# main()
