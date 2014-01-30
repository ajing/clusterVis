'''
    ligand similarity for NAMS
'''
from ligandGraphall import *

# for nams
from nams import nams
ms=nams.Nams()

# for clean smile string
import openbabel

def getSimilarityNAMS(smile1, smile2):
    smile1_clean = CleanSmile(smile1)
    smile2_clean = CleanSmile(smile2)
    mol_t1 = ("smi", smile1_clean)
    mol_t2= ("smi", smile2_clean)
    mol1, mol_info1 = ms.get_mol_info(mol_t1[0],mol_t1[1])
    mol2, mol_info2 = ms.get_mol_info(mol_t2[0],mol_t2[1])
    sim11, d_atoms = ms.get_similarity(mol_info1, mol_info1)
    sim22, d_atoms = ms.get_similarity(mol_info2, mol_info2)
    sim12, d_atoms = ms.get_similarity(mol_info1, mol_info2)
    return sim12/(sim11+ sim22 -sim12)

def CleanSmile( smile ):
    # this function is for nams
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("smi", "smi")
    mol = openbabel.OBMol()
    obConversion.ReadString(mol, smile)
    mol.StripSalts()
    if mol.NumAtoms() < 6:
        return None
    clean_smi = obConversion.WriteString(mol)
    return clean_smi
