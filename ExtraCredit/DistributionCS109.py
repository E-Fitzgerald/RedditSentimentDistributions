import pandas as pd

red_pill = pd.read_csv("TheRedPill.tsv",
                       sep='\t',
                       names=["Word", "Mean Sent.", "STD Sent."])
politics = pd.read_csv("politics.tsv",
                       sep='\t',
                       names=["Word", "Mean Sent.", "STD Sent."])

def calculate_score(comment, sentiment_list, data):
    positive_words = 0
    positive_sum = 0
    negative_words = 0
    negative_sum = 0
    comment_ = str(comment)
    words = comment_.split(" ")
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

    percent_pos = positive_words / len(words)
    percent_neg = negative_words / len(words)
    positive_score = percent_pos * positive_sum
    negative_score = percent_neg * negative_sum
    return positive_score + negative_score

def scores_distribution(filename, use_donald = True):
    print("Reviewing " + filename)
    comments = pd.read_csv(filename, sep=',')
    scores = {"Very Neg.":0, "Mod. Neg.": 0, "Slight. Neg.":0, "Neutral": 0, "Slight Pos.":0, "Mod. Pos.": 0, "Very Pos.":0}
    raw_scores = []

    if use_donald:
        sentiment_list = red_pill["Word"].values
        data = red_pill
    else:
        sentiment_list = politics["Word"].values
        data = politics

    count = 0
    for comment in comments["0"]:
        if count % 500 == 0:
            print("Reviewed " + str(count) + " comments.")
        if type(comment) != float:
            difference = calculate_score(comment, sentiment_list, data)
            raw_scores.append(difference)

            if (difference <= .35 and difference >= -.35):
                scores["Neutral"] += 1
            elif (difference >= .35 and difference < 1):
                scores["Slight Pos."] += 1
            elif (difference >= 1 and difference < 2):
                scores["Mod. Pos."] += 1
            elif (difference >= 2):
                scores["Very Pos."] += 1
            elif (difference <= -.35 and difference > -1):
                scores["Slight. Neg."] += 1
            elif (difference <= -1 and difference > -2):
                scores["Mod. Neg."] += 1
            elif (difference <= -2):
                scores["Very Neg."] += 1

            count += 1

    print("")
    raw_scores.sort()
    return scores, raw_scores
