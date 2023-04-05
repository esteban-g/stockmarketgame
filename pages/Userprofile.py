
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



st.set_page_config(layout="wide")

st.title('🌍 Your information')


# if 'username' not in st.session_state:
#     st.write('Please log in')
#     modal = Modal("Log in",'div',20,500)
#     open_modal = st.button("Log in")

#     if open_modal:
#         modal.open()

#     if modal.is_open():
#         with modal.container():

#             with st.form("login_form"):

#                 username= st.text_input(label="Username", value="")
                

#                 password= st.text_input(label="Password", value="")
                
                            
#                 submitted = st.form_submit_button("Submit")
#                 if submitted:
#                     # st.write("slider")
#                     # st.write("slider", slider_val, "checkbox", checkbox_val)
#                     # insertPortfolio(newportfolio,currentCurrency)
#                     if validateUser(username,password):
#                         st.session_state.username = username
#                         st.session_state.password = password
#                         st.write('Welcome')
#                         print('username',username)
#                         modal.close()
#                     else:
#                         st.write('Try again')
# else:
#     st.write(st.session_state.username)                       
