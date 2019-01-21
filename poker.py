from random import randint

DECKSIZE = 52
SUITCOUNT = 4

TABLECOUNT = 5
GAMESIZE = 5

HAND = 0
SCORE = 1

ME = 0

SUIT = 0
SPADES = 0
DIAMONDS = 1
CLUBS = 2
HEARTS = 3

VALUE = 1
ACE = 0xC
KING = 0xB
QUEEN = 0xA
JACK = 0x9
TEN = 0x8
NINE = 0x7
EIGHT = 0x6
SEVEN = 0x5
SIX = 0x4
FIVE = 0x3
FOUR = 0x2
THREE = 0x1
TWO = 0

STRAIGHTFLUSH = 0x800000
FOUROFAKIND = 0x700000
FULLHOUSE = 0x600000
FLUSH = 0x500000
STRAIGHT = 0x400000
THREEOFAKIND = 0x300000
PAIRS = 0x200000
PAIR = 0x100000
HIGHEST = 0

def drawCard(deck):
    i = randint(0, len(deck) - 1)
    card = deck[i]
    del deck[i]
    return card

def _odds(players, playersin, table, simcount):
    
    suitsize = DECKSIZE/SUITCOUNT
    wins = 0
    tableend = len(table)
    usedcards = players[ME][HAND] + table
    
    def straight(l):#checks if l is a straight
        maxstreak = 0
        streak = 0
        for i in xrange(suitsize - 1, -1, -1):
            streak *= l[i]
            streak += l[i] + ( (((i+1)%suitsize) == 0) * l[(i+1)%suitsize] )
            if streak >= maxstreak:
                maxstreak = streak
                topcard = suitsize - (i+1)
        if maxstreak >= GAMESIZE:#if the longest sequence is large enough
            return topcard
        else:
            return -1
    
    for i in xrange(simcount):
        deck = [(j/suitsize, j%suitsize) for j in xrange(DECKSIZE)
                if (j/suitsize, j%suitsize) not in usedcards]
                
        for j in xrange(1, len(players)):
            players[j][HAND] = [drawCard(deck), drawCard(deck)]
            
        table = table[:tableend]
        for j in xrange(tableend, TABLECOUNT):
            table.append(drawCard(deck))
       
        for p in players[:playersin]:
            hand = p[HAND] + table
            
            def score():
                game = [  [ 0 for j in xrange(suitsize) ] for k in xrange(SUITCOUNT)  ]
                for card in hand:
                    game[ card[SUIT] ][ suitsize - (card[VALUE] + 1) ] = 1

                matches = map(lambda x, y, w, z: x+y+w+z,
                              game[SPADES], game[DIAMONDS], game[CLUBS], game[HEARTS])
                
                #Checks for four of a kind
                if(4 in matches):
                    return FOUROFAKIND + (  (0x10 ** (GAMESIZE - 1)) *
                                            ( suitsize - (matches.index(4) + 1) )  )
                
                #Checks for straight flush. in a 7 card game, its not enough to
                #check for flush and straight separately
                for suit in game:
                    if reduce(lambda x, y: x + y, suit) >= GAMESIZE:#if flush
                        card = straight(suit)
                        if card > 0:
                            return STRAIGHTFLUSH + ((0x10 ** (GAMESIZE - 1)) * card)
                        
                #Checks for full house
                if(matches.count(3) > 1 or (matches.count(3) == 1 and 2 in matches)):
                    score = FULLHOUSE
                    hastriplet = False
                    haspair = False
                    for j in xrange(suitsize):
                        if hastriplet and haspair:
                            break
                        elif matches[j] == 3:
                            if not hastriplet:
                                score += (0x10 ** (GAMESIZE - 1)) * (suitsize - (j+1))
                                hastriplet = True
                            elif not haspair:
                                score += (0x10 ** (GAMESIZE - 2)) * (suitsize - (j+1))
                                haspair = True
                        elif matches[j] == 2 and not haspair:
                            score += (0x10 ** (GAMESIZE - 2)) * (suitsize - (j+1))
                            haspair = True
                    return score

                #Checks for flush           
                for suit in game:
                    if reduce(lambda x, y: x + y, suit) >= GAMESIZE:#if flush
                        score = FLUSH
                        multiplier = (0x10 ** (GAMESIZE - 1))
                        for j in xrange(suitsize):
                            if multiplier < 1:
                                break
                            if suit[j] != 0:
                                score += multiplier * (suitsize - (j+1))
                                multiplier /= 0x10
                        return score
                
                #Checks for highest straight possible
                values = map(lambda x, y, w, z: int( (x or y or w or z) ),
                              game[SPADES], game[DIAMONDS], game[CLUBS], game[HEARTS])
                card = straight(values)
                if card > 0:
                    return STRAIGHT + ((0x10 ** (GAMESIZE - 1)) * card)
                
                #Checks for three of a kind
                if(3 in matches):
                    index = matches.index(3)
                    multiplier = (0x10 ** (GAMESIZE - 1))
                    score = THREEOFAKIND + (multiplier * (suitsize - (index + 1)))
                    multiplier /= 0x10
                    for j in xrange(suitsize):
                        if (j != index) and (matches[j] != 0):
                            if multiplier < 0x100:
                                break
                            score += multiplier * (suitsize - (j+1))
                            multiplier /= 0x10
                    return score
                    
                #Checks for biggest two pairs
                if(matches.count(2) >= 2):
                    score = PAIRS
                    hashighpair = False
                    haslowpair = False
                    haskicker = False
                    for j in xrange(suitsize):
                        if hashighpair and haslowpair and haskicker:
                            break
                        elif matches[j] == 2:
                            if not hashighpair:
                                score += (0x10 ** (GAMESIZE - 1)) * (suitsize - (j + 1))
                                hashighpair = True
                            elif not haslowpair:
                                score += (0x10 ** (GAMESIZE - 2)) * (suitsize - (j + 1))
                                haslowpair = True
                            elif not haskicker:
                                score += (0x10 ** (GAMESIZE - 3)) * (suitsize - (j + 1))
                                haskicker = True    
                        elif matches[j] == 1 and not haskicker:
                            score += (0x10 ** (GAMESIZE - 3)) * (suitsize - (j + 1))
                            haskicker = True    
                    return score
                    
                #Checks for pair
                if matches.count(2) == 1:
                    score = PAIR + (0x10 ** (GAMESIZE - 1)) * ( suitsize - (matches.index(2) + 1) )
                    multiplier = (0x10 ** (GAMESIZE - 2))
                    for j in xrange(suitsize):
                        if matches[j] == 1:
                            if multiplier < 0x10:
                                break
                            else:
                                score += multiplier * (suitsize - (j+1))
                                multiplier /= 0x10
                    return score
                
                #Picks top five cards
                multiplier = (0x10 ** (GAMESIZE - 1))
                score = 0
                for j in xrange(suitsize):
                    if matches[j] == 1:
                        if multiplier < 0x1:
                            break
                        else:
                            score += multiplier * (suitsize - (j+1))
                            multiplier /= 0x10
                return score            
            #score() end
            
            p[SCORE] = score()
        
        if max(  [ players[j][SCORE] for j in xrange(len(players)) ]  ) == players[ME][SCORE]:
            wins += 1
        
    return float(wins)/simcount
    
def odds(myhand, playersdealt, playersin, table, simcount):
    players = [ [None, 0] for i in xrange(playersdealt) ]
    players[ME][HAND] = myhand
    return _odds(players, playersin, table, simcount)
    
def help():
    print """\nThe function odds() calculates the probability of a given hand to win, according to the number of players in the game and the known common cards.
    
    
    A card is passed to the function in the format (SUIT, VALUE).
    
    Values:         Suits:
    ACE             SPADES  
    KING            DIAMONDS
    QUEEN           CLUBS
    JACK            HEARTS
    TEN
    NINE
    EIGHT
    SEVEN
    SIX
    FIVE
    FOUR
    THREE
    TWO
    
    So, the ace of spades is written (SPADES, ACE)
    
    function odds(myhand, playersdealt, playersin, table, simcount)
    
    myhand is a list of two cards, between brackets separated by a comma.
    A hand with king of diamonds and a seven of clubs is written
        [(DIAMONDS, KING), (CLUBS, SEVEN)]
        
    playerdealt is the total number of players INCLUDING YOU for whom hands have been dealt.
    
    playersin is the total number of players INCLUDING YOU that are still in the pot.
    
    table is a list that contains the common cards at that point.
    preflop: empty list []
    flop: list with three cards eg: [(CLUBS, TWO), (SPADES,QUEEN), (DIAMONDS,THREE)]
    turn: list with four cards
    river: list with five cards
    
    DO NOT TYPE 3 INSTEAD OF 'THREE' OR YOU'RE GONNA HAVE A BAD TIME
    
    simcount is the number of samples to be generated.
    the highest the number, the highest the accuracy and CPU time.
    
    odds([(SPADES,ACE),(DIAMONDS,ACE)], 4, 3, [], 1000) is an example of a call to odds()"""
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
