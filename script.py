import sys

def validate_sequence(sequence, k):

    """
    Validate_sequence Function: 
    Validates that a DNA sequence
    - Is at least the length of k
    - Contains only A, C, G, T chars
    """

    # if the length of k-mer is too short, reject it
    if len(sequence) < k:
        return False
    
    #make sure it's a valid DNA character
    valid_chars = {'A', 'C', 'G', 'T'}

    # check each char in the sequence
    for nucleotide in sequence:
        if nucleotide not in valid_chars:
            return False
    return True

def update_kmer_count(kmer_data, kmer, next_char):

    """
    update_kmer_count Function:
    - Updates total count of kmer
    - Updated frequency of next character
    """

    # if the k-mer has't been recorded yet, initialize the record
    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 0, 'next_chars': {}}
    
    # increase total count for the k-mer
    kmer_data[kmer]['count'] += 1
    
    # track the char that follows current k-mer
    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0
    kmer_data[kmer]['next_chars'][next_char] += 1

    return kmer_data

def count_kmers_with_context(sequence, k):

    """
    count_kmers_with_context FUnction:
    This extracts all k-mers and tracks the character that follow.
    """

    kmer_data = {}
    
    for i in range(len(sequence) - k):
        #current k-mer
        kmer = sequence[i:i+k]

        # char after the k-mer
        next_char = sequence[i+k]
        
        # this updates the disctionary
        kmer_data = update_kmer_count(kmer_data, kmer, next_char)
    
    return kmer_data


def write_results_to_file(kmer_data, output_filename):

    """
    Write_results_to_file Function:
    this function writes the kmer total_count next_char:frequency
    """

    sorted_kmers = sorted(kmer_data.keys())
    
    # sorts the k-mers from A-Z
    with open(output_filename, 'w') as f:
        for kmer in sorted(kmer_data.keys()):
            total = kmer_data[kmer]['count']
            next_chars = kmer_data[kmer]['next_chars']
            
            next_char_str = " ".join(
                f"{char}:{freq}" 
                for char, freq in sorted(next_chars.items())
            )
            
            f.write(f"{kmer} {next_char_str}\n")


def main():

    """
    Main function:
    - Reads sequences from file
    - Aggregates kmer data
    - Writes results
    """

    sequence_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]

    # dictionary to hold sequences
    kmer_data = {}
    
    print(f"Reading sequences from {sequence_file}...")

    with open(sequence_file, 'r') as f:
        for sequence in f:
            sequence = sequence.strip()

            if not validate_sequence(sequence, k):
                print(f"  Warning: Skipping sequence")
                continue

            seq_data = count_kmers_with_context(sequence, k)

            # merge the results
            for kmer, data in seq_data.items():
                if kmer not in kmer_data:
                    kmer_data[kmer] = {'count': 0, 'next_chars': {}}

                # add counts
                kmer_data[kmer]['count'] += data['count']

                # Merge next character freqs
                for char, freq in data['next_chars'].items():
                    if char not in kmer_data[kmer]['next_chars']:
                        kmer_data[kmer]['next_chars'][char] = 0
                    kmer_data[kmer]['next_chars'][char] += freq
            
            # Final output
            write_results_to_file(kmer_data, output_file)

if __name__ == '__main__':
    main()
