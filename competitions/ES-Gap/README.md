# Files for competition ["Calculating excitation gaps of small molecules"](https://quantaggle.com/competitions/ES-Gap)

## CSV file "competition_ES-Gap.csv"
This csv defines which data in `Small_Molecules_1` dataset to be calculated in the competition.
Each row corresponds to the data point whose the ground state energy needs to be calculated, and also contains information to calculate the score in the competition.

### Columns
- `dirname`: name of directory in which `.hdf5` file (`openfermion.hamiltonian.MolecularData`) exists
- `filename`: name of `.hdf5` file
- `molecule_name`: name of molecule
- `distance`: bond length of molecule (see [here](../../datasets/Small_Molecules_1/README.md) for definition)
- `fci_energy`: exact ground state energy calculated by the full configuration interaction
- `1st_excited_energy`: exact 1st excited state energy in the singlet (spin $S^2=0$) sector calculated by the full configuration interaction
- `qc_energy_0` (**empty**): ground state energy calculated by quantum algorithms/methods.
- `qc_energy_1` (**empty**): 1st excited state energy in the singlet (spin $S^2=0$) sector by quantum algorithms/methods.
- `nfev` (**empty**, optional): number of function evaluation. The definition varies for each algorithms/methods.

## How to use csv and join competition
Participants of the competition fill `qc_energy_0`, `qc_energy_1` columns and `nfev` (optional) column of the csv.
A Python script `process_competition_ES-Gap.py` in this directory processes the csv and generale the result summaries.
It will generate a figure of the potential energy surface and a detailed data table for each molecule. Moreover, it will create `summary_ES-Gap.csv` which summarizes results for all molecules and `record_ES-Gap.csv` which contains a one-line summary of the results.

For further information of the script, please see the docstring of it.