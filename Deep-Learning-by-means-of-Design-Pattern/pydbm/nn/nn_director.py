# -*- coding: utf-8 -*-
from pydbm.nn.interface.nn_builder import NNBuilder
from pydbm.synapse.neural_network_graph import NeuralNetworkGraph
from pydbm.activation.interface.activating_function_interface import ActivatingFunctionInterface


class NNDirector(object):
    '''
    `Director` in Builder Pattern.
    
    Compose synapses for building neural networks.
    '''

    # `Builder` in BUilder Pattern.
    __nn_builder = None
    # The list of nerual networks.
    __nn_list = []

    def get_nn_list(self):
        ''' getter '''
        if isinstance(self.__nn_list, list) is False:
            raise TypeError()

        for nn in self.__nn_list:
            if isinstance(nn, NeuralNetworkGraph) is False:
                raise TypeError()

        return self.__nn_list

    def set_nn_list(self, value):
        ''' setter '''
        if isinstance(value, list) is False:
            raise TypeError()

        for nn in value:
            if isinstance(nn, NeuralNetworkGraph) is False:
                raise TypeError()

        self.__nn_list = value

    nn_list = property(get_nn_list, set_nn_list)

    def __init__(self, nn_builder):
        '''
        Initialize `Builder`.

        Args:
            nn_builder     `Concrete Builder` in Builder Pattern.
        '''
        if isinstance(nn_builder, NNBuilder) is False:
            raise TypeError()

        self.__nn_builder = nn_builder

    def nn_construct(
        self,
        neuron_assign_list,
        activating_function_list
    ):
        '''
        Build neural networks.

        Args:
            neuron_assign_list:          The list of the number of neurons in each layers.
            activating_function_list:    The list of activation functions.
        '''
        if len(activating_function_list) != len(neuron_assign_list):
            raise ValueError()

        for activating_function in activating_function_list:
            if isinstance(activating_function, ActivatingFunctionInterface) is False:
                raise TypeError()

        input_neuron_count = neuron_assign_list[0]
        input_activating_function = activating_function_list[0]
        output_neuron_count = neuron_assign_list[-1]
        output_activating_function = activating_function_list[-1]

        self.__nn_builder.input_neuron_part(
            input_activating_function,
            input_neuron_count
        )

        for i in range(1, len(neuron_assign_list) - 1):
            hidden_neuron_count = neuron_assign_list[i]
            hidden_activating_function = activating_function_list[-1]
            self.__nn_builder.hidden_neuron_part(
                hidden_activating_function,
                hidden_neuron_count
            )

        self.__nn_builder.output_neuron_part(
            output_activating_function,
            output_neuron_count
        )

        self.__nn_builder.graph_part()

        self.nn_list = self.__nn_builder.get_result()
