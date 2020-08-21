import numpy as np
import requests
import time
import pandas as pd
from numpy.random import rand


def submissions_pushshift_praw(reddit, subreddit, start=None, end=None, limit=100, extra_query=""):
    """
    A simple function that returns a list of PRAW submission objects during a particular period from a defined sub.
    This function serves as a replacement for the now deprecated PRAW `submissions()` method.

    :param subreddit: A subreddit name to fetch submissions from.
    :param start: A Unix time integer. Posts fetched will be AFTER this time. (default: None)
    :param end: A Unix time integer. Posts fetched will be BEFORE this time. (default: None)
    :param limit: There needs to be a defined limit of results (default: 100), or Pushshift will return only 25.
    :param extra_query: A query string is optional. If an extra_query string is not supplied,
                        the function will just grab everything from the defined time period. (default: empty string)

    Submissions are yielded newest first.

    For more information on PRAW, see: https://github.com/praw-dev/praw
    For more information on Pushshift, see: https://github.com/pushshift/api
    """
    matching_praw_submissions = []

    # Default time values if none are defined (credit to u/bboe's PRAW `submissions()` for this section)
    utc_offset = 28800
    now = int(time.time())
    start = max(int(start) + utc_offset if start else 0, 0)
    end = min(int(end) if end else now, now) + utc_offset

    # Format our search link properly.
    search_link = ('https://api.pushshift.io/reddit/submission/search/'
                   '?subreddit={}&after={}&before={}&sort_type=score&sort=asc&limit={}&q={}')
    search_link = search_link.format(subreddit, start, end, limit, extra_query)

    # Get the data from Pushshift as JSON.
    retrieved_data = requests.get(search_link)
    returned_submissions = retrieved_data.json()['data']

    # Iterate over the returned submissions to convert them to PRAW submission objects.
    for submission in returned_submissions:
        # Take the ID, fetch the PRAW submission object, and append to our list
        praw_submission = reddit.submission(id=submission['id'])
        matching_praw_submissions.append(praw_submission)

    # Return all PRAW submissions that were obtained.
    return matching_praw_submissions




def subreddit_scraper(reddit):

    sub_donald = reddit.subreddit('the_donald')
    sub_donald.quaran.opt_in()
    sub_left = reddit.subreddit('politics')


    donald_filenames = ["donald_2016", "donald_2017", "donald_2018", "donald_2019", "donald_2020"]
    politics_filenames = ["politics_2016", "politics_2017", "politics_2018", "politics_2019", "politics_2020"]
    timestamps = {0: [1451606400, 1483228800], 1:[1483228800, 1514764800], 2:[1514764800, 1546300800], 3:[1546300800, 1577836800], 4:[1577836800, 1580515200]}

    i = 0
    while i < 4:
        # the start timestamp for both subreddits is for February 11, 2019, exactly one year ago from when this data was collected!
        print("Beginning the " + donald_filenames[i] + ".csv")
        counter = 0
        donald_comments = []
        all_d_submissions = submissions_pushshift_praw(reddit=reddit, subreddit=sub_donald, start=timestamps[i][0], end=timestamps[i][1], limit=100000000)
        prob_d = 1000/len(all_d_submissions)
        for submission in all_d_submissions:
            if rand() < prob_d:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if("**[Content Policy]" not in comment.body):
                        donald_comments.append(comment.body)
                        counter += 1
                        if counter % 1000 == 0:
                            print("There are " + str(counter) + " comments.")

        donald_array = np.array(donald_comments)
        print("There are " + str(len(donald_array)) + " total comments.")

        pd.DataFrame(donald_array).to_csv("data/"+donald_filenames[i]+".csv")


        print("Beginning the " + politics_filenames[i] + ".csv")
        counter2 = 0
        left_comments = []
        all_p_submissions = submissions_pushshift_praw(reddit=reddit, subreddit=sub_left, start=timestamps[i][0], end=timestamps[i][1], limit=100000000)
        prob_p = 400 / len(all_p_submissions)
        for submission in all_p_submissions:
            if rand() < prob_p:
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    if("As a reminder, this subreddit" not in comment.body):
                        left_comments.append(comment.body)
                        counter2 += 1
                        if counter2 % 1000 == 0:
                            print("There are " + str(counter2) + " comments.")


        left_array = np.array(left_comments)
        print("There are " + str(len(left_array)) + " total comments.")
        pd.DataFrame(left_array).to_csv("data/"+politics_filenames[i]+".csv")


        i += 1

