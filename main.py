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
        "Select a category 🧐", ["restaurant", "outdoors", "drinks", "party", "snacks", "culture", "leisure activities"]
    )
    tipo = st.selectbox(
        f"What kind of {category}?", dat.subcategory(f"{category}")
    )
    folium_static(dat.mapita(f"{category}", f"{tipo}"))
    st.dataframe(dat.datafr(f"{tipo}", f"{category}"))

elif filter == "type":
    tipo = st.selectbox(
        "Select a type of plan 👯‍♀️", ["friends", "couple", "individual", "team building", "family"]
    )

    plan = dat.type_of_plan(f"{tipo}")
    st.dataframe(dat.get_df(plan))
    folium_static(dat.get_map(plan))


elif filter == "price":
    max_ = st.select_slider(
        'Select max price 💸', options=[15,20,30,40,50,60,70,80,90,100,110,120,130]
    )
    st.dataframe(dat.select_plan(max_))
    with st.spinner(text='In progress'):
       time.sleep(5)
       st.success('Done')


