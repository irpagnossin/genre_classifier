#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import *
from os.path import exists
from outputfilename import get_output_filename
from summary import summary
import csv
import pandas as pd
import pickle
import sys


def build_track2genre_map(input_map, output_map):
    """
    Generates CSV with format <track_id>,<genre_id>.
    :param input_map: pickle file containing the mapping track_id->genre_id, generated at stage 2
    :param output_map: CSV file to save <track_id>,<genre_id>
    :return: None
    """

    genre_ids = pickle.load(file(input_map, 'rb'))

    with open(output_map, 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        writer.writerow(['track_id', 'genre_id'])
        for key, value in genre_ids.items():
            writer.writerow([key, value])


# TODO: remove pandas
def build_source2genre_map(detections, input_map, output_map):
    """
    Generates CSV with format <audio_source_id>,<genre_id>. genre_id = -1 means this audio_source_id was not used in
    analysis because tracks it has played did not reach occurrence threshold.
    :param detections: CSV file with detections, in format <created_at>|<audio_source_id>|<track_id>
    :param input_map: pickle file containing the mapping track_id->genre_id, generated at stage 2
    :param output_map: CSV file to save <audio_source_id>,<genre_id>
    :return: None
    """

    track2genre = pickle.load(file(input_map, 'rb'))

    df = pd.read_csv(detections, delimiter="|")
    df['genre_id'] = df['track_id'].apply(lambda track_id: track2genre[track_id] if track_id in track2genre else -1)  # TODO: problema!!!!

    doi = df[df['genre_id'] >= 0][['audio_source_id', 'genre_id', 'created_at']]  # Data of interest
    df2 = doi.groupby(['audio_source_id', 'genre_id']).agg(['count'])
    df3 = df2['created_at']['count']
    df3 = df3.reset_index()

    __source_ids = []
    __genre_ids = []

    # Defines the radio-station genre as the genre of the most frequent track
    for name, group in df3.groupby('audio_source_id'):
        idx = group['count'].idxmax()

        __source_ids.append(name)
        __genre_ids.append(df3.iloc[idx]['genre_id'])

    output = pd.DataFrame({'audio_source_id': __source_ids, 'genre_id': __genre_ids})
    output.to_csv(output_map, sep='|', index=False)


def main():
    """
    Builds CSV files containing the mappings in format <audio_source_id>,<genre_id> and <track_id>,<genre_id>.
    It reads file 'output/track2genre_x.pickle', where x is the occurrence threshold.
    It writes files 'output/track2genre_x.csv' and 'output/source2genre_x.csv'.
    """

    try:
        n = int(sys.argv[1])  # Occurrence threshold
    except IndexError:
        n = 1
    except ValueError:
        n = 1

    assert (type(n) == int)

    n_str = str(n)
    input_track2genre = get_output_filename(n, TRACK2GENRES)
    output_track2genre = get_output_filename(n, TRACK2GENRE_CSV)
    output_source2genre = get_output_filename(n, SOURCE2GENRE_CSV)

    if not exists(input_track2genre):
        print('File {} does not exist. Execute "python stage2.py {}" to generate it.'.format(input_track2genre, n_str))
        sys.exit(-1)

    print('Building CSV files containing mappings track->genre and source->genre...')
    build_track2genre_map(input_track2genre, output_track2genre)
    build_source2genre_map(DETECTIONS, input_track2genre, output_source2genre)
    summary(DETECTIONS, output_track2genre, output_source2genre)


if __name__ == '__main__':
    main()
