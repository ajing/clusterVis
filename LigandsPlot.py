"""
    Display a list of ligand structures in file
"""

import os
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

IMAGE_DIR = "./Image"

def ReturnFileDir(ligandname):
    return os.path.join(IMAGE_DIR, ligandname)

def PlotLigandStructures(ligands):
    N = len(ligands)
    col_num  = 2
    row_num  = N/col_num + 1
    for i in range(N):
        plt.subplot(row_num, col_num, i + 1)
        a_ligand = ligands[i]
        liganddir = ReturnFileDir(a_ligand)
        print liganddir
        img=mpimg.imread(liganddir)
        imgplot = plt.imshow(img)
        plt.title(a_ligand)
        plt.axis('off')
    plt.show()

if __name__ == "__main__":
    ligandlist = ["CHEMBL98350", "CHEMBL98172", "CHEMBL981"]
    PlotLigandStructures(ligandlist)
