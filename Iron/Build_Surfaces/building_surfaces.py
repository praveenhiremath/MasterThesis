# Author: Praveenkumar Hiremath, TU Bergakademie Freiberg, Sachsen, Germany (Postleitzahl: 09599). May, 2016. 

import os
import io
import ase
from ase.io import *
import pwtools
from pwtools.io import *
from ase.lattice.surface import *
from ase import Atoms

#Number of layers
layers=20
#(111) surface
bulk=bcc111('Fe',size=(4,4,layers),a=2.8665,vacuum=0.0,orthogonal=True)
#(100) surface
#bulk=bcc100('Fe',size=(4,4,layers),a=2.8665,vacuum=0.0)
#(110) surface
#bulk=bcc110('Fe',size=(4,4,layers),a=2.8665,vacuum=0.0,orthogonal=True)
write('ase_slab_111.cif',bulk)
with open('ase_bulk_111.cif','r') as file:
data=file.readlines()
with open('ase_bulk_111.cif','w') as file2:
file2.writelines(data)
temp=read_cif('ase_bulk_111.cif')
write_lammps('bcc_111.lmp',temp) 
