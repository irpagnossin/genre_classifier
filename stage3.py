#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import DETECTIONS
from os.path import exists
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
        writer = csv.writer(csv_file)
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

    genre_ids = pickle.load(file(input_map, 'rb'))

    df = pd.read_csv(detections, delimiter="|")
    df['genre_id'] = df['track_id'].apply(lambda track_id: genre_ids[track_id] if track_id in genre_ids else -1)
    doi = df[['audio_source_id', 'genre_id', 'created_at']]  # Data of interest
    df2 = doi.groupby(['audio_source_id', 'genre_id']).agg(['count'])
    df3 = df2['created_at']['count']
    df3 = df3.reset_index()

    __source_ids = []
    __genre_ids = []

    for name, group in df3.groupby('audio_source_id'):
        idx = group['count'].idxmax()

        __source_ids.append(name)
        __genre_ids.append(df3.iloc[idx]['genre_id'])

    output = pd.DataFrame({'audio_source_id': __source_ids, 'genre_id': __genre_ids})
    output.to_csv(output_map, index=False)


if __name__ == '__main__':
    """
    Builds the CSV files containing the mappings in format <audio_source_id>,<genre_id> and <track_id>,<genre_id>.
    It reads file 'output/track2genre_x.pickle', where x is the occurrence threshold.
    It writes files 'output/track2genre_x.csv' and 'output/source2genre_x.csv'.
    """

    try:
        n = sys.argv[1]  # Occurrence threshold
    except IndexError:
        n = 1

    n_str = str(n)
    input_track2genre = 'output/track2genre_' + n_str + '.pickle'
    output_track2genre = 'output/track2genre_' + n_str + '.csv'
    output_source2genre = 'output/source2genre_' + n_str + '.csv'

    if not exists(input_track2genre):
        print('File {} does not exist. Execute "python stage2.py {}" to generate it.'.format(input_track2genre, n_str))
        sys.exit(-1)

    build_track2genre_map(input_track2genre, output_track2genre)
    build_source2genre_map(DETECTIONS, input_track2genre, output_source2genre)
