"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


file = 'UFOS//UFOS-utf8-small.csv'
cont = None

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Encontrar puntos de interconexión aérea")
    print("3- Encontrar clústeres de tráfico aéreo")
    print("4- Encontrar la ruta más corta entre ciudades")
    print("5- Utilizar las millas de viajero")
    print("6- Cuantificar el efecto de un aeropuerto cerrado")
    print("7- : Comparar con servicio WEB externo")
    print("0- Salir")
    print("*******************************************")

catalog = None


"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de avistamientos ....")
        controller.loadData(cont, file)
        print('\nAvistmientos cargados: ' + str(controller.sightingsSize(cont)) + "\n")
        print("\nPrimeros 5 avistamientos cargados: \n")
        for position in range(1 , 6):
            sighting = lt.getElement(cont["sightings"] , position)
            print("Datetime: " + str(sighting["datetime"]) + " City: " + str(sighting["city"]))
        print("\nÚltimos 5 avistamientos cargados: \n ")
        for position2 in range(lt.size(cont["sightings"]) - 4 , lt.size(cont["sightings"]) + 1):
            sighting = lt.getElement(cont["sightings"] , position2)
            print("Datetime: " + str(sighting["datetime"]) + " City: " + str(sighting["city"]))

    elif int(inputs[0]) == 3:
        city = input("Ingrese la ciudad que desea consultar: ")

        tuple = controller.req1(cont , city)
        
        #Parte de imprimir.
        print("Se han reportado avistamientos en {} ciudades".format(tuple[0]))
        print("En la ciudad de {} se han reportado {} avistamientos.".format(city , tuple[2]))

        print("Los tres primeros y los tres últimos avistamientos son: ")
        for i in range(1,7):
            element = lt.getElement(tuple[1] , i)

            print("Fecha y Hora: {} Ciudad: {} Estado: {} Pais: {} Forma: {} Duración (segundos): {}".format(element["datetime"] , element["city"] , element["state"] , element["country"] , element["shape"] , element["duration (seconds)"]))

    elif int(inputs[0]) == 4:
        inferior = input("Ingrese el límite inferior en segundos: ")
        superior = input("Ingrese el límite superior en segundos: ")
 
        tuple = controller.req2(inferior , superior , cont)

        #Parte de impresión

        print("\nEl avistamiento más largo fue de {} segundos y ocurrió {} veces.\n".format(
            tuple[0] , tuple[1]
        ))
        print("\nLos 3 primeros y los 3 últimos avistamientos fueron:\n")
        for element in lt.iterator(tuple[2]):
            print("Fecha y Hora: {} Ciudad: {} Estado: {} Pais: {} Forma: {} Duración (segundos): {}".format(element["datetime"] , element["city"] , element["state"] , element["country"] , element["shape"] , element["duration (seconds)"]))
            
        for element in lt.iterator(tuple[3]):
            print("Fecha y Hora: {} Ciudad: {} Estado: {} Pais: {} Forma: {} Duración (segundos): {}".format(element["datetime"] , element["city"] , element["state"] , element["country"] , element["shape"] , element["duration (seconds)"]))

    elif int(inputs[0]) == 5:
        inferior = input("Ingrese el límite inferior en formato HH:MM ")
        superior = input("Ingrese el límite superior en formato HH:MM ")

        tuple = controller.req3(inferior , superior , cont)

        print("\nLos 3 primeros y los 3 últimos avistamientos fueron:\n")
        for element in lt.iterator(tuple[2]):
            print("Fecha y Hora: {} Ciudad: {} Estado: {} Pais: {} Forma: {} Duración (segundos): {}".format(element["datetime"] , element["city"] , element["state"] , element["country"] , element["shape"] , element["duration (seconds)"]))
            
        for element in lt.iterator(tuple[3]):
            print("Fecha y Hora: {} Ciudad: {} Estado: {} Pais: {} Forma: {} Duración (segundos): {}".format(element["datetime"] , element["city"] , element["state"] , element["country"] , element["shape"] , element["duration (seconds)"]))


    elif int(inputs[0]) == 6:
        inferior = input("Ingrese el límite inferior en formato AAAA-MM-DD: ")
        superior = input("Ingrese el límite superior en formato AAAA-MM-DD: ")
 
        tuple = controller.req4(inferior , superior , cont)

        #Parte de impresión

        print("El avistamiento más antiguo ocurrió {} veces en {}: ".format(tuple[1] , tuple[0]))
        print("Los 3 primeros y los 3 ultimos avistamientos ocurridos fueron: ")
        for i in range (1,7):
            element = lt.getElement(tuple[3] , i)
            print("Fecha y Hora: {} Ciudad: {} País {} Duracion (segundos): {} Forma del objeto: {}".format(element["datetime"], element["city"] , element["country"] , element["duration (seconds)"] , element["shape"]))

    elif int(inputs[0]) == 7:
        
        min_long = round(float(input("Ingrese el límite mínimo de longitud: ")) , 2)
        max_long = round(float(input("Ingrese el límite máximo de longitud: ")) , 2)

        min_lat = round(float(input("Ingrese el límite mínimo de longitud: ")) , 2)
        max_lat = round(float(input("Ingrese el límite máximo de longitud: ")) , 2)

        tuple = controller.req5(cont , min_long , max_long , min_lat , max_lat)

        print("El total de avistamientos en las coordenadas dadas fue {}".format(tuple[0]))
        print("Los tres primeros y los 3 ultimos avistamientos fueron: ")

        for i in range (1,7):
            element = lt.getElement(tuple[1] , i)
            print("Fecha y Hora: {} Ciudad: {} País {} Duracion (segundos): {} Forma del objeto: {}".format(element["datetime"], element["city"] , element["country"] , element["duration (seconds)"] , element["shape"]))



    else:
        sys.exit(0)
sys.exit(0)
