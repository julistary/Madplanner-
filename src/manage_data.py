import pandas as pd
from folium import Circle, Marker, Icon, Map

df_restaurants = pd.read_csv("data/restaurants.csv", index_col=0)
df_snacks = pd.read_csv("data/snacks.csv", index_col=0)
df_culture = pd.read_csv("data/culture.csv", index_col=0)
df_party = pd.read_csv("data/party.csv", index_col=0)
df_drinks = pd.read_csv("data/drinks.csv", index_col=0)
df_outdoors = pd.read_csv("data/outdoors.csv", index_col=0)
df_leisure = pd.read_csv("data/leisure.csv", index_col=0)

def mapita(category, tipo):
    map_1 = Map(location=[40.428990,-3.681209],zoom_start=15)

    if category == "restaurant": 
        df = df_restaurants
        color = "lightblue"
        icono = "cutlery"
        
    elif category == "snacks":
        df = df_snacks
        color = "blue"
        icono = "cutlery"
    
    elif category == "drinks":
        df = df_drinks
        color = "pink"
        icono = "beer"
    
    elif category == "leisure activities":
        df = df_leisure
        color = "red"
        icono = "rocket"
    
    elif category == "outdoors":
        df = df_outdoors
        color = "green"
        icono = "pagelines"

    elif category == "party":
        df = df_party
        color = "purple"
        icono = "glass"
    
    else:
        df = df_culture
        color = "white"
        icono = "book"
    
    for i, row in df.iterrows():
        if row["place"] == tipo:
            geom = {
                "location":[row["latitude"], row["longitude"]],
                "tooltip" : row["name"]
            }
            icon = Icon(color = color,
                            prefix = "fa",
                            icon = icono,
                            icon_color = "black"
            )


            Marker(**geom,icon = icon ).add_to(map_1)
  
   
    return map_1

def subcategory(category):
    if category == "restaurant":
        df = df_restaurants
    elif category == "outdoors":
        df = df_outdoors
    elif category == "leisure activities":
        df = df_leisure
    elif category == "drinks":
        df = df_drinks
    elif category == "party":
        df = df_party
    elif category == "snacks":
        df = df_snacks
    else:
        df = df_culture

    return list(df.place.unique())

def datafr(tipo,category):
    if category == "restaurant":
        df = df_restaurants
    elif category == "outdoors":
        df = df_outdoors
    elif category == "leisure activities":
        df = df_leisure
    elif category == "drinks":
        df = df_drinks
    elif category == "party":
        df = df_party
    elif category == "snacks":
        df = df_snacks
    else:
        df = df_culture

    df = df[df["place"]==tipo].drop(['price_level', 'place', 'CP', 'latitude',
    'longitude', 'geometry'], axis=1)
    df = df.reset_index()
    df = df.drop(["index"],axis=1)
    
    return df
  


