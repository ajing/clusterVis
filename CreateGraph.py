"""
    Create graph from smatrix
"""
import networkx as nx
import numpy as np
from random import choice
from MakeStructuresForSmiles import GetAllinfo
from BuildTree import BuildTree

def createGraph( smatrix, criteria ):
    newGraph = nx.Graph()
    row, col = smatrix.shape
    print row, col
    for eachrow in range(row):
        # in case, isolated nodes exist in graph
        newGraph.add_node( eachrow )
        for eachcol in range( eachrow + 1, col ):
            eachweight = smatrix[eachrow, eachcol]
            if eachweight > criteria:
                newGraph.add_edge( eachrow, eachcol, weight = eachweight )
    return newGraph

def RandomPickFromList( alist ):
    return choice( alist )

def BindingTypeFilter( alist, moldict, bindingType = None ):
    if bindingType is None:
        return alist
    newlist = []
    for eachIndex in alist:
        if moldict[ eachIndex ]["typeofbinding"] == bindingType:
            newlist.append( eachIndex )
    return newlist

def LeaderInCluster( graphObj, moldict ):
    leaderList = []
    for eachSubGraph in nx.connected_component_subgraphs( graphObj ):
        centerlist = nx.center(eachSubGraph)
        if centerlist < 1:
            raise "A subgraph with less than 1 center"
        leaderID   = RandomPickFromList(centerlist)
        leaderList.append( leaderID )
        graphSize  = len(eachSubGraph)
        moldict[ leaderID ][ "size" ] = graphSize
    return leaderList


def MoleculeDictionary( infile ):
    all_info = GetAllinfo( infile )
    totalrow = len( all_info[ "ligandid" ] )
    molDict  = dict()
    for index in range( totalrow ):
        ligandid = all_info[ "ligandid" ][ index ]
        bindingtype = all_info[ "typeofbinding" ][ index ]
        molDict[index] = { "ligandid": ligandid, "typeofbinding": bindingtype }
    return molDict


if __name__ == "__main__":
    smatrixfile = "./Data/similarityMatrix.npy"
    infile = "./Data/ligand_5_7_ppilot.txt"
    bindingtype = "allosteric"
    smatrix = np.load( smatrixfile )
    newgraph = createGraph( smatrix, 0.7 )
    ### edge test
    ##for each in newgraph.edges():
    ##    print each
    moldict = MoleculeDictionary( infile )
    leaderlist = LeaderInCluster( newgraph, moldict )
    print "length of leader list:"
    print len(leaderlist)
    leaderlist = BindingTypeFilter( leaderlist, moldict, bindingtype)
    #BuildTree( leaderlist, smatrix, moldict )
