#yeast_load_erc_output.py this script prepares two ERC tables for 
#comparison in  was used to compare tables of ERC values
# (compare to Nathan Clarks ERC values online)

import pandas as pd
import itertools
import csv

points_new = [["new_data"]]
points_old = [["old_data"]]

yeast_file = 'erc_yeast_all.tsv'
old_yeast_file = 'web_erc.tsv'
old_yeast_file = 'erc_yeast.tsv'

#import erc tables 
yeast_frame = pd.read_csv(yeast_file, index_col = False, na_values = [1.00, 0] , sep = '\t')
yeast_frame = yeast_frame.set_index(yeast_frame.columns)
old_yeast_frame = pd.read_csv(old_yeast_file, index_col = False, na_values = 1.00, sep = '\t', skip_blank_lines = False)
old_yeast_frame = old_yeast_frame.set_index(old_yeast_frame.columns)
combs_new = itertools.combinations(yeast_frame.columns, 2)
combs_old = itertools.combinations(old_yeast_frame.columns, 2)

for comb in combs_new:
    points_new.append([yeast_frame[comb[0]][comb[1]]])

with open('yeast_points_new_all.csv', 'wb') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(points_new)


for comb in combs_old:
    points_old.append([ old_yeast_frame[comb[0]][comb[1]]])

with open('yeast_points_old.csv', 'wb') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(points_old)

points_new = ["new_data"]
points_old = ["old_data"]

combs_new = itertools.combinations(yeast_frame.columns, 2)
combs_old = itertools.combinations(old_yeast_frame.columns, 2)
set1 = set(combs_new)
set2 = set(combs_old)
prev = 0

combs_intersect_set = set1 & set2
combs_intersect = list(combs_intersect_set)


#taking the set of proteins shared between the old and new data
#pair the erc values from the same protein together
for comb in combs_intersect:
    points_new.append(yeast_frame[comb[0]][comb[1]])
    points_old.append(old_yeast_frame[comb[0]][comb[1]])

points = zip(points_new, points_old)
labeled_points = zip(combs_intersect, points)

with open('yeast_points_all_labeled_13.csv', 'wb') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(labeled_points)
    
with open('yeast_points_all_13.csv', 'wb') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(points)      
zeros = 0
points_no_zeros = []
for ii, (new, old) in enumerate(points):
    
    if ii == 0:
        points_no_zeros.append((new, old))
        continue
        
    if (old != 0 and np.isnan(old) == False 
        and new != 0 and np.isnan(new) == False):
        zeros += 1
        points_no_zeros.append((new, old))
        
print "zeros: %d" % zeros
with open('yeast_points_no_zeros.csv', 'wb') as f_out:
    writer = csv.writer(f_out)
    writer.writerows(points_no_zeros)
#        
