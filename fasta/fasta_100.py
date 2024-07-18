from Bio import SeqIO
import pandas as pd

def parse_fasta(file_path):
    """解析 FASTA 文件并分类序列长度"""
    short_seqs = []
    long_seqs = []
    
    for record in SeqIO.parse(file_path, "fasta"):
        sequence_id = record.id.split('|')[1]  # 提取序列号，假设序列号总是在第二个位置
        sequence_length = len(record.seq)
        
        if sequence_length < 100:
            short_seqs.append(sequence_id)
        else:
            long_seqs.append(sequence_id)
    
    return pd.DataFrame(short_seqs, columns=["Sequence ID"]), pd.DataFrame(long_seqs, columns=["Sequence ID"])

# 调用函数并读取文件
df_short, df_long = parse_fasta("ruddii_proteome.fasta")



