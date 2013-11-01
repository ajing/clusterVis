"""
    For picking ligand names for a branch
"""

from TreeRebuilder import *

def GetLevelFromName(name):
    return len(name.strip().split("_"))

def GetLigandBranch(ligandname, level, treefile):
    for eachline in open(treefile):
        if ligandname in eachline and not IsEdge(eachline):
            name, attr = NameAndAttribute(eachline)
            if GetLevelFromName(name) > level:
                return name.split("_")

class Node:
    def __init__(self, name, width):
        self.name = name
        self.width = width

def SigNodeParser(treefile, cri_width):
    # input treefile, output node dict class
    node_list = []
    for eachline in open(treefile):
        if NodeNameExist(eachline) and not IsEdge(eachline):
            name, attr = NameAndAttribute(eachline)
            width = GetAttributeValue("width", attr)
            if float(width) > cri_width:
                anode = Node(name, width)
                node_list.append(anode)
    return node_list

def SignificantClusters(ligands, nodelist):
    sig_ligands = []
    for each in ligands:
        for eachnode in nodelist:
            if each == eachnode.name:
                sig_ligands.append(each)
    return sig_ligands

def GetBranchLargeCluster(ligandname, treefile):
    level = 15
    width_cut = 0.02
    all_ligands_in_cluster = GetLigandBranch(ligandname, level, treefile)
    node_list = SigNodeParser(treefile, width_cut)
    s_ligands = SignificantClusters(all_ligands_in_cluster, node_list)
    return s_ligands

if __name__ == "__main__":
    tree_file = "./Data/all_0.9.gv"
    ligandname = "ASD01910452"
    GetBranchLargeCluster(ligandname, tree_file)
