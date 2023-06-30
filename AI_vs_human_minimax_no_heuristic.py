from os import name, system
import random

def clear_terminal():
    if(name == 'nt'):
        clear = system('cls')
    else:
        clear = system('clear')
    

def create_map():
    map = []
    for row in range(6):

        temp_row = []
        for col in range(7):
            temp_row.append(0)
        
        map.append(temp_row)
    return map


def print_map(map):

    print('   1 2 3 4 5 6 7')
    for i in range(6):

        temp_unicode = []

        for j in map[i]:
            if(j == 0):
                temp_unicode.append('▦')                
            elif(j == 1):
                temp_unicode.append('○') 
            elif(j == 2):
                temp_unicode.append('◊')

        print(i+1,' ',end='')

        for j in temp_unicode:
            print(j,end=' ')
        print()


def available_choices(map):
    choices = []
    for i in range(7):
        if(map[0][i] == 0):
            choices.append(i+1)
    return choices


def select(map, column, value):

    copy = clone(map)
    for i in range(5,-1,-1):
        if(copy[i][column-1] == 0):
            copy[i][column-1] = value
            return copy
        

def filled_map(map):
    for i in map:
        for j in i:
            if(j == 0):
                return False
    return True


def successor(map, value):
    successors = []
    for i in available_choices(map):
        successors.append(select(map, i, value))
    return successors


def evaluate_slice(slice):

    score = 0

    if (slice.count(1) == 4):
        score += 100000

    if (slice.count(2) == 4):
        score -= 100000

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

def clone(map):
    new_map = []
    for row in range(6):
        temp_row = []
        for col in range(7):
            temp_row.append(map[row][col])
        new_map.append(temp_row)
    return new_map


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

def find_winner(map):

    for i in range(6):
        for j in range(4):                          # horizontally

            if(map[i][j] == 1 and map[i][j+1] == 1
               and map[i][j+2] == 1 and map[i][j+3] == 1):
                
                return 'winner=1'
            
            elif(map[i][j] == 2 and map[i][j+1] == 2
               and map[i][j+2] == 2 and map[i][j+3] == 2):
    
                return 'winner=2'

    for i in range(3):
        for j in range(7):                           # vertically

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

def main():
    map = create_map()
    player1turn = random.choice([True, False])

    while(not filled_map(map)):

        turn = 1 if player1turn else 2

        clear_terminal()
        if(player1turn):
            print('~~~((Your turn!))~~~\nYou: ○\nMegamind: ◊\n\n')
        else:
            print("~~~((Megamind's turn!))~~~\nnYou: ○\nMegamind: ◊\n\n")            
        print_map(map)

        if(player1turn):

            possible_choices = available_choices(map)
            print(f'\n--available choices:{possible_choices}')

            choice = input('Enter your choice: ')
            while(True):

                if(str.isdecimal(choice) and possible_choices.__contains__(int(choice))):
                    break
                print(f'--Invalid. please choose through:{possible_choices}')
                choice = input('Enter your choice: ')

            map = select(map, int(choice), 1)
                
        else:
            print('\nThe Megamind is thinking!')
            best_choice = None
            best_score = 10000000                   # must be minimized  

            for s in successor(map, 2):
                score = minimax(s, False, 4)
                if(score < best_score):
                    best_choice = s
                    best_score = score

            map = best_choice

        player1turn = not player1turn
        
        if(find_winner(map) == 'winner=1'):
            clear_terminal()
            print('You: ○\nMegamind: ◊\n\n')
            print_map(map)
            print('\n#######  You won!! #######')
            break

        elif(find_winner(map) == 'winner=2'):
            clear_terminal()
            print('You: ○\nMegamind: ◊\n\n')
            print_map(map)
            print('\n#######  Megamind has won!! #######')
            break

        elif(find_winner(map) == '1-1'):
            clear_terminal()
            print('You: ○\nMegamind: ◊\n\n')
            print_map(map)
            print('\n#######  no winners!  #######')
            break

main()