#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configuration import *
from progressbar import printProgress
from read_large_csv import get_row
from scipy.sparse import csr_matrix
from trackoccurrences import TrackOccurrences
import numpy as np
import pickle
import time


def tracks_occurrence(csvfile, delimiter=',', rows=-1, min_occur=1):
    """
    Iterate over detections data-set (CSV file) to construct an optimized representation of tracks spectra
    :param csvfile: the name of the CSV file containing detections, in format <created_at>,<audio_source_id>,<track_id>
    :param delimiter: delimiter character
    :param rows: amount of rows to scan. If -1, all data-set shall be scanned
    :return: an optimized representation of tracks-spectra
    :rtype: TrackComponents
    """

    tracks = TrackOccurrences(min_occur)

    count = 0
    for row in get_row(csvfile, delimiter, rows):
        try:
            track_id = int(row[2])
            source_id = int(row[1])
            tracks.add(track_id, source_id)

            count += 1
            if count % 100 == 0:
                time.sleep(0)

        except IndexError:  # Ignore malformed rows
            pass

        except ValueError:  # Ignore malformed rows
            pass

    return tracks


def to_array(tracks):
    """
    Construct spectra np.array based on tracks-features
    :param tracks:
    :return: tracks spectra as np.array
    :rtype: (list,np.array)
    """

    n_tracks = tracks.n_tracks()
    n_components = tracks.n_components()
    print('{} tracks x {} features'.format(n_tracks, n_components))

    spectra = np.zeros(shape=(n_tracks, n_components))

    track_ids = []  # TODO: change to array
    i = 0
    for track_id, spectrum in tracks.get_tracks().iteritems():
        for component_idx, value in spectrum.iteritems():
            spectra[i, component_idx] = value
        i += 1
        track_ids.append(track_id)

        if i % 100 == 0:
            printProgress(i, n_tracks)
            time.sleep(0)

    printProgress(n_tracks, n_tracks)

    return track_ids, spectra


def construct_spectra(input_detections, output_tracks, output_track_ids, min_occur=1):
    print('Inspecting detections data-set...')
    start = time.time()
    tracks_dict = tracks_occurrence(input_detections, delimiter='|', min_occur=min_occur)
    end = time.time()
    print('It took {0:.3f} seconds to inspect detections data-set'.format(end-start))

    print('Constructing tracks spectra...')
    start = time.time()
    track_ids, spectra = to_array(tracks_dict)
    end = time.time()
    print('It took {0:.3f} seconds to construct tracks spectra'.format(end-start))

    print('Saving spectra...')
    tracks = np.divide(spectra, np.sum(spectra, axis=1, dtype=np.float64)[:, np.newaxis])
    sparse_matrix = csr_matrix(tracks)
    np.savez(output_tracks, data=sparse_matrix.data, indices=sparse_matrix.indices, indptr=sparse_matrix.indptr,
             shape=sparse_matrix.shape)

    print('Saving track_ids...')
    pickle.dump(track_ids, file(output_track_ids, 'wb'), pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    construct_spectra(DETECTIONS, TRACKS, TRACK_IDS, 1)
