'''
Funciones para procesamiento de datos.
Datasets: https://drive.google.com/drive/u/1/folders/1zWp6zOgLjMIJr1t4a4R6fXipP276l1Fv
'''
import pandas as pd
import numpy as np

def drop_columns(df):
    '''
    Elimina columnas que no se utilizaron y columnas con un solo valor único. 
    '''

    S = df.nunique()
    # columnas con un solo valor único
    to_drop = S[S==1].index.to_list()

    # agregamos a la lista las columnas que no son útiles para 
    # la clasificación
    to_drop += ['Unnamed: 0', 'id', 'start_date', 'end_date','created_on', 'l3','l4','l5','l6', 'geometry']

    df.drop(to_drop, axis='columns', inplace=True)

    return None


def USD_to_COP(df):
    '''
    Cambia precios en USD a COP usando la columna currency.
    '''

    df.loc[df.currency == 'USD', 'price'] = df.price*3691.3167
    df.drop(['currency'], axis='columns', inplace=True)

    return None


def delete_outliers(df, column='price'):
    '''
    Elimina outliers en una columna utilizando el IQR.
    '''

    # usamos el iqr
    q1 = df[column].quantile(.25)
    q3 = df[column].quantile(.75)
    iqr = q3-q1

    # definimos los limites
    lower = q1 - 1.5*iqr
    upper = q3 + 1.5*iqr

    #filtramos
    filter = (df[column] >= lower) & (df[column] <= upper) | (df[column].isnull())
    df = df.loc[filter]

    return df

def fill_prices(df):
    '''
    Rellena precios nulos con la media.
    '''

    df.loc[df.price.isnull(), 'price'] = df.price.mean()

    return None

def fill_lat_lon(df):
    '''
    Rellena latitud y longitud en base al nivel administrativo l2.
    '''

    dict_lat = {
    'Antioquia': 7.154030, 'Atlántico': 10.987760, 'Cundinamarca': 4.781800,
    'Meta': 3.2720, 'Valle del Cauca': 3.858560, 'Caldas': 6.090000,
    'Risaralda': 4.606880, 'Magdalena': 10.249170, 'Santander': -0.622170,
    'Cauca': 8.252500, 'Huila': 3.376450, 'Bolívar': 1.833650, 'Tolima': 4.034880,
    'Norte de Santander': 8.084580, 'Quindío': 4.396070, 'Caquetá': 1.113340,
    'Sucre': 8.811250, 'Guainía': 2.719020, 'La Guajira': 11.427780,
    'Boyacá': 5.453740, 'Cesar': 10.769930, 'Amazonas': -2.056290,
    'San Andrés Providencia y Santa Catalina': 12.542720, 'Casanare': 5.296580,
    'Vichada': 4.712170, 'Córdoba': 9.586680, 'Chocó': 6.320330
    }

    dict_lon = {
    'Antioquia': -75.503349, 'Atlántico': -74.954620, 'Cundinamarca': -73.970757,
    'Meta': -73.0877, 'Valle del Cauca': -76.519810, 'Caldas': -75.636627,
    'Risaralda': -74.071840, 'Magdalena': -74.261080, 'Santander': -72.382812,
    'Cauca': -74.722893, 'Huila': -74.802391, 'Bolívar': -76.967293, 'Tolima': -75.255890, 
    'Norte de Santander': -72.842781, 'Quindío': -75.640083, 'Caquetá': -73.813004, 
    'Sucre': -74.721390, 'Guainía': -67.566940, 'La Guajira': -72.388634,
    'Boyacá': -73.362480, 'Cesar': -73.004791, 'Amazonas': -71.892921,
    'San Andrés Providencia y Santa Catalina': -81.717900, 'Casanare': -71.456268,
    'Vichada': -69.414350, 'Córdoba': -74.826302, 'Chocó': -76.944901
    }

    # Rellenamos con estos valores de acuerdo a l2 solo si lat y lon son nulos
    df.lat = np.where(df.lat.isnull(), df.l2.map(dict_lat), df.lat)
    df.lon = np.where(df.lon.isnull(), df.l2.map(dict_lon), df.lon)

    df.drop(['l2'], axis='columns', inplace=True)

    return None

def get_number_bathrooms(df):
    '''
    Halla el numero de baños en descripción y rellena los faltantes.
    Si no se encuentra en descripción, rellena con la moda por tipo 
    de propiedad.
    '''

    # formateamos str
    df.description = df.description.str.capitalize().str.strip()
    # eliminamos tildes
    df.description = df.description.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    # Rellenamos las filas sin descripcion
    df.loc[df.description.isnull(), 'description'] = 'No description'
    
    # Cambiamos los numeros escritos por numeros
    dict_num = {' uno ': ' 1 ', ' dos ':' 2 ', ' tres ':' 3 ', 
                ' cuatro ':' 4 ', ' cinco ':' 5 ', ' seis ':' 6 ', 
                ' siete ':' 7 ', ' ocho ':' 8 ', ' nueve ':' 9 '}
                
    for old, new in dict_num.items():
        df.description = df.description.str.replace(old, new, regex=False)

    # Extraigo el numero de strings como "n banos"
    pat = f"(\d+)[\s-](?:{'bano'})"
    bathrooms = df.loc[df.bathrooms.isnull()].description.str.extract(pat)

    df = df.join(bathrooms)
    # donde hay nulos, sustituimos por el numero de baños hallado en description
    df.loc[(df.bathrooms.isnull()) & (df[0].notnull()), 'bathrooms'] = df[0]
    
    # Dropeo la columna agregada para la sustitución
    df.drop([0], axis='columns',inplace=True)

    # Rellenamos los que hayan quedado como nulos con la moda por tipo de propiedad
    moda_bath = df.groupby(['property_type']).bathrooms.agg(pd.Series.mode)
    # los parqueaderos parecen no tener baño
    moda_bath.loc['Parqueadero'] = 0

    # Sustituimos con la moda
    df.bathrooms = np.where(df.bathrooms.isnull(), df.property_type.map(moda_bath), df.bathrooms)
    df.bathrooms = df.bathrooms.astype(int)

    return df

def add_crime(df):
    '''
    Agrega una columna por el crimen por cada 100mil habitantes en 2020
    según el segundo nivel administrativo l2.
    '''
    
    crime = {
        'Cundinamarca': 2068, 'Antioquia': 2328, 'Caldas': 1914,
        'Atlántico': 1743, 'Valle del Cauca': 2334, 'Risaralda': 1938,
        'Cauca': 1850, 'Nariño': 1683, 'Meta': 2733,
        'Norte de Santander': 1959, 'Quindío': 2362, 'Santander': 2408,
        'Bolívar': 1825, 'Magdalena': 1363, 'Tolima': 2567,
        'Huila': 2206, 'Boyacá': 1984, 'Chocó': 1236,
        'Córdoba': 921, 'Cesar': 1599, 'Caquetá': 1986,
        'Guainía': 1615, 'Casanare': 2080, 'Sucre': 1298,
        'Guaviare': 2551, 'La Guajira': 985, 'Amazonas': 1802,
        'San Andrés Providencia y Santa Catalina': 3015, 
        'Putumayo': 2163, 'Vichada': 1022, 'Arauca': 1724
        }
    
    df['crime'] = df['l2'].map(crime)

    return None

def property_type_dummies(df):
    '''
    Agrega columna de dummies de tipos de propiedad
    '''

    df[['Apartamento','Casa','Finca','Local comercial','Lote','Oficina','Otro','Parqueadero']] = pd.get_dummies(df.property_type)
    df.drop('property_type',axis='columns', inplace=True)

    return None

def create_target(df):
    '''
    Crea columna boleana donde 1 es precio sobre la media y 0
    es precio debajo de la media.
    '''
    y = pd.Series(np.where(df['price']>=df.price.mean(), 1, 0))
    df.drop(['price'], axis='columns', inplace=True)

    return y