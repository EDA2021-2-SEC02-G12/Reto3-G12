"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import orderedmap as om
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert config

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los avistamientos
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'sightings': None,
                'citymap': None,
                'datetime': None,
                'seconds': None
                }

    analyzer['sightings'] = lt.newList('SINGLE_LINKED')
    analyzer['citymap'] = mp.newMap(maptype='PROBING')
    analyzer['datetime'] = om.newMap(omaptype='RBT')
    analyzer['seconds'] = om.newMap(omaptype='RBT')
    return analyzer

# Funciones para agregar informacion al catálogo
def addSight(analyzer, sight):
    """
    """
    lt.addLast(analyzer['sightings'], sight)
    update_map_city(analyzer['citymap'], sight)
    update_date(analyzer["datetime"] , sight)
    update_seconds(analyzer["seconds"] , sight)
    return analyzer

def update_map_city(map, sight):
    """
    """
    city = sight['city']
    entry = mp.get(map, city)
    if entry is None:
        cityentry = newDataEntry(sight)
        mp.put(map, city, cityentry)
    else:
        cityentry = me.getValue(entry)
    addDateIndex(cityentry, sight)

    return map

def addDateIndex(cityentry, sight):
    """
    Toma un valor del map de ciudades y le agrega información. Esta se compone
    de un ordered map con las fechas de los avistamientos y una list de los mismos
    por cada ciudad en el map.
    """
    lst = cityentry['lstsightings']
    lt.addLast(lst, sight)
    size = lt.size(lst)
    cityentry['number_of_sightings'] = size
    sigtings_map = cityentry['sightings']
    occurreddate = sight['datetime']
    sightdate = datetime.datetime.strptime(occurreddate, '%Y-%m-%d %H:%M:%S')
    entry2 = om.get(sigtings_map, sightdate.date())

    if entry2 is None:
        datentry = newDate_HourEntry(sightdate)
        om.put(sigtings_map, sightdate.date(), datentry)
    else:
        datentry = me.getValue(entry2)
    lt.addLast(datentry["sights"] , sight)
    return sigtings_map


def newDataEntry(sight):
    """
    Crea una entrada en el indice por ciudad, es decir map de ciudades.
    """
    entry = {'sightings': None, 'lstsightings': None }
    entry['sightings'] = om.newMap(comparefunction=compareDates)
    entry['lstsightings'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newDate_HourEntry(sightdate):
    """
    Crea una entrada en el indice por ciudad, es decir map de ciudades.
    """
    entry = {'date_time': None , "sights":None}
    entry['date_time'] = sightdate
    entry['sights'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def update_date(map, sight):
    """
    Requerimiento 4: Añade elementos al map de fechas.
    """

    occurreddate = sight['datetime']
    occurreddate2 = occurreddate.split(" ")[0]
    sightdate = datetime.datetime.strptime(occurreddate2, '%Y-%m-%d')
    entry = om.get(map, sightdate.date())
    if entry is None:
        datentry = newDataEntry_2(sight)
        om.put(map, sightdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    lt.addLast(datentry["sights"] , sight)
    return map

def newDataEntry_2(sight):
    """
    Crea una entrada en el indice por ciudad, es decir map de ciudades.
    """
    entry = {"sights":None}
    entry['sights'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def update_seconds(map, sight):
    """
    Requerimiento 2: Añade elementos al map de segundos.
    """

    duration_seconds = sight['duration (seconds)']
    duration_flot = float(duration_seconds)
    entry = om.get(map, duration_flot)
    if entry is None:
        duration_entry = newseconds_entry(duration_flot)
        om.put(map, duration_flot, duration_entry)
    else:
        duration_entry = me.getValue(entry)
    lt.addLast(duration_entry["sights"] , sight)

    sublist = lt.subList(duration_entry["sights"] , 1 , lt.size(duration_entry["sights"]))
    ordered_list = mer.sort(sublist, cmpAlphabetically)

    duration_entry["sights"] = ordered_list

    return map


def newseconds_entry(duration):
    """
    Crea una entrada en el indice por ciudad, es decir map de ciudades.
    """
    entry = {"sights":None}
    entry['sights'] = lt.newList('ARRAY_LIST', compareDates)
    return entry


# Funciones para creacion de datos

# Funciones de consulta

def sightingsSize(analyzer):
    """
    Número de avistamientos
    """
    return lt.size(analyzer['sightings'])

def req1(analyzer , city):
    """
    Función para extraer los datos del requerimiento 1
    """

    map_cities = analyzer["citymap"]
    size = mp.size(map_cities)
    city_sigthings = mp.get(map_cities , city)
    city_value = me.getValue(city_sigthings)
    ordered_map = city_value["sightings"]
    size_city = om.size(ordered_map)
    ret_list = lt.newList()
    
    # Se añade el elemento mas pequeño a la lista.
    first_element_key = om.minKey(ordered_map)
    first_element = om.get(ordered_map , first_element_key)
    first_element = me.getValue(first_element)
    first_element = lt.firstElement(first_element["sights"])
    lt.addLast(ret_list , first_element)

    values = om.valueSet(ordered_map)
    for i in range(2,4):
        value = lt.getElement(values , i)
        sight = value["sights"]
        sight = lt.getElement(sight , 1)
        lt.addLast(ret_list , sight)
    
    for j in range(lt.size(values)-2 , lt.size(values) + 1):
        value = lt.getElement(values , j)
        sight = value["sights"]
        sight = lt.getElement(sight , 1)
        lt.addLast(ret_list , sight)

    return size , ret_list , size_city


def req4(inferior , superior , analizer):
    inferior2 = datetime.datetime.strptime(inferior, '%Y-%m-%d')
    superior2 = datetime.datetime.strptime(superior, '%Y-%m-%d')

    map = analizer["datetime"]

    value_min_key = om.minKey(map) # Llave minima 
    value_min = om.get(map , value_min_key)
    value_min = me.getValue(value_min)
    value_min = value_min["sights"]
    number_of_elements_min = lt.size(value_min) #Numero de elementos en la fecha mas antigua.

    list_ret = om.values(map, inferior2.date() , superior2.date()) #Lista con values
    size_sight = lt.size(list_ret)

    list_filtered = lt.newList(datastructure='ARRAY_LIST')
    
    for i in range(1 , 4):
        element = lt.getElement(list_ret , i)
        sights = lt.getElement(element["sights"] , 1)
        lt.addLast(list_filtered , sights)
    
    for j in range(lt.size(list_ret) - 2 , lt.size(list_ret) + 1):
        element = lt.getElement(list_ret , j)
        sights = lt.getElement(element["sights"] , 1)
        lt.addLast(list_filtered , sights)

    # Value min key = Llave más pequeña
    # Number of elements_min: Numero de elementos en esa fecha
    # Size_sight = Numero de avistamientos en el rango de fechas
    # List Filtered = Primeros Tres y Ultimos 3
    return value_min_key , number_of_elements_min , size_sight , list_filtered

def req2(inferior , superior , analizer):
    map = analizer["seconds"]
    keys = om.keySet(map)
    maxkey = om.maxKey(map)
    number_seeings = om.get(map , maxkey)
    number_seeings = me.getValue(number_seeings)
    number_sights = lt.size(number_seeings["sights"])

    values_in_range = om.values(map , float(inferior) , float(superior)+0.1)

    list_first3 = lt.newList()
    list_last3 = lt.newList()

    for i in range(1 , 4):
        value = lt.getElement(values_in_range, i)
        for sight in lt.iterator(value["sights"]):
            lt.addLast(list_first3 , sight)
    
    sublist_first3 = lt.subList(list_first3 , 1 , 3)

    for i in range(lt.size(values_in_range)-2 , lt.size(values_in_range)+1):
        value = lt.getElement(values_in_range, i)
        for sight in lt.iterator(value["sights"]):
            lt.addLast(list_last3 , sight)
    
    sublist_last3 = lt.subList(list_last3 , lt.size(list_last3)-2 , 3)


    return maxkey , number_sights , sublist_first3 , sublist_last3


# Funciones utilizadas para comparar elementos dentro de una lista

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def cmpAlphabetically(country1, country2):
    """
    
    Realiza una compración lexicográfica
    Args:
    country1
    country2
    """
    ret = None 

    if country1["city"] < country2["city"]:
        ret = True
    else:
        ret = False

    return ret