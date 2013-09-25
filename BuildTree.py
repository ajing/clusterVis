'''
    Build Tree from smatrix
'''
import ete2
from hcluster import linkage, to_tree

class BuildTree():
    def __init__( self, leaderlist, smatrix, moldict):
        self.distanceMatrix = smatrix
        self.leaderList = leaderlist
        self.molDict = moldict
        self.imgPath = "./Image/"
        self.drawTree()

    def LeaderMatrix( self, smatrix, leaderlist ):
        return smatrix[leaderlist, :][:, leaderlist]

    def imageFace( self, nodeID ):
        imageFileName = self.molDict[ nodeID ][ "ligandid" ]
        ligandFace    = ete2.faces.ImgFace( self.imgPath + imageFileName)
        return ligandFace

    def prepareTree( self ):
        # Y is a distance matrix for all elements
        #hcluster part
        Y = self.LeaderMatrix( self.distanceMatrix, self.leaderList )
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
                    origID  = self.leaderList[ch_node.id]
                    ch.name = str(origID)
                    # give one more attribute for size
                    #ch.size = ch_node.id
                    print ch_node.id
                    print self.molDict[ ch_node.id ]
                    ch.img_style["size"] = self.molDict[ origID ]["size"]
                    ligandFace = self.imageFace( ch_node.id )
                    ch.add_face( ligandFace, column = 1 )
                    item2node[node].add_child(ch)
                    item2node[ch_node] = ch
                    to_visit.append(ch_node)
        # This is your ETE tree structure
        tree = root
        return tree

    def drawTree( self ):
        ts = ete2.TreeStyle()
        ts.mode = "c"
        t = self.prepareTree( )
        t.show( tree_style = ts )

if __name__ == "__main__":
    pass

