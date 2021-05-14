import streamlit as st
from PIL import Image
import src.streamlit as ss
import src.maps as map
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
    if category == "restaurant":
        tipo = st.selectbox(
            "What type of food do you want to eat?", ['japanese', 'burger', 'vietnamese', 'tapas', 'korean', 'brewery',
        'greek', 'vegan', 'french', 'mexican', 'asian', 'ramen',
        'argentino', 'grill', 'italian', 'thai', 'mid eastern', 'indian',
        'pizza', 'healthy', 'vegetarian', 'seafood', 'gluten free',
        'pet friendly restaurant']
            )
        folium_static(map.mapita(f"{category}", f"{tipo}"))
        st.dataframe(map.datafr(f"{tipo}"))
    else:
        folium_static(map.mapita(f"{category}", "ninguno"))
