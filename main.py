import streamlit as st
from PIL import Image
import src.manage_data as dat
from streamlit_folium import folium_static
import time
import pandas as pd 
from datetime import datetime

df_madrid = pd.read_csv("data/df_madrid.csv",index_col=0)
df_m = pd.read_csv("data/df_districts_2.csv",index_col=0)

c = open("preferences/cat.csv", "a+")
l = open("preferences/loc.csv", "a+")
t = open("preferences/type.csv", "a+")
p = open("preferences/price.csv", "a+")
r = open("preferences/rat.csv", "a+")

st.set_page_config(page_title="madplanner", page_icon="⚡️", layout='centered', initial_sidebar_state='auto')

imagen = Image.open("images/madrid.png")
st.image(imagen)
name = st.text_input('Enter your name')

years = st.number_input('Enter your age')

time_ = datetime.now()

st.header("""
What do you want to do today? ⚡️⚡️ 
""")

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
    tipo = st.selectbox(
        f"What kind of {category}?", ["select.."] + dat.subcategory(f"{category}")
    )
    folium_static(dat.mapita(f"{category}", f"{tipo}"))
    st.dataframe(dat.datafr(f"{tipo}", f"{category}"))
    if tipo == "cinema":
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  

    query = f"\n{name},{years},{category},{tipo},category,{time_}"
    c.write(query)

elif filter == "type":
    tipo = st.selectbox(
        "Select a type of plan 👯‍♀️", ["select..","friends", "couple", "individual", "team building", "family"]
    )
    time.sleep(4)
    with st.spinner(text='Thinking🧠'):
        plan = dat.type_of_plan(f"{tipo}")
        st.dataframe(dat.get_df(plan))
        df_tr = dat.geoquery_2([plan.latitude.unique()[0],plan.longitude.unique()[0]])
        folium_static(dat.get_map(plan,df_tr))
        st.success('Done 🚀')  

    if "cinema" in list(plan.place.unique()):        
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  
    query = f"\n{name},{years},{tipo},type,{time_}"
    t.write(query)

elif filter == "price":
    maxmin = st.select_slider(
        'Select max price 💸', options=[15,20,30,40,50,60,70,80,90,100,110,120,130,300]
    )
    time.sleep(2)
    with st.spinner(text='In progress..'):
        plan = dat.planes_2("price",maxmin)
        st.success('Done 🚀')
    st.dataframe(dat.get_df(plan))
    df_tr = dat.geoquery_2([plan.latitude.unique()[0],plan.longitude.unique()[0]])
    folium_static(dat.get_map(plan,df_tr))   
    if "cinema" in list(plan.place.unique()):
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  
    query = f"\n{name},{years},{maxmin},price,{time_}"
    p.write(query)

elif filter == "rating":
    maxmin = st.select_slider(
        'Select min rating 💎', options=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9]
    )
    time.sleep(2)
    with st.spinner(text='In progress..'):
       plan = dat.planes_2("rating",maxmin)
       st.success('Done 🚀')
    st.dataframe(dat.get_df(plan))
    df_tr = dat.geoquery_2([plan.latitude.unique()[0],plan.longitude.unique()[0]])
    folium_static(dat.get_map(plan,df_tr))   
    if "cinema" in list(plan.place.unique()):
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  
    query = f"\n{name},{years},{maxmin},rating,{time_}"
    r.write(query)

elif filter == "location":
    time.sleep(1)
    donde = st.selectbox(
        "Where? 🗺", ["select..",'Madrid', 'Other towns in Madrid']
    )


    if f"{donde}" == 'Madrid': 
        time.sleep(4)
        district = st.selectbox(
            "Select a district", ["select..", 'Arganzuela', 'Barajas','Carabanchel',
                    'Centro', 'Chamartín', 'Chamberí', 'Ciudad Lineal', 
                    'Fuencarral-El Pardo', 'Hortaleza', 'Latina', 'Moncloa-Aravaca', 'Moratalaz',
                    'Puente de Vallecas', 'Retiro', 'Salamanca', 'San Blás-Canillejas', 'Tetuán',
                    'Usera', 'Vicálvaro', 'Villa de Vallecas', 'Villaverde']
        )

    else: 
        district = st.selectbox(
            "Select a village", ["select..",'Alcalá de Henares', 'Alcobendas', 'Alcorcón', 'Algete',
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

        )
    st.warning('It may take a few seconds, please wait☺️')
    time.sleep(2)
    coordinates = dat.barrio_a_coordenadas(df_madrid,df_m,f"{district}")
    st.write("Plans")
    st.dataframe(dat.df_planes_bonito(dat.geoquery(coordinates)))
    st.write("Means of transport")
    st.dataframe(dat.df_tpte_bonito(dat.geoquery(coordinates)))
    folium_static(dat.mapita_2(dat.geoquery(coordinates),coordinates))

    query = f"\n{name},{years},{donde},{district},location,{time_}"
    l.write(query)

c.close()
l.close()
p.close()
r.close()
t.close()

