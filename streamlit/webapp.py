import streamlit as st
import requests
import plotly.express as px
import plotly.graph_objects as go
# from support.streamlit_mongo_conn import database
from support.collection_data import df_pop,df_unem
from support.api_connection import api_url


# HEADER -------------
st.image("img/sagrada-familia.jpg")
header = st.empty()
header.title("SOME DATA ABOUT BARCELONA CITY")

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
    title2 = st.header(f"You choosed {chosen} dataset")
    st.subheader("structure of data")
    st.json(db.json()[0])

# Getting some data from CSV to compare ----------------
    st.subheader("Dataframe")
    st.dataframe(df)


# FIRST DATA OFFERED MAKING API REQUESTS ------------------
    title3 = st.title('Let\'s check some interesting info')
    info_s = st.selectbox('', info.keys())


# SELECTED TOTAL DATA BY YEAR ----------------
    if info_s == list(info.keys())[1]:
        years = list(dict.fromkeys([e["Year"] for e in db.json()]))
        years.reverse()
    # Button for all time data
        t_year = st.checkbox('All time')
        if not t_year:
            year = st.slider("Select a Year for data review", int(years[-1]), int(years[0]))
            json = requests.get(api_url+f"{info[info_s]}{year}").json()
            # st.json(json)

            columns = st.columns(2)
            with columns[0]:
                st.markdown(f'<div style="background:#7D8AD2; text-align:center; color:black">{json["Year"]}</div>', unsafe_allow_html=True)
            with columns[1]:
                st.markdown(f'<div style="background:#7D8AD2; text-align:center; color:black">{json["Total"]}</div>', unsafe_allow_html=True)
            
            if chosen=="unemployed":
                api = requests.get(api_url+url+f"?Year={int(year)}").json()
                months = list(dict.fromkeys([e["Month"] for e in db.json()]))
                month_list = []
                for i in months:
                    month_list.append(sum([e["Total"] for e in api if (e["Month"]==i)]))
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=months, 
                    y=month_list,
                    marker_color='indianred'))
                fig.update_layout(title_text=f"Registered Unemployed on year {year}")
                st.plotly_chart(fig)


        if t_year:
            y_coord = []
            for i in years:
                res = requests.get(api_url+f"{info[info_s]}{i}").json()
                y_coord.append(res["Total"])
            fig = go.Figure([go.Scatter(x=years,y=[int(y) for y in y_coord])])
            fig.update_layout(title_text=f"Total {chosen} in BCN")
            st.plotly_chart(fig)


# SELECTED DATA BY DISTRICT NAME ----------------        
    if info_s == list(info.keys())[2]:
        dist_names = list(dict.fromkeys([e["District"]["Name"] for e in db.json()]))
        d_name = st.selectbox("Select a District for data review", dist_names)
        json = requests.get(api_url+f"{info[info_s]}{d_name}").json()

        years = list(dict.fromkeys([e["Year"] for e in db.json()]))
        years.reverse()
    # Button for all time data
        t_year = st.checkbox('All time')
        if not t_year:
            year = st.slider("Select a Year for data review", int(years[-1]), int(years[0]))

            api = requests.get(api_url+url+f"?Year={int(year)}&District.Name={d_name}").json()
        
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

            


        total_year = []
        for i in years:
            total_year.append(sum([e["Total"] for e in json if e["Year"]==i]))
        
        if t_year:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=years, 
                y=total_year,
                name='Male citizens',
                marker_color='indianred'))
            fig.update_layout(title_text=f"Overall {chosen} count on {d_name}")
            st.plotly_chart(fig)


        if chosen=="population" and not t_year: 
            ages = list(dict.fromkeys([e["Age"] for e in db.json()]))
            age_list_male = []
            age_list_female = []
            for i in ages:
                age_list_male.append(sum([e["Total"] for e in api if (e["Gender"]=="Male" and e["Age"]==i)]))
                age_list_female.append(sum([e["Total"] for e in api if (e["Gender"]=="Female" and e["Age"]==i)]))


            fig = go.Figure()
            fig.add_trace(go.Bar(
            x=ages, 
            y=age_list_male,
            name='Male citizens',
            marker_color='indianred'))
            fig.add_trace(go.Bar(
            x=ages, 
            y=age_list_female,
            name='Female citizens',
            marker_color='lightsalmon'))
            fig.update_layout(title_text=f"Age & Gender distribution on {d_name}")
            st.plotly_chart(fig)

    # Button for all place data
        t_dist = st.checkbox('All Districts')
        if not t_year and t_dist:
            y_coord = []
            for i in dist_names:
                res = requests.get(api_url+f"{info[info_s]}{i}").json()
                y_coord.append(sum([e["Total"] for e in res if e["Year"]==f"{year}"]))
            fig = go.Figure([go.Bar(x=dist_names,y=[int(y) for y in y_coord],marker_color='indianred')])
            fig.update_layout(title_text=f"Overall {chosen} count by District")
            st.plotly_chart(fig)


# SELECTED DATA BY NEIGHBORHOOD NAME ----------------  
    if info_s == list(info.keys())[3]:
        dist_names = list(dict.fromkeys([e["Neighborhood"]["Name"] for e in db.json()]))
        d_name = st.selectbox("Select a Neighborhood for data review", dist_names)
        json = requests.get(api_url+f"{info[info_s]}{d_name}").json()

        years = list(dict.fromkeys([e["Year"] for e in db.json()]))
        years.reverse()

    # Button for all time data
        t_year = st.checkbox('All time')
        if not t_year:
            year = st.slider("Select a Year for data review", int(years[-1]), int(years[0]))

            api = requests.get(api_url+url+f"?Year={int(year)}&Neighborhood.Name={d_name}").json()

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

        total_year = []
        for i in years:
            total_year.append(sum([e["Total"] for e in json if e["Year"]==i]))
        
        if t_year:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=years, 
                y=total_year,
                name='Male citizens',
                marker_color='indianred'))
            fig.update_layout(title_text=f"Overall {chosen} count on {d_name}")
            st.plotly_chart(fig)

        if chosen=="population" and not t_year: 
            ages = list(dict.fromkeys([e["Age"] for e in db.json()]))
            print(ages)
            age_list_male = []
            age_list_female = []
            for i in ages:
                age_list_male.append(sum([e["Total"] for e in api if (e["Gender"]=="Male" and e["Age"]==i)]))
                age_list_female.append(sum([e["Total"] for e in api if (e["Gender"]=="Female" and e["Age"]==i)]))

            fig = go.Figure()
            fig.add_trace(go.Bar(
            x=ages, 
            y=age_list_male,
            name='Male citizens',
            marker_color='indianred'))
            fig.add_trace(go.Bar(
            x=ages, 
            y=age_list_female,
            name='Female citizens',
            marker_color='lightsalmon'))
            fig.update_layout(title_text=f"Age & Gender distribution on {d_name}")
            st.plotly_chart(fig)
            
    # Button for all place data
        t_dist = st.checkbox('All Neighborhoods')
        if not t_year and t_dist:    
            y_coord = []
            for i in dist_names:
                res = requests.get(api_url+f"{info[info_s]}{i}").json()
                y_coord.append(sum([e["Total"] for e in res if e["Year"]==f"{year}"]))
            fig = go.Figure([go.Bar(x=dist_names,y=[int(y) for y in y_coord],marker_color='indianred')])
            fig.update_layout(title_text=f"Overall {chosen} count by Neighborhood")
            st.plotly_chart(fig)





