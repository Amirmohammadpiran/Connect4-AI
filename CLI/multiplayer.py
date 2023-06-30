from os import name, system


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

    for i in range(5,-1,-1):
        if(map[i][column-1] == 0):
            map[i][column-1] = value
            return map
        

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

def main():
    map = create_map()
    player1turn = True

    while(not filled_map(map)):

        turn = 1 if player1turn else 2

        clear_terminal()
        print(f'~~~((Player #{turn} turn!))~~~\nPlayer 1: ○\nPlayer 2: ◊\n\n')
        print_map(map)

        possible_choices = available_choices(map)
        print(f'\n--available choices:{possible_choices}')

        choice = input('Enter your choice: ')
        while(True):

            if(str.isdecimal(choice) and possible_choices.__contains__(int(choice))):
                break
            print(f'--Invalid. please choose through:{possible_choices}')
            choice = input('Enter your choice: ')

        if(player1turn):
            map = select(map, int(choice), 1)
        else:
            map = select(map, int(choice), 2)

        player1turn = not player1turn
        
        if(find_winner(map) == 'winner=1'):
            clear_terminal()
            print('Player 1: ○\nPlayer 2: ◊\n\n')
            print_map(map)
            print('\n#######  Player 1 has won!! #######')
            break

        elif(find_winner(map) == 'winner=2'):
            clear_terminal()
            print('Player 1: ○\nPlayer 2: ◊\n\n')
            print_map(map)
            print('\n#######  Player 2 has won!! #######')
            break

        elif(find_winner(map) == '1-1'):
            clear_terminal()
            print('Player 1: ○\nPlayer 2: ◊\n\n')
            print_map(map)
            print('\n#######  no winners!  #######')
            break

main()
