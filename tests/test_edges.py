#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from dagger.parse import make_edge_Cypher_parser_object
from dagger.parse import make_edge_DOT_parser_object
from dagger.parse import make_JSON_parser_object

__author__ = "dhavala"
__copyright__ = "dhavala"
__license__ = "mit"

# test strings
s1 = """
 x > y
"""

print("\n\n\n **** \n\n\n")
test_str_02 = """x_01 > x_02 > x_03 A_01 !{"key":"val"} B_01
[y_01,y_02] > y_03 z_01 | z_02
[y_01,y_02] >{"key":1} [y_03,y_04] | y_05 >{"key":"val"} y_06 |{ola_01} y_07 | y_08
"""
edgeExpr = make_edge_Cypher_parser_object() 

edgeLists = test_str_02.splitlines()

for edges in edgeLists:
    print("***\n"+edges)
    result = edgeExpr.parseString(edges)
    for num, token in enumerate(result):
        print('token: #'+str(num))
        pprint.pprint(token)
    print("")


test_str = """x_01 > x_02 {"1":0,"2":1} > x_03 A_01 | B_01
y_01 > y_02 {"x1":"val1"} > y_03
z_01 > z_02 {"x1":"val1"} > z_03
x_01 | x_02 {"1":0,"2":1} ! x_03
"""
#edgeLists = (' ').splitlines()
edgeExpr = make_edge_DOT_parser_object() 
edgeLists = test_str.splitlines()
for edges in edgeLists:
    print("***\n"+edges)
    result = edgeExpr.parseString(edges)
    #result = edgeListExpr.parseString(edges)
    for num, token in enumerate(result):
        print('token: #'+str(num))
        pprint.pprint(token)
    print("")
