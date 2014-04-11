'''
    Histogram of edge length
'''
from TreeRebuilder import IsEdge, NameAndAttribute, GetAttributeValue
import matplotlib.pyplot as plt
import numpy

def LenHist(dotfile):
    # I assume dot file has len attribute for edge
    lenlist = []
    for line in open(dotfile):
        if IsEdge(line):
            name, attr = NameAndAttribute(line)
            lenvalue = GetAttributeValue("len", attr).replace('"', '').replace(",",'')
            lenlist.append(float(lenvalue))
    plt.hist(lenlist, 10)
    plt.show()

if __name__ == "__main__":
    infile = "Data/all_0.9.gv_beforeMod"
    infile = "Data/all_0.3.gv"
    infile = "Data/09_simple.gv"
    infile = "Data/03_simple.gv"
    infile = "Data/09_simple_10_2.gv"
    LenHist(infile)

