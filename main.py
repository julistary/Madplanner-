import streamlit as st
from PIL import Image
import src.manage_data as dat
from streamlit_folium import folium_static
import time
import pandas as pd 
df_madrid = pd.read_csv("data/df_madrid.csv",index_col=0)
df_distritos = pd.read_csv("data/df_districts.csv",index_col=0)

st.set_page_config(page_title="madplanner", page_icon="⚡️", layout='centered', initial_sidebar_state='auto')

imagen = Image.open("images/madrid.png")
st.image(imagen)

st.header("""
What do you want to do today? ⚡️⚡️ 
""")

st.write("""
How do you want to search?
""")

filter =  st.selectbox(
    "Select a filter", ["category", "location", "type", "price", "rating"]
)

if filter == "category":
    category = st.selectbox(
        "Select a category 🥑", ["restaurant", "outdoors", "drinks", "party", "snacks", "culture", "leisure activities"]
    )
    tipo = st.selectbox(
        f"What kind of {category}?", dat.subcategory(f"{category}")
    )
    folium_static(dat.mapita(f"{category}", f"{tipo}"))
    st.dataframe(dat.datafr(f"{tipo}", f"{category}"))
    if tipo == "cinema":
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  

elif filter == "type":
    tipo = st.selectbox(
        "Select a type of plan 👯‍♀️", ["friends", "couple", "individual", "team building", "family"]
    )

    plan = dat.type_of_plan(f"{tipo}")
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))
    if "cinema" in list(plan.place.unique()):        
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  

elif filter == "price":
    maxmin = st.select_slider(
        'Select max price 💸', options=[15,20,30,40,50,60,70,80,90,100,110,120,130,300]
    )
    time.sleep(2)
    with st.spinner(text='In progress..'):
        plan = dat.planes_2("price",maxmin)
        st.success('Done 🚀')
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))   
    if "cinema" in list(plan.place.unique()):
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  

elif filter == "rating":
    maxmin = st.select_slider(
        'Select min rating 💎', options=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8,4.9]
    )
    time.sleep(2)
    with st.spinner(text='In progress..'):
       plan = dat.planes_2("rating",maxmin)
       st.success('Done 🚀')
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))   
    if "cinema" in list(plan.place.unique()):
        st.write("""These are the films available in the cinema right now: """)
        st.dataframe(dat.films())  


elif filter == "location":
    donde = st.selectbox(
        "Where? 🗺", ['Madrid', 'Other towns']
    )

    if f"{donde}" == 'Madrid': 
        district = st.selectbox(
            "Select a district", ['Fuencarral','El Pardo', 'Hortaleza', 'Ciudad Lineal', 'San Blás',
                       'Canillejas', 'Barajas', 'Moratalaz', 'Puente de Vallecas', 'Vicálvaro',
                       'Villa de Vallecas', 'Villaverde', 'Usera', 'Carabanchel', 'Latina', 
                       'Moncloa','Aravaca', 'Centro', 'Tetuán', 'Chamartín', 'Chamberí', 'Retiro',
                       'Arganzuela', 'Salamanca']
        )

    else: 
        district = st.selectbox(
            "Select a village", ['Móstoles', 'Alcalá de Henares','Fuenlabrada',
                                'Leganés','Getafe','Alcorcón','Torrejón de Ardoz',
                                'Parla','Alcobendas', 'Las Rozas de Madrid', 'San Sebastián de los Reyes',
                                'Rivas-Vaciamadrid','Pozuelo de Alarcón', 'Coslada', 'Valdemoro',
                                'Majadahonda' , 'Collado Villalba', 'Aranjuez', 'Arganda del Rey',
                                'Boadilla del Monte', 'Pinto','Colmenar Viejo','Tres Cantos',
                                'San Fernando de Henares','Galapagar','Arroyomolinos','Navalcarnero',
                                'Villaviciosa de Odón','Paracuellos de Jarama','Ciempozuelos','Torrelodones',
                                'Mejorada del Campo','Villanueva de la Cañada','Algete','Humanes de Madrid',
                                'San Martín de la Vega','San Lorenzo de El Escorial','Villanueva del Pardillo', ' El Escorial']

        )
    time.sleep(5)
    try:
        coordinates = dat.barrio_a_coordenadas(df_madrid,df_distritos,f"{district}")
    except:
        time.sleep(5)
    finally:
        coordinates = dat.barrio_a_coordenadas(df_madrid,df_distritos,f"{district}")
    st.write("Plans")
    st.dataframe(dat.df_planes_bonito(dat.geoquery(coordinates)))
    st.write("Means of transport")
    st.dataframe(dat.df_tpte_bonito(dat.geoquery(coordinates)))
    folium_static(dat.mapita_2(dat.geoquery(coordinates),coordinates))

