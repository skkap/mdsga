import os
from matplotlib import pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def clean_directory(directory: str):
    """
    Removes files in the experiment dir
    :param directory: experiment dir
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)
    return


def save_scatter_plot(name: str, experiment_dir: str, array_x:list, array_y: list):
    plt.title(name)
    plt.plot(array_x, array_y, 'ro')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.savefig(experiment_dir + name + '.png')
    plt.close("all")
    plt.clf()
    return


def save_scatter_plot2(name: str, experiment_dir: str, array1_x:list, array1_y: list, array2_x:list, array2_y: list):
    plt.title(name)
    plt.plot(array1_x, array1_y, 'ro')
    plt.plot(array2_x, array2_y, 'go')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.savefig(experiment_dir + name + '.png')
    plt.close("all")
    plt.clf()
    return


def save_3d_plot(name: str, dir: str, points):
    xs = np.array(points[:, 0])
    ys = np.array(points[:, 1])
    zs = np.array(points[:, 2])
    plt.title(name)
    fig = plt.figure(figsize=(40, 40))
    ax = fig.gca(projection='3d')
    ax.plot(xs, ys, zs)
    plt.savefig(dir + name + '.png')
    plt.close("all")
    plt.clf()
    return
