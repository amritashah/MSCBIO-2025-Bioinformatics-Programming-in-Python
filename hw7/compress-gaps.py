from Bio import AlignIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment

import numpy as np
import sys
ip = sys.argv[1]
op = sys.argv[2]

records = AlignIO.read(ip, "fasta")

arr = np.array([list(str(rec.seq)) for rec in records])

keep=[]
for c in range(arr.shape[1]):
    counter=0
    for r in range(arr.shape[0]):
        if arr[r,c]=='-':
            counter+=1
    if counter<0.67*arr.shape[0]:
        keep.append(c)

new_records=[]
for rec in records:
    new_seq = ''.join(rec.seq[i] for i in keep)
    new_item= SeqRecord(Seq(new_seq), id=rec.id, description=rec.description)
    new_records.append(new_item)

filtered_alignment = MultipleSeqAlignment(new_records)
AlignIO.write(filtered_alignment, op, "fasta")
