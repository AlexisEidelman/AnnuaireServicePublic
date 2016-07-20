# -*- coding: cp1252 -*-
"""
Created on Tue Jul 19 18:01:29 2016

@author: User
"""

import pandas as pd
import graphistry

test = pd.read_csv('csv\\annuaire_20160629.csv', sep=',', 
                   encoding='cp1252')
test.rename(columns={
    'http://www.w3.org/2000/01/rdf-schema#label': 'label',
    },
    inplace=True)

api_key = '2d9f047b43b2953c1de263c85d85ba7b6907dc64bec82c713e3b3e07dffb40fafc523fbaec32a40b4479ec3a42fc46f6'
graphistry.register(key=api_key)

edges = test[['index', 'parent']]
nodes = test.copy().drop(['parent'], axis=1)

plotter = graphistry.bind(source="parent", destination='index')
plotter2 = plotter.bind(node='index', point_title='label')

plotter2.plot(edges, nodes)




# Convert our graph from Pandas to Igraph
import igraph
ig = plotter.pandas2igraph(edges)
igraph.summary(ig)

ig.vs['pagerank'] = ig.pagerank()
ig.vs['community'] = ig.community_infomap().membership 
igraph.summary(ig)
