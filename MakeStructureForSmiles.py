"""
  Using pybel to create image for each smile string
"""

import pybel

def GetAllinfo(infile):
    # To understand ligand cluster file
    rownum = 0
    all_info = dict()
    # first_col is only for descriptor file, the first column is a smile string
    first_col = dict()
    for line in open(infile):
        if rownum == 0:
            header = line.strip().split('\t')
            #print header
            for each in header:
                all_info[each] = []
        else:
            content = line.strip().split('\t')
            first_col[content[0]] = content[1:]
            for i in range(len(header)):
                try:
                    all_info[header[i]].append(content[i])
                except:
                    print content
        rownum += 1
    return all_info

def MakeStructuresForSmiles( all_info ):
    totalrow = len( all_info[ "ligandid" ] )
    relativedir = "./Data/"
    for index in range( totalrow ):
        smile = all_info[ "Canonical_Smiles" ][ index ]
        pngfile = all_info[ "ligandid" ][ index ]
        mol = pybel.readstring( "smi", smile )
        mol.draw( show=False, filename = relativedir + pngfile ) 


if __name__ == "__main__":
    infile = "./Data/ligand_5_7_ppilot.txt"
    all_info = GetAllinfo( infile )
    MakeStructuresForSmiles( all_info )
