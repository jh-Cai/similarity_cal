"""
功能：
根据excel中等位基因的ID信息，读取一个包含等位基因的fasta文件，
调用biopython对等位基因的两条序列进行比对，并计算和输出其相似度到新的excel表中
用法示例：
python similarity_cal.py -e 等位基因.xlsx -i HAB_allel.pep -o output.xlsx
python similarity_cal.py -e 等位基因.xlsx -i HAB_allel.cds -o cdsoutput.xlsx
-cjh 2023.8.30
"""
from Bio import SeqIO
from Bio.Align import PairwiseAligner
import pandas as pd
from argparse import ArgumentParser

arg = ArgumentParser(description='Description - SCAU Bio_Lab')
arg.add_argument("-e",
                 "--excel",
                 help="input excel file path")
arg.add_argument("-i",
                 "--input",
                 help="input pep or cds file path")
arg.add_argument("-o",
                 "--output",
                 help="output file path")
args = arg.parse_args()

excel_file = args.excel
fasta_file = args.input
output_file = args.output

if excel_file == None or fasta_file == None :
    exit('[error!] - Missing core parameter！\n Please use [ -h] to get help information!')

# 读取fasta文件
def read_fasta(fasta_file):
    seq = {}
    for record in SeqIO.parse(fasta_file,"fasta"):
        seq[record.id] = str(record.seq)
    return seq

# 定义相似度计算公式
def calculate_similarity(seq1,seq2):
    aligner = PairwiseAligner()
    alignments = aligner.align(seq1, seq2)
    score = alignments.score
    similarity = score / max(len(seq1), len(seq2))
    return similarity

def calculate_similarity_from_excel(excel_file,fasta_file,output_file):
    data = pd.read_excel(excel_file,header=None) # header =None 不将第一行作为列名
    seq = read_fasta(fasta_file)
    # 创建空列表
    results = []
    # i 是每一行的索引，row 是每一行的数据,for循环读取excel中每一行的数据
    for i,row in data.iterrows():
        gene1 = row[0]
        gene2 = row[1]
        seq1 = seq.get(gene1)
        seq2 = seq.get(gene2)

        if seq1 and seq2:
            similarity = calculate_similarity(seq1,seq2)
            results.append([gene1,gene2,similarity])
    # 写入数据
    result_df = pd.DataFrame(results,columns=["Gene1","Gene2","similarity"])
    result_df.to_excel(output_file,index=False)
# 调用函数
calculate_similarity_from_excel(excel_file,fasta_file,output_file)

print("[SUCCESS]")


