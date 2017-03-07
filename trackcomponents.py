class TrackComponents(object):

    def __init__(self):
        # type: () -> object
        """

        :rtype: object
        """
        self.tracks = dict()
        self.component_index = 0
        self.reindex_map = dict()

    def get_tracks(self):
        return self.tracks

    def n_tracks(self):
        return len(self.tracks)

    def n_components(self):
        return len(self.reindex_map)

    def add(self, track_id, source_id):

        try:
          track = self.tracks[track_id]
        except KeyError:
          source_idx = self.get_source_index(source_id, True)
          self.tracks[track_id] = dict({source_idx:1})
          return None

        source_idx = self.get_source_index(source_id, True)
        try:
          track[source_idx] += 1
        except KeyError:
          track[source_idx] = 1

        return None

    def get(self, track_id, source_id=-1):

        if source_id >= 0:
            source_idx = self.get_source_index(source_id)
            ans = self.tracks[track_id][source_idx]
        else:
            ans = self.tracks[track_id]

        return ans

    def get_source_index(self, source_id, create=False):

        try:
            ans = self.reindex_map[source_id]
        except KeyError as error:
            if create:
                ans = self.component_index

                self.reindex_map[source_id] = self.component_index
                self.component_index += 1
            else:
                raise error

        return ans
