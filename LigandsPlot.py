"""
    Display a list of ligand structures in file
"""

import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from TreeParser import *
from NodeReference import *

IMAGE_DIR = "./Image"

def ReturnFileDir(ligandname):
    return os.path.join(IMAGE_DIR, ligandname)

def PlotLigandStructures(ligands, nodesize):
    N = len(ligands)
    col_num  = 3
    row_num  = N/col_num + 1
    liganddict = LigandDict()
    plt.figure(figsize = (40,40))
    for i in range(N):
        plt.subplot(row_num, col_num, i + 1)
        a_ligand = ligands[i]
        proteinname = liganddict.GetProteinName(a_ligand)
        liganddir = ReturnFileDir(a_ligand)
        print liganddir
        img=mpimg.imread(liganddir)
        imgplot = plt.imshow(img)
        plt.title(a_ligand + "\n" + proteinname + "," + str(nodesize[i]), fontsize=35)
        plt.axis('off')
    plt.savefig( "./Data/" + str(ligands[0]) + ".pdf", format = 'pdf')
    plt.show()

if __name__ == "__main__":
    tree_file = "./Data/all_0.9.gv"
    #ligandname = "ASD01911150"  # 40
    #ligandname = "ASD01910794"  # 47
    #ligandname = "ASD01910452"  # 14
    #ligandname = "CHEMBL106917"  # 60
    #ligandname = "ASD03540047"  # 32
    #ligandname = "CHEMBL347077"  # 0
    #ligandname = "CHEMBL566469"  # 29
    #ligandname = "ASD01150884"  # 43
    #ligandname = "ASD02900007"  # 49 this ligand branch is kind of mixture of everything
    #ligandname = "ASD01410309"  # 5
    #ligandname = "ASD03720006"  # 42 mixed with different receptors
    #ligandname = "ASD01410309"  # 42
    #ligandname = "ASD00170564"  # 54
    #ligandname = "ASD01150113"  # 21
    #ligandname = "ASD01120069"  # 4
    #ligandname = "ASD01120153"  # 59
    #ligandname = "ASD03910042"  # 26
    ligandname = "CHEMBL596211"  # 16
    #ligandname = "ASD03090737"  # 37
    ligandlist, node_size = GetBranchLargeCluster(ligandname, tree_file)
    PlotLigandStructures(ligandlist, node_size)
    print ligandlist
    print node_size
