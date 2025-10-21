from Bio import AlignIO
from collections import Counter
import sys
ip = sys.argv[1]

msa = AlignIO.read(ip, "fasta")
con_chars = []
for i in range(msa.get_alignment_length()):
    col = [rec.seq[i] for rec in msa]
    counts = Counter(col)
    con_res = counts.most_common(1)[0][0]
    con_chars.append(con_res)

consensus_sequence = ''.join(con_chars)
print(consensus_sequence)