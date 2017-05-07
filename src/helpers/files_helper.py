import os
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import seaborn as sns


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


def save_scatter_plot(name: str, experiment_path: str, array_x: list, array_y: list):

    lim = max(array_x + array_y)

    plt.title(name)
    plt.xlim(0, lim)
    plt.ylim(0, lim)
    plt.plot(array_x, array_y, 'ro', markersize=1)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(experiment_path)
    plt.close("all")
    plt.clf()
    return


def save_scatter_plot2(name: str, experiment_dir: str, array1_x: list, array1_y: list, array2_x: list, array2_y: list):
    plt.title(name)
    plt.plot(array1_x, array1_y, 'ro')
    plt.plot(array2_x, array2_y, 'go')
    plt.grid(True)
    plt.gca().set_aspect('equal')
    plt.savefig(experiment_dir + name + '.png')
    plt.close("all")
    plt.clf()
    return


def save_hist(name: str, experiment_path: str, array: list):
    plt.title(name)
    plt.hist(array, 50, normed=False, facecolor='green')
    plt.grid(True)
    plt.savefig(experiment_path)
    plt.close("all")
    plt.clf()
    return


def save_rmse_hist(name: str, experiment_path: str, array1: list, array2: list):
    all_errors = []
    for i in range(0, len(array1)):
        rmse = np.math.sqrt((array1[i] - array2[i]) ** 2)
        all_errors.append(rmse)
    plt.title(name)
    plt.ylim(0, 0.05)
    n, b, p = plt.hist(all_errors, 50, normed=True, facecolor='green')
    plt.grid(True)
    plt.savefig(experiment_path)
    plt.close("all")
    plt.clf()
    return


def save_3d_plot_dep(name: str, path: str, points):
    xs = np.array(points[:, 0])
    ys = np.array(points[:, 1])
    zs = np.array(points[:, 2])
    plt.title(name)
    fig = plt.figure(figsize=(40, 40))
    ax = fig.gca(projection='3d')
    ax.plot(xs, ys, zs)
    plt.savefig(path)
    plt.close("all")
    plt.clf()
    return

def save_3d_plot(name: str, path: str, points):
    xs = np.array(points[:, 0])
    ys = np.array(points[:, 1])
    zs = np.array(points[:, 2])
    plt.title(name)
    fig = plt.figure(figsize=(40, 40))
    ax = fig.add_subplot(111, projection='3d')

    # Get rid of the panes
    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the spines
    ax.w_xaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.line.set_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.line.set_color((1.0, 1.0, 1.0, 0.0))

    # Get rid of the ticks
    # ax.set_xticks([])
    # ax.set_yticks([])
    # ax.set_zticks([])

    ax.xaxis.set_ticklabels([])
    ax.yaxis.set_ticklabels([])
    ax.zaxis.set_ticklabels([])

    ax.set_axis_bgcolor((1, 1, 1))

    line = ax.plot(xs, ys, zs)
    plt.setp(line, linewidth=8)

    plt.savefig(path)
    plt.close("all")
    plt.clf()
    return

def save_adjastency_matrix(name: str, path: str, data):
    plt.title(name)
    fig = plt.figure(figsize=(80, 80))
    f, ax = plt.subplots(figsize=(11, 9))
    colors = ["blue", "yellow", "red"]
    cmap = sns.blend_palette(colors, as_cmap=True)
    sns.heatmap(data, cmap=cmap, square=True, xticklabels=100, yticklabels=100)
    plt.savefig(path)
    plt.close("all")
    plt.clf()
    return
