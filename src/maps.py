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

    if category == "leisure activities":
        for i, row in df_leisure.iterrows():
            geom = {
                "location":[row["latitude"], row["longitude"]],
                "tooltip" : row["name"]
            }
            
        
            if row["place"] == "bowling":
                icon = Icon(color = "orange",
                            prefix = "fa",
                            icon = "circle",
                            icon_color = "black"
                )
                
            elif row["place"] == "spa":
                icon = Icon(color = "blue",
                            prefix = "fa",
                            icon = "heart",
                            icon_color = "black"
                )
            
            elif row["place"] == "escape room":
                icon = Icon(color = "green",
                            prefix = "fa",
                            icon = "search",
                            icon_color = "black"
                )
                
            elif row["place"] == "laser tag":
                icon = Icon(color = "beige",
                            prefix = "fa",
                            icon = "tag",
                            icon_color = "black"
                )
                
            elif row["place"] == "pista de hielo":
                icon = Icon(color = "pink",
                            prefix = "fa",
                            icon = "cube",
                            icon_color = "black"
                )
                
            elif row["place"] == "karts":
                icon = Icon(color = "red",
                            prefix = "fa",
                            icon = "car",
                            icon_color = "black"
                )
                
            elif row["place"] == "tunel de viento":
                icon = Icon(color = "lightgreen",
                            prefix = "fa",
                            icon = "rocket",
                            icon_color = "black"
                )
                
            elif row["place"] == "karts":
                icon = Icon(color = "red",
                            prefix = "fa",
                            icon = "car",
                            icon_color = "black"
                )

            elif row["place"] == "teleferico":
                icon = Icon(color = "purple",
                            prefix = "fa",
                            icon = "paper-plane",
                            icon_color = "black"
                )
                
            else:
                icon = Icon(color = "lightblue",
                            prefix = "fa",
                            icon = "hand-rock-o",
                            icon_color = "black"
                )
            Marker(**geom,icon = icon ).add_to(map_1)


    elif category == "restaurant":
        for i, row in df_restaurants.iterrows():
            if row["place"] == tipo:
                geom = {
                    "location":[row["latitude"], row["longitude"]],
                    "tooltip" : row["name"]
                }
                icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "cutlery",
                                icon_color = "black"
                )


                Marker(**geom,icon = icon ).add_to(map_1)
        
    elif category == "snacks":
        for i, row in df_snacks.iterrows():
            geom = {
                "location":[row["latitude"], row["longitude"]],
                "tooltip" : row["name"]
            }
            
        
            if row["place"] == "cake":
                icon = Icon(color = "beige",
                            prefix = "fa",
                            icon = "cutlery",
                            icon_color = "black"
                )
                
            elif row["place"] == "cupcakes":
                icon = Icon(color = "pink",
                            prefix = "fa",
                            icon = "cutlery",
                            icon_color = "black"
                )
            
            elif row["place"] == "sweets":
                icon = Icon(color = "lightblue",
                            prefix = "fa",
                            icon = "cutlery",
                            icon_color = "black"
                )
                
            elif row["place"] == "ice cream":
                icon = Icon(color = "white",
                            prefix = "fa",
                            icon = "cutlery",
                            icon_color = "black"
                )
                
            elif row["place"] == "juices":
                icon = Icon(color = "orange",
                            prefix = "fa",
                            icon = "cutlery",
                            icon_color = "black"
                )
                
            else:
                icon = Icon(color = "lightgreen",
                            prefix = "fa",
                            icon = "cutlery",
                            icon_color = "black"
                )
                
            Marker(**geom,icon = icon ).add_to(map_1)
    return map_1

def datafr(tipo):
    df = df_restaurants[df_restaurants["place"]==tipo].drop(['price_level', 'place', 'CP', 'latitude',
       'longitude', 'geometry'], axis=1)
    return df