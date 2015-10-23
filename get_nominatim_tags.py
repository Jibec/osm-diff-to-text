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

import csv

# dictionnaires des tags majeurs recherchés


def read_nominatim():
    tags_majors_texts = {}
    tags_majors_texts[('zzz', 'zzz')] = 'Aucune valeur'
    tags_to_mesure = []
    # import des chaînes de traductions de nominatims pour les tags majeurs
    # source : http://wiki.openstreetmap.org/wiki/Nominatim/Special_Phrases/FR
    with open('./main-tag-nominatim.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        # structure  key, value, string
        for row in spamreader:
            tags_majors_texts[(row[0], row[1])] = row[2]
            # s'il faut indiquer la distance ajoutée
            if row[3] == "oui":
                tags_to_mesure.append((row[0], row[1]))
    return (tags_majors_texts, tags_to_mesure)
