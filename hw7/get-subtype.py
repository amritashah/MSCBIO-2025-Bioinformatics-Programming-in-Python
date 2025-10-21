from Bio import AlignIO
from collections import defaultdict
import numpy as np
import sys
ip = sys.argv[1]
ss = sys.argv[2]
ssl = list(ss)

msa = AlignIO.read(ip, "fasta")

groupedseqs = defaultdict(list)               # dictionary w lists as vals
for rec in msa:                               # for each record in msa
    subtype = (rec.id).split('.')[0]          # split each record id by . and take first item (subtype str)
    groupedseqs[subtype].append(rec)          # append that record to list under dictionary key for the subtype
    
mean_diffs = {}                              # empty dict

for subtype, records in groupedseqs.items():  # iter. thru subtypes, records in dict of subtype:records, where records is a list
    matches=[]                                # init. matches list
    for val in records:                       # for each record in the list
        m = [s==r for s,r in zip(ssl, list(str(val.seq)))]   # dist = list of booleans saying if each char in rec.seq is diff. from char in ss
        matches.append(sum(m))                # add dist for each seq under that subtype to distance list.
    mean_diffs[subtype] = np.mean(matches)    # calculate mean of the distances list: total dist across seqs/# of seqs
sortdiffs = sorted(mean_diffs.items(), key=lambda x: x[1], reverse=True) # sort the dict via index [1] of (subtype,mean) tuples, descending. 
                                              # key here is arg for the method of sorting, not dict key
print(sortdiffs[0][0])
