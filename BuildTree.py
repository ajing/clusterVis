'''
    Build Tree from dmatrix
'''
import ete2
from ete2 import Tree, faces
import datetime
import math
from hcluster import linkage, to_tree

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

    def LeaderMatrix( self, dmatrix, leaderlist ):
        return dmatrix[leaderlist, :][:, leaderlist]

    def imageFace( self, nodeID ):
        imageFileName = self.molDict[ nodeID ][ "ligandid" ]
        ligandFace    = ete2.faces.ImgFace( self.imgPath + imageFileName, 100, 100)
        return ligandFace

    def prepareTree( self ):
        # Y is a distance matrix for all elements
        #hcluster part
        Y = self.LeaderMatrix( self.distanceMatrix, self.leaderList )
        N = Y.shape[0]
        Z = linkage(Y, "single")
        T = to_tree(Z)
        #ete2 section
        root = ete2.Tree()
        root.dist = 0
        root.name = "root"
        item2node = {T: root}
        to_visit = [T]
        while to_visit:
            node = to_visit.pop()
            cl_dist = node.dist /2.0
            for ch_node in [node.left, node.right]:
                if ch_node:
                    ch = ete2.Tree()
                    ch.dist = cl_dist
                    if ch_node.id < N:
                        origID  = self.leaderList[ch_node.id]
                        ch.name = self.molDict[ origID ]["ligandid"]
                        style = ete2.NodeStyle()
                        style["vt_line_width"] = self.figuresize/5
                        style["hz_line_width"] = self.figuresize/5
                        # give one more attribute for size
                        #ch.size = ch_node.id
                        try:
                            style["size"] = math.log( self.molDict[ origID ]["size"] )
                            ch.img_style = style
                        except:
                            print self.molDict[ origID ]
                            raise LookupError("cannot find:" + str(origID))
                        ligandFace = self.imageFace( ch_node.id )
                        #ch.add_face( ligandFace, column = 1 )
                    item2node[node].add_child(ch)
                    item2node[ch_node] = ch
                    to_visit.append(ch_node)
        # This is your ETE tree structure
        tree = root
        return tree

    def my_layout( self, node ):
        if not node.is_leaf():
            node.img_style["size"] = 0

    def drawTree( self ):
        ts = ete2.TreeStyle()
        ts.mode = "c"
        ts.layout_fn = self.my_layout
        t = self.prepareTree()
        t.unroot()
        fmt='%Y-%m-%d-%Hh-%Mm_{fname}'
        newfilename = datetime.datetime.now().strftime(fmt).format(fname = self.figure)
        newfile = self.savePath + newfilename
        #t.show( tree_style = ts )
        t.render( newfile, tree_style=ts)

if __name__ == "__main__":
    pass

