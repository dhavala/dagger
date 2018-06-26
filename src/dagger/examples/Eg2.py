#!/usr/bin/env python

import yaml
import pprint




with open("SampleDag.yaml", 'r') as stream:
    try:
        for doc in yaml.load_all(stream):
        	print('***')
        	pprint.pprint(doc)

    
    except yaml.YAMLError as exc:
        print(exc)

	