# similarity_cal
等位基因相似度计算
功能：
根据excel中等位基因的ID信息，读取一个包含等位基因的fasta文件，
调用biopython对等位基因的两条序列进行比对，并计算和输出其相似度到新的excel表中
## Usage
```
python similarity_cal.py -e 等位基因.xlsx -i input.pep -o output.xlsx
```
