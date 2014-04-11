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

def LenHist(numpyfile):
    dmatrix = numpy.load(numpyfile)
    print dmatriz.size

def LenHistMain():
    nfile = "Data/all_0.9.npz"
    LenHist(nfile)

if __name__ == "__main__":
    LenHistMain()
