import pandas as pd

def limpito(df,name):
    """
    Cleans the dataframe  
    Args:
        df(df) : the dataframe to be cleaned
    Returns:
        The dataframe cleaned
    """
    df.drop(['stop_code', 'zone_id', 'stop_url', 'location_type', 'parent_station',
       'stop_timezone', 'wheelchair_boarding'], axis=1, inplace=True)
    
    latitude = list(df.stop_lat)
    longitude = list(df.stop_lon)
    geometry = []
    for lat,lon in zip(latitude, longitude):
        geometry.append({"type": "Point", "coordinates": [lat , lon]})

    df["geometry"] = geometry
    df["type"] = name

    df = df.rename(columns={"stop_lat": "latitude", "stop_lon": "longitude"})

    return df

def limpito_parking(df):
    """
    Cleans the dataframe  
    Args:
        df(df) : the dataframe to be cleaned
    Returns:
        The dataframe cleaned
    """
    df.drop(['DESCRIPCION-ENTIDAD', 'EQUIPAMIENTO', 'TRANSPORTE', 
    'DESCRIPCION', 'ACCESIBILIDAD', 'CONTENT-URL','NOMBRE-VIA', 
    'CLASE-VIAL', 'TIPO-NUM', 'NUM', 'PLANTA', 'PUERTA', 'ESCALERAS',
     'ORIENTACION', 'LOCALIDAD', 'PROVINCIA', 'CODIGO-POSTAL', 
     'COORDENADA-X', 'COORDENADA-Y', 'HORARIO', 'TELEFONO', 'FAX', 
     'EMAIL', 'TIPO', 'Unnamed: 30'],axis=1,inplace=True)

    lat = list(df.LATITUD)
    long= list(df.LONGITUD)
    geometry = []
    latitude = []
    longitude = []


    for la,lo in zip(lat,long):
        latitude.append(float(la[:6]))
        longitude.append(float(lo[:6]))


    for lat,lon in zip(latitude, longitude):
        geometry.append({"type": "Point", "coordinates": [lat , lon]})

    df["geometry"] = geometry
    df["type"] = "parking"
    df["LATITUD"] = latitude
    df["LONGITUD"] = longitude


    df = df.rename(columns={"LATITUD": "latitude", "LONGITUD": "longitude"})

    return df 