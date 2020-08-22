import requests
import numpy as np
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import datetime as dt

##importa datos desde enlace IOC
###para correr:
###from ioc2data import ioc2data
###tiempo,prs,rad=ioc2data(url,graficos)

def ioc2data(url,plots):
    URL = url
    page = requests.get(URL) #Carga pagina
    soup = BeautifulSoup(page.content, 'html.parser') #extrae el contenido (tabla) y deja en formato 'amigable'
    ###crea lista con las filas de la tabla en string (texto)
    data_ioc=[] #lista vacia que guardará tiempo y mediciones
    for row in soup.find_all('tr'): # para cada fila de la tabla extraida de la URL
        row_str=str(row.get_text(" ")).rsplit(sep=" ",maxsplit=2) #extrae el texto, separa las dos ultimas columnas que se encuentran espaciados (" ").
        data_ioc.append(row_str) #agrega el texto separado a una nueva lista con filas ['tiempo', 'prs', 'rad']
    
    #print(data_ioc[0]) #imprime titulo de las columnas de la tabla
    data_ioc=np.array(data_ioc[1:]) #guarda solo los datos, sin titulo de columnas
    
    ###genera variables, a partir de filas en string
    tiempo=[] #lista que guardará los tiempos
    prs=[] #lista que guardará el registro del sensor de presion
    rad=[] #lista que guardara el registro del sensor de radar
    
    for row in data_ioc: #para cada fila
        if row[1]!='\xa0' and row[2]!='\xa0':
          tiempo.append(dt.datetime.strptime(row[0],'%Y-%m-%d %H:%M:%S')) #guarda la primera columna con formato datetime
          prs.append(row[1].astype(float)) #guarda segunda columna en lista prs
          rad.append(row[2].astype(float)) #guarda tercera columna en lista rad
    tiempo=np.array(tiempo) #transforma a arreglo np (mas comodo de trabajar)
    prs=np.array(prs)
    rad=np.array(rad)
    
    if plots==1:
        fig, ax = plt.subplots(figsize=(15,3))
        ax.plot(tiempo, prs,label='prs')
        ax.plot(tiempo, rad,label='rad')
        ax.legend()
        ax.grid()
    
    print(str(len(tiempo))+' datos.')
    print('Desde '+str(tiempo[0])+' hasta '+str(tiempo[-1]))
    
    return tiempo, prs,rad