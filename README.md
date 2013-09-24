clusterVis
==========

Input: graph format with edge weight.

Process: 1. create a graph object with networkX
         2. clustering graph by minimun distance between clusters (networkX?)
         3. only keep one molecule for each cluster (networkX center function)
         4. create image for each molecule (I probably should create image for all molecules)
         5. build a tree with center molecule (ete)

Data structure:
         1. graph: keep all information of molecule similarity
         2. molecule dictionary: mapping from id to molecule image, smile string

Corresponding functions:
         1. CreateGraph( smatrix )
                : smatrix is a similarity matrix for taminoto coefficient produced by ligandGraphall
                : output is a networkX graph object 
         2. EdgesLessThan( graphObj, criteria )
                : return a list of edges with weight less than criteria
            ClusterGraph( graphObj, criteria )
                : remove edges return from EdgesLessThan
                : return a new graphObj
         3. LeaderInCluster( graphObj )
                : biconnected_component_subgraphs() and center() in networkX
                : return a list of ids to represent leaders
         4. MakeStructureForSmiles( )
                : mymol = readstring("smi", "CCCC")  mymol.draw(show=False, filename="test") from pybel  
                : save all PNG files to a folder with certain name
         5. BuildTree( leaderlist, moldict )
                : leaderlist return from LeaderInCluster, moldict mapping from molecule id to imagedir
