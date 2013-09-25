"""
    Create graph from smatrix
"""
import networkx as nx
import numpy as np
from random import choice

def CreateGraph( smatrix, criteria ):
    newGraph = nx.Graph()
    row, col = smatrix.shape
    for eachrow in range(row):
        for eachcol in range( eachrow + 1, col ):
            eachweight = smatrix[eachrow, eachcol]
            if eachweight > criteria:
                newGraph.add_edge( eachrow, eachcol, weight = eachweight )
    return newGraph

def randomPickFromList( alist ):
    return choice( alist )

def LeaderInCluster( graphObj ):
    leaderList = []
    for eachSubGraph in nx.biconnected_component_subgraphs( graphObj ):
        centerlist = nx.center(eachSubGraph)
        if centerlist < 1:
            raise "A subgraph with less than 1 center"
        leaderList.append( randomPickFromList(centerlist) )
    return leaderList

def LeaderMatrix( smatrix, leaderlist ):
    return smatrix[leaderlist, :][:, leaderlist]

if __name__ == "__main__":
    smatrixfile = "/home/jing/Dropbox/alloster/workspace/Second_Age/Data/similarityMatrix.npy"
    smatrix = np.load( smatrixfile )
    newgraph = CreateGraph( smatrix, 0.1 )
    ## edge test
    #for each in newgraph.edges():
    #    print each
    leaderlist = LeaderInCluster( newgraph )
    print LeaderMatrix( smatrix, leaderlist ) 

