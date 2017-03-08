#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import DETECTIONS
from scipy.sparse import csr_matrix
from trackspectra import spectra, track_occurrences
import numpy as np
import pickle
import sys
import time


def build_spectra(input_detections, output_tracks, output_track_ids, min_occur=1):
    """
    Builds spectra, as a np.array, of all tracks which fulfill threshold occurrence
    :param input_detections: CSV file with detections, in format <created_at>|<audio_source_id>|<track_id>
    :param output_tracks: filename .npz where spectra shall be saved as np.array in CSR (compact sparse row) format
    :param output_track_ids: filename .pickle where the list of track_ids shall be saved
    :param min_occur: occurrence threshold. Tracks which do not show up more than this will not be considered
    :return:
    """

    print('Inspecting detections data-set...')
    start = time.time()
    tracks_dict = track_occurrences(input_detections, delimiter='|', min_occur=min_occur)
    end = time.time()
    print('It took {0:.3f} seconds to inspect detections data-set'.format(end-start))

    print('Constructing tracks spectra...')
    start = time.time()
    track_ids, _spectra = spectra(tracks_dict)
    end = time.time()
    print('It took {0:.3f} seconds to construct tracks spectra'.format(end-start))

    print('Saving spectra...')
    tracks = np.divide(_spectra, np.sum(_spectra, axis=1, dtype=np.float64)[:, np.newaxis])
    sparse_matrix = csr_matrix(tracks)
    np.savez(output_tracks, data=sparse_matrix.data, indices=sparse_matrix.indices, indptr=sparse_matrix.indptr,
             shape=sparse_matrix.shape)

    print('Saving track_ids...')
    pickle.dump(track_ids, file(output_track_ids, 'wb'), pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    """
    Builds spectra for a given occurrence threshold (argument).
    """

    try:
        n = sys.argv[1]  # Occurrence threshold
    except IndexError:
        n = 1

    n_str = str(n)
    tracks = 'output/tracks_' + n_str + '.npz'
    track_ids = 'output/track_ids_' + n_str + '.pickle'

    build_spectra(DETECTIONS, tracks, track_ids, n)
