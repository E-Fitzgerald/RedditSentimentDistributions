import statistics
from ResultsCS109 import point_plotter


def quartiles(dataPoints):
    sortedPoints = sorted(dataPoints)
    mid = len(sortedPoints) // 2 # uses the floor division to have integer returned
    if (len(sortedPoints) % 2 == 0):
        # even
        lowerQ = statistics.median(sortedPoints[:mid])
        upperQ = statistics.median(sortedPoints[mid:])
    else:
        # odd
        lowerQ = statistics.median(sortedPoints[:mid])  # same as even
        upperQ = statistics.median(sortedPoints[mid + 1:])

    return (lowerQ, upperQ)

def normal_stats(distribution, name, filename, color):


    # # Print to a text file all the distributions and percentages

    new_dist = []
    dlowerQ, dupperQ = quartiles(distribution)
    diqr = dupperQ - dlowerQ
    dupper = dupperQ + 1.5 * diqr
    dlower = dlowerQ - 1.5 * diqr
    for item in distribution:
        if item < dupper and item > dlower:
            new_dist.append(item)

    point_plotter(new_dist, name, filename, bins=40, clr=color)
    dist_stats = {"Min":min(new_dist), "Max":max(new_dist), "Mean":statistics.mean(new_dist),
                  "Std.":statistics.stdev(new_dist)}
    print("Min and Max and Mean and Std.: " + str(dist_stats["Min"]) + " and " + str(dist_stats["Max"]) + " and " +
          str(dist_stats["Mean"]) + " and " + str(dist_stats["Std."]))

    return dist_stats

