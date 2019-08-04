# Files for competition ["Calculating potential energy surface of ground states of small molecules"](https://quantaggle.com/competitions/GS-PES)

## CSV file "competition_GS-PES.csv"
This csv defines which data in `Small_Molecules_1` dataset to be calculated in the competition.
Each row corresponds to the data point whose the ground state energy needs to be calculated, and also contains information to calculate the score in the competition.

### Columns
- `dirname`: name of directory in which `.hdf5` file (`openfermion.hamiltonian.MolecularData`) exists
- `filename`: name of `.hdf5` file
- `molecule_name`: name of molecule
- `distance`: bond length of molecule (see [here](../../datasets/Small_Molecules_1/README.md) for definition)
- `fci_energy`: exact ground state energy calculated by the full configuration interaction
- `1st_excited_energy`: exact 1st excited state energy in the singlet (spin $S^2=0$) sector calculated by the full configuration interaction
- `bond_length_opt`: optimal bond length in which `fci_energy` takes minimum (4 digits accuracy after the decimal point). This value is common among data points for the same molecule. 
- `fci_energy_lowest`: ground state energy at `bond_length_opt`.
- `qc_energy` (**empty**): ground state energy calculated by quantum algorithms/methods.
- `nfev` (**empty**, optional): number of function evaluation. The definition varies for each algorithms/methods.

## How to use csv and join competition
Participants of the competition fill `qc_energy` columns and `nfev` (optional) of the csv.
A Python script `process_competition_GS_PES.py` in this directory processes the csv and generale the result summaries.
It will generate a figure of the potential energy surface and a detailed data table for each molecule. Moreover, it will create `summary_GS-PES.csv` which summarizes results for all molecules and `record_GS-PES.csv` which contains a one-line summary of the results.

For further information of the script, please see the docstring of it.