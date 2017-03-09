from configuration import *
from os.path import exists
from outputfilename import get_output_filename
import numpy as np
import pandas as pd
import sys


# TODO: to organize this mess!
def recap(detections_csv, track2genre_csv, source2genre_csv, track2genre_recap_csv):
    """
    Tries to identify the genres of missed tracks based on the genres of the radio-stations
    :param detections_csv:
    :param track2genre_csv:
    :param source2genre_csv:
    :param track2genre_recap_csv:
    :return:
    """

    detections = pd.read_csv(detections_csv, sep='|')
    track2genre = pd.read_csv(track2genre_csv)
    source2genre = pd.read_csv(source2genre_csv)

    mask = np.logical_not(detections['track_id'].isin(track2genre['track_id']))
    unknown_tracks = detections[mask]

    source2genre_dict = dict(zip(source2genre['audio_source_id'], source2genre['genre_id']))
    get_genre = lambda gdi: source2genre_dict[gdi] if gdi in source2genre_dict else -1

    # TODO: fix pandas warning
    #tmp = unknown_tracks['audio_source_id'].apply(get_genre)
    #unknown_tracks = pd.concat([unknown_tracks, tmp], axis=1)
    unknown_tracks['genre_id'] = unknown_tracks['audio_source_id'].apply(get_genre)

    df2 = unknown_tracks.groupby(['track_id', 'genre_id']).agg(['count'])
    df3 = df2['created_at']['count']
    df3 = df3.reset_index()

    __track_ids = []
    __genre_ids = []

    for name, group in df3.groupby('track_id'):
        idx = group['count'].idxmax()

        __track_ids.append(name)
        __genre_ids.append(df3.iloc[idx]['genre_id'])

    g = pd.DataFrame({'track_id': __track_ids, 'genre_id': __genre_ids})

    g2 = g[g['genre_id'] >= 0]

    g2.to_csv(track2genre_recap_csv, columns=['track_id', 'genre_id'])

    n_tracks_ok = len(track2genre)
    n_tracks_total = len(set(detections['track_id']))

    n_recap_tracks = len(g2)

    p_recap_tracks = 100.0 * n_recap_tracks / n_tracks_total
    p_tracks_ok = 100.0 * (n_tracks_ok + n_recap_tracks) / n_tracks_total
    p_tracks_ok_before_recap = 100.0 * n_tracks_ok / n_tracks_total

    print('Recapped tracks: {0} ({1:.2f}%)'.format(n_recap_tracks, p_recap_tracks))
    print('Clusterized tracks before recap: {0} ({1:.2f}%)'.format(n_tracks_ok, p_tracks_ok_before_recap))
    print('Clusterized tracks after recap: {0} ({1:.2f}%)'.format(n_tracks_ok + n_recap_tracks, p_tracks_ok))


def main():
    """
    Tries to identify the genres of missed tracks based on the genres of the radio-stations
    """

    try:
        n = int(sys.argv[1])  # Occurrence threshold
    except IndexError:
        n = 1
    except ValueError:
        n = 1

    assert (type(n) == int)

    n_str = str(n)
    track2genre_csv = get_output_filename(n, TRACK2GENRE_CSV)
    source2genre_csv = get_output_filename(n, SOURCE2GENRE_CSV)
    track2genre_recap_csv = get_output_filename(n, TRACK2GENRE_RECAP_CSV)

    if not exists(track2genre_csv):
        print('File {} does not exist. Execute "python stage3.py {}" to generate it.'.format(track2genre_csv, n_str))
        sys.exit(-1)

    if not exists(source2genre_csv):
        print('File {} does not exist. Execute "python stage3.py {}" to generate it.'.format(source2genre_csv, n_str))
        sys.exit(-1)

    recap(DETECTIONS, track2genre_csv, source2genre_csv, track2genre_recap_csv)


if __name__ == '__main__':
    main()
