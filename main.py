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

import os
import argparse
import reader
import get_changeset_xdiff

def main(**kwargs):
    changeset = str(kwargs['changeset'])

    get_changeset_xdiff.get_augmented_diff(changeset)
    results = reader.read_diff_file(changeset)
    print(results)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read a osm changeset et write it in a human way')
    parser.add_argument('changeset', type=int, help='Changeset number')
    args = parser.parse_args()
    main(**vars(args))
