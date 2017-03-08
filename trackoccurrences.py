#!/usr/bin/env python
# -*- coding: utf-8 -*-


class TrackOccurrences(object):

    def __init__(self, minimum=1):
        # type: () -> object
        """

        :rtype: object
        """
        self.candidate_tracks = dict()
        self.definitive_tracks = dict()
        self.component_index = 0
        self.reindex_map = dict()
        self.minimum = minimum

    def get_tracks(self):
        return self.definitive_tracks

    def n_tracks(self):
        return len(self.definitive_tracks)

    def n_components(self):
        return len(self.reindex_map)

    def add(self, track_id, source_id):

        try:
            track = self.definitive_tracks[track_id]

            try:
                source_idx = self.get_source_index(source_id)
                track[source_idx] += 1

            except KeyError:
                source_idx = self.create_source_index(source_id)
                track[source_idx] = 1

        except KeyError:
            try:
                track = self.candidate_tracks[track_id]

                try:
                    track[source_id] += 1

                except KeyError:
                    track[source_id] = 1

            except KeyError:
                self.candidate_tracks[track_id] = dict({source_id: 1})

            finally:
                if self.__get_accumulated_occurrence(track_id) >= self.minimum:

                    components = dict()
                    for (k, v) in self.candidate_tracks[track_id].iteritems():

                        idx = self.get_source_index(k) if k in self.reindex_map else self.create_source_index(k)
                        components[idx] = v

                    self.definitive_tracks[track_id] = components
                    del self.candidate_tracks[track_id]

    def get_occurrence(self, track_id, source_id):
        """
        Get absolute frequency (occurrence) of track <track_id> at radio-station <source_id>
        :param track_id:
        :param source_id:
        :return:
        """

        source_idx = self.get_source_index(source_id)
        return self.definitive_tracks[track_id][source_idx]

    def get_occurrences(self, track_id):
        """
        Get absolute frequencies (occurrences) of track <track_id> ot all radio-stations
        :param track_id:
        :return:
        """
        return self.definitive_tracks[track_id]

    def get_source_index(self, source_id):
        return self.reindex_map[source_id]

    def create_source_index(self, source_id):

        try:
            ans = self.reindex_map[source_id]
        except KeyError:

            ans = self.component_index

            self.reindex_map[source_id] = self.component_index
            self.component_index += 1

        return ans

    def __get_accumulated_occurrence(self, track_id):

        ans = 0
        for (k, v) in self.candidate_tracks[track_id].iteritems():
            ans += v

        return ans
