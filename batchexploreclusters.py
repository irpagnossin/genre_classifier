from configuration import *
from outputfilename import get_output_filename
import track_genres as tg
import time

if __name__ == '__main__':
    """
    Builds track->genre mapping for varying occurrence threshold.
    """

    for n in range(200, 1000, 50):

        print('----------------------------------------------------')
        print('Evaluating how many clusters there are for spectra of tracks with absolute frequencies >= {}'.format(n))

        n_str = str(n)
        tracks = get_output_filename(n, TRACKS)
        track_ids = get_output_filename(n, TRACK_IDS)
        silhouette = get_output_filename(n, SILHOUETTE_ANALYSIS_RESULT)
        track2genre = get_output_filename(n, TRACK2GENRES)

        start = time.time()
        tg.construct_track2genre_map(tracks, track_ids, silhouette, track2genre, 30)
        end = time.time()
        print('It took {} seconds'.format(end-start))
