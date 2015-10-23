#!/usr/bin/env python3


# -*- encoding: utf-8 -*-
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/gpl-3.0.html>.
#
# @author Jean-Baptiste Holcroft <jb.holcroft@gmail.com>

from xml.dom.minidom import parse, parseString, getDOMImplementation
from math import asin, cos, radians, sin, sqrt
import get_nominatim_tags

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))

    # 6367 km is the radius of the Earth
    m = 6367000 * c
    return m

def get_tag_length_or_value(tag, c, signe):
    """ 
    Calcule la longueur de l'objet impacté en mètres si pertinent sinon en nombre
    """
    m    = 0
    lon1, lat1, lon2, lat2 = 0, 0, 0, 0
    
    if tag not in tags_to_mesure:
        return (1*signe, "")
    
    # parcours des noeuds
    for element in c.getElementsByTagName("nd"):
        if lat1 == lon1 == 0:
            lat1 = float(element.attributes["lat"].value)
            lon1 = float(element.attributes["lon"].value)
        else:
            lat2 = float(element.attributes["lat"].value)
            lon2 = float(element.attributes["lon"].value)
            m += haversine(lon1, lat1, lon2, lat2)
            lat1, lon1 = lat2, lon2
    
    return (m*signe, "m")

def add_major(results, tag, action, m, minors):
    """ 
    Ajoute aux résultats un nouveau tag majeur, puis ses tags mineurs
    """
    if tag not in results:
        results[tag] = {'number': 0, 'unit':""}
        results[tag]['create'] = {}
        results[tag]['delete'] = {}

    results[tag]['number'] += m[0]
    results[tag]['unit']    = m[1]
    results[tag][action]    = add_minor(results[tag][action], minors)

    return results

def add_minor(actual = {}, new = {}):
    """ 
    Ajoute les tags mineurs à la liste déjà existante.
    """
    for (minor, values) in new.items():
        actual[minor] = actual.get(minor, {})
        for value, nombre in values.items():
            actual[minor][value] = actual[minor].get(value, 0) + nombre
    
    return actual

def split_major_and_minors(tags):
    minors    = {}
    tag_major = ('zzz','zzz')
    for (k, v) in tags:
            tag = (k, v)
            if tag in tags_majors_texts:
                tag_major = tag
            else:
                minors[k] = minors.get(k, {})
                minors[k][v] = minors[k].get(v, 0) + 1
    
    return (tag_major, minors)

def read_diff_file(diff_file_name):
    """ 
    Lecture du fichier diff augmenté puis renvoi du résultats en Str
    """

    dom = parse(diff_file_name)
    
    # Note : les résultats sont sous la forme :
    # Tag majeur {
    #  create = {}
    #  delete = {}
    #  number = int
    #  unit   = str
    #  }
    #
    # chaque partie create ou delete contient un {} des tags mineurs
    # chaque minors est tuple (nom, nombre)
    
    results = {}
    global tags_majors_texts
    global tags_to_mesure
    tags_majors_texts = {}
    tags_to_mesure    = []
    # initialisation des tags nominatims qui seront les tags majeurs
    tags_majors_texts, tags_to_mesure = get_nominatim_tags.read_nominatim()



    for action in dom.getElementsByTagName("action"):
        modification_type = action.attributes['type'].value
        
        if modification_type == "create":
            k_new = [(tag.attributes['k'].value, tag.attributes['v'].value)
                        for tag in action.getElementsByTagName("tag")]
            
            tag_major, minors = split_major_and_minors(k_new)
            mesure  = get_tag_length_or_value(tag_major, action, 1)
            results = add_major(results, tag_major, "create", mesure, minors)
        # les types modify et delete contiennent deux hiérarchies
        # on les sépare et on retire les valeurs communes avant ajout aux résultats
        elif modification_type in ["modify","delete"]:
            tags_new = action.getElementsByTagName("new")[0]
            tags_old = action.getElementsByTagName("old")[0]
            k_new, k_old, k_real_new, k_real_old = [], [], [], []

            k_new = [(tag.attributes['k'].value, tag.attributes['v'].value)
                        for tag in tags_new.getElementsByTagName("tag")]
            k_old = [(tag.attributes['k'].value, tag.attributes['v'].value)
                        for tag in tags_old.getElementsByTagName("tag")]
            k_real_new = [k for k in k_new if k not in k_old]
            k_real_old = [k for k in k_old if k not in k_new]
            
            tag_major, minors = split_major_and_minors(k_real_new)
            mesure = get_tag_length_or_value(tag_major, tags_new, 1)
            results = add_major(results, tag_major, "create", mesure, minors)
            

            tag_major, minors = split_major_and_minors(k_real_old)
            mesure = get_tag_length_or_value(tag_major, tags_old, -1)
            results = add_major(results, tag_major, "delete", mesure, minors)

        
    out = "\n*** Affichage du résultat :"

    for major_tag, value in results.items():
        tag = str(major_tag[0])
        val = str(major_tag[1])
        text = tags_majors_texts[(tag, val)]
        
        out = out + ("\n\n%s (%s=%s) | %i%s | " % (text, tag, val, value["number"], value["unit"]))
        out = out + "\n__Dont tags mineurs créés : "
        if (len(value['create'].items()) > 0):
            for minor_key, key_values_dic  in value['create'].items():
                out = out + "%s [" % minor_key
                
                for mineur,nombre  in key_values_dic.items():
                    out = out + "%s (%s)_" % (mineur, nombre)
                out = out[:-1]
                out = out + "]; "
            out = out[:-2]
        out = out + "\n__Dont tags mineurs supprimés : "
        if (len(value['delete'].items()) > 0):
            out = out + " : "
            for minor_key, key_values_dic  in value['delete'].items():
                out = out + "%s [" % minor_key
                
                for mineur,nombre  in key_values_dic.items():
                    out = out + "%s (%s)_" % (mineur, nombre)
                out = out[:-1]
                out = out + "]; "
            out = out[:-2]
    return out
