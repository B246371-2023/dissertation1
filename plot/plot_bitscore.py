import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def read_data(primary_file, tertiary_file):
    # 读取一级序列比对数据
    primary_df = pd.read_csv(primary_file, sep='\t', header=None)
    primary_df.columns = ["qseqid", "sseqid", "pident", "length", "mismatch", "gapopen", "qstart", "qend", "sstart", "send", "evalue", "bitscore"]

    # 读取三级序列比对数据
    tertiary_df = pd.read_csv(tertiary_file, sep='\t', header=None)
    tertiary_df.columns = ["name1", "name2", "score", "pvalue"]

    return primary_df, tertiary_df

def preprocess_data(primary_df, tertiary_df):
    # 提取 qseqid 和 sseqid 中间的部分
    primary_df['qseqid'] = primary_df['qseqid'].str.split('|').str[1]
    primary_df['sseqid'] = primary_df['sseqid'].str.split('|').str[1]

    # 将列转换为字符串类型以确保匹配
    primary_df['qseqid'] = primary_df['qseqid'].astype(str)
    primary_df['sseqid'] = primary_df['sseqid'].astype(str)
    tertiary_df['name1'] = tertiary_df['name1'].astype(str)
    tertiary_df['name2'] = tertiary_df['name2'].astype(str)

    # 处理一级序列比对数据，只保留相似度（pident）和比对的序列对
    primary_similarity = primary_df[["qseqid", "sseqid", "bitscore"]]

    # 处理三级序列比对数据，只保留得分（score）和比对的序列对
    tertiary_similarity = tertiary_df[["name1", "name2", "score"]]

    # 修改 score 列的值
    tertiary_similarity["score"] = tertiary_similarity["score"] / 10

    # 合并一级和三级比对数据
    merged_df = pd.merge(primary_similarity, tertiary_similarity, left_on=["qseqid", "sseqid"], right_on=["name1", "name2"], how="outer")

    # 填充缺失值
    merged_df["bitscore"] = merged_df["bitscore"].fillna(0)
    merged_df["score"] = merged_df["score"].fillna(0)
    merged_df = merged_df[merged_df["score"] != 10]
    # merged_df = merged_df[merged_df["pident"] < 100]


    return merged_df

def plot_data(merged_df):
    # 绘制散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(merged_df["bitscore"], merged_df["score"], alpha=0.5)
    plt.xlabel('Primary bitscore')
    plt.ylabel('Tertiary raw Score')
    plt.title('Primary bit score vs Tertiary raw Score')
    plt.grid(True)

    # 保存图像为文件
    plt.savefig('primary_bitscore_vs_tertiary_score.png')
    print("Image saved as 'bitscore_vs_score.png'")

    # 显示图像
    plt.show()

def plot_specific(merged_df):
    # 模拟数据
    # np.random.seed(0)
    # merged_df = pd.DataFrame({
    #     "pident": np.random.uniform(0, 100, 100),
    #     "score": np.random.uniform(0, 1000, 100)
    # })

    # 添加趋势线
    z = np.polyfit(merged_df["bitscore"], merged_df["score"], 1)
    p = np.poly1d(z)

    plt.figure(figsize=(10, 6))
    plt.scatter(merged_df["bitscore"], merged_df["score"], alpha=0.6, label='bit core vs Score')
    plt.plot(merged_df["bitscore"], p(merged_df["bitscore"]), "r--", label='Trend line')

    # 高亮特定点
    highlight = merged_df[(merged_df["bitscore"] < 30) & (merged_df["score"] > 800)]
    plt.scatter(highlight["bitscore"], highlight["score"], color='red', s=50, edgecolor='k', label='Key Points')

    plt.xlabel('Primary bitscore')
    plt.ylabel('Tertiary raw Score')
    plt.title('Analysis of Primary vs Tertiary Comparisons')
    plt.grid(True)
    plt.legend()
    plt.savefig('enhanced_primary_bitscore_vs_tertiary_rarscore.png')
    print("Image saved as 'enhanced_primary_bitscore_vs_tertiary_rawscore.png'")
    plt.show()
    

def main():
    primary_alignment_file = 'primary_alignment.txt'
    tertiary_alignment_file = 'tertiary_alignment.txt'
    
    # 读取数据
    primary_df, tertiary_df = read_data(primary_alignment_file, tertiary_alignment_file)
    
    # 预处理数据
    merged_df = preprocess_data(primary_df, tertiary_df)
    
    # 绘制图表
    plot_data(merged_df)
    plot_specific(merged_df)

if __name__ == "__main__":
    main()
