from Bio import AlignIO
import numpy as np
import sys
ip = sys.argv[1]
ss = sys.argv[2]

msa = AlignIO.read(ip, "fasta")

ssl = list(ss)
hamming = []
for rec in msa:
    dist = [s==r for s,r in zip(ssl, list(str(rec.seq)))]
    hamming.append(sum(dist))
    
high = np.argsort(hamming)[::-1]
top3 = [int(i) for i in high[:3]]
for x in top3:
    print(msa[x].seq)