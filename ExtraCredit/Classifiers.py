import math
import pandas as pd
from DistributionCS109 import calculate_score

def normal(dist_stats_donald, dist_stats_politics, score):
    prob_donald = (1 / (dist_stats_donald["Std."] * math.sqrt(math.pi * 2))) * math.exp(
        (-(score - dist_stats_donald["Mean"]) ** 2) / (2 * (dist_stats_donald["Std."]) ** 2))
    prob_politics = (1 / (dist_stats_politics["Std."] * math.sqrt(math.pi * 2))) * math.exp(
        (-(score - dist_stats_politics["Mean"]) ** 2) / (2 * (dist_stats_politics["Std."]) ** 2))

    if (prob_politics != 0):
        donald_politics = prob_donald / prob_politics
    else:
        if prob_donald == 0:
            donald_politics = 1
        else:
            donald_politics = 2

    if (donald_politics > 1):
        return 1, prob_donald-prob_politics
    else:
        return -1, prob_politics-prob_donald

def normal_classifier(filename, dist_stats_donald, dist_stats_politics):
    comments = pd.read_csv(filename, sep=',')

    red_pill = pd.read_csv("TheRedPill.tsv",
                           sep='\t',
                           names=["Word", "Mean Sent.", "STD Sent."])
    politics = pd.read_csv("politics.tsv",
                           sep='\t',
                           names=["Word", "Mean Sent.", "STD Sent."])

    sentiment_list_d = red_pill["Word"].values
    sentiment_list_p = politics["Word"].values

    classifications =[]

    count = 0

    for comment in comments["0"]:
        comment_ = str(comment)

        classification_score_1 = calculate_score(comment_, sentiment_list_d, red_pill)
        classification_score_2 = calculate_score(comment_, sentiment_list_p, politics)

        class_donald, dwinning_prob = normal(dist_stats_donald, dist_stats_politics, classification_score_1)
        class_politics, pwinning_prob = normal(dist_stats_donald, dist_stats_politics, classification_score_2)

        if (class_donald == class_politics):
            classification_normal = class_donald
        elif dwinning_prob > pwinning_prob:
            classification_normal = class_donald
        elif pwinning_prob > dwinning_prob:
            classification_normal = class_politics
        else:
            classification_normal = 0

        classifications.append(classification_normal)

        count+=1

    return classifications

def wordToProbMapper(list):
    comments = list
    prob_map = {}
    for comment in comments:
        comment_ = str(comment)
        for word in comment_.split(" "):
            if word not in prob_map.keys():
                prob_map[word] = 1
            else:
                prob_map[word] += 1
    total_words = len(prob_map)
    for key in prob_map.keys():
        prob_map[key] = prob_map[key]/total_words

    return prob_map


def term_frequency(comments, prob_map_donald, prob_map_politics):
    classifications = []
    bigger_prob = 1
    for comment in comments:
        comment_ = str(comment)
        words = comment_.split(" ")
        logprob_donald = 0
        logprob_politics = 0
        for word in words:
            dprob = 1
            pprob = 1
            if word in prob_map_politics.keys():
                pprob = prob_map_politics[word]
            if word in prob_map_donald.keys():
                dprob = prob_map_donald[word]
            logprob_donald += math.log(dprob)
            logprob_politics += math.log(pprob)


        if (logprob_donald > logprob_politics):
            bigger_prob = logprob_donald-logprob_politics
            classifications.append(1)
        elif (logprob_donald < logprob_politics):
            bigger_prob = logprob_politics-logprob_donald
            classifications.append(-1)
        else:
            classifications.append(0)

    return classifications, bigger_prob

def term_frequency_classifier(filename, prob_map_donald, prob_map_politics):
    comments = pd.read_csv(filename, sep=',')
    output1, output2 = term_frequency(comments["0"],  prob_map_donald, prob_map_politics)
    return output1


def ComboClassifier(comment, correct_given_donald_normal, correct_given_politics_normal, correct_given_donald_term,
                    correct_given_politics_term, prob_map_donald, prob_map_politics, dist_stats_donald, dist_stats_politics):
    red_pill = pd.read_csv("TheRedPill.tsv",
                           sep='\t',
                           names=["Word", "Mean Sent.", "STD Sent."])
    politics = pd.read_csv("politics.tsv",
                           sep='\t',
                           names=["Word", "Mean Sent.", "STD Sent."])

    sentiment_list_d = red_pill["Word"].values
    sentiment_list_p = politics["Word"].values

    classification_score_1 = calculate_score(comment, sentiment_list_d, red_pill)
    classification_score_2 = calculate_score(comment, sentiment_list_p, politics)

    class_donald, dwinning_prob = normal(dist_stats_donald, dist_stats_politics, classification_score_1)
    class_politics, pwinning_prob = normal(dist_stats_donald, dist_stats_politics, classification_score_2)
    winning_prob_normal = 1

    if(class_donald == class_politics):
        classification_normal = class_donald
    elif dwinning_prob > pwinning_prob:
        classification_normal = class_donald
        winning_prob_normal = dwinning_prob
    elif pwinning_prob > dwinning_prob:
        classification_normal = class_politics
        winning_prob_normal = pwinning_prob
    else:
        classification_normal = 0

    classification_term, winning_prob_term = term_frequency([comment], prob_map_donald, prob_map_politics)
    classification_term = classification_term[0]

    if classification_normal == 1:
        normal_score = classification_normal*correct_given_donald_normal * winning_prob_normal
    else:
        normal_score = classification_normal*correct_given_politics_normal * winning_prob_normal

    if (classification_term == 1):
        term_score = classification_term * correct_given_donald_term * winning_prob_term
    else:
        term_score = classification_term * correct_given_politics_term * winning_prob_term


    ultimate_score = normal_score + term_score
    if(ultimate_score < 0):
        return -1
    elif ultimate_score >0:
        return 1
    else:
        return 0

def NaiveBayes(all_donald_comments, all_politics_comments, test_data):
    comments = []
    for comment in all_donald_comments:
        comments.append(str(comment))
    for comment in all_politics_comments:
        comments.append(str(comment))
    print("Num Comments: " + str(len(comments)))

    scaling_factor = len(all_politics_comments)/len(all_donald_comments)

    dictionary = []
    for comment in comments:
        lst = comment.split(" ")
        for word in lst:
            dictionary.append(word)

    # do for donald
    d_count = {}
    p_count = {}
    for word in dictionary:
        d_count[word] = 0
        p_count[word] = 0

    num_donald = len(all_donald_comments)
    y_donald = (num_donald + 1) / (len(comments) + 2)
    num_politics = len(all_politics_comments)
    y_politics = (num_politics + 1) / (len(comments) + 2)

    for comment in all_donald_comments:
        lst = str(comment).split(" ")
        lst = list(dict.fromkeys(lst))
        for word in lst:
            d_count[word] += 1
    for comment in all_politics_comments:
        lst = str(comment).split(" ")
        lst = list(dict.fromkeys(lst))
        for word in lst:
            p_count[word] += 1


    # laplace
    data = pd.read_csv(test_data, sep=',')
    test_comments = [str(comment) for comment in data["0"]]
    assignments = []


    for comment in test_comments:
        prob_d = y_donald
        prob_p = y_politics
        lst = comment.split(" ")
        for word in lst:
            if word in dictionary:
                d_event = d_count[word] + 1
                p_event = p_count[word] + 1
                sample = d_count[word] + p_count[word] + 2
            else:
                d_event = 1
                p_event = 1
                sample = 2

            prob_d *= d_event / sample
            prob_p *= p_event / sample

        if (prob_d) > (prob_p):
            assignments.append(1)
        else:
            assignments.append(0)

    return assignments







    # print(donald_count)

    pass