import praw
from Scraper import subreddit_scraper
from Preprocessing import preprocess_comments
from Distribution import scores_distribution
from Results import plotter, file_output


def main():
    client_id = input("What is the client id?")
    client_secret = input("What is the client 'secret'?")
    user_agent = input("What is the user agent?")

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         user_agent=user_agent)

    # scrape r/politics and r/The_Donald for data
    subreddit_scraper(reddit)

    # put the comments through preprocessing/cleaning
    preprocess_comments()


    donald_data = ["data/donald_2016_processed.csv", "data/donald_2017_processed.csv", "data/donald_2018_processed.csv",
                   "data/donald_2019_processed.csv"]
    politics_data = ["data/politics_2016_processed.csv", "data/politics_2017_processed.csv",
                     "data/politics_2018_processed.csv", "data/politics_2019_processed.csv"]

    # determine the distribution of sentiments for both r/The_Donald and r/politcs
    donald_distributions = []
    politics_distributions = []
    for data in donald_data:
        donald_distributions.append(scores_distribution(data))
    for data in politics_data:
        politics_distributions.append(scores_distribution(data))

    donald_distributions = [{'Neutral': 912, 'Negative': 655, 'Positive': 378}, {'Neutral': 2167, 'Negative': 1513, 'Positive': 661}, {'Neutral': 1577, 'Negative': 1238, 'Positive': 532}, {'Neutral': 1885, 'Negative': 1494, 'Positive': 646}]
    politics_distributions = [{'Neutral': 1770, 'Negative': 2082, 'Positive': 1958}, {'Neutral': 2102, 'Negative': 2132, 'Positive': 2593}, {'Neutral': 2516, 'Negative': 2599, 'Positive': 3083}, {'Neutral': 3293, 'Negative': 3673, 'Positive': 4025}]

    donald_plot_names = ["2016 r/The_Donald Sentiment Distribution", "2017 r/The_Donald Sentiment Distribution",
                    "2018 r/The_Donald Sentiment Distribution", "2019 r/The_Donald Sentiment Distribution"]
    donald_filenames = ["Results/2016Donald.png", "Results/2017Donald.png", "Results/2018Donald.png", "Results/2019Donald.png"]
    politics_plot_names = ["2016 r/politics Sentiment Distribution", "2017 r/politics Sentiment Distribution",
                      "2018 r/politics Sentiment Distribution", "2019 r/politics Sentiment Distribution"]
    politics_filenames = ["Results/2016politics.png", "Results/2017politics.png", "Results/2018politics.png", "Results/2019politics.png"]

    # Print to a text file all the distributions and percentages
    for i in range(len(donald_distributions)):
        plotter(donald_distributions[i], donald_plot_names[i], donald_filenames[i], 'r')
        plotter(politics_distributions[i], politics_plot_names[i], politics_filenames[i], 'b')

    file_output(donald_distributions, politics_distributions, donald_plot_names, politics_plot_names)

if __name__ == "__main__":
    main()

