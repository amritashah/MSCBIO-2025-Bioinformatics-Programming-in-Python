from Bio import AlignIO
import sys
ip = sys.argv[1]
ss = sys.argv[2]

msa = AlignIO.read(ip, "fasta")
count = 0
for rec in msa:
    if rec.seq.find(ss) != -1:
        count+=1
print(count/len(msa))
    