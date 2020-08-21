import praw
import pandas as pd
import pickle
from Scraper import subreddit_scraper
from Preprocessing import preprocess_comments
from DistributionCS109 import scores_distribution
from ResultsCS109 import bar_plotter, point_plotter
from NormalCS109 import normal_stats
from Classifiers import normal_classifier, term_frequency_classifier, wordToProbMapper, ComboClassifier, NaiveBayes


def main():
    # scrape the data from reddit (if you haven't already)
    while(True):
        response = input("Have you already scraped data? Y/N")
        if(response == "Y"):
            break
        elif(response == "N"):
            client_id = input("What is the client id?")
            client_secret = input("What is the client 'secret'?")
            user_agent = input("What is the user agent?")

            reddit = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent)

            # scrape r/politics and r/The_Donald for data
            subreddit_scraper(reddit)
            break
        else:
            print("That was not a valid option, please try again.")

    donald_distributions_bars = []
    donald_distributions_points = []
    politics_distributions_bars = []
    politics_distributions_points = []

    # preprocess comments and find their distributions (if you haven't already)
    while (True):
        response = input("Have you already preprocessed the data? Y/N")
        if (response == "Y"):
            f = open("data/politics_points.pickle", 'rb')
            politics_distributions_points = pickle.load(f)
            f.close()

            h = open("data/politics_bars.pickle", 'rb')
            politics_distributions_bars = pickle.load(h)
            h.close()

            g = open("data/donald_points.pickle", 'rb')
            donald_distributions_points = pickle.load(g)
            g.close()

            k = open("data/donald_bars.pickle", 'rb')
            donald_distributions_bars = pickle.load(k)
            k.close()



            break
        elif (response == "N"):
            # put the comments through preprocessing/cleaning
            preprocess_comments()

            donald_data = ["data/donald_2016_processed.csv", "data/donald_2017_processed.csv",
                           "data/donald_2018_processed.csv", "data/donald_2019_processed.csv"]
            politics_data = ["data/politics_2016_processed.csv", "data/politics_2017_processed.csv",
                             "data/politics_2018_processed.csv", "data/politics_2019_processed.csv"]

            for data in donald_data:
                dbar_distribution, dpoints_distribution = scores_distribution(data)
                donald_distributions_bars.append(dbar_distribution)
                donald_distributions_points.append(dpoints_distribution)
            for data in politics_data:
                pbar_distribution, ppoints_distribution = scores_distribution(data)
                politics_distributions_bars.append(pbar_distribution)
                politics_distributions_points.append(ppoints_distribution)

            f = open("data/politics_points.pickle", 'wb')
            pickle.dump(politics_distributions_points, f)
            f.close()

            h = open("data/politics_bars.pickle", 'wb')
            pickle.dump(politics_distributions_bars, h)
            h.close()

            g = open("data/donald_points.pickle", 'wb')
            pickle.dump(donald_distributions_points, g)
            g.close()

            k = open("data/donald_bars.pickle", 'wb')
            pickle.dump(donald_distributions_bars, k)
            k.close()

            break
        else:
            print("That was not a valid option, please try again.")

    donald_plot_names = ["2016 r/The_Donald Sentiment Distribution", "2017 r/The_Donald Sentiment Distribution",
                         "2018 r/The_Donald Sentiment Distribution", "2019 r/The_Donald Sentiment Distribution"]
    bdonald_filenames = ["Results/2016DonaldBar.png", "Results/2017DonaldBar.png", "Results/2018DonaldBar.png",
                         "Results/2019DonaldBar.png"]
    hdonald_filenames = ["Results/2016DonaldHist.png", "Results/2017DonaldHist.png",
                         "Results/2018DonaldHist.png",
                         "Results/2019DonaldHist.png"]
    politics_plot_names = ["2016 r/politics Sentiment Distribution", "2017 r/politics Sentiment Distribution",
                           "2018 r/politics Sentiment Distribution", "2019 r/politics Sentiment Distribution"]
    bpolitics_filenames = ["Results/2016politicsBar.png", "Results/2017politicsBar.png",
                           "Results/2018politicsBar.png",
                           "Results/2019politicsBar.png"]
    hpolitics_filenames = ["Results/2016politicsHist.png", "Results/2017politicsHist.png",
                           "Results/2018politicsHist.png",
                           "Results/2019politicsHist.png"]

    all_donald = []
    for lst in donald_distributions_points:
        all_donald = all_donald + lst

    all_politics = []
    for lst in politics_distributions_points:
        all_politics = all_politics + lst


    # plot your results (if you haven't already)
    while (True):
        response = input("Have you already made your graphs (bar and histogram)? Y/N")
        if (response == "Y" or response=="y"):
            break
        elif (response == "N" or response=="n"):

            for i in range(len(donald_plot_names)):
                bar_plotter(donald_distributions_bars, donald_plot_names[i], bdonald_filenames[i])
                bar_plotter(politics_distributions_bars, politics_plot_names[i], bpolitics_filenames[i])
                point_plotter(donald_distributions_points, donald_plot_names[i], hdonald_filenames[i])
                point_plotter(politics_distributions_points, politics_plot_names[i], hpolitics_filenames[i])
            break
        else:
            print("That was not a valid option, please try again. Enter Y/N")

    d2016comments = pd.read_csv("data/donald_2016_processed.csv", sep=',')
    d2017comments = pd.read_csv("data/donald_2017_processed.csv", sep=',')
    d2018comments = pd.read_csv("data/donald_2018_processed.csv", sep=',')
    d2019comments = pd.read_csv("data/donald_2019_processed.csv", sep=',')
    p2016comments = pd.read_csv("data/politics_2016_processed.csv", sep=',')
    p2017comments = pd.read_csv("data/politics_2017_processed.csv", sep=',')
    p2018comments = pd.read_csv("data/politics_2018_processed.csv", sep=',')
    p2019comments = pd.read_csv("data/politics_2019_processed.csv", sep=',')
    all_donald_comments = d2016comments["0"].values.tolist() + d2017comments["0"].values.tolist() + \
                          d2018comments["0"].values.tolist() + d2019comments["0"].values.tolist()
    all_politics_comments = p2016comments["0"].values.tolist() + p2017comments["0"].values.tolist() + \
                            p2018comments["0"].values.tolist() + p2019comments["0"].values.tolist()



    # the first three classifiers
    while (True):
        response = input("Have you already run the Normal, TF, and Combo Classifiers? Y/N")
        if (response == "Y" or response=="y"):
            break
        elif (response == "N" or response=="n"):
            # begin to classify
            dname = "All Donald Histogram"
            dfilename = "Results/AllDonaldHist.png"
            pname = "All Politics Histogram"
            pfilename = "Results/AllPoliticsHist.png"

            donald_stats = normal_stats(all_donald, dname, dfilename, color='r')
            politics_stats = normal_stats(all_politics, pname, pfilename, color='b')
            # file_output(all_donald, all_politics, donald_plot_names, politics_plot_names)


            print("Using the Normal Distribution Classifier:")
            donald_normal_classifications = normal_classifier("data/donald_2020_processed.csv", donald_stats,
                                                              politics_stats)
            politics_normal_classifications = normal_classifier("data/politics_2020_processed.csv", donald_stats,
                                                                politics_stats)

            num_d = 0
            num_p = 0
            dcorrect = 0
            for i in range(len(donald_normal_classifications)):
                if donald_normal_classifications[i] == 1:
                    dcorrect += 1
                    num_d += 1
                elif donald_normal_classifications[i] == -1:
                    num_p += 1
            print(
                "The proportion of donald correctly labeled was: " + str(dcorrect / len(donald_normal_classifications)))

            pcorrect = 0
            for i in range(len(politics_normal_classifications)):
                if politics_normal_classifications[i] == -1:
                    pcorrect += 1
                    num_p += 1
                elif politics_normal_classifications[i] == 1:
                    num_d += 1
            print("The proportion of politics correctly labeled was: " + str(
                pcorrect / len(politics_normal_classifications)))
            correct_given_donald_normal = dcorrect / num_d
            correct_given_politics_normal = pcorrect / num_p
            print("The proportion of those labeled donald that were right: " + str(correct_given_donald_normal))
            print("The proportion of those labeled politics that were right: " + str(correct_given_politics_normal))

            print("Using the Term Frequency Classifier:")


            donald_prob_map = wordToProbMapper(all_donald_comments)
            politics_prob_map = wordToProbMapper(all_politics_comments)

            donald_term_classifications = term_frequency_classifier("data/donald_2020_processed.csv", donald_prob_map,
                                                                    politics_prob_map)
            politics_term_classifications = term_frequency_classifier("data/politics_2020_processed.csv",
                                                                      donald_prob_map, politics_prob_map)

            num_d = 0
            num_p = 0
            dcorrect = 0
            for i in range(len(donald_term_classifications)):
                if donald_term_classifications[i] == 1:
                    dcorrect += 1
                    num_d += 1
                elif donald_term_classifications[i] == -1:
                    num_p += 1
            print("The proportion of donald correctly labeled was: " + str(dcorrect / len(donald_term_classifications)))

            pcorrect = 0
            for i in range(len(politics_term_classifications)):
                if politics_term_classifications[i] == -1:
                    pcorrect += 1
                    num_p += 1
                elif politics_term_classifications[i] == 1:
                    num_d += 1
            print("The proportion of politics correctly labeled was: " + str(
                pcorrect / len(politics_term_classifications)))

            correct_given_donald_term = dcorrect / num_d
            correct_given_politics_term = pcorrect / num_p
            print("The proportion of those labeled donald that were right: " + str(correct_given_donald_term))
            print("The proportion of those labeled politics that were right: " + str(correct_given_politics_term))

            print("Using the Combined Classifier")
            num_d = 0
            num_p = 0
            dcorrect = 0
            dclass = []
            for comment in all_donald_comments:
                i = ComboClassifier(comment, correct_given_donald_normal, correct_given_politics_normal,
                                    correct_given_donald_term,
                                    correct_given_politics_term, donald_prob_map, politics_prob_map, donald_stats,
                                    politics_stats)
                dclass.append(i)
                if i == 1:
                    dcorrect += 1
                    num_d += 1
                elif i == -1:
                    num_p += 1
            print("The proportion of donald correctly labeled was: " + str(dcorrect / len(dclass)))

            pclass = []
            pcorrect = 0
            for comment in all_politics_comments:
                i = ComboClassifier(comment, correct_given_donald_normal, correct_given_politics_normal,
                                    correct_given_donald_term,
                                    correct_given_politics_term, donald_prob_map, politics_prob_map, donald_stats,
                                    politics_stats)
                pclass.append(i)
                if i == -1:
                    pcorrect += 1
                    num_p += 1
                elif i == 1:
                    num_d += 1
            print("The proportion of politics correctly labeled was: " + str(pcorrect / len(pclass)))

            correct_given_donald_combo = dcorrect / num_d
            correct_given_politics_combo = pcorrect / num_p
            print("The proportion of those labeled donald that were right: " + str(correct_given_donald_combo))
            print("The proportion of those labeled politics that were right: " + str(correct_given_politics_combo))

            break
        else:
            print("That was not a valid option, please try again. Enter Y/N")


    print("Using the Naive Bayes Classifier:")
    donald_nb_classifications = NaiveBayes(all_donald_comments, all_politics_comments, "data/donald_2020_processed.csv")
    politics_nb_classifications = NaiveBayes(all_donald_comments, all_politics_comments, "data/politics_2020_processed.csv")

    num_d = 0
    num_p = 0
    dcorrect = 0
    for i in range(len(donald_nb_classifications)):
        if donald_nb_classifications[i] == 1:
            dcorrect += 1
            num_d += 1
        elif donald_nb_classifications[i] == 0:
            num_p += 1
    print(
        "The proportion of donald correctly labeled was: " + str(dcorrect / len(donald_nb_classifications)))

    pcorrect = 0
    for i in range(len(politics_nb_classifications)):
        if politics_nb_classifications[i] == 0:
            pcorrect += 1
            num_p += 1
        elif politics_nb_classifications[i] == 1:
            num_d += 1
    print("The proportion of politics correctly labeled was: " + str(pcorrect / len(politics_nb_classifications)))
    correct_given_donald_nb = dcorrect / num_d
    correct_given_politics_nb = pcorrect / num_p
    print("The proportion of those labeled donald that were right: " + str(correct_given_donald_nb))
    print("The proportion of those labeled politics that were right: " + str(correct_given_politics_nb))



if __name__ == "__main__":
    main()

