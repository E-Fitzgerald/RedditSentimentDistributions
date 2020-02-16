import matplotlib.pyplot as plt
import math
from scipy import stats

def plotter(distribution, name, filename, clr='g'):
    names = distribution.keys()
    values = distribution.values()

    plt.figure(figsize=(8, 5))

    plt.subplot(111)
    plt.bar(names, values, color=clr)

    plt.title(name)
    plt.savefig(filename)

def file_output(donald_distributions, politics_distributions, donald_plot_names, politics_plot_names):
    with open('Results/DistributionResults.txt', 'w') as f:
        f.write("Sentiment Distributions for r/The_Donald:\n")
        f.write("-------------------------------------------------------\n")

        for i in range(len(donald_distributions)):
            donald_sum = donald_distributions[i]["Neutral"] + donald_distributions[i]["Negative"] + \
                         donald_distributions[i]["Positive"]
            f.write(donald_plot_names[i] + " \n-- Negative:" + str(donald_distributions[i]["Negative"]) + " \n-- Neutral: "
                    + str(donald_distributions[i]["Neutral"]) + " \n-- Positive: " + str(donald_distributions[i]["Positive"]) + "\n")


            f.write("Negative Percentage: " + str(donald_distributions[i]["Negative"]/donald_sum) + "\n")
            f.write("Neutral Percentage: " + str(donald_distributions[i]["Neutral"] / donald_sum) + "\n")
            f.write("Positive Percentage: " + str(donald_distributions[i]["Positive"] / donald_sum) + "\n")
            f.write("\n")

        f.write("\n\n")
        f.write("Sentiment Distributions for r/politics:\n")
        f.write("-------------------------------------------------------\n")
        for i in range(len(politics_distributions)):
            politics_sum = politics_distributions[i]["Neutral"] + politics_distributions[i]["Negative"] + \
                           politics_distributions[i]["Positive"]

            f.write(politics_plot_names[i] + " \n-- Negative:" + str(politics_distributions[i]["Negative"]) + " \n-- Neutral: "
                    + str(politics_distributions[i]["Neutral"]) + " \n-- Positive: " + str(politics_distributions[i]["Positive"]) +"\n")

            f.write("Negative Percentage: " + str(politics_distributions[i]["Negative"] / politics_sum) + "\n")
            f.write("Neutral Percentage: " + str(politics_distributions[i]["Neutral"] / politics_sum) + "\n")
            f.write("Positive Percentage: " + str(politics_distributions[i]["Positive"] / politics_sum) + "\n")
            f.write("\n")

        f.write("\n\n")
        f.write("Two-Proportion Z-Test for significances of Negativity and Positivity across all four years:\n")
        f.write("-------------------------------------------------------\n")
        donald_negativity_sum = 0
        donald_positivity_sum = 0
        donald_sum = 0
        politics_negativity_sum = 0
        politics_positivity_sum = 0
        politics_sum = 0
        for i in range(len(donald_distributions)):
            donald_negativity_sum += donald_distributions[i]["Negative"]
            donald_positivity_sum += donald_distributions[i]["Positive"]
            donald_sum += donald_distributions[i]["Negative"] + donald_distributions[i]["Neutral"] + donald_distributions[i]["Positive"]

            politics_negativity_sum += politics_distributions[i]["Negative"]
            politics_positivity_sum += politics_distributions[i]["Positive"]
            politics_sum += politics_distributions[i]["Negative"] + politics_distributions[i]["Neutral"] + \
                            politics_distributions[i]["Positive"]

        donald_negative_proportion = donald_negativity_sum / donald_sum
        donald_positive_proportion = donald_positivity_sum / donald_sum
        politics_negative_proportion = politics_negativity_sum / politics_sum
        politics_positive_proportion = politics_positivity_sum / politics_sum

        f.write("Negative Sentiment Tests \n")
        f.write("Total Proportion of Negative r/The_Donald comments: " + str(donald_negative_proportion)
                + " (" + str(donald_negativity_sum) + " / " + str(donald_sum) + ")\n")
        f.write("Total Proportion of Negative r/politics comments: " + str(politics_negative_proportion)
                + " (" + str(politics_negativity_sum) + " / " + str(politics_sum) + ")\n")

        negative_z_score_donald_greater = (donald_negative_proportion - politics_negative_proportion) / math.sqrt(
            ((donald_negative_proportion * (1-donald_negative_proportion))/donald_sum) + (
            (politics_negative_proportion * (1-politics_negative_proportion))/politics_sum))
        negative_p_value_donald_greater = stats.norm.sf((negative_z_score_donald_greater))

        negative_z_score_politics_greater = (politics_negative_proportion - donald_negative_proportion) / math.sqrt(
            ((donald_negative_proportion * (1 - donald_negative_proportion)) / donald_sum) + (
            (politics_negative_proportion * (1 - politics_negative_proportion)) / politics_sum))
        negative_p_value_politics_greater = stats.norm.sf((negative_z_score_politics_greater))

        f.write("The p-value = " + str(negative_p_value_donald_greater) + ", and is less than .05, so we may conclude that the sentiment of r/The_Donald is more negative than that of r/politics.\n")
        f.write("The p-value = " + str(negative_p_value_politics_greater) + ", and is greater than .05, so we may conclude that the sentiment of r/politics is not more negative than that of r/The_Donald.\n")
        f.write("\n")

        f.write("Positive Sentiment Tests \n")
        f.write("Total Proportion of Positive r/The_Donald comments: " + str(donald_positive_proportion) + " (" + str(donald_positivity_sum) + " / " + str(donald_sum) + ")\n")
        f.write("Total Proportion of Positive r/politics comments: " + str(politics_positive_proportion) + " (" + str(politics_positivity_sum) + " / " + str(politics_sum) + ")\n")

        positive_z_score_donald_greater = (donald_positive_proportion - politics_positive_proportion) / math.sqrt(
            ((donald_positive_proportion * (1 - donald_positive_proportion)) / donald_sum) + (
            (politics_positive_proportion * (1 - politics_positive_proportion)) / politics_sum))
        positive_p_value_donald_greater = stats.norm.sf((positive_z_score_donald_greater))

        positive_z_score_politics_greater = (politics_positive_proportion - donald_positive_proportion) / math.sqrt(
            ((donald_positive_proportion * (1 - donald_positive_proportion)) / donald_sum) + (
            (politics_positive_proportion * (1 - politics_positive_proportion)) / politics_sum))
        positive_p_value_politics_greater = stats.norm.sf((positive_z_score_politics_greater))

        f.write("The p-value = " + str(positive_p_value_donald_greater) + ", and is greater than .05, so we may conclude that the sentiment of r/The_Donald is not more positive than that of r/politics.\n")
        f.write("The p-value = " + str(positive_p_value_politics_greater) + ", and is less than .05, so we may conclude that the sentiment of r/politics is more positive than that of r/The_Donald.\n")
        f.write("\n")

    f.close()
