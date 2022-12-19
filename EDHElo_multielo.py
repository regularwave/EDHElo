import sys
from multielo import MultiElo

# check to see how many args were given
# if no scores were given as args, prompt for scores
# 0: prompt for 3 or more scores
# 1 or 2: not enough scores; exit
# 3 or more: send scores through to multielo
match len(sys.argv):
    case 1:
        nArgs = [int(x) for x in input("scores: ").replace(",", " ").split()]
        if len(nArgs) < 3:
            print("need more players")
            exit()
        # prompt
    case 2 | 3:
        print("need more players")
        exit()
    case _:
        nArgs = [int(x) for x in str(sys.argv[1:]).replace(
            "[", "").replace("]", "").replace("'", "").replace(",", " ").split()]

# set Elo K-factor; multielo uses a default of 32
# higher K-factor makes the point swing larger, which makes the ratings change "faster"
KFACTOR = 48
melo = MultiElo(k_value=KFACTOR)

# the first score is for the winning player, the rest of the players tie for second
wArr = [1]
for _ in range(len(nArgs) - 1):
    wArr.append(2)

# print the given ratings and then the new ratings
print("Old ratings:", nArgs)
print("New ratings:", [int(x) for x in melo.get_new_ratings(nArgs, wArr)])
