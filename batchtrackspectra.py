from configuration import DETECTIONS
import construct_track_spectra as ts


if __name__ == '__main__':

    for n in range(50, 1000, 50):

        print('----------------------------------------------------')
        print('Building spectra for tracks with absolute frequencies >= {}'.format(n))

        tracks = 'output/tracks_' + str(n) + '.npz'
        track_ids = 'output/track_ids_' + str(n) + '.pickle'

        ts.construct_spectra(DETECTIONS, tracks, track_ids, min_occur=n)
