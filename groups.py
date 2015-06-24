#!/usr/bin/env python3
#
# This program creates a ks.cfg file based of the configuration options given.
#
# Copyright (C) 2015 Dennis Chen <barracks510@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>
#

import xml.etree.ElementTree as etree


class metapackage (object):

    def __init__(self):
        self.name = None
        self.abbrev = None
        self.desc = None
        self.packages = {}


def create_groups():
    package_xml = etree.parse("packages/packages.en.xml")

    root = package_xml.getroot()

    xml_grp_choices = len(root)

    groups = []
    categories = []
    environments = []

    for index in range(0, xml_grp_choices):
        root_index = root[index]
        collection_type = root_index.tag
        if collection_type == "group":
            x = metapackage()
            x.name = root_index[1].text
            x.abbrev = root_index[0].text
            x.desc = root_index[2].text
            for package in root_index[5]:
                x.packages[package.text] = package.attrib["type"]
            groups.append(x)
        if collection_type == "category":
            x = metapackage()
            x.name = root_index[1].text
            x.abbrev = root_index[0].text
            x.desc = root_index[2].text
            for package in root_index[3]:
                x.packages[package.text] = "mandatory"
            categories.append(x)
        if collection_type == "environment":
            x = metapackage()
            x.name = root_index[1].text
            x.abbrev = root_index[0].text
            x.desc = root_index[2].text
            for package in root_index[4]:
                x.packages[package.text] = "mandatory"
            for package in root_index[5]:
                x.packages[package.text] = "optional"
            environments.append(x)
        if collection_type == "langpacks":
            pass
    return {
        "groups": groups,
        "categories": categories,
        "environments": environments
    }
