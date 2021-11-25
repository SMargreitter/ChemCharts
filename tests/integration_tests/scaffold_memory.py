import pandas as pd

# load data and generate an object for each molecule
from chemcharts.core.container.chemdata import ChemData
from chemcharts.utils.dimensional_reduction import calculate_embedding
from chemcharts.utils.fp_utils import add_fingerprints
from chemcharts.core.container.smiles import FingerprintContainer
from chemcharts.utils.plot_generating import generate_chemcharts_scatter_plot

loaded_data = pd.read_csv("../../data/DEKOIS2_Dataset_selected.csv")
COX2_smiles = list(loaded_data['Actives'].dropna())+list(loaded_data['Inactives'])
ERBB2_smiles = list(loaded_data['Actives.1'].dropna())+list(loaded_data['Inactives.1'])
QPCT_smiles = list(loaded_data['Actives.2'].dropna())+list(loaded_data['Inactives.2'])

# make list of booleans (actives and inactives resp.)
active_inactive_list = [True] * 40 + [False] * 1200

# generate an instance of the data_set class and set to COX2_set variable
COX2_set = ChemData(name="COX2", active_inactive_list=active_inactive_list, smiles_obj=FingerprintContainer(COX2_smiles))
ERBB2_set = ChemData(name="ERBB2", active_inactive_list=active_inactive_list, smiles_obj=FingerprintContainer(ERBB2_smiles))
QPCT_set = ChemData(name="QPCT", active_inactive_list=active_inactive_list, smiles_obj=FingerprintContainer(QPCT_smiles))
#print(COX2_set.smiles_obj.smiles_list)

# call function to add fingerprints to instances of data_set class
add_fingerprints(COX2_set)
add_fingerprints(ERBB2_set)
add_fingerprints(QPCT_set)

# call function to add embedding to instances of data_set class
calculate_embedding(COX2_set)
calculate_embedding(ERBB2_set)
calculate_embedding(QPCT_set)

# call function to generate scatter plot
data_sets = [COX2_set, ERBB2_set, QPCT_set]

# choose scatter_plot_type: "single_scatterplots" or "concatenated_scatterplots"
chemchar_scatter_plot = generate_chemcharts_scatter_plot(data_sets=data_sets,
                                                         path="../junk/",
                                                         scatter_plot_type="concatenated_scatterplots")

#print(len(chemchar_dic["fingerprints"]))