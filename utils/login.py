
import streamlit as st
from streamlit_modal import Modal
from utils.investigamedb import *

def loginprocedure():
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
                            