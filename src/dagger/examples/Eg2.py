#!/usr/bin/env python

import yaml
import pprint

from ..parse import *

class Lib(yaml.YAMLObject):
	yaml_tag = '!Lib'
	pass


with open("Eg2.yaml", 'r') as stream:
    try:
        for doc in yaml.load_all(stream):
        	print('***')
        	pprint.pprint(doc)

    
    except yaml.YAMLError as exc:
        print(exc)

	