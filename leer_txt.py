# lee un archivo txt cualquiera, y entrega las lineas en la variable "lineas"

# Uso: lineas=leer_txt(txt)

def leer_txt(txt):
    lineas=[]   #lista vacia que guardará las lineas del archivo txt
    with open(txt, 'r') as reader:  # abre el archivo para lectura
        for linea in reader:    # para cada linea del archivo
            linea = linea.replace('\n','') # quita el ultimo caracter "\n" del salto de linea en el texto
            lineas.append(linea) # cada linea la va agregando a la variable lineas
    return lineas