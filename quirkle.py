# Useful stuff for lizzie!

# To run this file, you'll need to the Terminal from the dock
# If it isn't there already, type `cd quirkle` then hit enter
# You can then run `python quirkle.py` to run it
# If you want to stop running it, press `Ctrl-C` (not cmd)

# Saving can be done with GitHub...
# You can `commit` work whenever you like, and you can always get back to a commit
# When you hit the `Sync` button, I can get your work on my computer too


import random
import sys
from termcolor import cprint

max_size = 20

# initialise stuff here
Board = {}
for y in range(0,max_size):
  for x in range(0,max_size):
    Board[x,y] = "--"

colors = ['r','o','y','g','b','p']
shapes = ['1','2','3','4','5','6']

distinct_pieces = [c+s for c in colors for s in shapes]

bag_of_pieces = distinct_pieces*3
random.shuffle(bag_of_pieces)
player1bag = []
player2bag = []

# print out the board state:
def printboard():
  for y in range(0,max_size):
    for x in range(0,max_size):
      bg = ''
      color = ''
      if Board[x,y][0] == "g":
        bg = 'on_green'
        color = 'grey'
      if Board[x,y][0] == "b":
        bg = 'on_cyan'
        color = 'grey'
      if Board[x,y][0] == "r":
        bg = 'on_red'
        color = 'grey'
      if Board[x,y][0] == "o":
        bg = 'on_cyan' #can't do orange in termbg
        color = 'yellow'
      if Board[x,y][0] == "y":
        bg = 'on_yellow'
        color = 'grey'
      if Board[x,y][0] == "p":
        bg = 'on_magenta'
        color = 'grey'
      if empty_square(x,y):
        bg = 'on_grey'
        color = 'white'
      
      cprint(Board[x,y], color, bg, end=' ')
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


def empty_square(x,y):
  return Board[x,y] == '--'

def in_bounds(x,y):
  return 0 <= x < max_size and 0 <= y < max_size

def has_adjacent(x,y):
  return (
            (in_bounds(x+1,y) and not empty_square(x+1,y)) or
            (in_bounds(x,y+1) and not empty_square(x,y+1)) or
            (in_bounds(x-1,y) and not empty_square(x-1,y)) or
            (in_bounds(x,y-1) and not empty_square(x,y-1))
         )


def list_of_same_shape(pieces):
  first_shape = pieces[0][1]
  for piece in pieces:
    if piece[1] != first_shape:
      return False
  return True

def list_of_same_color(pieces):
  first_color = pieces[0][0]
  for piece in pieces:
    if piece[0] != first_color:
      return False
  return True


def row(x,y,piecename):
  left_row = []
  next_cell_left = x-1
  while not empty_square(next_cell_left,y):
    left_row.insert(0,Board[next_cell_left,y])
    next_cell_left = next_cell_left-1
  right_row = []
  next_cell_right = x+1
  while not empty_square(next_cell_right,y):
    right_row.append(Board[next_cell_right,y])
    next_cell_right = next_cell_right+1
  return left_row+[piecename]+right_row

def column(x,y,piecename):
  pieces_above =[]
  pieces_below = []
  next_cell_above = y-1
  next_cell_below = y+1
  while not empty_square(x,next_cell_above):
    pieces_above.insert(0,Board[x,next_cell_above])
    next_cell_above = next_cell_above-1
  while not empty_square(x,next_cell_below):
    pieces_below.append(Board[x,next_cell_below])
    next_cell_below = next_cell_below+1
  return pieces_above+[piecename]+pieces_below



def get_error_message(piececommand, bag):
  components = piececommand.split(":")
  if len(components) != 2:
    return "Move should look like this p1:1,2"

  piecename = components[0]
  piececoords = components[1].split(',')
  x = int(piececoords[0])
  y = int(piececoords[1])

  if not piecename in bag:
    return "you don't have this piece in your bag DUH!"

  if not in_bounds(x,y):
    return "You must place your piece on the board"

  if not empty_square(x,y):
    return "You can't place a piece on top of another"

  if not has_adjacent(x,y):
    return "You must place your piece next to an existing piece"

  if not (list_of_same_shape(row(x,y,piecename)) or list_of_same_color(row(x,y,piecename))):
    return "You must place your piece to make a row of the same shape or color"

  if not (list_of_same_shape(column(x,y,piecename)) or list_of_same_color(column(x,y,piecename))):
    return "You must place your piece to make a column of the same shape or color"

  return ""


def execute_move(piececommand, bag):
  components = piececommand.split(":")
  piecename = components[0]
  piececoords = components[1].split(',')
  x = int(piececoords[0])
  y = int(piececoords[1])
  print row(x,y,piecename)
  print column(x,y,piecename)
  bag.remove(piecename)
  Board[x,y] = piecename



print("welcome to Lizzie's Quirkle game!")

refillbag(player1bag)
refillbag(player2bag)

printboard()

piecename = raw_input("please choose the first piece from your bag " + ','.join(player1bag) + ":\n")
while not piecename in player1bag:
  piecename = raw_input("please choose the first piece from your bag " + ','.join(player1bag) + ":\n")
player1bag.remove(piecename)
Board[max_size/2,max_size/2] = piecename
printboard()

while len(player1bag) > 0:
  userinput = raw_input("place another a piece from your bag " + ','.join(player1bag) + " (or hit enter to finish your turn):\n")
  if userinput == "":
    break
  while get_error_message(userinput, player1bag) != "":
    userinput = raw_input("Invalid move: ["+get_error_message(userinput, player1bag)+"] please place a piece (or hit enter to finish your turn): \n")
    if userinput == "":
      break
  execute_move(userinput, player1bag)
  printboard()

refillbag(player1bag)


player1next=False
while not gameisfinished():
  if player1next:
    print "player 1's turn"

    userinput = raw_input("please place a piece from your bag " + ','.join(player1bag) + ":\n")
    while get_error_message(userinput, player1bag) != "":
      userinput = raw_input("Invalid move: ["+get_error_message(userinput, player1bag)+"] please place a piece: \n")
    execute_move(userinput, player1bag)
    printboard()

    while len(player1bag) > 0:
      userinput = raw_input("place another a piece from your bag " + ','.join(player1bag) + " (or hit enter to finish your turn):\n")
      if userinput == "":
        break
      while get_error_message(userinput, player1bag) != "":
        userinput = raw_input("Invalid move: ["+get_error_message(userinput, player1bag)+"] please place a piece (or hit enter to finish your turn): \n")
        if userinput == "":
          break
      execute_move(userinput, player1bag)
      printboard()

    refillbag(player1bag)

  else:
    print "player 2's turn"
    # TODO:

  player1next = not player1next

print "game is finished"

