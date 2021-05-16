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

def planes(df_1, df_2, coll_1, coll_2):
    
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
        options = options_friend
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
    df = df.set_index("name")
    return df.drop(["place", "CP", "latitude", "longitude"], axis=1)

def get_map(df):
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
        
    return map_1





