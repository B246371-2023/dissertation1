def read_sequences(filename):
    with open(filename, 'r') as file:
        sequences = [line.strip() for line in file.readlines()]
    return sequences

def write_pairs(sequences, output_filename):
    with open(output_filename, 'w') as file:
        for seq1 in sequences:
            for seq2 in sequences:
                file.write(f"{seq1} {seq2}\n")

def main():
    input_filename = 'short_sequences.fasta'
    output_filename = 'short_sequences_pairs.txt'
    sequences = read_sequences(input_filename)
    write_pairs(sequences, output_filename)

if __name__ == "__main__":
    main()

