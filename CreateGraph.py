"""
    Create graph from smatrix
"""
import networkx as nx
import numpy as np
import os
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
    if len(newlist) == 0:
        raise RuntimeError("Empty list after filtering!!")
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

def CheckExistingLeaderlist( typeofbinding, criteria ):
    criString = str(criteria)
    for eachfile in os.listdir("./Data/"):
        if typeofbinding in eachfile and criString in eachfile:
            return eachfile
    return None

def SaveLeader(leaderlist, typeofbinding, criteria):
    criString = str(criteria)
    filename = "_".join([ typeofbinding, criString ])
    saveDir  = "./Data/"
    np.save( saveDir + filename, leaderlist )

def main( bindingtype ):
    minDistance = 0.3
    smatrixfile = "./Data/similarityMatrix_small.npy"
    infile      = "./Data/ligand_5_7_ppilot.txt"
    smatrix     = np.load( smatrixfile )
    leaderfile  = CheckExistingLeaderlist( bindingtype, minDistance )
    if leaderfile:
        leaderlist = np.load( leaderfile )
    else:
        newgraph = createGraph( smatrix, minDistance )
        moldict = MoleculeDictionary( infile )
        leaderlist = LeaderInCluster( newgraph, moldict )
        SaveLeader(leaderlist, bindingtype, minDistance)
    leaderlist = BindingTypeFilter( leaderlist, moldict, bindingtype)
    print "length of leader list:"
    print len(leaderlist)
    BuildTree( leaderlist, smatrix, moldict, bindingtype )

if __name__ == "__main__":
    distanceList = [ 0.5, 0.45, 0.4, 0.35, 0.25 ]
    for each in ["allosteric"]:
        main(each)
