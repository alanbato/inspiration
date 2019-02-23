from collections import Counter
from pathlib import Path

def get_k_grams(sequence, K=3):
    K = min(len(sequence), K)
    grams = []
    for k in range(1, K):
        grams.extend((tuple(sequence[i:i+k+1]) for i in range(len(sequence) - k)))
    return grams

def T_union(k_grams):
    union = set()
    for grams in k_grams:
        union |= set(grams)
    return sorted(list(union))

def get_frequency(grams, universe):
    counts = Counter(grams)
    freqs = [counts[gram] for gram in universe]
    return freqs

def main(songs):
    print('Songs:')
    print(songs)
    k_grams = [get_k_grams(song) for song in songs]
    union = T_union(k_grams)
    print('Union:')
    print(*union)
    songs_in_freqs = [
        get_frequency(grams, union)
        for grams in k_grams
    ]
    print('Freq Matrix')
    for song in songs_in_freqs:
        print(song)
    


if __name__ == '__main__':
    samples = []
    with open(Path('data') / 'Top10MostCommonPOPROCK.txt') as sample_file:
        samples = [line.split('-') for line in sample_file.readlines()]
    samples = [[chord.strip() for chord in song] for song in samples]
    main(samples)