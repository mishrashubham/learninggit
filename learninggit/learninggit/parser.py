import json
from pprint import pprint
import pickle

def header():
 list=["cubedpi.json","cubetethering.json"]
 d=dict()
 for r in list:
  with open(r) as data_file:
    data = json.load(data_file)
    if r=="cubedpi.json":

      atlascubes=data["cubes"].keys()
    else:
      tetheringcubes=data["cubes"].keys()
  for i in data["cubes"].keys():
    for y in data["cubes"][i].keys():
        if y=="dimension_types":
         dimension_set=[str(k.keys()).strip("]").strip("[").strip("u'")+"(dimension)" for k in data["cubes"][i][y]]
        elif y=="measure_operations":
         measure_set=[str(k.keys()).strip("]").strip("[").strip("u'")+"(measure)" for k in data["cubes"][i][y]]
        else:
           continue
    m=dimension_set+measure_set
    print i,":",m
    d[i]=m
 return d,atlascubes,tetheringcubes
k,atlascubes,tetheringcubes=header()

