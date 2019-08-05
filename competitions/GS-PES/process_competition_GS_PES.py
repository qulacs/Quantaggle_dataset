import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
from datetime import date

def process_competition_GS_PES_csv(dirname, filename, methodname = None, authorname=None, datestr=None):
    """
    Process `competition_GS-PES.csv` for competition "https://quantaggle.com/competitions/GS-PES"
    Detailed definition of problems and score is given there.

    Args:
        dirname (str): directory name where the csv file exists.
        filename (str): file name of csv within the directory.
                        path for file become "{dirname}/{filename}.csv".
        methodname (str): name for method. if none, set to dirname. 
        authorname (str): name of authors. if None, set to "NA".
        datestr (str): string of datetime. if None, set to today's date (yyyy-mm-dd).
    Returns:
        None
    Outputs:
        "(molnames)_GS-PES.png": PES for each molecule.
        "(molnames)_GS-PES.csv": extracted results for each molecule.
        "summary.csv"   : summarized result for all data.
        "records.csv"   : overall score, author, date, etc.

    """
    if methodname is None: methodname = dirname
    if authorname is None: authorname = "NA"
    if datestr    is None: datestr =  str(date.today())


    ## list for molname and associate dictionary for each molecule.
    ## You can set molecule-dependent options or parameters by using dictionary.
    molname_and_dict_list = [\
    ("H2line", dict()), \
    ("H4line", dict()), \
    ("H4ring", dict()), \
    ("H6line", dict()), \
    ("H6ring", dict()), \
    ("LiH",    dict()), \
    ("BeH2",   dict()), \
    ("H2O",    dict()), \
    ]

    ## bond_length for this competition, common for all molecules.
    length_list = np.linspace(0.5, 2, 15+1)

    filepath = dirname + "/" +  filename + ".csv"
    df_allresult = pd.read_csv(filepath)
    score_mean_list = []
    nfev_mean_list = []

    for ind in range(len(molname_and_dict_list)):
        molname, dictionary = molname_and_dict_list[ind]
        print(molname)

        ## extract data for each molecule
        df_mol = df_allresult[ df_allresult["molecule_name"] == molname ].copy()

        ## determin a shift, defined as E_{QC}(R_FCIopt) - E_{FCI}(R_FCIopt) 
        bond_length_opt = df_mol["bond_length_opt"].iloc[0]
        fci_energy_lowest = df_mol["fci_energy_lowest"].iloc[0]
        qc_energy_R_fciopt = df_mol[ df_mol["distance"] == bond_length_opt ]["qc_energy"].iloc[0]
        delta_m = qc_energy_R_fciopt - fci_energy_lowest

        ## removing row of bond_length_opt
        rowIndex_to_drop = df_mol.index[ df_mol["distance"] == bond_length_opt ]
        df_mol = df_mol.drop(rowIndex_to_drop)

        ## calculate score at each distance
        score_at_each_distance = ( (df_mol["qc_energy"] - delta_m) - df_mol["fci_energy"] ) / (df_mol["fci_energy"] - fci_energy_lowest)
        score_at_each_distance = np.abs(score_at_each_distance)
        score_mean_list.append( score_at_each_distance.mean() )

        ## calculte nfev_mean
        nfev_mean_list.append( np.mean(df_mol["nfev"]) )

        ## create output csv
        df_mol_output = df_mol[ ["distance", "fci_energy", "qc_energy"] ].copy()
        df_mol_output["score_at_each_distance"] = score_at_each_distance.copy() # columns are added
        df_mol_output["num_of_func_eval"] = df_mol["nfev"].copy()
        df_mol_output.to_csv(f"{dirname}/{molname}_GS-PES.csv", index=False)

        ## plot result for each molecule
        plt.rc('xtick',labelsize=12)
        plt.rc('ytick',labelsize=12)

        plt.plot(df_mol_output["distance"], df_mol_output["qc_energy"],  "o", color="orange", label="QC")
        plt.plot(df_mol_output["distance"], df_mol_output["fci_energy"], "-", color="blue", label="FCI")
        
        plt.xlabel("bond length [Angstrom]", fontsize=14)
        plt.title(f"{molname}, energy [Hartree]", fontsize=14)

        plt.savefig(f"{dirname}/{molname}_GS-PES.png")
        plt.close()

    ## calculate final score
    final_score = np.mean(score_mean_list)

    ## calculate nfev_mean
    nfev_mean = np.mean(nfev_mean_list)

    ## create summary.csv
    df_summary = pd.DataFrame(columns = ["molecule_name", "score_mean", "num_of_func_eval_mean"])
    df_summary["molecule_name"] = [x[0] for x in molname_and_dict_list]
    df_summary["score_mean"] = score_mean_list
    df_summary["num_of_func_eval_mean"] = nfev_mean_list
    ## add "all" row
    df_summary = df_summary.append({"molecule_name": "all", "score_mean": final_score, "num_of_func_eval_mean": nfev_mean}, ignore_index=True)
    ## save csv
    df_summary.to_csv(f"{dirname}/summary_GS-PES.csv", index=False)

    ## create record.csv
    df_record = pd.DataFrame(columns = ["author", "method", "score", "num_of_func_eval_mean", "date"])
    df_record = df_record.append( {"author": authorname, "method": methodname,  "score": final_score, "num_of_func_eval_mean":nfev_mean, "date":datestr}, ignore_index=True)
    df_record.to_csv(f"{dirname}/record_GS-PES.csv", index=False)    

if __name__ == '__main__':
    dirname = "sample"
    filename = "result_sample"
    process_competition_GS_PES_csv(dirname, filename)
