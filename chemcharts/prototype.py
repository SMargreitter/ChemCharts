from typing import Any, Union

import pandas
import umap
import rdkit

########################################################
############   FUNCTION DEFINITION  ####################
########################################################

# def transform_smile_strings_to_bit_vectors(parameter1: str) => list:
#   """I am transforming smile strings to bit vectors by using the XXX rd kit function.
#    input:
#       smile strings -- every smile encodes one molecule, the characters represent chemical elements
#    output:
#       bit vectors -- lists with 0 and 1 or numbers
#    """

# LOAD FROM PANDAS
#from pandas import Series, DataFrame
#from pandas.io.parsers import TextFileReader --

# Whatever: Union[Union[TextFileReader, Series, DataFrame, None], Any] = pandas.read_csv("hrdata.csf")
# print(Whatever)
#    return Whatever


# WRITE OUT FROM PANDAS
# whatever.to_csv("filename")


#testdata:
# 3 groups with two categories each and multiple molecules in it
# header looks like: COX2,Actives,Inactives,,ERBB2,Actives,Inactives,,QPCT,Actives,Inactives


#####################################################################################################


# def bit_vectors_reduced_to_two_floats_per_molecule():
#    """I doing a dimensionally reduction of bit vectors into vectors with 2 float dimensions each
#    by using the umap algorithm XXX.
#   input:
#       bit vectors -- lists with 0 and 1 or numbers
#   output:
#       vectors -- 2 float dimensions
#   """


##############################################################################################


# def generate_graph_dimensional_reduction():    
# """I am generating a graph to visualize the 2 dimensions of a vector by using matplotlib.
# input:
# vectors -- 2 float dimensions
# output:
# graph -- by matplotlib
# """


########################################################
############   FUNCTION CALLS  #########################
########################################################