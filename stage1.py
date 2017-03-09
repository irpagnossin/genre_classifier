#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import *
from outputfilename import get_output_filename
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
    _track_ids, _spectra = spectra(tracks_dict)
    end = time.time()
    print('It took {0:.3f} seconds to construct tracks spectra'.format(end-start))

    print('Saving spectra...')
    _tracks = np.divide(_spectra, np.sum(_spectra, axis=1, dtype=np.float64)[:, np.newaxis])
    sparse_matrix = csr_matrix(_tracks)
    np.savez(output_tracks, data=sparse_matrix.data, indices=sparse_matrix.indices, indptr=sparse_matrix.indptr,
             shape=sparse_matrix.shape)

    print('Saving track_ids...')
    pickle.dump(_track_ids, file(output_track_ids, 'wb'), pickle.HIGHEST_PROTOCOL)


def main():
    """
    Builds spectra for a given occurrence threshold (argument).
    """

    try:
        n = int(sys.argv[1])  # Occurrence threshold
    except IndexError:
        n = 1
    except ValueError:
        n = 1

    assert(type(n) == int)

    n_str = str(n)
    tracks = get_output_filename(n, TRACKS)
    track_ids = get_output_filename(n, TRACK_IDS)

    print('Building spectra for tracks with occurrence threshold >= {}...'.format(n_str))

    build_spectra(DETECTIONS, tracks, track_ids, n)

if __name__ == '__main__':
    main()
