"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pprint 

import pandas as pd

def readfile(ruta):
  df = pd.read_fwf(
    ruta,
    skiprows=4,  # Saltar las filas iniciales
    header=None,  # No usar encabezados del archivo
    names=['cluster', 'cantidad_de_palabras_clave', 'porcentaje_de_palabras_clave', 'principales_palabras_clave'],  # Asignar nombres
  )
  # print(df)
  return df

def limpieza(df):
  print (df)
  # Limpiar las columnas
  df['cluster'] = df['cluster'].fillna(method='ffill')  # Rellenar valores vacíos en la columna 'cluster'
  df['principales_palabras_clave'] = df['principales_palabras_clave'].fillna('')  # Rellenar valores vacíos con cadenas vacías

  return df


def combinar(df):
  # Concatenar las palabras clave por cada cluster
    df = df.groupby(['cluster'], as_index=False).agg({
        'cantidad_de_palabras_clave': 'first',  # Tomar el primer valor válido
        'porcentaje_de_palabras_clave': 'first',  # Tomar el primer valor válido
        'principales_palabras_clave': lambda x: ' '.join(x)  # Concatenar todas las líneas de palabras clave
    })

    return df

def espacios(df):
  # Limpiar espacios múltiples y caracteres adicionales
  df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace(r'\s+', ' ', regex=True).str.strip()
  df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace(r',\s+', ', ', regex=True)
  #Quitar punto final
  df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace(r'\.$', '', regex=True)
  return df

def tipos(df):
  df = df.astype({
    'cluster': 'int',  # Cambiar de float64 a int
    'cantidad_de_palabras_clave': 'int',  # Cambiar de float64 a int
  })
  
  return df

def puntos(df):
  df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace(r',', '.')
  df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace(r'%', '').astype(float)
  return df


def pregunta_01():
    
    df = readfile('files/input/clusters_report.txt')
    df = limpieza(df)
    df = combinar(df)
    df = espacios(df)
    df = tipos(df)
    df = puntos(df)
    return df
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.
    """


# pregunta_01()
print(pregunta_01().principales_palabras_clave.to_list()[0])