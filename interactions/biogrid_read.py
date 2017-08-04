# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 02:26:19 2017

@author: Brandon Jernigan

biogrid_read.py used to identify interacting proteins and compare their ERC values

"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

MIN_PUBLICATION_NUM = 6

#import biogrid interaction database
df_biogrid = pd.read_csv("BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-3.4.146.tab2.txt", index_col = False, sep = '\t')
df_e = pd.read_csv('yeast_protein_erc_values.tsv', index_col = False, na_values = [1.00, 0] , sep = '\t')
df_e = df_e.set_index(df_e.columns)

df_hist = np.asarray(df_e).flatten()
df_hist = df_hist[~np.isnan(df_hist)]
df_choices = np.random.choice(df_hist, 1000).tolist()

#choose experiment types to select out of database
df_biogrid_acms = df_biogrid[df_biogrid["Experimental System"].isin(["Affinity Capture-MS"])]

   
intact_dict = {}
ID_dict = {}

#for those proteins that interact, what is the erc value between them?
for index, row in df_biogrid_acms.iterrows():
    if index % 1000 == 0:
        print(index)
    sym_A = row["Official Symbol Interactor A"]
    sym_B = row["Official Symbol Interactor B"]
    ID = row["Pubmed ID"]
    try:
        if ~np.isnan(df_e.loc[sym_A, sym_B]):
            intact_dict["%s %s" % (sym_A, sym_B)] = df_e.loc[sym_A, sym_B]
            
            if "%s %s" % (sym_A, sym_B) in ID_dict:
                ID_dict["%s %s" % (sym_A, sym_B)] = ID_dict["%s %s" % (sym_A, sym_B)] + 1
            else:
                ID_dict["%s %s" % (sym_A, sym_B)] = 1
        elif ~np.isnan(df_e.loc[sym_B, sym_A]):
            intact_dict["%s %s" % (sym_B, sym_A)] = df_e.loc[sym_B, sym_A]
            
            if "%s %s" % (sym_B, sym_A) in ID_dict:
                ID_dict["%s %s" % (sym_B, sym_A)] = ID_dict["%s %s" % (sym_B, sym_A)] + 1
            else:
                ID_dict["%s %s" % (sym_B, sym_A)] = 1

    except Exception:
        pass
    
intact_more_dict ={}

for key, item in ID_dict.items():
    if item >= MIN_PUBLICATION_NUM:
        intact_more_dict[key] = intact_dict[key]

#plots to see how ERC value changes with interacting proteins
list_values = [ v for v in intact_more_dict.values() ]
int_choices = np.random.choice(list_values, 1000)
plt.hist(df_choices)
plt.title("All ERC\n Mean = %.4f" % np.mean(df_choices))
plt.show()
print("ERC mean for all: %.4f" % np.mean(df_choices))
plt.hist(int_choices)
plt.title("Interacting ERC\n Mean = %.4f" % np.mean(int_choices))
plt.show()
print("ERC mean for interacting: %.4f" % np.mean(int_choices))

sm.qqplot_2samples(np.asarray(df_choices), np.asarray(int_choices),xlabel="All ERC", ylabel="Interacting ERC")
plt.plot()
plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.plot( [-1,1],[-1,1] , 'r')
plt.gca().set_aspect('equal', adjustable='box')
plt.draw()


df_biogrid_acms.to_csv("ACMS_BIOGRID-ORGANISM-Saccharomyces_cerevisiae_S288c-3.4.146.tab2.txt", sep = '\t')
