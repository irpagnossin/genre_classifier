from configuration import DETECTIONS
import track_genres as tg
import time

if __name__ == '__main__':

    for n in range(200, 1000, 50):

        print('----------------------------------------------------')
        print('Evaluating how many clusters there are for spectra of tracks with absolute frequencies >= {}'.format(n))

        n_str = str(n)
        tracks = 'output/tracks_' + n_str + '.npz'
        track_ids = 'output/track_ids_' + n_str + '.pickle'
        silhouette = 'output/silhouette_' + n_str + '.csv'
        track2genre = 'output/track2genre_' + n_str + '.pickle'

        start = time.time()
        tg.construct_track2genre_map(tracks, track_ids, silhouette, track2genre, 30)
        end = time.time()
        print('It took {} seconds'.format(end-start))
