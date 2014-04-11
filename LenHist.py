'''
    Histogram of edge length
'''
from TreeRebuilder import IsEdge, NameAndAttribute, GetAttributeValue
import matplotlib.pyplot as plt
import numpy

def EdgeHist(dotfile):
    # I assume dot file has len attribute for edge
    lenlist = []
    for line in open(dotfile):
        if IsEdge(line):
            name, attr = NameAndAttribute(line)
            lenvalue = GetAttributeValue("len", attr).replace('"', '').replace(",",'')
            lenlist.append(float(lenvalue))
    plt.hist(lenlist, 10)
    plt.show()

def EdgeHistMain():
    infile = "Data/all_0.9.gv_beforeMod"
    infile = "Data/all_0.3.gv"
    infile = "Data/09_simple.gv"
    infile = "Data/03_simple.gv"
    infile = "Data/09_simple_10_2.gv"
    EdgeHist(infile)

def LenHist(clusterleader, matrixfile):
    leader = numpy.load(clusterleader)
    dmatrix = numpy.load(matrixfile)
    leaderindex = numpy.array(leader["arr_0"])
    leaderindex.sort()
    print leaderindex
    leader_dmatrix = dmatrix[:,leaderindex][leaderindex, :]
    print leader_dmatrix.size
    leader_dvector = leader_dmatrix.flatten()
    leader_dvector = leader_dvector[leader_dvector < 1]
    print leader_dvector
    print len(leader_dvector)
    plt.hist( leader_dvector, bins = 100, normed = True)
    plt.show()

def LenHistMain():
    leaderfile = "Data/all_0.9.npz"
    matrixfile = "Data/similarityMatrix.npy"
    LenHist(leaderfile, matrixfile)

if __name__ == "__main__":
    LenHistMain()
