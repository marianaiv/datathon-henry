'''
Pipeline para procesamiento de datos, entrenamiento y predicciones.

Datasets: https://drive.google.com/drive/u/1/folders/1zWp6zOgLjMIJr1t4a4R6fXipP276l1Fv
'''

import argparse         # opciones para correr el script
from utils import *     # funciones para procesar datos
import pandas as pd     # para leer archivos
import numpy as np      # manejo de arrays
import os               # uso de paths

# Para entrenamiento y clasificación
from sklearn.pipeline import Pipeline                   # Pipeline de entrenamiento
from sklearn.preprocessing import StandardScaler        # Scaler
from sklearn.ensemble import RandomForestClassifier     # Clasificador utilizado


def procesamiento_train(df, train=False):

    # Eliminamos columnas que no se utilizaron
    drop_columns(df)

    if train:
        # Cambiamos los valores en USD a COP
        USD_to_COP(df)

        # Eliminamos outliers de precios
        # df = delete_outliers(df)

        # Rellenamos los precios nulos con la media
        fill_prices(df)

        # Eliminamos outliers de lat y lon 
        df = df.loc[~(df.lat > 30)]
        df = df.loc[~(df.lat < -20)] 
    
    else:
        df.drop(['currency'], axis='columns', inplace=True)

    # Rellenamos lat y lon
    fill_lat_lon(df)

    # Extraemos el número de baños de description
    df = get_number_bathrooms(df)

    # Eliminamos columna de description y las demás columnas
    # que no rellenamos
    df.drop(['rooms','bedrooms','surface_total','surface_covered', 'title', 'description'], axis='columns', inplace=True)

    # Obtenemos variables dummies de property_type
    property_type_dummies(df)
    
    return df


def main():
    # Opciones para correr el script
    parser = argparse.ArgumentParser(description="Pipeline para datathon de Henry")
    parser.add_argument('--path', type=str, default='../datasets/', help=' Carpeta que contiene los archivos de entrada [Default: ../datasets/]')
    parser.add_argument('--out', type=str, default='../logs/', help='Carpeta donde se guardan los archivos de salida [Default: ../logs]')
    parser.add_argument('--name', type=str, default='log', help='Nombre del archivo de salida. La carpeta se crea en --out [Default: log]')
    parser.add_argument('--train', type=str, default='properties_colombia_train.csv', help='Nombre del archivo de train [Default: properties_colombia_train.csv]')
    parser.add_argument('--test', type=str, default='properties_colombia_test.csv', help='Nombre del archivo de test [Default: properties_colombia_test.csv]')

    flags = parser.parse_args()

    # Path donde se encuentran los datos de entrada y salida
    PATH_IN = flags.path
    PATH_OUT = flags.out

    # Revisamos que exista la carpeta de salida
    if not os.path.exists(PATH_OUT):
        os.makedirs(PATH_OUT)

    # Nombres de los archivos
    #OUT_NAME = flags.name+'.csv'
    OUT_NAME = 'marianaiv'+'.csv'
    TRAIN = flags.train
    TEST = flags.test

    # Path completo de los archivos
    PATH_TRAIN = os.path.join(PATH_IN,TRAIN)
    PATH_TEST = os.path.join(PATH_IN,TEST)
    OUT_FILE = os.path.join(PATH_OUT,OUT_NAME)

    ####################### PIPELINE #######################

    ### Procesamiento del conjunto de entrenamiento ###
    print('Los datos de entrenamiento se están cargando y procesando.')
    X_train = pd.read_csv(PATH_TRAIN)
    X_train = procesamiento_train(X_train, train=True)

    print('Se procesaron satisfactoriamente. Las columnas de entrenamiento son: ', X_train.columns.to_list())

    ### Entrenamiento del modelo ###
    print('Se entrenará el modelo. Esto puede tardar.')
    y_train = create_target(X_train)

    clf = Pipeline(steps=[('ss', StandardScaler()), ('clf', RandomForestClassifier(random_state=15))])
    clf.fit(X_train, y_train)

    print('El modelo se entrenó correctamente.')

    ## Lectura y procesamiento de archivo de test ##
    print('Los datos de prueba se están cargando y procesando.')
    X_test = pd.read_csv(PATH_TEST)
    X_test = procesamiento_train(X_test)

    print('Se procesaron satisfactoriamente. Las columnas de prueba son: ', X_test.columns.to_list())

    ## Predicción
    print('Se están realizando las predicciones.')
    pred_test = clf.predict(X_test)

    pred = pd.Series(pred_test) 
    pred = pred.rename('pred')
    pred.to_csv(OUT_FILE, index=False)

    print('Predicciones realizadas exitosamente. El archivo se encuentra en {}'.format(PATH_OUT))

if __name__ == "__main__":
    main()