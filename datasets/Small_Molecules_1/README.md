#  `Small_Molecules_1` dataset
This dataset contains electronic Hamiltonians of several small molecules with various configurations.

This dataset is used in the following competitions:
- [Calculating potential energy surface of ground states of small molecules](https://quantaggle.com/competitions/GS-PES)
- [Calculating excitation gaps of small molecules](https://quantaggle.com/competitions/ES-Gap)

## Details of dataset
### Molecules
This dataset contains electronic Hamiltonians of the following molecules:
- H<sub>2</sub>
- H<sub>4</sub> (line)
- H<sub>6</sub> (line)
- H<sub>4</sub> (ring)
- H<sub>6</sub> (ring)
- LiH
- BeH<sub>2</sub>
- H<sub>2</sub>O

Here, H<sub>n</sub> (line) denotes the molecule where n hydrogen atoms are aligned in line and have the same distance between each adjacent atom.
For H<sub>n</sub> (ring), n hydrogen atoms are placed on the circle with the same adjacent bond length.
The bond lengths of `Be-H` in BeH<sub>2</sub> are taken as the same and all atoms are aligned in line.
The angle of two `O-H` bond in H<sub>2</sub>O is taken as 104.5 degree and each bond length is taken as the same.

Therefore, the configurations of each molecule are specified by a single scaler (`bond_length`). We choose `bond_length` from 0.5 to 2.0 with spacing of 0.01 (unit is Angstrom). Also, we add a datum at the optimal `bond_length`, where the exact molecular energy calculated by the full configuration interactions is minimized, for each molecule.

### Dataformat
All data contained in `Small_Molecules_1` dataset are  `openfermion.hamiltonian.MolecularData` class of [OpenFermion](https://github.com/quantumlib/OpenFermion) in `.hdf5` format, which contain information on self-consistent field (SCF) molecular orbitals and their overlaps.
The data are constructed through `run_pyscf` function provided by [OpenFermion-PySCF](https://github.com/quantumlib/OpenFermion-PySCF).

The conditions for SCF calculations are
- basis set: sto-3g minimal basis set
- spin: singlet ($S^2=0$)
- charge: neutral (0)

### Filename convention
Data for each molecule are contained in `{MoleculeName}` directories, named as `{MoleculeName}_sto-3g_singlet_{bond_length}.hdf5`. 
`MolecularName` denotes the name of molecule, and `bond_length` denotes a distance between atoms in the unit of Angstrom (see "Molecules" section above for definition).
- For hydrogenic molecules, we set `MolecularName` = `H{n}_{line,ring}` where `n` is the number of H atoms and `{line,ring}` denotes the type of arrangement.
- For H<sub>2</sub>O molecule, we set `bond_length` = `{length1}_{angle}_{length2}` where `length1, length2` are two individual bond lengths of `H-O` and `angle` is an angle between two H-O bonds.

### Additional attributes in data
- `MolecularData.description`:  `MolecularName`
- `MolecularData.general_calculations` - a python dictionary having
  - key `bond_length`:  value=`bond_length` 
  - key `1st_excited_energy`: value = (1st excited state energy in the singlet sector ($S^2=0$) in Hartree calculated by the full configuration interactions)

### Usage
An example code to use the file in the dataset are following:
~~~python
from openfermion.hamiltonians import MolecularData
from openfermion.transforms import get_fermion_operator, jordan_wigner

molecular_data = MolecularData(filename="path/to/hdf5 file") # load hdf5 file
molecular_hamiltonian = get_fermion_operator(molecule_data.get_molecular_hamiltonian()) # get an instance of second quantized hamiltonian
jw_hamiltonian = jordan_wigner(molecular_hamiltonian) # get a Pauli operator representation of the hamiltonian
...
~~~