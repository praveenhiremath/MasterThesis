# Author: Praveenkumar Hiremath, TU Bergakademie Freiberg, Sachsen, Germany (Postleitzahl: 09599). May, 2016. 
# This script collects output data from elk runs and converts it to input configuration file format of potfit package.

import os
import sys
import numpy as np
from pathlib import Path

f_in = open('INFO.OUT','r')
info_file_data = f_in.readlines()
f_in.close()

search_species = 'Species :    '

search_vectors = 'Lattice vectors :'

search_scf_status = '| Self-consistent loop stopped |'

search_forces = 'Forces :'

search_atom_forces = '   total force               :'

search_num_atoms = 'Total number of atoms per unit cell :'

search_energies = ' total energy                :'

search = 'Convergence targets achieved'

search_atomic_positions = ' atomic positions (lattice), magnetic fields (Cartesian) :'

config_weight = 10#int(input("Enter config weight\n"))
num_species = 0
type_species = 0
vectors = np.zeros([3,3])
forces = []
position = []
num_atoms = 0
tot_energy = []
for k, line in enumerate(info_file_data):
  with open('inputs_for_potfit_config.dat','a') as out1:

    if line.startswith(search_species):
        species=info_file_data[k]
        num_species = int(species.split()[2])
        type_species = species.split()[3].replace('(','').replace(')','')
        out1.write(str(num_species))
        out1.write("\n")
        out1.write(str(type_species))
        out1.write("\n")

    if line.startswith(search_vectors):
        vec1, vec2, vec3 = info_file_data[k+1], info_file_data[k+2], info_file_data[k+3]
        #print (vec1, vec2, vec3)
        vec1_x, vec1_y, vec1_z = float(vec1.split()[0]), float(vec1.split()[1]), float(vec1.split()[2])
        vec2_x, vec2_y, vec2_z = float(vec2.split()[0]), float(vec2.split()[1]), float(vec2.split()[2])
        vec3_x, vec3_y, vec3_z = float(vec3.split()[0]), float(vec3.split()[1]), float(vec3.split()[2])
        vectors = np.array([["{:.10f}".format(vec1_x),"{:.10f}".format(vec1_y),"{:.10f}".format(vec1_z)],["{:.10f}".format(vec2_x),"{:.10f}".format(vec2_y),"{:.10f}".format(vec2_z)],["{:.10f}".format(vec3_x),"{:.10f}".format(vec3_y),"{:.10f}".format(vec3_z)]])
        out1.write("Lattice vectors:")
        out1.write("\n")
        out1.write(str(vectors[0,:]).replace("'",''))
        out1.write("\n")
        out1.write(str(vectors[1,:]).replace("'",''))
        out1.write("\n")
        out1.write(str(vectors[2,:]).replace("'",''))
        out1.write("\n")

    if line.startswith(search_atom_forces):
        forces.append(info_file_data[k].split()[3]+'    '+info_file_data[k].split()[4]+'    '+info_file_data[k].split()[5])
        out1.write(info_file_data[k].split()[3]+'    '+info_file_data[k].split()[4]+'    '+info_file_data[k].split()[5])
        out1.write("\n")


    if line.startswith(search_num_atoms):
        num_atoms = int(info_file_data[k].split()[8])
        print (num_atoms)
        for i in range(1,num_atoms+1,1):
            position.append(info_file_data[k-2-(num_atoms)+i].split()[2]+'   '+info_file_data[k-2-(num_atoms)+i].split()[3]+'   '+info_file_data[k-2-(num_atoms)+i].split()[4])

    if line.startswith(search_energies):
        tot_energy.append(info_file_data[k].split()[3])
        #print (np.asarray(tot_energy))



print (num_atoms)
print (position[0])
print (tot_energy[len(tot_energy)-1])

position_forces = []
for i in range(0,num_atoms,1):
    position_forces.append('0 \t'+str("{:.10f}".format(np.multiply(float(position[i].split()[0]),np.linalg.norm(vectors[0,:]))))+' \t'+str("{:.10f}".format(np.multiply(float(position[i].split()[1]),np.linalg.norm(vectors[1,:]))))+' \t'+str("{:.10f}".format(np.multiply(float(position[i].split()[2]),np.linalg.norm(vectors[2,:]))))+' \t'+forces[i]+'\n')


#    position_forces.append('0 \t'+str("{:.10f}".format(np.multiply(float(position[i].split()[0]),np.linalg.norm(vectors[0,:]))).replace("'",''))+' \t'+str("{:.10f}".format(np.multiply(float(position[i].split()[1]),np.linalg.norm(vectors[1,:]))))+' \t'+str("{:.10f}".format(np.multiply(float(position[i].split()[2]),np.linalg.norm(vectors[2,:]))))+' \t'+forces[i]+'\n')


#    position_forces.append('0 \t'+str(np.multiply(float(position[i].split()[0]),np.linalg.norm(vectors[0,:])))+' \t'+str(np.multiply(float(position[i].split()[1]),np.linalg.norm(vectors[1,:])))+' \t'+str(np.multiply(float(position[i].split()[2]),np.linalg.norm(vectors[2,:])))+' \t'+forces[i]+'\n')

#path_info_file = 

f_out = open('potfit.config','w')
f_out.write('#N '+str(num_atoms)+' '+str(num_species))
f_out.write('\n')
f_out.write('#C '+str(type_species))
f_out.write('\n')
f_out.write('#X '+str(vectors[0,:]).replace("[",'').replace("]",''))
f_out.write('\n')
f_out.write('#Y '+str(vectors[1,:]).replace("[",'').replace("]",''))
f_out.write('\n')
f_out.write('#Z '+str(vectors[2,:]).replace("[",'').replace("]",''))
f_out.write('\n')
f_out.write('#W '+str(config_weight))
f_out.write('\n')
f_out.write('#E '+str(np.multiply(np.divide(float(tot_energy[len(tot_energy)-1]),num_atoms),27.2114)))
f_out.write('\n')
f_out.write('##S ')
f_out.write('\n')
f_out.write('#F \n')
for i in range(0,num_atoms,1):
    f_out.write(position_forces[i])
