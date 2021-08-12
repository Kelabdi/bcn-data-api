import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
# from support.streamlit_mongo_conn import database
from support.collection_data import df_pop,df_unem
from support.api_connection import api_url


# HEADER -------------
header = st.empty()
header.title("BCN DATA")

# Selecting Collection --------------
coll = ["","population", "unemployed"]
chosen = st.selectbox("Please choose a dataset",coll)

if chosen:
    if chosen=="population":
        url = "/read/population"
        db = requests.get(api_url+url)
        df = df_pop
        info = {"":"",
            "Total Population by year":"/bcn-population-by-year/",
            "Population by district name":"/bcn-population-by-district/",
            "Population by neighborhood name":"/bcn-population-by-neighborhood/"
            }
    elif chosen=="unemployed":
        url = "/read/unemployed"
        db = requests.get(api_url+url)
        df = df_unem
        info = {"":"",
            "Total Unemployment by year":"/bcn-unemployment-by-year/",
            "Registered unemployees by district name":"/bcn-unemployed-by-district/",
            "Registered unemployees by neighborhood name":"/bcn-unemployed-by-neighborhood/"
            }
    title2 = st.title(f"You choosed {chosen} dataset")
    st.text("structure of data")
    st.json(db.json()[0])

# Getting some data from CSV to compare ----------------
    st.text("Dataframe")
    st.dataframe(df)

    # filters = df.columns
    # print(filters)
    # data = st.multiselect("Select data to groupby", filters)
    # gby = [x for x in data]
    # project = {x:1 for x in filter}
    # project["_id"] = 0
    # print(project)
    # st.dataframe(df[filter].groupby(gby))


# FIRST DATA OFFERED MAKING API REQUESTS ------------------

    title3 = st.title('Let\'s check some interesting info')
    info_s = st.selectbox('', info.keys())

    if info_s == list(info.keys())[1]:
        years = list(dict.fromkeys([e["Year"] for e in db.json()]))
        print(years)
        year = st.slider("Select a Year for population data review", int(years[-1]), int(years[0]))
        json = requests.get(api_url+f"{info[info_s]}{year}").json()
        st.json(json)
        y_coord = []
        for i in years:
            res = requests.get(api_url+f"{info[info_s]}{year}").json()
            y_coord.append(res["Total"])
        print(y_coord)
        chart = go.Figure([go.Bar(x=years,y=y_coord)])
        st.plotly_chart(chart)
        
    if info_s == list(info.keys())[2]:
        dist_names = list(dict.fromkeys([e["District"]["Name"] for e in db.json()]))
        print(dist_names)
        d_name = st.select_slider("Select a District for data review", dist_names)
        years = list(dict.fromkeys([e["Year"] for e in db.json()]))
        print(years)
        year = st.slider("Select a Year for population data review", int(years[-1]), int(years[0]))
        # json = requests.get(api_url+f"{info[info_s]}{d_name}").json()
        # st.json(json)

        api = requests.get(api_url+url+f"?Year={int(year)}&District.Name={d_name}").json()
        # st.json(api)

        male = [e["Total"] for e in api if e["Gender"]=="Male"]
        female = [e["Total"] for e in api if e["Gender"]=="Female"]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=["Male"], 
            y=[sum(male)],
            name='Male citizens',
            marker_color='indianred'))
        fig.add_trace(go.Bar(
            x=["Female"], 
            y=[sum(female)],
            name='Female citizens',
            marker_color='lightsalmon'))
        fig.update_layout(title_text=f"Gender distribution on {d_name}")
        st.plotly_chart(fig)


        # for i in info_s:
        #     res = requests.get(api_url+f"{info[i]}{year}").json()
        # # data_year = list(db.json()({"Year":f"{year}"}))
        # # data_y = [e[] for e in db.json()]
        #     st.json(res)


# st.text(value)

# columns = st.columns(2)
# with columns[0]:
#     st.color_picker("color",key="1")
# with columns[1]:
#     text_color = st.color_picker("Color #4","#227022")

# num_cols = st.slider('Columns', min_value=1, max_value=10)

# columns = st.columns(num_cols)

# colors = ["#2E8B57","#BA55D3","#FFC0CB", "#4169E1", "#F4A460", "#696969", "#F5F5DC", "#FF1493", "#FFFF00", "#00FA9A"]

# for i in range(num_cols):
#     columns[i].markdown(f'<div style="background:{colors[i]}; text-align:center; color:{text_color}">{i+1}</div>', unsafe_allow_html=True)



# prop = st.slider('Columns', min_value=1, max_value=99, value=50)
# props = [prop, 100-prop]

# columns = st.columns((prop,100-prop))

# for i in [0,1]:
#     columns[i].markdown(f'<div style="background:{colors[i]}; text-align:center; color:{text_color}">{props[i]}</div>', unsafe_allow_html=True)



