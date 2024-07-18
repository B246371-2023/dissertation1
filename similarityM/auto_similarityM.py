import pandas as pd
import numpy as np
import subprocess

def inspect_file(file_path):
    """Prints the first few lines of the file to inspect its format and headers"""
    with open(file_path, 'r') as file:
        for _ in range(5):
            print(file.readline())


def read_and_prepare_data(file_path):
    """Reads the P-value data and prepares the unique protein list from 'name1'."""
    df = pd.read_csv(file_path, comment='#', sep='\s+', usecols=[0, 1, 2, 3], header=None,
                     names=['name1', 'name2', 'score', 'probability'])
    
    # for sure the data frame
    print("DataFrame Head:\n", df.head())
    print("DataFrame Columns:", df.columns)

    # Remove any potential NaN values in 'name1' just in case
    df = df.dropna(subset=['name1'])
    # Extract unique proteins from 'name1'
    proteins = df['name1'].unique()
    return df, proteins

def initialize_similarity_matrix(proteins):
    """Initializes a square similarity matrix with 0 values."""
    size = len(proteins)
    sim_matrix = np.zeros((size, size))
    return sim_matrix

def fill_similarity_matrix_score(sim_matrix, proteins, df):
    """Fills the similarity matrix with score values using only 'name1'."""
    protein_index = {protein: idx for idx, protein in enumerate(proteins)}
    for _, row in df.iterrows():
        if row['name1'] in protein_index:
            idx1 = protein_index[row['name1']]
            # Only fill the matrix if 'name2' also exists in the index
            if row['name2'] in protein_index:
                idx2 = protein_index[row['name2']]
                sim_matrix[idx1, idx2] = row['score']
                sim_matrix[idx2, idx1] = row['score']  
    np.fill_diagonal(sim_matrix, 0)  # Diagonal elements are 0 (self-similarity)
    sim_matrix_score = sim_matrix
    return sim_matrix_score

def fill_similarity_matrix_p_value(sim_matrix, proteins, df):
    """Fills the similarity matrix with p-value values using only 'name1'."""
    protein_index = {protein: idx for idx, protein in enumerate(proteins)}
    for _, row in df.iterrows():
        if row['name1'] in protein_index:
            idx1 = protein_index[row['name1']]
            # Only fill the matrix if 'name2' also exists in the index
            if row['name2'] in protein_index:
                idx2 = protein_index[row['name2']]
                sim_matrix[idx1, idx2] = row['probability']
                sim_matrix[idx2, idx1] = row['probability']  
    np.fill_diagonal(sim_matrix, 0)  # Diagonal elements are 0 (self-similarity)
    sim_matrix_p_value = sim_matrix
    return sim_matrix_p_value

def format_and_save_matrix(sim_matrix, proteins, file_path):
    """Formats the similarity matrix and saves it to a file."""
    with open(file_path, 'w') as file:
        # Write the number of proteins
        file.write(f"{len(proteins):>4}\n")
        for i, protein in enumerate(proteins):
            formatted_name = f"{protein:<12}"
            values = '  '.join(f"{value:.12f}" for value in sim_matrix[i])
            file.write(f"{formatted_name}{values}\n")

def main():
    file_path = '/home/s2530615/dissertation/similarityM/db.txt'  #edit the file path by yourself
    
    # Read data and prepare protein list
    df, proteins = read_and_prepare_data(file_path)
    
    # Initialize and fill the similarity matrix
    sim_matrix = initialize_similarity_matrix(proteins)
    sim_matrix_score = fill_similarity_matrix_score(sim_matrix, proteins, df)
    sim_matrix = initialize_similarity_matrix(proteins)
    sim_matrix_p_value = fill_similarity_matrix_p_value(sim_matrix, proteins, df)
    
    # Save the formatted similarity matrix to a file
    format_and_save_matrix(sim_matrix_score, proteins, 'similarityM_rmsd_score.txt')
    format_and_save_matrix(sim_matrix_p_value, proteins, 'similarityM_rmsd_p_value.txt')
# Run the main function
if __name__ == "__main__":
    main()

