"""Addition task as used in the IRNN paper:

https://arxiv.org/pdf/1504.00941.pdf


At every time step, the input is a random signal and a mask signal.
Mask is zero at all timesteps except for two, when it has value one.
The task is to add the two random numbers present when the mask is
one.

We generate a fixed number of examples for a training and test set.
It is rather a lot, so this might get a bit gross, memory wise.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import tensorflow as tf


def _gen_numpy_data(sequence_length, num_examples, seed=1001):
    """Make a rather large batch of examples. Results will be
    shape `[number, time_step, 2]` (2 because we have two input
    lines: data and mask)."""
    np.random.seed(seed)
    # as per Le and Hinton, the random data is in [0,1]
    random_data = np.random.sample((num_examples, sequence_length))
    random_data = random_data.astype(np.float32)
    # now we have to figure out where to put the marks
    mask = np.zeros((num_examples, sequence_length), dtype=np.float32)
    # get the first one, between 0 and sequence_length / 2
    first_marks = np.random.randint(sequence_length/2, size=(num_examples,))
    # and the second
    second_marks = np.random.randint(sequence_length/2, sequence_length,
                                     size=(num_examples,))
    eg_idx = np.arange(num_examples)
    mask[eg_idx, first_marks] = 1.0
    mask[eg_idx, second_marks] = 1.0

    targets = np.einsum('ij, kj->k', random_data, mask)

    return np.stack((random_data, mask), axis=-1), targets
    
    
