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

import requests
from xml.dom.minidom import parseString
import os.path

def get_augmented_diff(changeset_number):
    osm_api = "https://www.openstreetmap.org/api/0.6/changeset/"
    overpass_api = "https://overpass-api.de/api/interpreter?data=[adiff:%created_at%,%closed_at%];(node(bbox)(changed);way(bbox)(changed););out meta geom(bbox);&bbox=min_lon,min_lat,max_lon,min_lon"
    if not os.path.isfile(changeset_number):
        request_osm = requests.get("%s%s" % (osm_api, changeset_number))

        dom = parseString(request_osm.text)
        changeset  = dom.getElementsByTagName("changeset")[0]

        values = {}
        values['created_at'] = changeset.attributes['created_at'].value
        values['closed_at']  = changeset.attributes['closed_at'].value
        values['min_lon'] = changeset.attributes['min_lon'].value
        values['min_lat'] = changeset.attributes['min_lat'].value
        values['max_lon'] = changeset.attributes['max_lon'].value
        values['max_lat'] = changeset.attributes['max_lat'].value
        
        changeset_file = open(str(changeset_number), 'w')

        overpass_api = "https://overpass-api.de/api/interpreter?data=[adiff:\"%s\",\"%s\"];(node(bbox)(changed);way(bbox)(changed););out meta geom(bbox);&bbox=%s,%s,%s,%s" % (values['created_at'], values['closed_at'], values['min_lon'], values['min_lat'], values['max_lon'], values['max_lat'])

        request_overpass = requests.get(overpass_api)

        changeset_file.write(request_overpass.text)
        changeset_file.close
        
    else:
        print("Le changeset est déjà téléchargé")
    return 1
