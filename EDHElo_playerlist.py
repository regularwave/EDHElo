import pyperclip

text = pyperclip.paste()

playerList = text.split("\n")

for i, line in enumerate(playerList):
    if line.strip() == "LAST NAME":
        playerList = playerList[i+1:]
        break

for i, line in enumerate(playerList):
    if line.strip() == "Companion App Lobby":
        playerList = playerList[:i]
        break

playerList = [line.rstrip() for line in playerList]

formatted_plist = [last_name + ', ' + first_name for first_name, last_name in zip(playerList[::2], playerList[1::2])]

pyperclip.copy('\n'.join(formatted_plist))