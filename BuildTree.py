'''
    Build Tree from dmatrix
'''
import ete2
from ete2 import Tree, faces
import datetime
import math
from hcluster import linkage, to_tree
from TreeConstruction import *
import pickle

class ImgFace(faces.Face):
    def __init__(self, img_file, width=None, height=None):
        faces.Face.__init__(self)
        self.img_file = img_file
        self.width = width
        self.height = height

    def update_pixmap(self):
        self.pixmap = QtGui.QPixmap(self.img_file)
        if self.width and self.height:
            self.pixmap = self.pixmap.scaled(self.width, self.height)

class BuildTree():
    def __init__( self, leaderlist, dmatrix, moldict, figurename):
        self.distanceMatrix = dmatrix
        self.leaderList = leaderlist
        self.molDict  = moldict
        self.figuresize = len(leaderlist)
        self.figure   = figurename + ".svg"
        self.savePath = "./Data/"
        self.imgPath = "./Image/"
        self.size    = len(leaderlist)
        self.drawTree()

    def LeaderName( self, leaderlist ):
        leadername = []
        for each in leaderlist:
            leadername.append(self.molDict[each]["ligandid"])
        return leadername

    def LeaderMatrix( self, dmatrix, leaderlist ):
        return dmatrix[leaderlist, :][:, leaderlist]

    def imageFace( self, nodeID ):
        imageFileName = self.molDict[ nodeID ][ "ligandid" ]
        ligandFace    = ete2.faces.ImgFace( self.imgPath + imageFileName, 100, 100)
        return ligandFace

    def prepareNJ(self):
        leader_name = self.LeaderName(self.leaderList)
        d_shrink_matrix = self.LeaderMatrix( self.distanceMatrix, self.leaderList )
        if not d_shrink_matrix.size == len(leader_name)**2:
            raise ValueError("size doesn't match between leaderlist and distance matrix")
        DMatrix = DistanceMatrix(leader_name, d_shrink_matrix)
        root    = nj(DMatrix, self.molDict)
        fmt='%Y-%m-%d-%Hh-%Mm_{fname}_pickle_tree'
        newfilename = datetime.datetime.now().strftime(fmt).format(fname = self.figure)
        pickle.dump(root, open(newfilename, "w"))
        return root

    def my_layout( self, node ):
        if not node.is_leaf():
            node.img_style["size"] = 0

    def drawTree( self ):
        ts = ete2.TreeStyle()
        ts.mode = "c"
        ts.show_leaf_name = True
        ts.layout_fn = self.my_layout
        t = self.prepareNJ()
        t.unroot()
        fmt='%Y-%m-%d-%Hh-%Mm_{fname}'
        fmt_newick='%Y-%m-%d-%Hh-%Mm_{fname}_newick'
        newfilename = datetime.datetime.now().strftime(fmt).format(fname = self.figure)
        newfile = self.savePath + newfilename
        #t.show( tree_style = ts )
        t.render( newfile, tree_style=ts)
        newick_filename = datetime.datetime.now().strftime(fmt_newick).format(fname = self.figure)
        open(newick_filename, "w").write(t.write(format=1))

if __name__ == "__main__":
    pass
