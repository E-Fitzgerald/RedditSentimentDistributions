import emoji
import pandas as pd
from nltk.corpus import stopwords
import re
from nltk import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import string

lm = WordNetLemmatizer()

def space_emojis(comment):
    output_string = ""
    for c in comment:
        if( c in emoji.UNICODE_EMOJI):
            output_string = output_string + " " + c
        else:
            output_string = output_string + c

    return(output_string)


# start replaceTwoOrMore
#this is normalization
def replaceTwoOrMore(word):
    # look for 2 or more repetitions of character
    pattern = re.sub(r"(.)\1{1,}", r"\1\1", word)
    return pattern

# start process_tweet
def processComment(comment):
    comment = comment.replace("...", " ")
    string_ = []
    for e in comment.lower():
        if e in string.ascii_lowercase:
            string_.append(e)
        elif e == " ":
            string_.append(e)
    processComment = ''.join(string_)

    return processComment


#tokenization and stemming
def tokenize_stem(comment):
    words = word_tokenize(comment)
    token_comment = ""
    for word in words:
        token_comment = token_comment + lm.lemmatize(word) + " "
    return token_comment

def remove_stopwords(comment):
    words = word_tokenize(comment, language="english")
    rebuilt_comment = ""
    for word in words:
        # replace two or more with two occurrences
        word = replaceTwoOrMore(word)
        # strip punctuation
        # word = word.strip('\'"?,.')
        # ignore if it is a stopWord
        if (word in set(stopwords.words('english'))):
            rebuilt_comment = rebuilt_comment + ""
        else:
            rebuilt_comment = rebuilt_comment + word + " "
    return rebuilt_comment


def preprocess_comments():
    input_files = ["data/donald_2016.csv", "data/donald_2017.csv", "data/donald_2018.csv", "data/donald_2019.csv",
                   "data/politics_2016.csv", "data/politics_2017.csv", "data/politics_2018.csv", "data/politics_2019.csv"]

    output_files = ["data/donald_2016_processed.csv", "data/donald_2017_processed.csv", "data/donald_2018_processed.csv", "data/donald_2019_processed.csv",
                   "data/politics_2016_processed.csv", "data/politics_2017_processed.csv", "data/politics_2018_processed.csv", "data/politics_2019_processed.csv"]


    for j in range(0, len(input_files)):
        print("Processing " + input_files[j])
        #import the spreadsheets of tweets and convert excel to pd df
        xl = pd.read_csv(input_files[j], sep=',')
        inComments = pd.DataFrame(xl)
        #import the stopwords
        stopWords = stopwords.words("english")



        #process the tweets
        featureList = []
        tweets = []
        outTweets = pd.DataFrame([])
        print("Cleaning...")
        for k in range(0,len(inComments["0"]),1):
            inComments.at[k ,"0"] = processComment(inComments["0"][k])

        print("Removing stopwords...")
        for k in range(0, len(inComments["0"]), 1):
            inComments.at[k, "0"] = remove_stopwords(inComments["0"][k])

        print("Lemmatizing...")
        for k in range(0,len(inComments["0"]),1):
            inComments.at[k ,"0"] = tokenize_stem(inComments["0"][k])

        print("Spacing emojis...")
        for k in range(0,len(inComments["0"]),1):
            inComments.at[k ,"0"] = space_emojis(inComments["0"][k])


        inComments.to_csv(output_files[j], index=False)
        print("")
