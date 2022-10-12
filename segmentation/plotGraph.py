# %%
import matplotlib.pyplot as plt
import numpy as np

# %%


def plot_histogram_threshold(hist, bin_edges, threshs):
    plt.plot(bin_edges, hist)
    plt.title('histogram')
    for t in threshs:
        plt.axvline(x=t, color='r')

# %%


def plot_image_histogram(img, hist, bin_edges):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title('image')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 2, 2)
    plt.plot(bin_edges, hist)
    plt.title('histogram')

    plt.show()

# %%


def plot_image_histogram_threshold(img, hist, bin_edges, threshs):
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img, cmap='gray')
    plt.title(f'Threshold(s): {threshs}')
    plt.xticks([])
    plt.yticks([])

    plt.subplot(1, 2, 2)
    plot_histogram_threshold(hist, bin_edges, threshs)

    plt.show()

# %%


def plot_histogram(hist):
    plt.plot(hist)
    plt.title('Histogram')

# %%


def show_image(img, title):
    plt.figure(figsize=(20, 7))
    plt.title(title, fontsize=20)
    plt.imshow(img, cmap='gray')
    plt.plot()
