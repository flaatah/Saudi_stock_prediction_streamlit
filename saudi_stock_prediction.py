# Import Streamlit and yfinance modules
import streamlit as st
import yfinance as yf
from datetime import date
from prophet.plot import plot_plotly, plot_components_plotly
from plotly import graph_objs as go
import pandas as pd
from prophet import Prophet
from datetime import datetime
import datetime

st.title("التنبؤ بأسعار الاسهم السعودية")
st.write("صفحة خاصة للتنبؤ لبعض أسعار السهم السعودية ")
st.warning("الصفحة عبارة عن وسيلة لمساعدة المستخدمين لمعرفة اتجاه الاسعار ولسيت نصيحة أو توصية للشراء",
            icon="⚠️")




# Define the start and end dates
START = "2000-01-01"
TODAY = datetime.datetime.now()

# Create a dictionary of symbols and names of the companies
companies = {"2222.SR": "ارامكو", "1211.SR": "معادن","2010.SR": "سابك", "3060.SR": "اسمنت ينبع",
	      "4164.SR": "النهدي","2050.SR": "صافولا","2280.SR": "المراعي","1180.SR": "الاهلي",
		  "1120.SR": "الراجحي", "1010.SR": "الرياض", "8010.SR": "التعاونية","7010.SR": "الاتصالات",
		  "7020.SR": "موبايلي","5110.SR": "كهرباء السعودية","4220.SR": "اعمار"}

# Slider for user to choose number of months
# The model can predict up to 12 months
n_months = st.slider("اختر عدد الشهور", 0, 12)
st.write(" اختيار 0 يعني عدم التنبؤ \n أما اختيار من 1-12 التبنؤ بالاشهر المستقبلية")
period = n_months 


# Create a list of names for the select box options
names = list(companies.values())

# Display a select box widget with the names as options
selected_name = st.selectbox("اختر الشركة", names)

# Get the symbol corresponding to the selected name
selected_symbol = list(companies.keys())[names.index(selected_name)]

# Download and cache the stock data for the selected symbol
data = yf.download(selected_symbol, START, TODAY)
data.reset_index(inplace=True)

# Display the stock data as a line chart
st.write(" البيانات الحقيقية لاخر ستة أيام")
st.write(data.tail(6))
#st.line_chart(data["Close"])



# Plot raw data
def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="الافتتاح"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="الاغلاق"))
	fig.layout.update(title_text='عرض البيانات الزمنية التاريخية', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)	
plot_raw_data()


# Predict forecast with Prophet.
train = data[['Date','Close']]
train = train.rename(columns={"Date": "ds", "Close": "y"})

#To datetime
train['ds'] = pd.to_datetime(train['ds'])

#Fit and predict
m = Prophet(yearly_seasonality=True)
m.fit(train)
future = m.make_future_dataframe(periods=period, freq="M")
forecast = m.predict(future)

# Show and plot forecast
st.subheader('البيانات المتنبؤة')
st.write(forecast[['ds', 'trend', 'yhat', 'yhat_lower', 'yhat_upper']]
.tail(12))
    
st.write(f' عرض توقع الاسعار ل {period} أشهر')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write("مكونات التنبؤ")
fig2 = plot_components_plotly(m,forecast)
st.write(fig2)
#m.plot_plotly()
