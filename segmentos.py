import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt

def segmentos(tiempo_serie,delta_t,tiempo,y,graficos):  
  
  diff_tiempo=np.diff(tiempo) #out[i] = a[i+1] - a[i]
  indice_discontinuidades=np.where(diff_tiempo>timedelta(seconds=delta_t))
  
  segmentos_t=[]
  segmentos_y=[]
    
  t0=0
  for delta in indice_discontinuidades[0]:
      if (tiempo[delta]-tiempo[t0])>=timedelta(seconds=tiempo_serie):
          #print(tiempo[delta]-tiempo[t0])
          #print(t0,delta,(tiempo[delta]-tiempo[t0]).total_seconds()/60/60,tiempo[t0],tiempo[delta])
          segmento_t=tiempo[t0:delta+1].tolist()
          #print(t0,delta,(segmento_t[-1]-segmento_t[0]).total_seconds()/60/60,segmento_t[0],segmento_t[-1])
          segmento_y=y[t0:delta+1].tolist()     
          segmentos_t.append(segmento_t)
          segmentos_y.append(segmento_y)
      t0=delta+1
  if graficos==1:
    fig, ax = plt.subplots(figsize=(15,3))
    ax.grid()
  for i in range(len(segmentos_t)):
      #print(i, (segmentos_t[i][-1]-segmentos_t[i][0]).total_seconds()/60/60)
      segmentos_t[i]=segmentos_t[i][0:int(tiempo_serie/60)+1]
      segmentos_y[i]=segmentos_y[i][0:int(tiempo_serie/60)+1]
      if graficos==1:
        plt.plot(segmentos_t[i],segmentos_y[i],label='y')
      #print((segmentos_t[i][-1]-segmentos_t[i][0]).total_seconds()/60/60)
      #print(len(segmentos_t[i]))
  return segmentos_t,segmentos_y
    