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
 """

import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

# Funciones para la carga de datos
def loadData(analyzer, file):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for sighting in input_file:
        model.addSight(analyzer, sighting)
    return analyzer

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def sightingsSize(analyzer):
    """
    Numero de avistamientos.
    """
    return model.sightingsSize(analyzer)

def req1(analizer , city):
    return model.req1(analizer , city)

def req2(inferior , superior , analizer):
    return model.req2(inferior , superior , analizer)

def req4(inferior , superior , analizer):
    return model.req4(inferior , superior , analizer)

def req3(inferior , superior , analizer):
    return model.req3(inferior , superior , analizer)

def req5(cont , min_long , max_long , min_lat , max_lat):
    return model.req5(cont , min_long , max_long , min_lat , max_lat)