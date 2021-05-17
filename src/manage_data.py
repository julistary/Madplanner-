import pandas as pd
from folium import Circle, Marker, Icon, Map
from pymongo import MongoClient, GEOSPHERE
import random
import numpy as np
conn = MongoClient("localhost:27017")
db = conn.get_database("madrid")
import requests
from bs4 import BeautifulSoup
import json
import unicodedata 


leisure = db.get_collection("leisure")
outdoors = db.get_collection("outdoors")
restaurants = db.get_collection("restaurants")
drinks = db.get_collection("drinks")
party = db.get_collection("party")
snacks = db.get_collection("snacks")
culture = db.get_collection("culture")
transport = db.get_collection("transport")

df_restaurants = pd.read_csv("data/restaurants.csv", index_col=0)
df_snacks = pd.read_csv("data/snacks.csv", index_col=0)
df_culture = pd.read_csv("data/culture.csv", index_col=0)
df_party = pd.read_csv("data/party.csv", index_col=0)
df_drinks = pd.read_csv("data/drinks.csv", index_col=0)
df_outdoors = pd.read_csv("data/outdoors.csv", index_col=0)
df_leisure = pd.read_csv("data/leisure.csv", index_col=0)
df_madrid = pd.read_csv("data/df_madrid.csv",index_col=0)
df_distritos = pd.read_csv("data/df_districts.csv",index_col=0)

def mapita(category, tipo):
    """
    It gives a map with the places according to what you want to look for.
    Args:
        category(str): the category for which you want to search for places
        tipo(str):the subcategory for which you want to search for places
    Returns:
        The map with markers
    """
        
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
    """
    It gives all the subcategories available in a category
    Args:
        category(str): the category for which you want to search for places
    Returns:
        A list with all the subcategories
    """
        
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
    """
    Creates a dataframe with the places of the subcategory 
    Args:
        category(str): the category for which you want to search for places
        tipo(str):the subcategory for which you want to search for places
    Returns:
        The df with al the places
    """
        
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
    'longitude', 'geometry', 'type', 'subtype'], axis=1)
    df = df.reset_index()
    df = df.drop(["index"],axis=1)
    
    return df

def planes(df_1, df_2, coll_1, coll_2):

    """
    Creates a dataframe with two locations that together meet certain conditions
    Args:
        df_1(df): a dataframe with all the places of a category
        df_2(df): a dataframe with all the places of a category
        coll_1(mongo collection): a collection with all the places of a category
        coll_2(mongo collection): a collection with all the places of a category
    Returns:
        The df with the plan
    """
    
    intersection = set(list(df_1.CP.unique())).intersection(set(list(df_2.CP.unique())))

    cp = list(intersection)

    cp_random = random.choice(cp)

    plan1 = list(coll_1.find({"CP":str(int(cp_random))}))

    plan2 = list(coll_2.find({"CP":str(int(cp_random))}))
    
    p1_random = random.choice(plan1)
    p2_random = random.choice(plan2)

    df1 = pd.DataFrame.from_dict(p1_random)
    df2 = pd.DataFrame.from_dict(p2_random)
    df = pd.concat([df1,df2])
    
    df = df.set_index("_id")
    df =df.drop(["geometry"], axis = 1)
    df = df.drop_duplicates()
    
    return df

def type_of_plan(plan):
    """
    Calls the previous function "planes", with some values that depends on the desired type of plan selected.
    Args:
        plan(str): the type of plan that has been selected
    Returns:
        The call to "planes"
    """
    
    
    options_team_building = { "option_1" : [df_outdoors, df_restaurants, outdoors, restaurants],
                             "option_2" : [df_leisure, df_restaurants, leisure, restaurants]
                            }

    options_friends = { "option_1" : [df_restaurants, df_drinks, restaurants, drinks],
                        "option_2" : [df_outdoors, df_restaurants, outdoors, restaurants],
                        "option_3" : [df_leisure, df_restaurants, leisure, restaurants],
                        "option_4" : [df_party, df_restaurants, party, restaurants],
                        "option_5" : [df_drinks, df_party, drinks, party],
                        "option_6" : [df_snacks, df_leisure, snacks, leisure],
                        "option_7" : [df_outdoors, df_snacks, outdoors, snacks]
                     }

    options_couple = { "option_1" : [df_restaurants, df_drinks, restaurants, drinks],
                       "option_2" : [df_leisure, df_restaurants, leisure, restaurants],
                       "option_3" : [df_culture, df_restaurants, culture, restaurants],
                       "option_4" : [df_culture, df_snacks, culture, snacks]
                     }

    options_individual = { "option_1" : [df_culture, df_restaurants, culture, restaurants],
                           "option_2" : [df_culture, df_snacks, culture, snacks]
                         }

    options_family = {  "option_1" : [df_culture, df_restaurants, culture, restaurants],
                        "option_2" : [df_culture, df_snacks, culture, snacks],
                        "option_3" : [df_outdoors, df_restaurants, outdoors, restaurants],
                        "option_4" : [df_outdoors, df_snacks, outdoors, snacks],
                        "option_5" : [df_leisure, df_restaurants, leisure, restaurants],
                        "option_6" : [df_leisure, df_snacks, leisure, snacks]
                     }
    
    if plan == "family":
        options =  options_family
    elif plan == "friends":
        options = options_friends
    elif plan == "individual":
        options = options_individual
    elif plan == "couple":
        options = options_couple
    elif plan == "team building":
        options = options_team_building
     
    opt = random.choice(list(options.keys()))
    args = options[opt]
    arg_1 = args[0]  
    arg_2 = args[1]  
    arg_3 = args[2]  
    arg_4 = args[3]  
    
    return planes(arg_1, arg_2, arg_3, arg_4)

def get_df(df):
    """
    Cleans a dataframe
    Args:
        df(df): the dataframe that has to be cleaned
    Returns:
        The df cleaned
    """
    
    df = df.set_index("name")
    return df.drop(["price_level", "CP", "latitude", "longitude", "type", "subtype"],  axis=1)

def geoquery_2(coordinates):
    coord_point = {"type":"Point", "coordinates": coordinates}
    collection = db.get_collection("transport")
    query = {"geometry": {"$near": {"$geometry": coord_point,"$minDistance": 0, "$maxDistance": 2000}}}
    query_final = collection.find(query)
    df = pd.DataFrame((query_final))
    return df

def get_map(df,df_tr):
    """
    Creates a map with the values of a dataframe
    Args:
        df(df): the dataframe with the places that have to be displayed
    Returns:
        The map
    """
    
    map_1 = Map(location=[list(df.latitude.unique())[0],list(df.longitude.unique())[0]],zoom_start=15)
    for i, row in df.iterrows():
        geom = {
                    "location":[row["latitude"], row["longitude"]],
                    "tooltip" : row["name"]
                }
        icon = Icon(color = "white",
                                prefix = "fa",
                                icon = "trophy",
                                icon_color = "black"
                )

        Marker(**geom,icon = icon ).add_to(map_1)
    
    for i, row in df_tr.iterrows():
        geom = {
                    "location":[row["latitude"], row["longitude"]],
                    "tooltip" : row["name"]
                }
        if row["place"] == "bus":            
             icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "bus",
                                icon_color = "black"
                )   
        elif row["place"] == "train" or row["place"] == "metro":
            icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "train",
                                icon_color = "black"
                )
        else:
            icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "car",
                                icon_color = "black"
                ) 
        Marker(**geom,icon = icon ).add_to(map_1)        
    
        
    return map_1
   
def planes_2(tipo,maxmin):

    """
    Creates a dataframe with two locations that together meet certain conditions
    Args:
        tipo(str): the name of the condition.
        maxmin(float): the condition limit value
    Returns:
        The df with the plan
    """

    options = {"snacks + restaurant" : [df_snacks, df_restaurants, snacks, restaurants],
     "snacks + leisure activity" : [df_snacks, df_leisure, snacks, leisure],
     "snacks + outdoors activity" : [df_snacks, df_outdoors, snacks, outdoors],
     "snacks + culture" : [df_snacks, df_culture, snacks, culture],
     "snacks + drinks" : [df_snacks, df_drinks, snacks, drinks],
     "snacks + party" : [df_snacks, df_party, snacks, party],
     "restaurant + leisure activity" : [df_restaurants, df_leisure, restaurants, leisure],
     "restaurant + outdoors activity" : [df_restaurants, df_outdoors, restaurants, outdoors],
     "restaurant + culture" : [df_restaurants, df_culture, restaurants, culture],
     "restaurant + drinks" : [df_restaurants, df_drinks, restaurants, drinks],
     "restaurant + party" : [df_restaurants, df_party, restaurants, party],
     "leisure activity + outdoors activity" : [df_leisure, df_outdoors, leisure, outdoors],
     "leisure activity + culture" : [df_leisure, df_culture, leisure, culture],
     "leisure activity + drinks" : [df_leisure, df_drinks, leisure, drinks],
     "leisure activity + party" : [df_leisure, df_party, leisure, party],  
     "outdoors activity + culture" : [df_outdoors, df_culture, outdoors, culture],
     "outdoors activity + drinks" : [df_outdoors, df_drinks, outdoors, drinks],
     "outdoors activity + party" : [df_outdoors, df_party, outdoors, party],
     "culture + drinks" : [df_culture, df_drinks, culture, drinks],
     "culture + party" : [df_culture, df_party, culture, party],
     "drinks + party" : [df_drinks, df_party, drinks, party]
    }
     
    opt = random.choice(list(options.keys()))
    args = options[opt]
    df_1 = args[0]  
    df_2 = args[1]  
    coll_1 = args[2]  
    coll_2 = args[3] 
    
    df = planes(df_1, df_2, coll_1, coll_2)
    
    if tipo == "price":
        prices = []
        for p in list(df.price_level):
            if p == 0.0:
                prices.append(0)
            elif p == 1.0:
                prices.append(15)
            elif p == 2.0:
                prices.append(25)
            elif p == 3.0:
                prices.append(50)
            else: 
                prices.append(150)

        if sum(prices) <= maxmin:
            return df
        else: 
            return planes_2("price",maxmin)
    
    elif tipo == "rating":
        rate = []
        for r in list(df.rating):
            rate.append(r)

        if np.mean(rate) <= maxmin:
            return planes_2("rating",maxmin)
        else: 
            return df

def films():
    """
    Creates a dataframe with all the movies that are displayed right now at the cinema by scrapping "Cinesa"
    Returns:
        A df with all the films available.
    """
    
    url = "https://www.cinesa.es/peliculas/cartelera"
    html = requests.get(url)
    soup = BeautifulSoup(html.content, "html.parser")

    films = soup.find_all("a", {"class": "vf"})

    list_of_films = [a.getText().strip() for a in films]
    list_of_films_cleaned = []
    for index,f in enumerate(list_of_films):
        if index%2 == 0:
            list_of_films_cleaned.append(f)
    list_of_films_cleaned

    dict_films = {"films available" : list_of_films_cleaned}

    return pd.DataFrame.from_dict(dict_films, orient = "columns")
    
def barrio_a_coordenadas(df_madrid,df_distritos, district):
    coordinates = {}
    district = unicodedata.normalize('NFD', district)\
    .encode('ascii', 'ignore')\
    .decode("utf-8")
    print(district)
    lista_distritos = ['fuencarral','el pardo', 'hortaleza', 'ciudad lineal', 'san blas',
                       'canillejas', 'barajas', 'moratalaz', 'puente de vallecas', 'vicalvaro',
                       'villa de vallecas', 'villaverde', 'usera', 'carabanchel', 'latina', 
                       'moncloa','aravaca', 'centro', 'tetuan', 'chamartin', 'chamberi', 'retiro',
                       'arganzuela', 'salamanca']
    if district.lower() in lista_distritos:
        district = district.upper()
        cp = 28037
        for index, row in df_distritos.iterrows():
            if district in row.Distrito:
                cp = row.CP
        datos = requests.get(f"https://geocode.xyz/{cp}?json=1").json()
        datos = datos["alt"]["loc"]
        for country in datos:
            if country['countryname'] == "Spain":
                coordinates["latt"] = country["latt"]
                coordinates["long"] = country["longt"]
    else:
        for index, row in df_madrid.iterrows():
            if district.upper() in row.poblacion.upper():
                coordinates["latt"] = row["lon"][:6]
                coordinates["long"] = row["lat"][:6]            
                break
    return coordinates

def geoquery(coordinates):
    collection = db.get_collection("todo")
    coord_point = {"type":"Point", "coordinates": [float(coordinates['latt']), float(coordinates['long'])]}
    query = {"geometry": {"$near": {"$geometry": coord_point,"$minDistance": 0, "$maxDistance": 1500}}}
    query_final = collection.find(query)
    df = pd.DataFrame((query_final))
    return df

def df_planes_bonito(df):
    df_plan = df[df["type"]=="plan"]
    df_plan = df_plan.set_index("name")
    try:
        df_plan = df_plan.drop(["_id","CP","price_level", "type","subtype", "latitude", "longitude", "geometry"],axis=1)
        df_plan = df_plan.drop(["place"],axis=1).drop_duplicates()
        return df_plan
    except: 
        pass
    
def df_tpte_bonito(df):
    df_tpte = df[df["type"]=="transport"]
    df_tpte = df_tpte.set_index("name")
    try:
        df_tpte = df_tpte.drop(["subtype","rating","_id","CP","price_level","address", "type", "latitude", "longitude", "geometry","price"],axis=1)
        df_tpte = df_tpte.drop_duplicates()
        df_tpte = df_tpte.rename(columns={"place":"mean of transport near"})
        return df_tpte
    except:
        df_tpte = df_tpte.drop(['_id', 'latitude', 'longitude', 'geometry', 'type'],axis=1)
        df_tpte = df_tpte.drop_duplicates()
        df_tpte = df_tpte.rename(columns={"place":"mean of transport near"})
        return df_tpte
    
def mapita_2(df,coordinates):
    map_1 = Map(location=[float(coordinates['latt']), float(coordinates['long'])],zoom_start=15)

    for i, row in df.iterrows():
        if row["type"] == "plan":
            geom = {
            "location":[row["latitude"], row["longitude"]],
            "tooltip" : row["name"]
            }
            
            if row["subtype"] == "restaurants":
                iconito = "cutlery"
            elif row["subtype"] == "leisure":
                iconito = "rocket"
            elif row["subtype"] == "outdoors":
                iconito = "pagelines"
            elif row["subtype"] == "snacks":
                iconito = "cutlery"
            elif row["subtype"] == "party":
                iconito = "glass"
            elif row["subtype"] == "drinks":
                iconito = "glass"
            else:
                iconito = "book"

            icon = Icon(color = "lightgreen",
                            prefix = "fa",
                            icon = iconito,
                            icon_color = "black"
            )

        elif row["type"] == "transport":
            geom = {
            "location":[row["latitude"], row["longitude"]],
            "tooltip" : row["place"]
            }

            if row["place"] == "bus":            
                icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "bus",
                                icon_color = "black"
                )   
            elif row["place"] == "train" or row["place"] == "metro":
                icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "train",
                                icon_color = "black"
                )
            else:
                icon = Icon(color = "lightblue",
                                prefix = "fa",
                                icon = "car",
                                icon_color = "black"
                ) 


        Marker(**geom,icon = icon ).add_to(map_1)
    return map_1