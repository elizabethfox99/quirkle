import random

import sys

max = 20

print("welcome to Lizzie's Quirkle game!")



# initialise stuff here
Board = {}
for y in range(0,max):
  for x in range(0,max):
    Board[x,y] = "--"

colors = ['r','o','y','g','b','p']
shapes = ['1','2','3','4','5','6']

distinct_pieces = [c+s for c in colors for s in shapes]

bag_of_pieces = distinct_pieces*3
random.shuffle(bag_of_pieces)
print(bag_of_pieces)
player1bag = []
player2bag = []

# print out the board state:
def printboard():
  for y in range(0,max):
    for x in range(0,max):
      sys.stdout.write(' '+Board[x,y])
    sys.stdout.write("\n")


def gameisfinished():
  if (not player1bag) or (not player2bag):
    return True
  else:
    return False


def refillbag(bag):
  pieces_remaining = len(bag_of_pieces)
  desired_number = 6 - len(bag)
  number_to_take = min(pieces_remaining, desired_number)
  for i in range(0,number_to_take):
    bag.append(bag_of_pieces.pop())

refillbag(player1bag)
refillbag(player2bag)


def processinput(userinput, bag):
  for piececommand in userinput.split(" "):
    components = piececommand.split(":")
    piecename = components[0]
    piececoords = components[1].split(',')
    x = piececoords[0]
    y = piececoords[1]

    print(piecename+x+y)



player1next=True
while not gameisfinished():
  if player1next:
    print "player 1's turn"
    print player1bag
    userinput = raw_input("please choose where to go (e.g. 'r1:30,40 r2:1,20'):")
    processinput(userinput, player1bag)
  else:
    print "player 2's turn"
    print player2bag
    userinput = raw_input("please choose where to go (e.g. 'r1:30,40'):")
    processinput(userinput, player1bag)

  player1next = not player1next

print "game is finished"

