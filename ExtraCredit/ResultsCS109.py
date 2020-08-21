import matplotlib.pyplot as plt

def bar_plotter(distribution, name, filename, clr='g'):
    names = distribution.keys()
    values = distribution.values()

    plt.figure(figsize=(10, 5))

    plt.subplot(111)
    plt.bar(names, values, color=clr)

    plt.title(name)
    plt.savefig(filename)

def point_plotter(distribution, name, filename, bins=30, clr='g'):
    plt.figure(figsize=(10, 5))

    plt.subplot(111)
    plt.hist(distribution, color=clr, bins=bins)

    plt.title(name)
    plt.savefig(filename)
