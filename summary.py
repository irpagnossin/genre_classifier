#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import *
from os.path import exists
from outputfilename import get_output_filename
import pandas as pd
import sys


def summary(detections, track2genre, source2genre):
    """
    Evaluates and prints statistic summary
    :param detections: CSV file with detections, in format <created_at>|<audio_source_id>|<track_id>
    :param track2genre: CSV file with format <track_id>,<genre_id>, generated at stage3.py
    :param source2genre: CSV file with format <audio_source_id>,<genre_id>, generated at stage3.py
    :return: None
    """

    detections_df = pd.read_csv(detections, delimiter='|')
    n_tracks = len(set(detections_df['track_id']))
    n_sources = len(set(detections_df['audio_source_id']))

    track2genre_df = pd.read_csv(track2genre)
    n_classified_tracks = len(track2genre_df)
    p_classified_tracks = 100.0 * n_classified_tracks / n_tracks

    source2genre_df = pd.read_csv(source2genre)
    n_classified_sources = len(source2genre_df)
    p_classified_sources = 100.0 * n_classified_sources / n_sources

    print('-- Tracks --')
    print('Total tracks: {}'.format(n_tracks))
    print('Clusterized tracks: {0} ({1:.2f}%)'.format(n_classified_tracks, p_classified_tracks))
    print('')
    print('-- Sources --')
    print('Total sources: {}'.format(n_sources))
    print('Clusterized sources: {0} ({1:.2f}%)'.format(n_classified_sources, p_classified_sources))


if __name__ == '__main__':
    """
    Evaluates and prints statistic summary
    """

    try:
        n = sys.argv[1]  # Occurrence threshold
    except IndexError:
        n = 1

    n_str = str(n)
    track2genre_csv = get_output_filename(n, TRACK2GENRE_CSV)
    source2genre_csv = get_output_filename(n, SOURCE2GENRE_CSV)

    if not exists(track2genre_csv):
        print('File {} does not exist. Execute "python stage3.py {}" to generate it.'.format(track2genre_csv, n_str))
        sys.exit(-1)

    if not exists(source2genre_csv):
        print('File {} does not exist. Execute "python stage3.py {}" to generate it.'.format(source2genre_csv, n_str))
        sys.exit(-1)

    summary(DETECTIONS, track2genre_csv, source2genre_csv)
