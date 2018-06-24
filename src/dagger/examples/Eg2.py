#!/usr/bin/env python

import yaml

class Lib(yaml.YAMLObject):
	yaml_tag = '!Lib'
	pass


with open("Eg2.yaml", 'r') as stream:
    try:
        for doc in yaml.load_all(stream):
        	print('***')
        	print(doc)

    
    except yaml.YAMLError as exc:
        print(exc)

	