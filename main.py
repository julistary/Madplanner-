import streamlit as st
from PIL import Image
import src.manage_data as dat
from streamlit_folium import folium_static
import time
import pandas as pd 
from datetime import datetime
from dotenv import load_dotenv
import os
import numpy as np
from pymongo import MongoClient, GEOSPHERE


url_mongo = os.getenv("url")
conn = MongoClient(url_mongo)
db = conn.get_database("madrid")
users = db.get_collection("users")


leisure = db.get_collection("leisure")
df_madrid = pd.read_csv("data/df_madrid.csv",index_col=0)
df_m = pd.read_csv("data/df_districts_2.csv",index_col=0)

st.set_page_config(page_title="madplanner", page_icon="⚡️", layout='centered', initial_sidebar_state='auto')

imagen = Image.open("images/madrid.png")
st.image(imagen)
name = st.text_input('Enter your name')

years = st.number_input('Enter your age')

gender = st.selectbox('Enter your gender', ['Select..','Female','Male','Other','Prefer not to answer'])

ocupation = st.selectbox('Enter your ocupation', ['Select..','Working','Studying','None'])

children = st.selectbox('Do you have any children?', ['Select..','YES','NO'])

world = st.selectbox('Where do you live?', ['Select..','Madrid','Another city in Spain','Outside of Spain'])

time_ = datetime.now()

weekday = datetime.today().weekday()

if ((years != 0.0) and (gender in ['Female','Male','Other','Prefer not to answer'])) and ((ocupation in ['Working','Studying','None']) and (children in ['YES','NO'])) and world in ['Madrid','Another city in Spain','Outside of Spain']:
    
    st.header(f"Hello {name}. What do you want to do today? ⚡️⚡️ ")

    st.write("""
    How do you want to search?
    """)

    filter =  st.selectbox(
        "Select a filter", ["select..","category", "location", "type", "price", "rating"]
    )

    if filter == "category":
        category = st.selectbox(
            "Select a category 🥑", ["select..","restaurant", "outdoors", "drinks", "party", "snacks", "culture", "leisure activities"]
        )
        if category in ["restaurant", "outdoors", "drinks", "party", "snacks", "culture", "leisure activities"]:
            tipo = st.selectbox(
                f"What kind of {category}?", ["select.."] + dat.subcategory(f"{category}")
            )
            if tipo in dat.subcategory(f"{category}"):
                folium_static(dat.mapita(f"{category}", f"{tipo}"))
                st.dataframe(dat.datafr(f"{tipo}", f"{category}"))
                query = { "name": f"{name}",
                        "age" : f"{years}",
                        "filter" : "category",
                        "category": f"{category}",
                        "subcategory": f"{tipo}",
                        "time": f"{time_}",
                        "weekday": f"{weekday}",  
                        "gender": f"{gender}", 
                        "ocupation": f"{ocupation}", 
                        "children": f"{children}",
                        "residence": f"{world}" }
                users.insert_one(query)

            
            if tipo == "cinema":
                st.write("""These are the films available in the cinema right now: """)
                st.dataframe(dat.films())  


    elif filter == "type":
        tipo = st.selectbox(
            "Select a type of plan 👯‍♀️", ["select..","friends", "couple", "individual", "team building", "family"]
        )
        if tipo in ["friends", "couple", "individual", "team building", "family"]:
            with st.spinner(text='Thinking🧠'):
                plan = dat.type_of_plan(f"{tipo}")
                st.dataframe(dat.get_df(plan))
                df_tr = dat.geoquery_2([plan.latitude.unique()[0],plan.longitude.unique()[0]])
                folium_static(dat.get_map(plan,df_tr))
                st.success('Done 🚀')  
                query = { "name": f"{name}",
                        "age" : f"{years}",
                        "filter" : "type",
                        "category" : f"{tipo}",
                        "subcategory": np.nan,
                        "time": f"{time_}",
                        "weekday": f"{weekday}",  
                        "gender": f"{gender}", 
                        "ocupation": f"{ocupation}", 
                        "children": f"{children}",
                        "residence": f"{world}" }
                users.insert_one(query)

            if "cinema" in list(plan.place.unique()):        
                st.write("""These are the films available in the cinema right now: """)
                st.dataframe(dat.films())  


    elif filter == "price":
        maxmin = st.select_slider(
            'Select max price and then click the button💸', options=[15,20,30,40,50,60,70,80,90,100,110,120,130,300]
        )
        b = st.button('Hit me!')
        if b == True:
            with st.spinner(text='In progress..'):
                plan = dat.planes_2("price",maxmin)
                st.success('Done 🚀')
            st.dataframe(dat.get_df(plan))
            df_tr = dat.geoquery_2([plan.latitude.unique()[0],plan.longitude.unique()[0]])
            folium_static(dat.get_map(plan,df_tr))   
            if "cinema" in list(plan.place.unique()):
                st.write("""These are the films available in the cinema right now: """)
                st.dataframe(dat.films())  
            query = { "name": f"{name}",
                    "age" : f"{years}",
                    "filter" : "price",
                    "category" : f"{maxmin}",
                    "subcategory": np.nan,
                    "time": f"{time_}",
                    "weekday": f"{weekday}",  
                    "gender": f"{gender}", 
                    "ocupation": f"{ocupation}", 
                    "children": f"{children}",
                    "residence": f"{world}" }
            users.insert_one(query)

    elif filter == "rating":
        maxmin = st.select_slider(
            'Select min rating 💎', options=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9]
        )
        b = st.button('Hit me!')
        if b == True:
            with st.spinner(text='In progress..'):
                plan = dat.planes_2("rating",maxmin)
                st.success('Done 🚀')
            st.dataframe(dat.get_df(plan))
            df_tr = dat.geoquery_2([plan.latitude.unique()[0],plan.longitude.unique()[0]])
            folium_static(dat.get_map(plan,df_tr))   
            if "cinema" in list(plan.place.unique()):
                st.write("""These are the films available in the cinema right now: """)
                st.dataframe(dat.films())  
            query = { "name": f"{name}",
                    "age" : f"{years}",
                    "filter" : "rating",
                    "category" : f"{maxmin}",
                    "subcategory": np.nan,
                    "time": f"{time_}",
                    "weekday": f"{weekday}",  
                    "gender": f"{gender}", 
                    "ocupation": f"{ocupation}", 
                    "children": f"{children}",
                    "residence": f"{world}" }
            users.insert_one(query)

    elif filter == "location":

        districts = ['Arganzuela', 'Barajas','Carabanchel',
                            'Centro', 'Chamartín', 'Chamberí', 'Ciudad Lineal', 
                            'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca', 'Moratalaz',
                            'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blás-Canillejas', 'Tetuán',
                            'Usera', 'Vicálvaro', 'Villa de Vallecas', 'Villaverde']

        towns = ['Alcalá de Henares', 'Alcobendas', 'Alcorcón', 'Algete',
                                    'Aranjuez', 'Arganda del Rey', 'Arroyomolinos',
                                    'Boadilla del Monte', 'Ciempozuelos', 'Collado Villalba',
                                    'Colmenar Viejo', 'Coslada', 'El Escorial', 'Fuenlabrada',
                                    'Galapagar', 'Getafe', 'Humanes de Madrid', 'Las Rozas de Madrid',
                                    'Leganés', 'Majadahonda', 'Mejorada del Campo', 'Móstoles',
                                    'Navalcarnero', 'Paracuellos de Jarama', 'Parla', 'Pinto',
                                    'Pozuelo de Alarcón', 'Rivas-Vaciamadrid',
                                    'San Fernando de Henares', 'San Lorenzo de El Escorial',
                                    'San Martín de la Vega', 'San Sebastián de los Reyes',
                                    'Torrejón de Ardoz', 'Torrelodones', 'Tres Cantos', 'Valdemoro',
                                    'Villanueva de la Cañada', 'Villanueva del Pardillo',
                                    'Villaviciosa de Odón']
        time.sleep(1)
        donde = st.selectbox(
            "Where? 🗺", ["select..",'Madrid', 'Other towns in Madrid']
        )
        if donde in ['Madrid', 'Other towns in Madrid']:

            if f"{donde}" == 'Madrid': 
                district = st.selectbox(
                    "Select a district", ["select.."] + districts
                )

            else: 
                district = st.selectbox(
                    "Select a village", ["select.."] + towns
                )
        
        
            if district in (districts + towns):
                st.warning('It may take a few seconds, please wait☺️')
                time.sleep(15)
                coordinates = dat.barrio_a_coordenadas(df_madrid,df_m,f"{district}")
                st.write("Plans")
                st.dataframe(dat.df_planes_bonito(dat.geoquery(coordinates)))
                st.write("Means of transport")
                st.dataframe(dat.df_tpte_bonito(dat.geoquery(coordinates)))
                folium_static(dat.mapita_2(dat.geoquery(coordinates),coordinates))
                
                query = { "name": f"{name}",
                        "age" : f"{years}",
                        "filter" : "location",
                        "category" : f"{donde}",
                        "subcategory": f"{district}",
                        "time": f"{time_}",
                        "weekday": f"{weekday}",  
                        "gender": f"{gender}", 
                        "ocupation": f"{ocupation}", 
                        "children": f"{children}",
                        "residence": f"{world}" }
                users.insert_one(query)
