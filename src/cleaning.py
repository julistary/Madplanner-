import pandas as pd
import numpy as np
import re 

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
         "french restaurant", "mexican", "asian", "rooftop", "cocktail",  "ramen", "argentino",
          "grill", "italian",
         "thai", "cake", "cupcakes", "coffee", "mid eastern",
         "indian", "pizza", "sweets", "teatro", "spa", "ice cream",
         "sports bar", "healthy", "vegetarian", 
         "jazz", "wine", "karaoke", "dancing", "seafood", "escape room",
         "centro comercial", "pista padel", "pista tenis", "campo de futbol", 
         "paintball", "multiaventura", "cancha baloncesto", "gluten free", 
         "autocine", "cata de vino", "pista de hielo", "senderismo", "karts", "laser tag",
          "tunel de viento", "brunch", "teleferico", "escalada", "golf",
          "circus", "piano bar", "salsa club", "samba club", "water park", 
          "pet friendly restaurant", "parque de atracciones"]

    for place in lista:
        name = "../" + "data/" + place + ".csv"
        locals()[place] = pd.read_csv(name, index_col=0)


    df_names = []
    for place in listita:
        df_names.append(locals()[place])
    df = pd.concat(df_names, ignore_index=True)
    df['type'] = "plan"
    return df


def address(df):
    import re
    """
    Creates a column with de zip code   
    Args:
        df(df) :  the df to be cleaned
    Returns:
        The dataframe with the zip code
    """
    pattern = r'\b\d{5}\b'

    df['CP'] = df.address.apply(lambda x: re.findall(pattern, x))

    list_ = []
    for sublist in list(df['CP']):
        try:
            list_.append(sublist[0])
        except:
            list_.append(np.nan)
    df['CP'] = list_
    return df

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
        try:
            l = (c.split("["))[1].split(",")[0]
            longitude.append(float((c.split("["))[1].split(",")[0]))
            latitude.append(float((c.split(l + ", "))[1].split("]")[0]))
        except:
            longitude.append(np.nan)
            latitude.append(np.nan)
    df["latitude"] = latitude
    df["longitude"] = longitude
    
    df.drop(["location"],axis=1,inplace=True)

    geometry = []
    for lat,lon in zip(latitude, longitude):
        geometry.append({"type": "Point", "coordinates": [lat , lon]})
    
    df["geometry"] = geometry
    return df

def drop_row(df,code):
    """
    Drops useless row    
    Args:
        df(df): the df to be cleaned
        code(str): the place to be cleaned
    Returns:
        The dataframe without the rows
    """
    
    zoo_drop = ['Rinoceronte Indio', 'Oso Hormiguero',
           'Suricata', 'Cig??e??as', 'Sea lions', 'Yack', 'Gorilas',
           'Koalas', 'Espect??culos de aves', 'Estanque de los delfines',
           'Elefantes', 'Ping??inos', 'Tigers', 'Rinoceronte',
           'Mariposas - El Jard??n del Ed??n', 'Lemures', 'Leopardos', 'Monos']
    
    tlf_drop = ['Telef??rico en Rosales',
       'Teleferico de Madrid - Country House Station', 'G??ra Ebbot',
       'Parque Teleferico Madrid', 
       'Bar - Teleferico Casa de Campo'] 
    
    park_drop = ['Splash Bash', 'Divertiland Park',
       'Entrada Bat??n - Parque de Atracciones Madrid',
       'Los R??pidos', 'La Jungla',
       'La Lanzadera', 'El Aserradero', 'Los Fiordos', 'Tif??n',
       'The Walking Dead Experience', 'Microfauna',
       'Pirate Ship Playground', 'Globos Locos', 'Lordcultura S L',
       'Magneto Jimmy Neutron', 'Patrulla Canina', 'Rotor',
       'Tienda Glove World', 'Vertigo', 'La Cueva de las Tar??ntulas',
       'Peque Square Sanchinarro',
       'Licencia para Conducir de las Tortugas Ninja', 'Star Flyer',
       'Tar??ntula', 'Padrinos Voladores', 'Urban Planet Jump',
       'Cazamedusas de Patricio', 'Parque Warner Madrid', 'Top Spin',
       'Hero Spin', 'La Aventura de Dora', 'Sillas Voladoras',
       'Diversi??n en la Granja', 'Parque Hormiguero', 'Space area',
       'Parque Inclusivo "M??dulo Lunar"', 'La Pergola', 'Urban Planet',
       'Urban Planet: Trampoline Park', 'Zeppelin', 'El Retiro Park',
       'Jard??n de Rocas (MUNCYT)', 'Offices Amusement Park',
       'Clamber Park Arroyosur', 'Vertical Park',
       'Ferrocarril de las Delicias',
       'Madrid R??o Park', 'VR Virtual Recall Park & \u200b\u200bAcademy',
       'Sould Park La Vaguada', 'Casa de Campo Park']
    
    rest_drop = ['Clinica De Fisioterapia Healthy Life']

    laser_drop = ['NonameSport (Oficinas)',  'RonquidosMadrid',
       'Paintball Madrid Action Live', 
       'Universal Games Recinto Delta Force',
       'Multiaventura Park en Madrid - Parque Europa',
       'Paintball Park Madrid', 
       'Zero Latency', 'Humor Amarillo Madrid',
       'Instituto M??dico Espa??ol Est??tica Avanzada Sl',
       'Cl??nica Dermatol??gica Laser - Seraf??n Fern??ndez-Ca??adas',
       'Bolo 11, Tienda de equipaci??n y material para el bowling','Federaci??n Espa??ola de Bolos']

    if code == "zoo":
        list_ = zoo_drop
    elif code == "park":
        list_ = park_drop
    elif code == "tlf":
        list_ = tlf_drop
    elif code == "laser":
        list_ = laser_drop
    elif code == "rest":
        list_ = rest_drop
        
    for i in list_: 
        df.drop(df[df.name==i].index, axis=0, inplace=True)
        
    return df
        
def pricing(row):
    """
    Creates a row with the price based on price level   
    Args:
        row(df): the row to be translated
    Returns:
        The dataframe with the new column
    """
        
    if row == 0.0:
        return "Free"
    elif row == 1.0:
        return "1-15???"
    elif row == 2.0:
        return "15-25???"
    elif row == 3.0:
        return "25-50???"
    else: 
        return "More than 50???"