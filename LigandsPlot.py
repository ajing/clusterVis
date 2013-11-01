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

def PlotLigandStructures(ligands):
    N = len(ligands)
    col_num  = 5
    row_num  = N/col_num + 1
    liganddict = LigandDict()
    for i in range(N):
        plt.subplot(row_num, col_num, i + 1)
        a_ligand = ligands[i]
        proteinname = liganddict.GetProteinName(a_ligand)
        liganddir = ReturnFileDir(a_ligand)
        print liganddir
        img=mpimg.imread(liganddir)
        imgplot = plt.imshow(img)
        plt.title(a_ligand + " " + proteinname)
        plt.axis('off')
    plt.show()

if __name__ == "__main__":
    tree_file = "./Data/all_0.9.gv"
    ligandname = "ASD01910452"
    ligandname = "ASD01910380"
    ligandlist = GetBranchLargeCluster(ligandname, tree_file)
    PlotLigandStructures(ligandlist)
