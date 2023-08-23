import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
import yfinance as yf
import streamlit as st
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go

st.title("التنبؤ بأسعار الاسهم السعودية")
st.write("صفحة خاصة للتنبؤ لبعض أسعار السهم السعودية ")
st.warning("الصفحة عبارة عن وسيلة لمساعدة المستخدمين لمعرفة اتجاه الاسعار ولسيت نصيحة أو توصية للشراء",
            icon="⚠️")


#Import historical from yfinance
start = "2000-01-01"
end = date.today()

stocks = ["2222.SR", "1211.SR", "2010.SR", "3060.SR", "4164.SR","2050.SR", "2280.SR",
        "1180.SR", "1120.SR", "1010.SR", "8010.SR","7010.SR", "7020.SR","5110.SR", "4220.SR"]


selected_stock = st.selectbox('الرجاء اختيار الشركة', stocks)

n_weeks = st.slider("اختر عدد الشهور", 0, 6)
st.text(" اختيار 0 يعني عدم التنبؤ \n أما اختيار من 0-6 التبنؤ بالاشهر المستقبلية")

period = n_weeks 


@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, start, end)
    data.reset_index(inplace=True)
    return data


#Load data
data_load_state = st.text("جاري تجهيز البيانات")
data = load_data(selected_stock)
data = data.rename(columns={"2222.SR": "ارامكو"})
data_load_state.text('!جاري تجهيز البيانات... تم')

st.subheader("البيانات الحقيقية")
st.write(data.tail())

# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="الافتتاح"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="الاغلاق"))
	fig.layout.update(title_text='البيانات الزمنية', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()

# Predict forecast with Prophet.
train = data[['Date','Close']]
train = train.rename(columns={"Date": "ds", "Close": "y"})

#To datetime
train['ds'] = pd.to_datetime(train['ds'])

#Fit and predict
m = Prophet(weekly_seasonality=True)
#m.
m.fit(train)
future = m.make_future_dataframe(periods=period, freq="M")
forecast = m.predict(future)

# Show and plot forecast
st.subheader('البيانات المتنبؤة')
st.write(forecast.tail(14))
    
st.write(f'عرض توقع الاسعار {period} الاسابيع')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("مكونات التنبؤ")
fig2 = m.plot_components(forecast)
st.write(fig2)
#m.plot_plotly()