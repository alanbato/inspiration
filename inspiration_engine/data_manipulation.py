from collections import Counter
from itertools import permutations, product
from pathlib import Path

NOTES = 'I II III IV V VI VII'.split()

def parse_song(song_str):
    if '–' in song_str:
        return song_str.split('–')
    if '-' in song_str:
        return song_str.split('-')
    elif ',' in song_str:
        return song_str.split(',')
    else:
        raise ValueError('Unrecognized separator for {}'.format(song_str))

def parse_file(filepath):
    with open(filepath) as song_file:
        return [parse_song(line.strip()) for line in song_file]

def get_k_grams(sequence, K):
    K = min(len(sequence), K)
    grams = []
    for k in range(1, K):
        grams.extend((tuple(sequence[i:i+k+1]) for i in range(len(sequence) - k)))
    return grams

def big_bang(K):
    universe = []
    for k in range(2, K):
        universe.extend(product(NOTES, repeat=k))
    return universe
            


def T_union(k_grams):
    union = set()
    for grams in k_grams:
        union |= set(grams)
    return sorted(list(union))

def get_frequency(grams, universe):
    counts = Counter(grams)
    freqs = [counts[gram] for gram in universe]
    return freqs

def get_frequency_matrix(songs, universal=True, K=3):
    k_grams = [get_k_grams(song, K) for song in songs]
    if universal:
        universe = big_bang(K)
    else:
        universe = T_union(k_grams)
    songs_in_freqs = [
        get_frequency(song_grams, universe)
        for song_grams in k_grams
    ]
    return songs_in_freqs
    


if __name__ == '__main__':
    samples = parse_file(Path('data') / 'Top10MostCommonPOPROCK.txt')
    get_frequency_matrix(samples)