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

def LeaderInCluster( graphObj, moldict ):
    leaderList = []
    for eachSubGraph in nx.biconnected_component_subgraphs( graphObj ):
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
        molDict[index] = { "ligandid": ligandid }
    return molDict
    

if __name__ == "__main__":
    smatrixfile = "/home/jing/Dropbox/alloster/workspace/Second_Age/Data/similarityMatrix.npy"
    infile = "./Data/ligand_5_7_ppilot.txt"
    smatrix = np.load( smatrixfile )
    newgraph = createGraph( smatrix, 0.1 )
    ## edge test
    #for each in newgraph.edges():
    #    print each
    moldict = MoleculeDictionary( infile ) 
    leaderlist = LeaderInCluster( newgraph, moldict )
    BuildTree( leaderlist, smatrix, moldict )
