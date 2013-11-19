'''
    Get the target protein name for that ligand
'''

LibDir  = "/home/ajing/Documents/alloster/pylib/cluster"
FileDir = "/home/ajing/Documents/alloster/Cluster/database/"
import sys
sys.path.append(LibDir)
from database_parser import database

class LigandDict:
    def __init__(self):
        self.liganddict = self.GetLigandTarget()

    def GetLigandTarget(self):
        liganddict = dict()
        data = database(FileDir)
        ligandinfo = data.get_ligand_info()
        proteininfo = data.get_protein_info()
        ligandid   = ligandinfo["ligandid"]
        ligand_proteinid = ligandinfo["proteinid"]
        proteinid  = proteininfo["proteinid"]
        proteinname  = proteininfo["description"]
        num_ligand = len(ligandid)
        for i in range(num_ligand):
            the_ligand = ligandid[i]
            the_proteinid = ligand_proteinid[i]
            try:
                the_proteinname = proteinname[proteinid.index(the_proteinid)]
                liganddict[the_ligand] = the_proteinname
            except:
                pass
        return liganddict

    def GetProteinName(self, ligandname):
        return self.liganddict[ligandname]

if __name__ == "__main__":
    GetLigandTarget()
