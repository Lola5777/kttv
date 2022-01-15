import streamlit as st
import pandas as pd
import pydeck as pdk
import requests, json
from urllib.error import URLError
import time
# import tkinter
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import requests, json, io
from pandas.io.json import json_normalize
import weatherapp




# @st.cache(suppress_st_warning=True)  
def show_values_on_bars(p,axs):
    def _show_on_single_plot(ax):        
        for p in ax.patches:
            _x = p.get_x() + p.get_width() / 2
            _y = p.get_y() + p.get_height()
            value = '{:.2f}'.format(p.get_height())
            ax.text(_x, _y, value, ha="center") 

    if isinstance(axs, np.ndarray):
        for idx, ax in np.ndenumerate(axs):
            _show_on_single_plot(ax)
    else:
        _show_on_single_plot(axs)  
def choice_location():
    lat = ''
    lon = ''
    choice = st.radio(
        "Choices",
        ('Location', 'City')
     )
    if choice == 'Location':
        chat = []
        lat =  st.text_input('latitude :')
        lon =  st.text_input('longitude :')
        if st.button("View weather"):
            return lat,lon,''
    else:
        choices =  {0:" - ",1: "Hà nội", 2: "Đà nẵng", 3: "TPHCM"}   
        option = st.selectbox("Chọn thành phố", choices.keys(), format_func=lambda x:choices[ x ])
        city=''
        if option == 0:
            return '','',''
        if option == 1:
            lat = '21.022736'
            lon = '105.8018581'
            city = 'hanoi'
        elif option == 2:
            lat = '16.0717633'
            lon = '107.9376931'
            city = 'danang'
        elif option == 3:
            lat = '10.7542869'
            lon = '106.1333107'
            city = 'saigon'

    if len(lat) < 3 or len(lon) < 3:
        return '','',''
    return lat,lon,city
def weather(lat,lon,city):
    new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;"><b><u>Dự báo cho 2 ngày tới</u></b></p>'
    st.markdown(new_title, unsafe_allow_html=True)
    complete_url = "https://api.openweathermap.org/data/2.5/onecall?lat="+lat+"&lon="+lon+"&units=metric&lang=vi&exclude=alerts,daily&appid=48d1cb52728b2558b0aa14f2517bb14d"
    response = requests.get(complete_url)
    x = response.json()  
    df = pd.json_normalize(x)
    new_title = '<p style="font-family:sans-serif; color:Blue; font-size: 32px;">TimeZone : '+df['timezone'][0]+'</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    # st.text("lat = "+str(df['lat'][0])+", lon = "+str(df['lon'][0]))
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 22px;">Lat : '+str(df['lat'][0])+' Lon : '+str(df['lon'][0])
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:sans-serif; color:Green; font-size: 22px;">Weather :</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    new_title = '<p style="font-family:sans-serif; color:Black; font-size: 18px;">'
    new_title += '<br>Main : '+df['current.weather'][0][0]['main']
    new_title += '<br>Description : '+df['current.weather'][0][0]['description']
    new_title += ' <img src="http://openweathermap.org/img/w/' + df['current.weather'][0][0]['icon'] + '.png"></p>' 
    st.markdown(new_title, unsafe_allow_html=True)
    # st.write(df)
    # for k,v in df.items():
    #     if k in ['timezone_offset','timezone','minutely','lat','lon','current.weather']:
    #         continue
    #     st.write(k+" ===> "+str(v[0]))
    table = None
    for h in df['hourly']:
        i=1
        
        for t in h:
            rows = []
            # rows.append("Hour "+str(i+1))
            rows.append(convertUNIX_timestamp(t['dt']))
            rows.append(str(t['temp']))
            rows.append(str(t['wind_speed']))
            rows.append(str(t['pressure']))
            rows.append(str(t['humidity']))
            rows.append(str(t['visibility']))
            if 'rain' in t.keys():
                rows.append(str(t['rain']["1h"]))
            else:
                rows.append("0.0")
            # st.write(t)
            if 'weather' in t.keys():
                for x in t['weather']:
                    rows.append(x['description'])
            else:
                rows.append(" - ")
            i += 1
            a = pd.Series(rows).T
            if table is None:
                table = pd.DataFrame(rows)
                table = table.T
            else:
                table = table.append(a,ignore_index=True)   
    table.columns = ['Hourly','Temp','Wind','Pressure','Humidity','Visibility','Rain','Description']       
    st.subheader("Thông số trong 48h tới")    
    st.write(table)
    temp = table['Temp'].astype(float)
    wind = table['Wind'].astype(float)
    # h = [i for i in range(0,48)]
    # fig = plt.figure(figsize = (10, 5))
    # plt.bar(h,temp)
    # plt.xlabel("Giờ")
    # plt.ylabel("Nhiệt độ")
    # plt.title("Nhiệt độ trong 2 ngày tới")
    # st.pyplot(fig)  
    st.subheader("Nhiệt độ trong 2 ngày tới")
    st.bar_chart(temp) 
    st.line_chart(temp)     
    st.subheader("Tốc độ gió trong 2 ngày tới")
    st.bar_chart(wind)  
    st.line_chart(wind)  
    if len(city) > 2:
        st.image('https://wttr.in/'+city+'.png?m3&lang=vi') 
        st.image('https://wttr.in/'+city+'.png?format=v2')
        st.image('https://v3.wttr.in/'+city+'.png')

#==============================
def menu():
    # rad =st.sidebar.selectbox("Menu",["Khí tượng","Thủy văn","Mưa","Hải văn","Dự báo cho 2 ngày tới","Dự báo 6 ngày tới"])  
    rad =st.sidebar.selectbox("Menu",["Dự báo cho 2 ngày tới","Dự báo cho 6 ngày tới"])  
    # if rad == "Khí tượng":
    #     # st.title(rad)
    #     new_title = '<p style="font-family:sans-serif; color:Red; font-size: 42px;"><b>'+rad+' ngày : '+d+'</b></p>'
    #     st.markdown(new_title, unsafe_allow_html=True)

    #     get_dataKT(d)
    if rad == "Dự báo cho 2 ngày tới":
        lat,lon,city = choice_location()
        if len(lat) > 3 or len(lon) > 3:
            weather(lat,lon,city)
    elif rad == "Dự báo cho 6 ngày tới":
        weatherapp.main() 

def main(d):
    menu(d)

    

if __name__ == "__main__":
    # count = st_autorefresh(interval=60 * 1000, key="dataframerefresh")
#     d = datetime.now().strftime('%m/%d/%Y')
    main()
    # st.write(f"Count refresh :  {count} ")
