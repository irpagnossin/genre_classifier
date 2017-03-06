from trackcomponents import TrackComponents
import csv
import numpy as np

def scan_table(csvfile):
    tracks = TrackComponents()

    with open(csvfile, 'r') as input:
      reader = csv.reader(input, delimiter=',')
      reader.next() # Skip header
      for row in reader:
        tracks.add(int(row[1]), int(row[0]))

    return tracks


def construct_array(tracks):

    n_tracks = tracks.n_tracks()
    n_components = tracks.n_components()
    print('{} tracks x {} components.'.format(n_tracks, n_components))

    spectra = np.zeros(shape=(n_tracks,n_components))

    i = 0
    for track_id, spectrum in tracks.get_tracks().iteritems():
        for component_idx, value in spectrum.iteritems():
            spectra[i,component_idx] = value
        i += 1

    return spectra

s = construct_array(scan_table('tests/2-tracks_6-features.csv'))
tracks = np.divide(s, np.sum(s, axis=1, dtype=np.float64)[:, np.newaxis])
print(s)
print(tracks)
