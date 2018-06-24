#!/usr/bin/env python

import yaml

with open("EgDSLpureYaml.yaml", 'r') as stream:
    try:
        doc = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(doc)