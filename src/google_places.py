import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
import numpy as np
import time
load_dotenv()


key = os.getenv("key")

url_query = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
what = "query="
key_endpoint = "&key=" + key
fields = "&fields=place_id, rating, name, price_level, geometry, formatted_address"
pt = "pagetoken="


def gp_call(query):
    """
    Makes calls to the Google Places API
    Args:
        query (string): the site to be searched 
    Returns:
        The request as a list
    """
    return requests.get(url= url_query+what+query+fields+key_endpoint).json()

def next_page(next_page_token):
    """
    Requiered to get more data from Google Places API
    Args:
        next_page_token(string): result from the previous request
    Return:
        The request as a list
    """
    return requests.get(url = url_query + pt + next_page_token + key_endpoint).json()

def request_to_df(query):
    """
    Transforms the list obtained from the request to a dataframe     
    Args:
        list_: the request to foursquare as a list
    Returns:
        The dataframe
    """
    lista = []
    data = query.get("results")
    name = []
    latitude = []
    longitude = []
    addres = []
    rating = []
    price_level = []

    for d in data:
        list_ = {}
        list_["name"] = d.get("name")
        list_["rating"] = d.get("rating")
        list_["latitude"] = d.get("geometry").get("location").get("lat")
        list_["longitude"] = d.get("geometry").get("location").get("lng")
        list_["address"] = d.get("formatted_address")
        try:
            list_["price_level"] = d.get("price_level")
        except:
            list_["price_level"] = np.nan
        lista.append(list_)

    documentos = []
    for diccionario in lista:
        temporal = {
            "name": diccionario.get("name"),
            "rating" : diccionario.get("rating"),
            "location": {"type": "Point", "coordinates": [diccionario.get("longitude"), diccionario.get("latitude")]},
            "address" : diccionario.get("address"),
            "price_level" : diccionario.get("price_level")
        }
        documentos.append(temporal)


    df = pd.DataFrame(documentos)
    return df

def todo(listita):
    """
    Makes calls to the Google Places API and creates and exports dataframes
    Args:
        listita (string): the list of sites to be searched 
    """
    for place in listita:
        query = place + " in madrid"
        name_1 = gp_call(query)
        time.sleep(2)
        try: 
            name_2 = next_page(name_1["next_page_token"])
            time.sleep(2)
            name_3 = next_page(name_2["next_page_token"])
            time.sleep(2)
            df_name_1 = request_to_df(name_1)
            df_name_2 = request_to_df(name_2)
            df_name_3 = request_to_df(name_3)
            df_name_1["place"] = place
            df_name_2["place"] = place
            df_name_3["place"] = place
            df = pd.concat([df_name_1,df_name_2, df_name_3])
            save = "../data/" + place + ".csv"
            df = df.reset_index()
            df = df.drop(["index"],axis=1)
            df.to_csv(save)
        except: 
            df = request_to_df(name_1)
            df["place"] = place
            save = "../data/" + place + ".csv"
            df = df.reset_index()
            df = df.drop(["index"],axis=1)
            df.to_csv(save)
