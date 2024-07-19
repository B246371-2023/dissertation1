import os
import gzip
from pymol import cmd

# 初始化 PyMOL
cmd.reinitialize()

def process_file(cif_gz_path, output_directory):
    # 解压 .cif.gz 文件
    with gzip.open(cif_gz_path, 'rb') as f:
        cif_data = f.read()

    cif_path = cif_gz_path[:-3]  # 移除 .gz 扩展名
    with open(cif_path, 'wb') as f:
        f.write(cif_data)

    # 加载解压后的 CIF 文件到 PyMOL
    cmd.load(cif_path, "molecule")

    # 保存为 PDB 文件
    pdb_path = os.path.join(output_directory, os.path.basename(cif_path).replace('.cif', '.pdb'))
    cmd.save(pdb_path, "molecule")

    # 清除 PyMOL 中的分子数据
    cmd.delete("molecule")

    # 删除解压后的临时 CIF 文件
    os.remove(cif_path)

def walk_and_process(input_directory, output_directory):
    # 确保输出文件夹存在
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # 遍历目录
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".cif.gz"):
                cif_gz_path = os.path.join(root, file)
                process_file(cif_gz_path, output_directory)

# 定义输入和输出路径
input_directory = "/home/s2530615/dissertation/biojava-protein-comparison-tool-4.0.0/PDBs/data/structures/divided/mmCIF"
output_directory = "/home/s2530615/dissertation/biojava-protein-comparison-tool-4.0.0/PDBs/"

# 执行处理函数
walk_and_process(input_directory, output_directory)

# 结束 PyMOL 会话
cmd.quit()
