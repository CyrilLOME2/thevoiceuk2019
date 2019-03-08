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
            csv_notes['id_candidat'] = row['id_candidat']
            csv_notes['sum_rt_com_like'] = row['sum_rt_com_like']
            sum_mark = 0
            for i in range(1,6):
                sum_mark += int(row['note_proche_voisin_' + str(i)])
            if row['smiley_happy'] == '0' and row['smiley_unhappy'] == '0':
                csv_notes['note'] = sum_mark / 5
            else :
                note_smiley = calculate_smiley_mark(int(row['smiley_happy']), int(row['smiley_unhappy']))
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
            score = log(int(row["sum_rt_com_like"])) * (float(row["note"]) - 3)
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
             'candidate' : max_candidate,
             'score' : score_candidate[candidate]})
        del score_candidate[max_candidate]
    with open(path_output, 'w', newline='') as csvfile:
        fieldnames = ['ranking', 'candidate', 'score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for csv_score in list_score_canidate:
            writer.writerow(csv_score)


if __name__ == '__main__':

    path_input = "template/output_W2V.csv"
    path_output = "template/output_marks_for_each_tweet.csv"
    write_csv_calculated_marks(path_input, path_output)

    path_input = "template/output_marks_for_each_tweet.csv"
    path_output = "template/output_final.csv"
    write_csv_calculating_ranking(path_input, path_output)