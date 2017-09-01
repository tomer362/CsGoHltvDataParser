import requests
from bs4 import BeautifulSoup

#const names
WINNER = "resultWinner"
LOSER = "resultLoser"

def get_data(add_page, name_list, file_name):

    if add_page == 0:
        url = "http://www.hltv.org/results/"
    else:
        url = "http://www.hltv.org/results/" + str(add_page * 50) + "/"
    print "Getting Data From:", url

    write_file = None
    source_code = requests.get(url)
    content = source_code.content
    soup = BeautifulSoup(content, "html.parser")

    game_boxes = soup.findAll('div', {'class': 'matchListBox'})
    if  add_page == 0:
        write_file = open(file_name, "w")
    else:
        write_file = open(file_name, "a")
    for game_box in game_boxes:
        try:
            team1_name = game_box.contents[1].find("div", {"class", "matchTeam1Cell"}).find("a").text.rstrip().lstrip()
            team2_name = game_box.contents[1].find("div", {"class", "matchTeam2Cell"}).find("a").text.rstrip().lstrip()
            team1_score = game_box.contents[1].find("div", {"class", "matchScoreCell"}).contents[1]
            team2_score = game_box.contents[1].find("div", {"class", "matchScoreCell"}).contents[3]
            team1_score_text = team1_score.text
            team2_score_text = team2_score.text
            team1_name.decode("ascii")
            team2_name.decode("ascii")

            if not(team1_name in name_list):
                if str(team1_score).find(WINNER) != -1:
                    name_list[team1_name] = [1, 0] #entering to a list of win/loss
                elif str(team1_score).find(LOSER) != -1:
                    name_list[team1_name] = [0, 1]
            else:
                if str(team1_score).find(WINNER) != -1:
                    name_list[team1_name][0] += 1 
                elif str(team1_score).find(LOSER) != -1:
                    name_list[team1_name][1] += 1

            if not(team2_name in name_list):
                if str(team2_score).find(WINNER) != -1:
                    name_list[team2_name] = [1, 0] #entering to a list of win/loss
                elif str(team2_score).find(LOSER) != -1:
                    name_list[team2_name] = [0, 1]
            else:
                if str(team2_score).find(WINNER) != -1:
                    name_list[team2_name][0] += 1 
                elif str(team2_score).find(LOSER) != -1:
                    name_list[team2_name][1] += 1
                    
            str_output = team1_name + " Vs. " + team2_name + "\n"
            write_file.write(str_output)
            str_output = game_box.contents[1].find("div", {"class", "matchTimeCell"}).text + "\n"
            write_file.write(str_output)

            str_output = team1_score_text + " - " + team2_score_text
            write_file.write(str_output)
            if game_box != game_boxes[len(game_boxes) - 1]:
                write_file.write("\n\n")
        except Exception as ex:
            print ex
    write_file.close()

    
if __name__ == "__main__":

    name_list = {}
    matches_file_name = raw_input("Choose Matches output file name: ") + ".txt"
    team_file_name = raw_input("Choose Team analysis file name: ") + ".txt"
    for i in xrange(0, input("Enter Max page number: ")):
        get_data(i, name_list, matches_file_name)
        
        teams_file = open(team_file_name, "w")
        teams_file.write("TEAMS (Win/Loss):\n")
        teams_file.write("-----------\n")
		#sorting by alphabetic names
        for team_name, team_scores in sorted(name_list.iteritems(), key = lambda x: x[1][0] - x[1][1], reverse = True):
            teams_file.write((team_name + " " + str(team_scores[0]) + "/" + str(team_scores[1])))
            #printing enter when its not the last row
            if team_name != name_list.keys()[-1]:
                teams_file.write("\n")
        teams_file.close()
    raw_input("Done!")