import random
import pygame

pink = (255, 220, 230)

pygame.init()
window = pygame.display.set_mode((1100,980))
pygame.display.set_caption("~◊ Connect-4 ◊~")
blue = pygame.image.load('sources/blue.png')
red = pygame.image.load('sources/red.png')
line = pygame.image.load('sources/line.png')
line2 = pygame.image.load('sources/line2.png')
line3 = pygame.image.load('sources/line3.png')
line4 = pygame.image.load('sources/line4.png')
blank1 = pygame.image.load('sources/blank1.png')
blank2 = pygame.image.load('sources/blank2.png')
font = pygame.font.Font('sources/SHUTTLE-X.ttf', 102)
winner1 = font.render('YOU WON!!', False, pink)
winner2 = font.render('AI WON!!!', False, pink)
draw = font.render('DRAW!!!!', False, pink)


def set_column(column):
    return 52 + 145 * column

def set_row(row):
    return 185 + 125 * row


def create_map():
    map = []
    for row in range(6):

        temp_row = []
        for col in range(7):
            temp_row.append(0)
        
        map.append(temp_row)
    return map



def successor(map, value):
    successors = []
    for i in available_choices(map):
        successors.append(select(map, i-1, value))
    return successors

def evaluate_slice(slice):

    score = 0

    if (slice.count(1) == 4):
        score += 1000

    elif (slice.count(1) == 3 and slice.count(0) == 1):
        score += 10

    elif (slice.count(1) == 2 and slice.count(0) == 2):
        score += 1

    if (slice.count(2) == 4):
        score -= 1000

    elif (slice.count(2) == 3 and slice.count(0) == 1):
        score -= 10

    elif (slice.count(2) == 2 and slice.count(0) == 2):
        score -= 1

    return score


def heuristic(map):

    score = 0
    for i in range(6):                                      # horizontally
        for j in range(4):
            score += evaluate_slice(map[i][j:j+4])

    for i in range(3):                                      # vertically
        for j in range(7):
            score += evaluate_slice([map[i+r][j] for r in range(4)])

    return score

def print_map(map):

    window.blit(line, (15, 140))  
    window.blit(line2, (0, 183))     
    window.blit(line3, (15, 935))
    window.blit(line4, (1050, 186))  
    for i in range(6):

        for j in range(len(map[i])):

            if(map[i][j] == 1):
                window.blit(blue, (set_column(j), set_row(i)))  
            elif(map[i][j] == 2):
                window.blit(red, (set_column(j), set_row(i))) 
    

def available_choices(map):
    choices = []
    for i in range(7):
        if(map[0][i] == 0):
            choices.append(i+1)
    return choices


def is_column_filled(map, j):
    return map[0][j] != 0

def is_leaf(map):
    return True if(filled_map(map) or find_winner(map) != 'no winners yet') else False

def minimax(map, isAI_Turn, depth):

    if (depth == 0 or is_leaf(map)):
        return heuristic(map)
    
    if(isAI_Turn):
        value = 100000000
        nodes = successor(map, 2)
        for n in nodes:
            value = min(value, minimax(n, False, depth-1))

        return value
    
    else:
        value = -100000000
        nodes = successor(map, 1)
        for n in nodes:
            value = max(value, minimax(n, True, depth-1))

        return value


def select(map, column, value):

    copy = clone(map)
    for i in range(5,-1,-1):
        if(copy[i][column] == 0):
            copy[i][column] = value
            return copy


def filled_map(map):
    for i in map:
        for j in i:
            if(j == 0):
                return False
    return True


def find_winner(map):

    for i in range(6):
        for j in range(4):  # horizontally

            if(map[i][j] == 1 and map[i][j+1] == 1
               and map[i][j+2] == 1 and map[i][j+3] == 1):
                
                return 'winner=1'
            
            elif(map[i][j] == 2 and map[i][j+1] == 2
               and map[i][j+2] == 2 and map[i][j+3] == 2):
    
                return 'winner=2'

    for i in range(3):
        for j in range(7):  # vertically

            if(map[i][j] == 1 and map[i+1][j] == 1
               and map[i+2][j] == 1 and map[i+3][j] == 1):
                
                return 'winner=1'
            
            elif(map[i][j] == 2 and map[i+1][j] == 2
               and map[i+2][j] == 2 and map[i+3][j] == 2):
                
                return 'winner=2'
    
    if(filled_map(map)):
        return '1-1'                # If map is filled then the game is equal for 2 players
    else:
        return 'no winners yet'     # If map is not fully filled the game isn't over yet



def clone(map):
    new_map = []
    for row in range(6):
        temp_row = []
        for col in range(7):
            temp_row.append(map[row][col])
        new_map.append(temp_row)
    return new_map

def main():

    i = 0
    j_blue = 15
    gameIsOver = False

    isAI_turn = random.choice((True,False))
    map = create_map()

    while True:
        pygame.time.delay(120)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return

        if(not isAI_turn):
            keys = pygame.key.get_pressed()

            if (keys[pygame.K_RIGHT] and i<6 and not gameIsOver):
                i += 1

            elif (keys[pygame.K_LEFT] and i>0 and not gameIsOver):
                i -= 1

            elif ((keys[pygame.K_RETURN] or keys[pygame.K_SPACE])
                and not is_column_filled(map,i) and not gameIsOver):
                j_blue = set_row(i)

        window.fill((0,0,0))
        print_map(map)

        if(j_blue == 15 and not isAI_turn and not gameIsOver):
            window.blit(blue, (set_column(i),j_blue))

        elif(not isAI_turn and not gameIsOver):
            map = select(map,i,1)
            isAI_turn = not isAI_turn
            j_blue = 15

        elif(isAI_turn and not gameIsOver):
            best_choice = None
            best_score = 10000000                   # must be minimized  

            for s in successor(map, 2):
                score = minimax(s, False, 3)
                if(score < best_score):
                    best_choice = s
                    best_score = score

            map = best_choice
            isAI_turn = not isAI_turn

        print_map(map)

        if(find_winner(map) == 'winner=1'):
            window.blit(blank1, (0,0))
            window.blit(winner1, (305,30))
            gameIsOver = True

        elif(find_winner(map) == 'winner=2'):
            window.blit(blank1, (0,0))
            window.blit(winner2, (330,30))
            gameIsOver = True       

        elif(find_winner(map) == '1-1'):
            window.blit(blank2, (20,0))
            window.blit(draw, (320,30))
            gameIsOver = True

        pygame.display.update()
main()
            
