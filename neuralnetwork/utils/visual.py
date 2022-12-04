"""Functions for visualisations."""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from plotly.matplotlylib.mplexporter._py3k_compat import xrange

from neuralnetwork.utils import plane


def plot_landmarks_3d(save_dir, train, name, landmarks_mean, landmarks_gt, dim):
    """Plot predicted landmarks in 3D space

    Args:
      save_dir: Directory storing the results.
      train: train or test dataset
      name: name of patient.
      landmarks_mean: predicted landmarks. [num_landmarks, 3]
      landmarks_gt: GT landmarks [num_landmarks, 3]
      dim: volume size [3]

    """
    # plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(landmarks_mean[:, 0], landmarks_mean[:, 1], landmarks_mean[:, 2], 'g.')
    ax.plot(landmarks_gt[:, 0], landmarks_gt[:, 1], landmarks_gt[:, 2], 'r.')
    ax.set_title('{}'.format(name))
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim([-dim[0], dim[0]])
    ax.set_ylim([-dim[1], dim[1]])
    ax.set_zlim([-dim[2], dim[2]])
    if train:
        save_dir = os.path.join(save_dir, 'train')
    else:
        save_dir = os.path.join(save_dir, 'test')
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    fig.savefig(os.path.join(save_dir, name+'.png'), bbox_inches='tight')
    plt.close(fig)


def plot_landmarks_path(save_dir, train, name, landmarks_all_steps, landmarks_gt, dim):
    """Save predicted landmark paths as gif.

    Args:
      save_dir: Directory storing the results.
      train: train or test dataset
      name: name of patient.
      landmarks_all_steps: predicted landmarks. [max_test_steps + 1, num_examples, num_landmarks, 3]
      landmarks_gt: GT landmarks [num_landmarks, 3]
      dim: volume size [3]

    """
    c = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
         'tab:olive', 'tab:cyan']
    num_landmarks = landmarks_all_steps.shape[2]
    max_test_steps = landmarks_all_steps.shape[0] - 1

    # plt.ion()
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #fig.set_tight_layout(True)
    ax.plot(landmarks_gt[:, 0], landmarks_gt[:, 1], landmarks_gt[:, 2], 'rx')
    pt = []
    for j in xrange(num_landmarks):
        pt.append(ax.plot(landmarks_all_steps[0, :, j, 0], landmarks_all_steps[0, :, j, 1],
                           landmarks_all_steps[0, :, j, 2], '.', c=c[j])[0])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_xlim([-dim[0], dim[0]])
    ax.set_ylim([-dim[1], dim[1]])
    ax.set_zlim([-dim[2], dim[2]])
    ax.set_title('{}'.format(name))

    def update(n):
        for j in xrange(num_landmarks):
            pt[j].set_data(landmarks_all_steps[n, :, j, 0], landmarks_all_steps[n, :, j, 1])  # x and y axis
            pt[j].set_3d_properties(zs=landmarks_all_steps[n, :, j, 2])  # z axis
        return pt

    anim = FuncAnimation(fig, update,
                         frames=np.arange(0, max_test_steps + 1, 1),
                         interval=600,
                         repeat_delay=3000,
                         repeat=True)
    if train:
        save_dir = os.path.join(save_dir, 'train')
    else:
        save_dir = os.path.join(save_dir, 'test')
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    anim.save(os.path.join(save_dir, name + '.gif'), dpi=80, writer='imagemagick')
    plt.close(fig)
