import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
from yahooquery import Ticker

# web app page settings
st.set_page_config(layout="wide")

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0.5rem;
                    padding-bottom: 0rem;
                    padding-left: 1rem;
                    padding-right: 2rem;
                }
        </style>
        """, unsafe_allow_html=True)


# title
st.markdown("<h1 style='text-align: center; color: white;'>Financial Data</h1>", unsafe_allow_html=True)

# sidebar title
st.sidebar.title('FinQuery')

# enter list of symbols separated by SPACES
#default: symbols=[^SPX ES=F ^RUT RTY=F ^NDX NQ=F ^DJI YM=F ZQ=F ZT=F ZN=F ZB=F TLT FVX TNX TYX AAPL TSLA GS]
symbols = st.sidebar.text_input('Enter a list of tickers!')
# validate existence of symbols during instantiation. Invalid symbols are dropped and can be viewed: invalid_symbols
if st.sidebar.checkbox('Validate'):
    validate = "True"
else:
    validate = "False"

# requests made to Yahoo Finance will be made asynchronously. Only necessary when using more than one symbol.
asynchronous = st.sidebar.radio('Make Asynchronous Requests', ('False', 'True'))

# """
# # other methods
# # checkbox
# if st.sidebar.checkbox('Make Asynchronous Requests'):
#     asynchronous = "True"
# else:
#     asynchronous = "False"

# # dropdown menu
# asynchronous = st.sidebar.selectbox('Make Asynchronous Requests', ['False', 'True'])
# """

tickers = Ticker(symbols, asynchronous=asynchronous, validate=validate)




# select a dashboard
options_list = ["Modules", "Data"]
page = st.sidebar.selectbox('Select a Dashboard', options_list)

if page == "Modules":

    st.header('Modules')
    # view available modules on the Ticker class
    available_modules = [i for i in Ticker.__dict__.keys() if "_" not in i[:2] and i not in ["option_chain", "history", "symbols"]]
    with st.expander("Click to View Available Modules"):
            st.write(available_modules)
    # if st.checkbox('View Available Modules'):
    #     st.write(available_modules)

    # View data available through the 'Summary' tab
    summary_details = tickers.summary_detail
    with st.expander("Click to View Available Data"):
            st.write(summary_details)
   

    # get data for a company
    #st.markdown('<span style="color:red; font-size: 18px;">GET DATA</span>', unsafe_allow_html=True)
    st.subheader('**:blue[Get Data]**')

    # select the company
    company = st.selectbox('Select a Company:', symbols.split()) #.split() is to create a list from words separated by spaces
    # select a module
    company_module = st.selectbox('Select Desired Module:', available_modules)
    ticker_module = getattr(tickers, company_module)    # this is equivalent to ticker.module where ticker is an instance of Ticker class
    st.write(ticker_module[company])
    # selected the desired data
    company_data = st.multiselect('Select Desired Data:', ticker_module[company].keys()) #.split() is to create a list from words separated by spaces
    for data in company_data:
        st.write(f'{data}: ', ticker_module[company].get(data))

if page == "Data":
    st.header('Options and Historical Data')
    st.subheader('**:blue[Get Options Data]**')
    company = st.selectbox('Select a Company:', symbols.split()) #.split() is to create a list from words separated by spaces
    temp = Ticker(company)

    with st.expander("View Options Chain"):
            st.write(temp.option_chain)
    #if st.checkbox('View Options Chain'):
        #st.write(temp.option_chain)
    if st.checkbox('View Most Active'):
        type = st.radio("Rank based on Volume or OI", ('volume', 'openInterest'))
        option_type = st.radio("Options Type", ('puts', 'calls', 'all'))
        top = st.slider('Select Top', min_value=1, max_value=20, value=10, step=1)
        chain = temp.option_chain
        if option_type == 'all':
             st.write(chain.nlargest(top, type))
        else:
             st.write(chain.iloc[chain.index.get_level_values('optionType')==option_type].nlargest(top, type))
             

    st.subheader('**:blue[Get Price Data]**')
    st.write("Select Data Range")
    start = st.date_input('Start Date')
    end = st.date_input('End Date')
    # default: yahooquery.ticker.history(self, period='ytd', interval='1d', start=None, end=None)
    with st.expander("Show Historical Data"):
    #if st.checkbox('Show Historical Data'):
        if company == "^SPX":
            st.write(Ticker("^GSPC").history(start=start, end=end))
        else:
            st.write(temp.history(start=start, end=end)) 





# symbols = st.sidebar.multiselect('Show Player for clubs?', df['Club'].unique())
# nationalities = st.sidebar.multiselect('Show Player from Nationalities?', df['Nationality'].unique())
# new_df = df[(df['Club'].isin(clubs)) & (df['Nationality'].isin(nationalities))]
# st.write(new_df)

# ####################       WIDGETS      ####################

# # (1) Slider
# # st.slider(label, min_value=None, max_value=None, value=None, step=None, format=None)
# x = st.slider('x')  #every time change the widget value the whole app runs from top to bottom 
# st.write(x, 'squared is', x * x)

# # (2) User/Text Input
# url = st.text_input('Enter URL')
# st.write('The Entered URL is: ', url)

# # (3) CheckBox
# # one use case is to show/hide a specific section in an app or setting up a boolean parameter value
# df = pd.read_csv("SPY_daily.csv")
# if st.checkbox('Show dataframe'):
#     st.write(df)

# # (4) SelectBox
# # one use case is as a simple dropdown menu
# option = st.selectbox(
#     'Which Column Would You Like to Select?',
#     df.columns)
# 'You selected: ', option

# # (5) MultiSelect
# options = st.multiselect(
#     'Which Columns Would You Like to Select?', 
#     df.columns)
# st.write('You selected:', options)