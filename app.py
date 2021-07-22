import yfinance as yf
import streamlit as st
import datetime
import numpy as np
import pandas as pd
pd.set_option("display.precision", 1)

st.sidebar.header('Input Parameters')
st.sidebar.subheader('Chart')
st.subheader('Chart')
tickerSymbol = st.sidebar.text_input('Symbol' ,'BTC-USD')

def  get_data ():
    st.write('Check_Symbol : https://finance.yahoo.com/')
    period = st.sidebar.selectbox('Period',('30m','1h', '4h' , '1d'))
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period=period ,  start='2021-7-15', end='2021-7-31')
    st.line_chart(tickerDf.Close)
    return tickerDf , tickerSymbol

st.sidebar.subheader('Rebalance_Dataframe')
def Rebalance_Buy  (data):
    st.subheader('Rebalance_Buy  :  แปรผกผัน ∝')
    Z = st.sidebar.slider('Rebalance_Buy : แปรผกผัน ∝', 3 , 200 , 3 )
    asset = [round(i , 0)  for i in  np.linspace(0 , data.Close[-1]*2 , Z)]
    cash = [round(i , 0)  for i in  np.linspace(data.Close[-1]*2 , 0 , Z)]
    df = pd.DataFrame(asset , columns= [ 'asset_50%'], index= cash)
    df['diff'] =    round( df['asset_50%'].shift(0) -  data.Close[-1] , 0)
    df['cash_50%'] = cash
    df['sum_100%'] = df.apply((lambda x : x['asset_50%']+ x['cash_50%'])  , axis= 1)
    st.dataframe(df)
    st.write( 1 ,  Symbol  , '=' , data.Close[-1])
    st.line_chart(df['asset_50%'])

def Rebalance_Sell  (data):
    st.subheader('Rebalance_Sell  :  แปรผันตรง /')
    Z = st.sidebar.slider('Rebalance_Sell : แปรผันตรง /', 3 , 200 , 3 )
    asset = [round(i , 0)  for i in  np.linspace(0 , data.Close[-1]*2 , Z)]
    cash = [round(i , 0)  for i in  np.linspace(data.Close[-1]*2 , 0 , Z)]
    df = pd.DataFrame(asset , columns= [ 'cash_50%'], index= cash)
    df['diff'] =   -1 *     round( df['cash_50%'].shift(0) -  data.Close[-1] , 0)
    df['asset_50%'] = cash
    df['sum_100%'] = df.apply((lambda x : x['asset_50%']+ x['cash_50%'])  , axis= 1)

    st.dataframe(df)
    st.write( 1 ,  Symbol  , '=' , data.Close[-1])
    st.line_chart(df['asset_50%'])

def plot (data):
    st.subheader('Benchmark_Returns')
    st.sidebar.subheader('Benchmark_Returns')

    Z = st.sidebar.slider('Rebalance ทุกๆ %', 1 , 10 , 5 ) ;  Z = Z / 100

    trade_dataset = data 
    trade_dataset['Tomorrows_Returns'] = np.log(trade_dataset['Close']/trade_dataset['Close'].shift(1))
    trade_dataset['Tomorrows_Returns'] = trade_dataset['Tomorrows_Returns'].shift(-1)
    trade_dataset['Strategy_Returns_buy'] = np.where(trade_dataset['Tomorrows_Returns']  > Z , trade_dataset['Tomorrows_Returns'] , 0)
    trade_dataset['Strategy_Returns_sell'] = np.where(trade_dataset['Tomorrows_Returns']  <  -(Z) , abs(trade_dataset['Tomorrows_Returns']) , 0)
    trade_dataset['Rebalance_Sell'] = np.cumsum(trade_dataset['Strategy_Returns_sell'])
    trade_dataset['Rebalance_Buy'] = np.cumsum(trade_dataset['Strategy_Returns_buy'])
    trade_dataset['Market_Returns'] = np.cumsum(trade_dataset['Tomorrows_Returns'])
    trade_plot = trade_dataset[['Market_Returns' ,  'Rebalance_Buy' ,  'Rebalance_Sell']]
    st.line_chart(trade_plot)
    st.write( 'Market_Returns', '=' , round(trade_dataset.Market_Returns[-2] , 2) )
    st.write( 'Rebalance_Buy', '=' , round(trade_dataset.Rebalance_Buy[-2] , 2) )
    st.write( 'Rebalance_Sell', '=' , round(trade_dataset.Rebalance_Sell[-2] , 2) )

st.write('_'*50) ; data , Symbol = get_data()
st.write('_'*50) ; Rebalance_Buy (data)
st.write('_'*50) ; Rebalance_Sell (data)
st.write('_'*50) ; plot(data)
st.write('_'*50)

st.subheader('F(X)_Returns')
st.write('  F(X) จะถูก Fix Position  ด้วย ***(Rebalance_Buy : แปรผกผัน ∝)***  และ  ***(Rebalance_Sell : แปรผันตรง /)***')
st.write('ควรจะต้องดีกว่า Benchmark Returns ถ้าหาไม่ได้ก็ควรจะใช้ Rebalance แบบปกติ Fix% ไปดีกว่า....')
st.write('_'*50)
st.write('Cr. กองทุนความมั่งคั่งแห่งชาติ ')
