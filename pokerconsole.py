from poker import *

simcount = 10000

HEADER = "\nPoker> "
CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "1", "j", "q", "k", "a"]
SUITS = ["s", "d", "c", "h"]
HANDSIZE = 2

PREFLOP = 0
FLOP = 3
TURN = 4
RIVER = 5

def consolehelp():
    print """commands:

n begins a new hand

c continues an already open hand.

sim sets the number of sample games to be generated (simcount).
    the higher the number, the higher the accuracy and CPU time.

help shows this text

exit quits pokerconsole

card format: each card is written with a character to represent its value and one to represent its suit.

values:        suits:
2        s pades
3        d iamonds
4        c lubs
5        h earts
6
7
8
9
10
j
q 
k
a

The ace of spades is written 'as'.
A hand with the 2 of clubs and the 10 of hearts is 2c10h
Same formatting applies to inputing the common cards. DO NOT SEPARATE CARDS

It's possible to make a new hand in any stage of the game, not only in its beginning (preflop).
It's also possible to add more than one step when continuing a game. For example, its possible to simulate a preflop and skip straight to the river"""
def printcard(cardlist):
    str = ""
    for card in cardlist:
        if card[VALUE] == ACE:
            str += 'ACE of '
        elif card[VALUE] == KING:
            str += 'KING of '
        elif card[VALUE] == QUEEN:
            str += 'QUEEN of '
        elif card[VALUE] == JACK:
            str += 'JACK of '
        elif card[VALUE] == TEN:
            str += 'TEN of '
        elif card[VALUE] == NINE:
            str += 'NINE of '
        elif card[VALUE] == EIGHT:
            str += 'EIGHT of '
        elif card[VALUE] == SEVEN:
            str += 'SEVEN of '
        elif card[VALUE] == SIX:
            str += 'SIX of '
        elif card[VALUE] == FIVE:
            str += 'FIVE of '
        elif card[VALUE] == FOUR:
            str += 'FOUR of '
        elif card[VALUE] == THREE:
            str += 'THREE of '
        else:
            str += 'TWO of '
            
        if card[SUIT] == SPADES:
            str += 'SPADES'
        elif card[SUIT] == DIAMONDS:
            str += 'DIAMONDS'
        elif card[SUIT] == CLUBS:
            str += 'CLUBS'
        else:
            str += 'HEARTS'
            
        str += '\n'
    return str + '\n' 
    
def action(input, myhand, playersdealt, playersin, table):
    if input == "n":
        global simcount
        playersdealt = 0
        playersin = 0
        myhand = []
        table = [-1]
        
        while len(input) != 2 * HANDSIZE:
            input = raw_input(HEADER + "Your hand: ").lower()
            if input == "help":
                consolehelp()
                return [[], 0, 0, []]
            input = input.replace("0", "")
            if len(input) == 2 * HANDSIZE:
                for i in range(2 * HANDSIZE):
                    if i%2 == 0 and input[i] in CARDS:
                        card = CARDS.index(input[i])
                    elif i%2 == 1 and input[i] in SUITS:
                        if (  (i == (2 * HANDSIZE) - 1)  and
                              ( (SUITS.index(input[i]), card) in myhand )  ):
                            print "Hand with repeated cards"
                            myhand = []
                            input = ""
                            break
                        else:
                            myhand.append( (SUITS.index(input[i]), card) )
                    else:
                        print "wrong format. type 'help' for format options"
                        myhand = []
                        input = ""
                        break
            else:
                print "Your hand must be " + str(2 * HANDSIZE) + " characters long"
        print printcard(myhand)
            
        
        
        while playersdealt < 2 or playersdealt > 23:
            try:
                playersdealt = int( raw_input(HEADER + "Number of players who received cards: ") )
            except ValueError:
                print "not a number"
            if playersdealt >= 2 and playersdealt <= 23:
                print playersdealt
            else:
                print "must be larger than 1 and no larger than 23"
        
        while playersin < 2 or playersin > playersdealt:
            try:
                playersin = int( raw_input(HEADER + "Number of players in the pot: ") )
            except ValueError:
                print "not a number"
            if playersin >= 2 and playersin <= playersdealt:
                print playersin
            else:
                print "must be larger than 1 and no larger than the total number of players"
        
        while len(table) not in [PREFLOP, FLOP, TURN, RIVER]:
            input = raw_input(HEADER + "Table cards: ").lower()
            if input == "help":
                consolehelp()
                return [[], 0, 0, []]
            input = input.replace("0", "")
            table = []
            if len(input) in [PREFLOP, FLOP * 2, TURN * 2, RIVER * 2]:
                for i in range(len(input)):
                    if i%2 == 0 and input[i] in CARDS:
                        card = CARDS.index(input[i])
                    elif i%2 == 1 and input[i] in SUITS:
                        c = (SUITS.index(input[i]), card)
                        if c not in myhand:
                            table.append(c)
                        else:
                            print "card already used: " + printcard([c])
                            table = [-1]
                            break
                    else:
                        print "wrong format. type 'help' for format options"
                        table = [-1]
                        break
            else:
                print "table must have 0, 3, 4 or 5 cards"
                table = [-1]
        print printcard(table)
        
        print ("\nYour odds are " +
               str( odds(myhand, playersdealt,
                         playersin, table, simcount) * 100 ) + "%")

        
    elif input == "c":
        if myhand == [] or len(table) >= RIVER:
            print "no hand to continue"
            return [[], 0, 0, []]
        print "\n\n**********\nYour hand:\n" + printcard(myhand) + "\n"
        print "Table so far:\n" + printcard(table) + "\n"
        print "Players who received cards = " + str(playersdealt)
        input = 0
        if playersin == 2:
            print "Players in the pot: 2"
        else:
            while input < 2 or input > playersin:
                try:
                    input = int( raw_input(HEADER +
                                        "Players in the pot (no more than " +
                                       str(playersin) + "): ") )
                    if input >= 2 and input <= playersin:
                        playersin = input
                    else:
                        print "must be a number between 2 and " + str(playersin)
                except ValueError:
                    print "not a number"
            print playersin
        
        input = ""
        tableend = len(table)
        while input == "" or ( (len(table) + len(input)/2) < FLOP ) :
            input = raw_input(HEADER + "New table card(s): ").lower()
            if input == "help":
                consolehelp()
                return [[], 0, 0, []]
            input = input.replace("0", "")
            if (len(table) + len(input)/2) in [FLOP, TURN, RIVER]:
                for i in range(len(input)):
                    if i%2 == 0 and input[i] in CARDS:
                        card = CARDS.index(input[i])
                    elif i%2 == 1 and input[i] in SUITS:
                        c = (SUITS.index(input[i]), card)
                        if c not in myhand + table:
                            table.append(c)
                        else:
                            print "card already used: " + printcard([c])
                            input = ""
                            table = table[:tableend]
                            break
                    else:
                        print "wrong format. type 'help' for format options"
                        input = ""
                        table = table[:tableend]
                        break
            else:
                print "table must have 3, 4 or 5 cards"
                input = ""
        print printcard(table)
        
        print ("\nYour odds are " +
               str( odds(myhand, playersdealt,
                         playersin, table, simcount) * 100 ) + "%")
    
    elif input == "sim":
        print "simcount is " + str(simcount)
        simcount = 0
        while simcount < 100:
            try:
                simcount = int( raw_input(HEADER + "new sampling number: ") )
            except ValueError:
                print "not a number"
            if simcount < 100:
                print "must be at least 100"
                
        print "sampling is: " + str(simcount)
    elif input!= "exit":
        print "unknown command"
    
    return [myhand, playersdealt, playersin, table]

def console():
    input = ""
    playersdealt = 0
    playersin = 0
    myhand = []
    table = []
    print"\n\n\n*************************************************"
    print("poker console, created by antonio lutfi\n"+
          "simcount is " + str(simcount) +"\n" + 
          "type help, exit or n to begin")
    while input != "exit":
        input = raw_input(HEADER).lower()
        if input == "help":
            consolehelp()
            continue
        [myhand, playersdealt, playersin, table] = action(input, myhand, playersdealt, playersin, table)
        
console()