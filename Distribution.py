import pandas as pd

red_pill = pd.read_csv("TheRedPill.tsv",
                  sep='\t',
                  names=["Word", "Mean Sent.", "STD Sent."])
politics = pd.read_csv("politics.tsv",
                  sep='\t',
                  names=["Word", "Mean Sent.", "STD Sent."])


def scores_distribution(filename):
    print("Reviewing " + filename)
    comments = pd.read_csv(filename, sep=',')
    scores = {"Negative":0, "Neutral":0, "Positive":0}

    if "donald" in filename:
        sentiment_list = red_pill["Word"].values
        data = red_pill
    else:
        sentiment_list = politics["Word"].values
        data = politics

    count = 0
    for comment in comments["0"]:
        if count % 500 == 0:
            print("Reviewed "+ str(count)+ " comments.")
        if type(comment) != float:
            positive_words = 0
            positive_sum = 0
            negative_words = 0
            negative_sum = 0
            words = comment.split(" ")
            for word in words:
                if word in sentiment_list:
                    row = data.loc[data['Word'] == word]
                    score = float(row["Mean Sent."])
                    if score < 0.0:
                        negative_words += 1
                        negative_sum += score
                    elif score > 0.0:
                        positive_words += 1
                        positive_sum += score

            percent_pos = positive_words/len(words)
            percent_neg = negative_words/len(words)
            positive_score = percent_pos * positive_sum
            negative_score = percent_neg * negative_sum
            difference = abs(positive_score - abs(negative_score))

            if(difference <= .5):
                scores["Neutral"] += 1
            elif(abs(negative_score) > positive_score):
                scores["Negative"] += 1
            elif(positive_score > abs(negative_score)):
                scores["Positive"] += 1

            count +=1


    print("")
    return scores
