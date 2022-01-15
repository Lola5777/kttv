import os
# import pytz
import pyowm
import streamlit as st
from matplotlib import dates
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib import rcParams
import plotly.graph_objects as go
import plotly.express as px
import requests
st.set_option('deprecation.showPyplotGlobalUse', False)

degree_sign= u'\N{DEGREE SIGN}'
API_KEY =  '48d1cb52728b2558b0aa14f2517bb14d'
owm = pyowm.OWM(API_KEY)
mgr=owm.weather_manager()
place = ''
unit_c = 'celsius'
def get_temperature():
    global place
    days = []
    dates = []
    temp_min = []
    temp_max = []
    try:
        forecaster = mgr.forecast_at_place(place, '3h')
    except:
        st.write("Không tìm thấy thành phố : ",place)
        return (None,None,None)
    forecast=forecaster.forecast
    for weather in forecast:
        day=datetime.utcfromtimestamp(weather.reference_time())
        #day = gmt_to_eastern(weather.reference_time())
        date = day.date()
        if date not in dates:
            dates.append(date)
            temp_min.append(None)
            temp_max.append(None)
            days.append(date)
        temperature = weather.temperature(unit_c)['temp']
        if not temp_min[-1] or temperature < temp_min[-1]:
            temp_min[-1] = temperature
        if not temp_max[-1] or temperature > temp_max[-1]:
            temp_max[-1] = temperature
    return(days, temp_min, temp_max)



def plot_temperatures(days, temp_min, temp_max):
    # days = dates.date2num(days)
    fig = go.Figure(
        data=[
            go.Bar(name='nhiệt độ thấp nhất', x=days, y=temp_min),
            go.Bar(name='nhiệt độ cao nhất', x=days, y=temp_max)
        ]
    )
    fig.update_layout(barmode='group')
    return fig


def plot_temperatures_line(days, temp_min, temp_max):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=temp_min, name='nhiệt độ thấp nhất'))
    fig.add_trace(go.Scatter(x=days, y=temp_max, name='nhiệt độ cao nhất'))
    return fig

def label_xaxis(days):
    plt.xticks(days)
    axes = plt.gca()
    xaxis_format = dates.DateFormatter('%m/%d')
    axes.xaxis.set_major_formatter(xaxis_format)

def draw_bar_chart():
    days, temp_min, temp_max = get_temperature()
    if days == None:
        return
    fig = plot_temperatures(days, temp_min, temp_max)
    st.plotly_chart(fig)
    fig = plot_temperatures_line(days, temp_min, temp_max)
    st.plotly_chart(fig)
    # st.title("Nhiệt độ thấp nhất và cao nhất cho 5 ngày tới :")
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 30px;">Nhiệt độ thấp nhất và cao nhất cho 5 ngày tới</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    for i in range (0,5):
        st.write("### ",temp_min[i],degree_sign,' ----- ',temp_max[i],degree_sign)


# def draw_line_chart():
#     days, temp_min, temp_max = get_temperature()
#     fig = plot_temperatures_line(days, temp_min, temp_max)
#     st.plotly_chart(fig)
#     st.title("Nhiệt độ thấp nhất và cao nhất cho 5 ngày tới")
#     for i in range (0,5):
#         st.write("### Từ ",temp_min[i],degree_sign,' đến ',temp_max[i],degree_sign)

def other_weather_updates():
    pass
    # forecaster = mgr.forecast_at_place(place, '3h')

    # st.title("Impending Temperature Changes :")
    # if forecaster.will_have_fog():
    #     st.write("### FOG Alert!")
    # if forecaster.will_have_rain():
    #     st.write("### Rain Alert")
    # if forecaster.will_have_storm():
    #     st.write("### Storm Alert!")
    # if forecaster.will_have_snow():
    #     st.write("### Snow Alert!")
    # if forecaster.will_have_tornado():
    #     st.write("### Tornado Alert!")
    # if forecaster.will_have_hurricane():
    #     st.write("### Hurricane Alert!")
    # if forecaster.will_have_clouds():
    #     st.write("### Cloudy Skies")    
    # if forecaster.will_have_clear():
    #     st.write("### Clear Weather!")
def mph_to_mps(mph):
    return  0.44704 * mph
def cloud_and_wind():
    try:
        obs=mgr.weather_at_place(place)
    except:
        return
    weather=obs.weather
    cloud_cov=weather.clouds
    winds=weather.wind()['speed']
    # st.title("Mây che phủ và tốc độ gió")
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 30px;">Mây che phủ và tốc độ gió hiện tại</p>'
    st.markdown(new_title, unsafe_allow_html=True)

    st.write('### Mây che phủ : ',cloud_cov,'%')
    st.write('### Tốc độ gió : ',mph_to_mps(winds),'m/s')

def sunrise_and_sunset():
    obs=mgr.weather_at_place(place)
    weather=obs.weather
    st.title("Thời gian mặt trời mọc và lặn :")
    ss=weather.sunset_time(timeformat='iso')
    sr=weather.sunrise_time(timeformat='iso')  
    st.write("### Mặt trời mọc là",sr)
    st.write("### Mặt trời lặn là",ss)

def updates():
    # other_weather_updates()
    cloud_and_wind()
    # sunrise_and_sunset()

# =======================
def plot_line(days, min_t, max_t):
    days = dates.date2num(days)
    rcParams['figure.figsize'] = 6, 4
    plt.plot(days, max_t, color='black', linestyle='solid', linewidth=1, marker='o', markerfacecolor='green',
             markersize=7)
    plt.plot(days, min_t, color='black', linestyle='solid', linewidth=1, marker='o', markerfacecolor='blue',
             markersize=7)
    plt.ylim(min(min_t) - 4, max(max_t) + 4)
    plt.xticks(days)
    x_y_axis = plt.gca()
    xaxis_format = dates.DateFormatter('%d/%m')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.grid(True, color='brown')
    plt.legend(["Nhiệt độ cao nhất", "Nhiệt độ thấp nhất"], loc=1)
    plt.xlabel('Ngày (ngày/tháng)')
    plt.ylabel('Nhiệt độ')
    plt.title('Dự báo cho 6 ngày tới')

    for i in range(5):
        plt.text(days[i], min_t[i] - 1.5, min_t[i],
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='black')
    for i in range(5):
        plt.text(days[i], max_t[i] + 0.5, max_t[i],
                 horizontalalignment='center',
                 verticalalignment='bottom',
                 color='black')
    # plt.show()
    # plt.savefig('figure_line.png')
    st.pyplot()
    plt.clf()


def plot_bars(days, min_t, max_t):
    # print(days)
    days = dates.date2num(days)
    rcParams['figure.figsize'] = 6, 4
    min_temp_bar = plt.bar(days - 0.2, min_t, width=0.4, color='r')
    max_temp_bar = plt.bar(days + 0.2, max_t, width=0.4, color='b')
    plt.xticks(days)
    x_y_axis = plt.gca()
    xaxis_format = dates.DateFormatter('%d/%m')

    x_y_axis.xaxis.set_major_formatter(xaxis_format)
    plt.xlabel('Ngày (ngày/tháng)')
    plt.ylabel('Nhiệt độ')
    plt.title('Dự báo cho 6 ngày tới')

    for bar_chart in [min_temp_bar, max_temp_bar]:
        for index, bar in enumerate(bar_chart):
            height = bar.get_height()
            xpos = bar.get_x() + bar.get_width() / 2.0
            ypos = height
            label_text = str(int(height))
            plt.text(xpos, ypos, label_text,
                     horizontalalignment='center',
                     verticalalignment='bottom',
                     color='black')
    st.pyplot()
    plt.clf()


# Main function
def weather_detail():
    global place
    mgr = owm.weather_manager()
    days = []
    dates_2 = []
    min_t = []
    max_t = []
    try:
        forecaster = mgr.forecast_at_place(place, '3h')
    except:
        st.write("Không tìm thấy thành phố : ",place)
        return

    forecast = forecaster.forecast
    obs = mgr.weather_at_place(place)
    weather = obs.weather
    temperature = weather.temperature(unit='celsius')['temp']
    unit_c = 'celsius'
    for weather in forecast:
        day = datetime.utcfromtimestamp(weather.reference_time())
        date1 = day.date()
        if date1 not in dates_2:
            dates_2.append(date1)
            min_t.append(None)
            max_t.append(None)
            days.append(date1)
        temperature = weather.temperature(unit_c)['temp']
        if not min_t[-1] or temperature < min_t[-1]:
            min_t[-1] = temperature
        if not max_t[-1] or temperature > max_t[-1]:
            max_t[-1] = temperature

    obs = mgr.weather_at_place(place)
    weather = obs.weather
    st.title(f" Dự báo cho '{place[0].upper() + place[1:]}' : ")
    plot_line(days, min_t, max_t)
    plot_bars(days, min_t, max_t)

    st.write(f"## ️ Nhiệt độ hôm nay : {temperature} °C")
    st.write(f"## ☁️ Mây che phủ: {weather.detailed_status}")
    st.write(f"##  Tốc độ gió : {round(weather.wind(unit='km_hour')['speed'])} km/h")
    st.write(f"### ⛅️ Mặt trời mọc :     {weather.sunrise_time(timeformat='iso')} GMT")
    st.write(f"### ☁️ Mặt trời lặn :      {weather.sunset_time(timeformat='iso')} GMT")

    # Expected Temperature Alerts
    st.title("❄️ Cảnh báo : ")
    if forecaster.will_have_fog():
        st.write("### ▶️ Sương mù !!")
    if forecaster.will_have_rain():
        st.write("### ▶️  Mưa ☔")
    if forecaster.will_have_storm():
        st.write("### ▶️ Bão ⛈️!!")
    if forecaster.will_have_snow():
        st.write("### ▶️ Tuyết ❄️!!")
    if forecaster.will_have_tornado():
        st.write("### ▶️ Lốc ️!!")
    if forecaster.will_have_hurricane():
        st.write("### ▶️ Bão ")
    if forecaster.will_have_clear():
        st.write("### ▶️ Dự báo !!")
    if forecaster.will_have_clouds():
        st.write("### ▶️ Trời nhiều mây ⛅")

    st.write('                ')
    st.write('                ')
    i = 0
    st.write(f"#  Ngày :  Thấp nhất - Cao nhất (°C)")
    for obj in days:
        ta = (obj.strftime("%d/%m"))
        st.write(f'### ➡️ {ta} :\t   ({min_t[i]} °C --->  {max_t[i]} °C)')
        i += 1
    st.image('https://wttr.in/'+place+'.png?m3&lang=vi')
    # st.image('https://wttr.in/'+place+'.png?format=v2')   
    st.image('https://v2.wttr.in/'+place+'.png') 
    st.image('https://v3.wttr.in/'+place+'.png')
def main():
    global place
    # st.title("THAM KHẢO")
    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 30px;"><b><i>THAM KHẢO</i></b></p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:sans-serif; color:Red; font-size: 38px;">Dự báo 6 ngày tới cho các thành phố</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    place=st.text_input("Tên thành phố :", "")
    if place == None:
        st.write("Chưa nhập tên thành phố!")

    if st.button("Dự báo"):
        # new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 32px;">Dự báo cho thành phố '+place+'</p>'
        # st.markdown(new_title, unsafe_allow_html=True)
        weather_detail()
        st.markdown('<hr>', unsafe_allow_html=True)
