# -*- coding: utf-8 -*-

import numpy as np

cimport numpy as np
from pydbm.dbm.deep_boltzmann_machine import DeepBoltzmannMachine


class StackedAutoEncoder(DeepBoltzmannMachine):
    '''
    Stacked Auto-Encoder.
    '''
    # auto-saved featrue points.
    __feature_points_arr = None

    def get_feature_points_arr(self):
        ''' getter '''
        return self.__feature_points_arr

    def set_readonly(self, value):
        ''' setter '''
        raise TypeError("This property is read-only.")

    feature_points_arr = property(get_feature_points_arr, set_readonly)

    def learn(
        self,
        np.ndarray observed_data_arr,
        int traning_count=1000
    ):
        '''
        Learning and auto-saving featrue points with `np.ndarray`.

        Args:
            observed_data_arr:      The `np.ndarray` of observed data points.
            traning_count:          Training counts.
        '''
        if isinstance(observed_data_arr, np.ndarray) is False:
            raise TypeError()

        cdef int row = observed_data_arr.shape[0]
        cdef int t
        cdef np.ndarray data_arr
        feature_points_list = [None] * row
        for t in range(traning_count):
            for i in range(row):
                data_arr = np.array([observed_data_arr[i]])
                super().learn(
                    observed_data_arr=data_arr,
                    traning_count=1
                )
                if t == traning_count - 1:
                    feature_points_arr = self.get_feature_point_list()
                    feature_points_list[i] = feature_points_arr

        self.__feature_points_arr = np.array(feature_points_list)
