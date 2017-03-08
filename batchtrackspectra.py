from configuration import *
from outputfilename import get_output_filename
import construct_track_spectra as ts


if __name__ == '__main__':
    """
    Builds many spectra for varying occurrence threshold.
    """

    for n in range(50, 1000, 50):

        print('----------------------------------------------------')
        print('Building spectra for tracks with occurrence threshold >= {}'.format(n))

        tracks = get_output_filename(n, TRACKS)
        track_ids = get_output_filename(n, TRACK_IDS)

        ts.construct_spectra(DETECTIONS, tracks, track_ids, min_occur=n)
