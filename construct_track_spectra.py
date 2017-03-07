from read_large_csv import getstuff
from scipy.sparse import csr_matrix
from trackcomponents import TrackComponents
import csv
import numpy as np
import pickle
import time

def scan_table(csvfile, delimiter=',', rows=-1):
    tracks = TrackComponents()

    for row in getstuff(csvfile, delimiter, rows):
        tracks.add(int(row[2]), int(row[1]))

    return tracks


def construct_array(tracks):

    n_tracks = tracks.n_tracks()
    n_components = tracks.n_components()
    print('{} tracks x {} components.'.format(n_tracks, n_components))

    spectra = np.zeros(shape=(n_tracks,n_components))

    track_ids = []
    i = 0
    for track_id, spectrum in tracks.get_tracks().iteritems():
        for component_idx, value in spectrum.iteritems():
            spectra[i,component_idx] = value
        i += 1
        track_ids.append(track_id)

    return (track_ids, spectra)

#s = construct_array(scan_table('tests/2-tracks_6-features.csv',rows=3))
start = time.time()
track_ids, s = construct_array(scan_table('detections-20141206.csv', delimiter='|'))
end = time.time()
print(s)
print('Levou {} s para construir os espectros'.format(end-start))

tracks = np.divide(s, np.sum(s, axis=1, dtype=np.float64)[:, np.newaxis])
sparse_matrix = csr_matrix(tracks)
np.savez('tracks.npz',
         data = sparse_matrix.data,
         indices = sparse_matrix.indices,
         indptr = sparse_matrix.indptr,
         shape = sparse_matrix.shape)

pickle.dump(track_ids)
