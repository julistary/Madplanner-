import pandas as pd

def create_subdata(listita):
    """
    Imports and joins dataframes creating subcategories    
    Args:
        listita: the list of elements that have to be in the df
    Returns:
        The dataframe
    """
    lista = ["cinema", "museum", "park", "zoo", "japanese",
         "burger", "vietnamese", "tapas", "korean", "brewery",
         "club", "pub", "bowling", "greek", "juices", "vegan",
         "french", "mexican", "asian", "rooftop", "cocktail", 
         "nightlife", "ramen", "argentino", "grill", "italian",
         "thai", "cake", "cupcakes", "coffee", "mid eastern",
         "indian", "pizza", "sweets", "theater", "spa", "ice cream",
         "sports bar", "healthy", "vegetarian", "drinks",
         "jazz", "wine", "karaoke", "dancing", "seafood", "discoteca", "escape room",
         "centro comercial", "pista padel", "pista tenis", "campo de futbol", 
         "paintball", "multiaventura", "cancha baloncesto", "gluten free", 
         "autocine", "cata de vino", "pista de hielo", "senderismo", "karts", "laser tag",
          "tunel de viento", "brunch", "teleferico", "escalada", "golf"]

    for place in lista:
        name = "data/" + place + ".csv"
        locals()[place] = pd.read_csv(name, index_col=0)


    df_names = []
    for place in listita:
        df_names.append(locals()[place])
    
    return pd.concat(df_names, ignore_index=True)

def address_1(row):
    """
    Cleans a row    
    Args:
        row: the row to be cleaned
    Returns:
        The dataframe with the row cleaned
    """
    return row[:-14]

def CP(row):
    """
    Cleans a row    
    Args:
        row: the row to be cleaned
    Returns:
        The dataframe with the row cleaned
    """
    return row[-5:]

def address_2(row):
    """
    Cleans a row    
    Args:
        row: the row to be cleaned
    Returns:
        The dataframe with the row cleaned
    """
    return row[:-7]

def fill_nulls(df):
    """
    Complete the nulls of a row with the mean of the group    
    Args:
        row: the df to work with
    Returns:
        The dataframe with the nulls filled
    """    
    return df['price_level'].fillna(df.groupby('place')['price_level'].transform('mean').round(0))

def latlon(df):
    """
    Creates columns latitude and longitude   
    Args:
        df (df): the df to work with
    Returns:
        The dataframe with the new columns
    """       
    latitude = []
    longitude = []
    for c in list(df["location"]):
        l = (c.split("["))[1].split(",")[0]
        longitude.append(float((c.split("["))[1].split(",")[0]))
        latitude.append(float((c.split(l + ", "))[1].split("]")[0]))
    df["latitude"] = latitude
    df["longitude"] = longitude
    
    df.drop(["location"],axis=1,inplace=True)

    geometry = []
    for lat,lon in zip(latitude, longitude):
        geometry.append({"type": "Point", "coordinates": [lat , lon]})
    
    df["geometry"] = geometry
    return df