import streamlit as st
from PIL import Image
import src.manage_data as dat
from streamlit_folium import folium_static
import time
st.set_page_config(page_title="madplanner", page_icon="⚡️", layout='centered', initial_sidebar_state='auto')

imagen = Image.open("images/madrid.png")
st.image(imagen)

st.header("""
What do you want to do today?  
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
        st.dataframe(dat.films())  

elif filter == "type":
    tipo = st.selectbox(
        "Select a type of plan 👯‍♀️", ["friends", "couple", "individual", "team building", "family"]
    )

    plan = dat.type_of_plan(f"{tipo}")
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))
    if "cinema" in list(plan.place.unique()):
        st.dataframe(dat.films())  

elif filter == "price":
    maxmin = st.select_slider(
        'Select max price 💸', options=[15,20,30,40,50,60,70,80,90,100,110,120,130,300]
    )
    time.sleep(2)
    with st.spinner(text='In progress..'):
       time.sleep(2)
       st.success('Done 🚀')
    plan = dat.planes_2("price",maxmin)
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))   
    if "cinema" in list(plan.place.unique()):
        st.dataframe(dat.films())  

elif filter == "rating":
    maxmin = st.select_slider(
        'Select min rating 💎', options=[0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5]
    )
    time.sleep(2)

    time.sleep(4)
    with st.spinner(text='In progress..'):
       time.sleep(2)
       st.success('Done 🚀')
    plan = dat.planes_2("rating",maxmin)
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))   
    if "cinema" in list(plan.place.unique()):
        st.dataframe(dat.films())  




