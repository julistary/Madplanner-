import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
import src.foursquares as fs
import numpy as np
load_dotenv()

key = os.getenv("key")

url_query = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
what = "query="
key_endpoint = "&key=" + key
fields = "&fields=place_id, rating, name, price_level, geometry, formatted_address"
pt = "pagetoken="


def gp_call(query):
    return requests.get(url= url_query+what+query+fields+key_endpoint).json()

def next_page(next_page_token):
    return requests.get(url = url_query + pt + next_page_token + key_endpoint).json()

def request_to_df(query):
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