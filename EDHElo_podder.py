import pathlib
from datetime import datetime
import pandas as pd
from EDHElo_secrets import SHEET_ID, SHEET_NAME

# get Google Sheets secrets from EDHElo_secrets.py
url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
players = []
podSizes = {"threes": 0, "fours": 0, "fives": 0, "total": 0}
pods = {}
gameDate = datetime.now().strftime("%Y%m%dT%H%M%S")


def main():
    # fetch player data from Google Sheet, randomize, then sort by rating
    # sheet is two columns, "Player Name" and "Bracket"
    players = fetchPlayerData().sample(frac=1).sort_values(by='Bracket', ascending=True)

    # determine number and size of pods
    genPodSizes(players)

    # put players into each pod
    genPodAssignments(players)

    # print pods to console
    for key in pods.keys():
        print("\n" + "#" * 30)
        print(key)
        print(pods[key])
    print("#" * 30)

    # write pods to file
    with open(pathlib.Path(__file__).parent / 'logs' / (gameDate + "_pods.txt"), 'a') as f:
        f.write(gameDate + " " + str(podSizes))
        for key in pods.keys():
            f.write("\n" + "#" * 30)
            f.write("\n" + key)
            f.write(pods[key].to_string())
        f.write("\n" + "#" * 30)

    # write log file
    with open(pathlib.Path(__file__).parent / 'logs' / (gameDate + "_db.txt"), 'a') as f:
        f.write(gameDate + " " + str(podSizes) + "\n")
        for key in pods.keys():
            f.write(pods[key].to_string(index=False, header=False))
            f.write("\n")

    prettyPrintPods(pods)


def fetchPlayerData():
    # use pandas to retrieve data from a Google Sheet
    return pd.read_csv(url)


def genPodSizes(players):
    # update the podSizes dictionary
    numPlayers = len(players)

    match numPlayers:
        case _ if numPlayers < 3:
            print(numPlayers, "players?! tsk tsk")
            exit()
        case _ if numPlayers % 4 == 0:
            podSizes["fours"] = int(numPlayers / 4)
        case 3 | 6 | 9:
            podSizes["threes"] = int(numPlayers / 3)
        case 5:
            podSizes["fives"] = 1
        case _:
            podSizes["threes"] = 4 - numPlayers % 4
            podSizes["fours"] = int((numPlayers - podSizes["threes"] * 3) / 4)

    podSizes["total"] = sum(podSizes.values())


def genPodAssignments(players):
    # generates and fills keys for pods{}
    indexPos = 0
    for p in range(podSizes["total"]):
        podName = "Pod " + str(p + 1)
        match p:
            case _ if p < podSizes["threes"]:
                pods[podName] = pd.DataFrame(players.iloc[indexPos:indexPos + 3])
                indexPos += 3
            case _ if (p >= podSizes["threes"]) & (p < (podSizes["threes"] + podSizes["fours"])):
                pods[podName] = pd.DataFrame(players.iloc[indexPos:indexPos + 4])
                indexPos += 4
            case _ if (p >= (podSizes["threes"] + podSizes["fours"])):
                pods[podName] = pd.DataFrame(players.iloc[indexPos:indexPos + 5])
            case _:
                print("zuh?")


def prettyPrintPods(pods):
    with open(pathlib.Path(__file__).parent / 'logs' / (gameDate + "_prettypods.html"), 'a') as f:
        f.write(
            "<!DOCTYPE html><html><head><meta name=\"viewport\"content=\"width=device-width,initial-scale=1\"><style>*{box-sizing:border-box;padding:2px;gap:2px;font-size:4vw;font-family:Sans-Serif}.row{display:flex;}.column{flex:50%;padding:10px;border:1px solid black;border-radius:10px 30px}</style></head><body><h2>Commander Pods " + gameDate.split("T")[0] + "</h2>")
        for i, (key, value) in enumerate(pods.items()):
            if i % 2 == 0:
                f.write("<div class=\"row\">")
            f.write("<div class=\"column\">")
            f.write("<strong>" + key + "</strong>")
            f.write("<br>")
            f.write("<br>".join(''.join([i for i in value.to_string(
                index=False, header=False) if not i.isdigit()]).split("\n")))
            f.write("</div>")
            if i % 2 == 1:
                f.write("</div>")
        f.write("</body></html>")


main()
