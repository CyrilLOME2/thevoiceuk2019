import csv
from math import log


def write_csv_calculated_marks(path_input, path_output):
    """
    :param path_input: path of csv file after KPPV and W2V
    :param path_output: path where to put the csv with the marks
    """
    csv_notes_list = []
    with open(path_input) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader :
            csv_notes = {}
            csv_notes['id_tweet'] = row['id_tweet']
            csv_notes['id_candidat'] = row['id_candidate']
            csv_notes['sum_rt_com_like'] = row['score_importance']
            sum_mark = 0
            for i in range(1,6):
                sum_mark += float(row['notation_' + str(i)])
            if row['nb_smiley_happy'] == '0' and row['nb_smiley_unhappy'] == '0':
                csv_notes['note'] = sum_mark / 5
            else :
                note_smiley = calculate_smiley_mark(int(row['nb_smiley_happy']), int(row['nb_smiley_unhappy']))
                csv_notes['note'] = (sum_mark + note_smiley) / 6
            csv_notes_list.append(csv_notes)
    with open(path_output, 'w', newline='') as csvfile:
        fieldnames = ['id_tweet', 'id_candidat', 'sum_rt_com_like', 'note']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for csv_notes in csv_notes_list:
            writer.writerow(csv_notes)


def calculate_smiley_mark(nb_happy, nb_unhappy):
    if nb_happy > 0 and nb_unhappy > 0:
        return 3
    elif nb_happy == 1 :
        return 4
    elif nb_happy > 1 :
        return 5
    elif nb_unhappy == 1:
        return 2
    else :
        return 0


def write_csv_calculating_ranking(path_input, path_output):
    """
    :param path_input: path of csv file containing the marks for each tweet
    :param path_output: path where the write the file with the ranking
    """
    score_candidate = {}
    with open(path_input) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            score = log(int(row["sum_rt_com_like"]) + 2) * (float(row["note"]))
            if row["id_candidat"] not in score_candidate:
                score_candidate[row["id_candidat"]] = score
            else :
                score_candidate[row["id_candidat"]] += score
    list_score_canidate = []
    rank = 0
    
    while score_candidate != {}:
        rank += 1
        max_candidate = None
        for candidate in score_candidate:
            if not max_candidate:
                max_candidate = candidate
            elif score_candidate[candidate] > score_candidate[max_candidate]:
                max_candidate = candidate
        list_score_canidate.append(
            {'ranking' : rank,
             'candidate' : id_candidate_to_candidate(max_candidate),
             'score' : score_candidate[max_candidate]})
        del score_candidate[max_candidate]
        
    with open(path_output, 'w', newline='') as csvfile:
        fieldnames = ['ranking', 'candidate', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for csv_score in list_score_canidate:
            writer.writerow(csv_score)

def id_candidate_to_candidate(id):
    fcandidate = open('Cadidate2019.txt', 'r', encoding = 'utf-8')
    Lcandidate = fcandidate.readlines()
    fcandidate.close()
    return(Lcandidate[int(id)].rstrip())
    
    
if __name__ == '__main__':

    path_input = "template/5nn-results-tweets_2019-01-04_2019-01-30_clean.csv"
    path_output = "template/mark-5nn-results-tweets_2019-01-04_2019-01-30_clean.csv"
    write_csv_calculated_marks(path_input, path_output)

    path_input = "template/mark-5nn-results-tweets_2019-01-04_2019-01-30_clean.csv"
    path_output = "template/ranking-mark-5nn-results-tweets_2019-01-04_2019-01-30_clean.csv"
    write_csv_calculating_ranking(path_input, path_output)