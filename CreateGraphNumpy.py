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

def LeaderMatrix( self, dmatrix, leaderlist ):
    return dmatrix[leaderlist, :][:, leaderlist]

def MapIndexbyBindingSite( moldict, bindingtype):
    indexList = []
    for eachID in moldict:
        if moldict[eachID]["typeofbinding"] == bindingtype:
            indexList.append(eachID)
        else:
            indexList.append(eachID)
    print "indexList length:", len(indexList)
    print "original length:", len(moldict.keys())
    return np.array(indexList)

def ClusterAssignment( dmatrix, criteria, indexarray ):
    print indexarray
    dim  =  dmatrix.shape
    modiarray   = indexarray[ indexarray < dim[0] ]
    if len(modiarray) < 1:
        raise LookupError("Cannot find this type of binding")
    dmatrixType = dmatrix[modiarray, :][:, modiarray]
    dlink = linkage(dmatrixType)
    #clusterIndex = fcluster(dlink, criteria, criterion="distance")
    clusterIndex = fcluster(dlink, criteria)
    return clusterIndex

def LeaderFilter( leaderID, moldict ):
    # filter1: does not include any group with size less than 8
    # disable this filter
    return False
    if moldict[ leaderID ][ "size" ] < 15:
        return True
    return False

def LeaderInCluster( clusterIndex, moldict ):
    leaderList = []
    print "the total number of groups:", max(clusterIndex)
    for groupID in range(1, max(clusterIndex) + 1):
        indices = (clusterIndex == groupID).nonzero()
        indicesConvert = indices[0].tolist()
        # probably I should find a way to get center of cluster
        numLoops = 0
        leaderID   = RandomPickFromList(indicesConvert)
        clusterSize = len(indicesConvert)
        moldict[ leaderID ][ "size" ] = clusterSize
        # add key to moldict, so I can easily get clusterSize
        moldict[ moldict[leaderID]["ligandid"] ] = [clusterSize, moldict[leaderID]["typeofbinding"]]
        if LeaderFilter( leaderID, moldict ):
            continue
        leaderList.append(leaderID)
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

def SanityCheck( moldict, dmatrix ):
    dmatrixdim = dmatrix.shape
    moldictlen = sum( [ 1 for each in moldict.keys() if isinstance(each, int)] )
    if not dmatrixdim[0] == moldictlen:
        print "dmatrixdim:", dmatrixdim[0]
        print "moldictlen:", moldictlen
        raise ImportError("The dmatrix and moldict dimension doesn't match")

def main( bindingtype, minDistance, dmatrix ):
    #minDistance = 0.75
    leaderAndmol = CheckExistingLeaderlist( bindingtype, minDistance )
    infile      = "./Data/ligand_5_7_ppilot_modified.txt"
    #leaderAndmol = False
    if leaderAndmol:
        leaderfile, moldictfile = leaderAndmol
        with np.load(leaderfile) as leader_moldict:
            print leader_moldict.files
            leaderlist     = leader_moldict["arr_0"]
            print "leaderlist length:", len(leaderlist)
        with open(moldictfile, "rb") as moldictobj:
            moldict        = pickle.load(moldictobj)
        SanityCheck( moldict, dmatrix )
        SizeHistogram( moldict )
    else:
        moldict = MoleculeDictionary( infile )
        SanityCheck( moldict, dmatrix )
        indexArray   = MapIndexbyBindingSite( moldict, bindingtype )
        clusterindex = ClusterAssignment( dmatrix, minDistance, indexArray )
        leaderlist = LeaderInCluster( clusterindex, moldict )
        print "leaderlist length:", len(leaderlist)
        SaveLeaderAndMolDict(leaderlist, moldict, bindingtype, minDistance)
        SizeHistogram( moldict )
    #leaderlist = BindingTypeFilter( leaderlist, moldict, bindingtype)
    BuildTree( leaderlist, dmatrix, moldict, str(minDistance) + "_" + bindingtype )

if __name__ == "__main__":
    smatrixfile = "./Data/similarityMatrix.npy"
    dmatrix = 1 - np.load(smatrixfile)
    # a small filter to set everything less than 0.7 to 0
    #dmatrix = dmatrix * (dmatrix > 0.7)
    #distanceList = [ 0.6, 0.65, 0.7, 0.8 ]
    #distanceList = [ 0.85, 0.9, 0.95 ]
    #distanceList = [ 0.96, 0.97, 0.98, 0.99 ]
    distanceList = [ 0.6 ]
    #print "for distance criterion"
    print "for non-consistent criterion"
    for each in ["all"]:
        for distance in distanceList:
            print "bindingtype:", each
            print "distance", distance
            main(each, distance, dmatrix)
