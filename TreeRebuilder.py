"""
    Rewrite file to make the node name simple, so graphviz can understand
    Assumption: 1. node names are started with CHEMBL or ASD
                2. only two kinds of statements contain node name: (1) node declaration (2) edge between nodes.
"""

import sys

def NodeNameExist(line):
    if "CHEMBL" in line or "ASD" in line:
        return True
    else:
        return False

def IsEdge(line):
    if "--" in line:
        return True
    else:
        return False

def NameAndAttribute(line):
    split_index = line.index("[")
    name   = line[:split_index]
    attr   = line[split_index:]
    return name, attr

def ProcessName(name, isedge):
    if isedge:
        firstnode, secondnode = name.split("--")
        firstnode = firstnode.strip()
        secondnode = secondnode.strip()
        return firstnode, secondnode
    else:
        return name.strip()

def static_var(varname,value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

@static_var("counter", 0)
@static_var("hashtable", dict())
def HashANode(nodename):
    if nodename in HashANode.hashtable:
        return "N" + str(HashANode.hashtable[nodename])
    else:
        HashANode.hashtable[nodename] = HashANode.counter
        HashANode.counter += 1
        return "N" + str(HashANode.hashtable[nodename])

def RewriteDot(infile):
    nodename = dict()
    newfilename = infile + "_simple"
    newfileobj  = open(newfilename, "w")
    for eachline in open(infile):
        if NodeNameExist(eachline):
            name, attr = NameAndAttribute(eachline)
            if IsEdge(eachline):
                fnode, snode = ProcessName(name, True)
                fnode_new = HashANode(fnode)
                snode_new = HashANode(snode)
                new_line  = "--".join([fnode_new, snode_new]) + attr
            else:
                node = ProcessName(name, False)
                node_new = HashANode(node)
                new_line = node_new + attr
            newfileobj.write(new_line)
        else:
            newfileobj.write(eachline)
    newfileobj.close()

if __name__ == "__main__":
    infile = sys.argv[1]
    print infile
    RewriteDot(infile)
