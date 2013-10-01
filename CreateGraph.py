"""
    Create graph from dmatrix
"""
import networkx as nx
import numpy as np
import os
from random import choice
from MakeStructuresForSmiles import GetAllinfo
from BuildTree import BuildTree
# Global variable so I can change easily
__SAVEDIR__ = "./Data/"

def createGraph( dmatrix, criteria, moldict, typeofbinding ):
    newGraph = nx.Graph()
    row, col = dmatrix.shape
    print row, col
    for eachrow in range(row):
        # in case, isolated nodes exist in graph
        if not IsTypeofBinding(eachrow, moldict, typeofbinding):
            continue
        newGraph.add_node( eachrow )
        for eachcol in range( eachrow + 1, col ):
            if not IsTypeofBinding(eachcol, moldict, typeofbinding):
                continue
            eachweight = dmatrix[eachrow, eachcol]
            if eachweight < criteria:
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
        if len(centerlist) < 1:
            raise "A subgraph with less than 1 center"
        leaderID   = RandomPickFromList(centerlist)
        leaderList.append( leaderID )
        graphSize  = len(eachSubGraph)
        moldict[ leaderID ][ "size" ] = graphSize
    return leaderList

def IsTypeofBinding( index, moldict, typeofbinding ):
    return moldict[index]["typeofbinding"] == typeofbinding

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
    for eachfile in os.listdir(__SAVEDIR__):
        if typeofbinding in eachfile and criString in eachfile:
            return __SAVEDIR__ + eachfile
    return None

def SaveLeaderAndMolDict(leaderlist, moldict, typeofbinding, criteria):
    criString = str(criteria)
    filename = "_".join([ typeofbinding, criString ])
    np.savez( __SAVEDIR__ + filename, leaderlist, moldict )

def main( bindingtype ):
    minDistance = 0.75
    smatrixfile = "./Data/similarityMatrix.npy"
    infile      = "./Data/ligand_5_7_ppilot.txt"
    dmatrix     = 1 - np.load( smatrixfile )
    leaderfile  = CheckExistingLeaderlist( bindingtype, minDistance )
    if leaderfile:
        leader_moldict = np.load(leaderfile)
        leaderlist     = leader_moldict["leaderlist"]
        moldict        = leader_moldict["moldict"]
    else:
        moldict = MoleculeDictionary( infile )
        newgraph = createGraph( dmatrix, minDistance, moldict, bindingtype)
        leaderlist = LeaderInCluster( newgraph, moldict )
        SaveLeaderAndMolDict(leaderlist, moldict, bindingtype, minDistance)
    leaderlist = BindingTypeFilter( leaderlist, moldict, bindingtype)
    print "length of leader list:"
    print len(leaderlist)
    BuildTree( leaderlist, dmatrix, moldict, bindingtype )

if __name__ == "__main__":
    distanceList = [ 0.6, 0.65, 0.7, 0.8 ]
    for each in ["allosteric", "competitive"]:
        main(each)
