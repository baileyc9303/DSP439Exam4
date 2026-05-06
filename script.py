import sys

def validate_sequence(sequence, k):
    if len(sequence) < k:
        return False
    valid_chars = {'A', 'C', 'G', 'T'}
    for nucleotide in sequence:
        if nucleotide not in valid_chars:
            return False
    return True

def update_kmer_count(kmer_data, kmer, next_char):
    if kmer not in kmer_data:
        kmer_data[kmer] = {'count': 0, 'next_chars': {}}
    
    kmer_data[kmer]['count'] += 1
    
    if next_char not in kmer_data[kmer]['next_chars']:
        kmer_data[kmer]['next_chars'][next_char] = 0
    kmer_data[kmer]['next_chars'][next_char] += 1

    return kmer_data

def count_kmers_with_context(sequence, k):
    kmer_data = {}
    
    for i in range(len(sequence) - k):
        kmer = sequence[i:i+k]
        next_char = sequence[i+k]
        
        kmer_data = update_kmer_count(kmer_data, kmer, next_char)
    
    return kmer_data


def write_results_to_file(kmer_data, output_filename):
    sorted_kmers = sorted(kmer_data.keys())
    
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
    sequence_file = sys.argv[1]
    k = int(sys.argv[2])
    output_file = sys.argv[3]

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

                kmer_data[kmer]['count'] += data['count']

                for char, freq in data['next_chars'].items():
                    if char not in kmer_data[kmer]['next_chars']:
                        kmer_data[kmer]['next_chars'][char] = 0
                    kmer_data[kmer]['next_chars'][char] += freq
            
            kmer_data = count_kmers_with_context(sequence, k) 
            
            write_results_to_file(kmer_data, output_file)

if __name__ == '__main__':
    main()
