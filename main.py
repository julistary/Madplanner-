import streamlit as st
from PIL import Image
import src.manage_data as dat
from streamlit_folium import folium_static

st.set_page_config(page_title="madplanner", page_icon="⚡️", layout='centered', initial_sidebar_state='auto')

st.title('Madrid, the place to be 🔥')

imagen = Image.open("images/madriz.jpeg")
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
        "Select a category", ["restaurant", "outdoors", "drinks", "party", "snacks", "culture", "leisure activities"]
    )
    tipo = st.selectbox(
        f"What kind of {category}?", dat.subcategory(f"{category}")
    )
    folium_static(dat.mapita(f"{category}", f"{tipo}"))
    st.dataframe(dat.datafr(f"{tipo}", f"{category}"))

elif filter == "location": 
    pass