import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import streamlit as st
import pydeck as pdk
MAPKEY = "sk.eyJ1IjoibWlrZXlxdWFudCIsImEiOiJja2lqN2pvMGgwZHdyMnZxcmF2cHF4ZGR0In0.pBJ7Tv-oTyWSAd_V1SOpQw"


REGIONS={"Northeast":["MA", "ME", "RI", "CT", "NH", "VT", "NY", "PA", "NJ","DE", "MD"],
      "Southeast": ["WV", "VA", "KY", "TN", "NC","SC", "GA", "AL", "MS","AK", "LA", "FL"],
      "Midwest": ["OH", "IN", "MI", "IL", "MO", "WI", "MN", "IA", "KS", "NE", "SD", "ND"],
      "Southwest": ["TX", "OK", "NM", "AZ"],
      "West": ["CO", "WY", "MT", "ID", "WA", "OR", "UT", "NV", "CA", "AL", "HI"],
         "All States":["CO", "WY", "MT", "ID", "WA", "OR", "UT", "NV", "CA", "AL", "HI","OH", "IN", "MI", "IL", "MO", "WI", "MN", "IA", "KS", "NE", "SD", "ND","TX", "OK", "NM", "AZ","WV", "VA", "KY", "TN", "NC","SC", "GA", "AL", "MS","AK", "LA", "FL","MA", "ME", "RI", "CT", "NH", "VT", "NY", "PA", "NJ","DE", "MD"]}

def preprocess_data():
    df=pd.read_csv("mcdonalds.csv")
    for index, row in df.iterrows():
        z = row["zip"]
        if len(z) == 4:
            cleaned_zip = "0" + z
            df.at[index, 'zip'] = cleaned_zip
    df=df.drop(columns=["storeUrl"])
    df["lat"]=df["Y"]
    df["lon"]=df["X"]
    df.to_csv("mcdonalds_clean1.csv", sep=',', index=False)


def bar_chart_data(df,option,region):

    states=region
    master=[]
    for state in states:
        values=[]
        dfs=df[df["state"]==state]
        total=len(state)
        totalv=0
        for value in dfs[option]:
            if value=="Y":
                values.append(1)
            else:
                values.append(0
                              )
        avg=np.average(values)
        master.append([state,avg])
    dfb=pd.DataFrame(master,columns=["State","Avg"])
    dfb1=pd.DataFrame(master,columns=["State","Avg"]).sort_values(by= "Avg", ascending=False).reset_index()
  
    return dfb1
def bar_chart(df,feat,reg):
    if feat=="Play Place":
        col="playplace"
    if feat=="Drive-Thru":
        col="driveThru"
    if feat=="Free Wifi":
        col="freeWifi"
    if feat=="Arch Card":
        col="archCard"



    data=bar_chart_data(df,col,REGIONS[reg])
    for index1, name in enumerate(data["State"]):
            plt.bar(name,data["Avg"][index1],label=name)
    plt.xticks(rotation='vertical')
    plt.title("% of locations with {}".format(col))
    plt.tight_layout()
    plt.xlabel("State")

    plt.ylabel("%")



    return plt

def filter_by_zip_feature(state,feat):
    x=[]
    df=pd.read_csv("mcdonalds_clean1.csv")
    if feat["archCard"]==True:
        df=df[df["archCard"]=="Y"]
        x.append("Arch Card")

    if feat["freeWifi"]==True:
        df=df[df["freeWifi"]=="Y"]
        x.append("Free Wifi")


    if feat["driveThru"]==True:
        df=df[df["driveThru"]=="Y"]
        x.append("Drive Through")


    if feat["playplace"]==True:
        df=df[df["playplace"]=="Y"]
        x.append("Play Place")
    string = ""
    for v in x:
        if v == "Free Wifi":
            string= string + v+" "
        else:
            string= string + v+"s"+ " "
    s=string.split(" ")
    s.pop(-1)

    if len(s)==4:
        s[1]=s[1].replace(s[1],s[1]+" and")
    string=""
    for x in s:
        string=string+x+ " "
    if len(s)==6:
        s[1]=s[1].replace(s[1],s[1]+", ")
        s[3]=s[3].replace(s[3],s[3]+" and")
    string=""
    for x in s:
        string=string+x+ " "
    if len(s)==8:
        s[1]=s[1].replace(s[1],s[1]+", ")
        s[3]=s[3].replace(s[3],s[3]+", ")
        s[5]=s[5].replace(s[5],s[5]+" and")
    string=""
    for x in s:
        string=string+x+ " "


    dff=df
    dff=df[df["state"]==(state.upper())]
    lon=dff["lon"]
    lat=dff["lat"]

    return dff,len(dff), string

preprocess_data()
df=pd.read_csv("mcdonalds_clean1.csv")
st.title("Mcdonalds Location Analysis")
page=st.sidebar.radio("Select Function: ",["Barchart","Filter Map"])
if page=="Barchart":
    st.sidebar.header("Bar Chart Filter Selection")
    feat=st.sidebar.radio("Please select a feature ", ["Play Place","Drive-Thru","Arch Card","Free Wifi"])
    reg=st.sidebar.radio("Please select a Region ", ["Northeast","Southeast","Midwest","Southwest","West","All States"])

    st.header(f'States with the best Mcdonalds features')
    if feat == "Free Wifi":
        st.write(f'Below is a bar graph of states that have the highest percent of {feat} ')
    else:
        st.write(f'Below is a bar graph of states that have the highest percent of {feat}s ')

    st.pyplot(bar_chart(df,feat,reg))
if page=="Filter Map":
    st.title("Find Mcdonalds by State with Feature Filters")
    st.sidebar.title("Map Filters: ")
    state=st.sidebar.text_input("Enter a State abbreviation","AL")
    if state.upper() in REGIONS["All States"]:
        pass
    else:
        st.sidebar.write("Please enter a valid abbreviation next time. Alabama will be used as default.")
        state="AL"     
    pp=st.sidebar.checkbox("Play Place")
    dt=st.sidebar.checkbox("Drive-Through")
    wf=st.sidebar.checkbox("Free Wifi")
    ac=st.sidebar.checkbox("Arch Card")
    features={"archCard":ac,"playplace":pp,"freeWifi":wf,"driveThru":dt}
    dff,count,string=filter_by_zip_feature(state,features)
    if len(string) > 0:
        st.write(f"There are {count}  Mcdonalds with {string} in {state.upper()}")
    else:
        st.write(f"There are {count}  Mcdonalds in {state.upper()}")

    view = pdk.data_utils.compute_view(dff[["lon", "lat"]])
    view.pitch = 20
    view.bearing = 0

    column_layer = pdk.Layer(
    "ColumnLayer",
    data=dff,
    get_position=["lon", "lat"],
    get_elevation=0,
    elevation_scale=3,
    radius=2000,

    pickable=True,
    auto_highlight=True,
    )
    tooltip={"html": "{storeNumber}\nPlay-Place:{playplace} \nDrive-Thru:{driveThru} \nArch Card:{archCard} \nFree Wifi:{freeWifi}", "style": {"background": "grey", "color": "white", "font-family": '"Helvetica Neue", Arial', "z-index": "10000"}}

    r = pdk.Deck(
        column_layer,
        initial_view_state=view,
        tooltip=tooltip,
        mapbox_key=MAPKEY,
        map_style='mapbox://styles/mapbox/light-v9'
    )

    st.pydeck_chart(r)
