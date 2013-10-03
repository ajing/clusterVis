"""
    Create graph from dmatrix
"""
import numpy as np
import os
import pickle
from random import choice
from MakeStructuresForSmiles import GetAllinfo
from BuildTree import BuildTree
from hcluster import linkage, fcluster
# Global variable so I can change easily
__SAVEDIR__ = "./Data/"

def ClusterAssignment( dmatrix, criteria ):
    dlink = linkage(dmatrix)
    clusterIndex = fcluster(dlink, criteria)
    return np.array(clusterIndex)

def LeaderInCluster( clusterIndex, moldict ):
    leaderList = []
    for groupID in range(1, max(clusterIndex + 1)):
        indices = (clusterIndex == groupID).nonzero()
        indicesConvert = indices[0].tolist()
        # probably I should find a way to get center of cluster
        print len(indicesConvert)
        if len(indicesConvert) < 1:
            raise "A subgraph with less than 1 center"
        leaderID   = RandomPickFromList(indicesConvert)
        print leaderID
        leaderList.append(leaderID)
        clusterSize = len(indicesConvert)
        print "clustersize", clusterSize
        moldict[ leaderID ][ "size" ] = clusterSize
    return leaderList

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
    expectFile = typeofbinding + "_" + criString
    numpyarray = None
    moldictfile = None
    for eachfile in os.listdir(__SAVEDIR__):
        if typeofbinding in eachfile and criString in eachfile:
            filedir = __SAVEDIR__ + eachfile
            if eachfile == expectFile + ".npz":
                numpyarray = filedir
            if eachfile == expectFile + ".p":
                moldictfile = filedir
    if not numpyarray is None and not moldictfile is None:
        return (numpyarray, moldictfile)
    return None

def SizeHistogram( moldict ):
    sizeList = []
    for eachID in moldict:
        try:
            sizeList.append(moldict[eachID]["size"])
        except:
            continue
    value, binedge = np.histogram(sizeList)
    print "number:", value
    print "value:", binedge

def SaveLeaderAndMolDict(leaderlist, moldict, typeofbinding, criteria):
    criString = str(criteria)
    filename = "_".join([ typeofbinding, criString ])
    filedir  = __SAVEDIR__ + filename
    np.savez( filedir, leaderlist )
    pickle.dump( moldict, open( filedir + ".p", "wb" ))

def main( bindingtype, minDistance, dmatrix ):
    #minDistance = 0.75
    infile      = "./Data/ligand_5_7_ppilot.txt"
    leaderAndmol = CheckExistingLeaderlist( bindingtype, minDistance )
    if leaderAndmol:
        leaderfile, moldictfile = leaderAndmol
        with np.load(leaderfile) as leader_moldict:
            print leader_moldict.files
            leaderlist     = leader_moldict["arr_0"]
            print "leaderlist length:", len(leaderlist)
        with open(moldictfile, "rb") as moldictobj:
            moldict        = pickle.load(moldictobj)
        SizeHistogram( moldict )
    else:
        moldict = MoleculeDictionary( infile )
        clusterindex = ClusterAssignment( dmatrix, minDistance)
        leaderlist = LeaderInCluster( clusterindex, moldict )
        SaveLeaderAndMolDict(leaderlist, moldict, bindingtype, minDistance)
        SizeHistogram( moldict )
    leaderlist = BindingTypeFilter( leaderlist, moldict, bindingtype)
    BuildTree( leaderlist, dmatrix, moldict, str(minDistance) + "_" + bindingtype )

if __name__ == "__main__":
    smatrixfile = "./Data/similarityMatrix_small.npy"
    dmatrix = 1 - np.load(smatrixfile)
    distanceList = [ 0.6, 0.65, 0.7, 0.8 ]
    #distanceList = [ 0.8 ]
    for each in ["allosteric", "competitive"]:
        for distance in distanceList:
            main(each, distance, dmatrix)
