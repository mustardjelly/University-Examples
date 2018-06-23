#############################################
#Magic Tournament Simulator                 #
#           tracks scores, pairs players    #
#@authors:  Annemiek Powell, Sam Powell     #
#@date:     03/01/2017                      #
#############################################

from Player import *
from Game import *
import random
import copy
import math
     
#########################
#Initializing Conditions#
#########################
  
'''Initial conditions for the Tournament program such as number of players.'''  
def initialize():
    player_list = []
    dup_found = False
    odd = False
    num_players = int(input('Please enter the number of players: '))
    #If number of players is odd append a Bye to the Tournament
    if num_players % 2 == 1:
        player_list.append(Player('**Bye**'))
    
    #Adds players to the Tournament
    while num_players > 0:
        name = input('Please enter a player name: ')
        for player in player_list:
            if player.get_name() == name:
                dup_found = True
        while name == '' or dup_found:
            if dup_found:
                name = input(name + ' is already used!\n Please enter a new name: ')
            else:
                name = input(name + ' is not valid!\n Please reenter that players name: ')
            #Checks for duplicates    
            dup_found = False
            for player in player_list:
                if player.get_name() == name:
                    dup_found = True
                    
        num_players -= 1
        player_list += [Player(name)]
        
    player_list = list_random(player_list)
    #Initializes each players player not played list
    for player in player_list:
        for player2 in player_list:
            if player2.get_name() != player.get_name():
                player.players_not_played.append(player2)
    print()
    
    return player_list

'''Randomly ranks our players in the list'''
def list_random(in_list):
    out_list = []
    while len(in_list) > 0:
        out_list.append(in_list.pop(random.randrange(0, len(in_list))))
    return out_list
   
###################
#Generate Pairings#
###################

'''Given a player list, attempts to create a fair pairing by
choosing the top ranked player and pairing him with the next
top ranked player he/she has not already played.'''
def generate_pairings(in_list, pair_count):
    out_info = []
    pair_count += 1
    brute_force = False
    #first player
    out_info.append(in_list.pop(0))
    try:
        for index in range(len(in_list)):
            if in_list[index].get_name() not in out_info[0].players_played:
                #Second player
                out_info.append(in_list.pop(index))
                return Game(out_info[0], out_info[1], pair_count), pair_count, brute_force
    except:
        brute_force = True
        return Game(Player('**dummy**'), Player('**dummy**'), pair_count), pair_count, brute_force

#CORE FUCNTION           
'''Creates a set of matches for the round by pairing players who haven't played
each other against each other'''
def make_pairs(match_history, pair_count, player_list):
    can_continue = False
    brute_force = False
    temp_match_append = []
    temp_pair_count = pair_count
    dup_player_list = player_list.copy()
    #Attempts to create a fairly matched round
    while not can_continue and not brute_force:
        for pair in range(int(len(dup_player_list) / 2)):
            try:
                game_info, temp_pair_count, brute_force = generate_pairings(dup_player_list, temp_pair_count)
                temp_match_append.append(game_info)
            except:
                temp_pair_count = pair_count
                brute_force = True
                break
        #If a succcessive round of fair matches is found
        if len(temp_match_append) == math.ceil(len(player_list) / 2):
            can_continue = True
    
    #If no fair game matching can be made, make a random valid game match for the round
    if brute_force:
        #print('brute force triggered')
        dup_player_list = player_list
        temp_match_append, pair_count = brute_force_combinations(dup_player_list, pair_count)
        if len(temp_match_append) == math.ceil(len(player_list) / 2):
            can_continue = True
        
    #If a valid round has been created, append the temporary match data to match history
    if can_continue:
        pair_count = temp_pair_count
        add_players_played(temp_match_append)
        match_history = match_history + temp_match_append
    else:
        print('INVALID MATCH APPENDAGE')
    
    return match_history, pair_count
    
'''Attempts to brute force a valid combination of players for the round.
Players must not have played each other.'''
def brute_force_combinations(player_list, pair_count):
    combination_valid = False
        
    number_of_players = len(player_list)
    number = len(player_list[0].players_not_played)
    '''Way to reference every unplayed player in a players players_not_played list
    i, j, ... o, p are indexes for the players_not_played list.'''
    for i in range(number):
        if number_of_players > 1:
            for j in range(number):
                if number_of_players == 2:
                    combination_valid, temp_match_append, temp_pair_count = check_combination([i, j], number_of_players, player_list, pair_count)
                    if combination_valid:
                        return temp_match_append, temp_pair_count
                if number_of_players > 2:
                    for k in range(number):
                        if number_of_players > 3:
                            for l in range(number):
                                if number_of_players == 4:
                                    combination_valid = check_combination([i, j, k, l], number_of_players, player_list, pair_count)
                                    if combination_valid:
                                        return temp_match_append, temp_pair_count
                                if number_of_players > 4:
                                    for m in range(number):
                                        if number_of_players > 5:
                                            for n in range(number):
                                                if number_of_players == 6:
                                                    combination_valid, temp_match_append, temp_pair_count = check_combination([i, j, k, l, m, n], number_of_players, player_list, pair_count)
                                                    if combination_valid:
                                                        return temp_match_append, temp_pair_count
                                                if number_of_players > 6:
                                                    for o in range(number):
                                                        if number_of_players > 7:
                                                            for p in range(number):
                                                                if number_of_players == 8:
                                                                    combination_valid, temp_match_append, temp_pair_count = check_combination([i, j, k, l, m, n, o, p], number_of_players, player_list, pair_count)
                                                                    if combination_valid:
                                                                        return temp_match_append, temp_pair_count
    print("ERROR NO VALID COMBINATIONS FOUND!!!!")

'''Attempts to create games for the round with the given indices. If the correct
number of games is generated the return is triggered as a valid combination.'''    
def check_combination(current_combination, number_of_players, player_list, pair_count):
    temp_match_list = []
    found_game = []
    combination_index = 0
    temp_pair_count = pair_count
    for index in range(len(player_list)):
        if player_list[index].get_name() not in found_game:
            temp_pair_count += 1
            temp_match_list.append(Game(player_list[index], \
            player_list[index].players_not_played[current_combination[combination_index]], temp_pair_count))
            found_game.append(player_list[index].get_name())
            found_game.append(player_list[index].players_not_played[current_combination[combination_index]].get_name())
        combination_index += 1
    if len(temp_match_list) == number_of_players / 2:
        return True, temp_match_list, temp_pair_count
    else:
        return False, temp_match_list, pair_count
        
    
'''Goes through our temporary list and adds each player in each game to each
others players_played list and remove them from each others not played list'''
def add_players_played(temp_match_list):
    for index in range(len(temp_match_list)):
        print(temp_match_list[index])
        player1 = temp_match_list[index].get_player1()
        player2 = temp_match_list[index].get_player2()
        player1.players_played.append(player2.get_name())
        player2.players_played.append(player1.get_name())
        remove_player_not_played(player1, player2)
        remove_player_not_played(player2, player1)
 
'''Removes player2 from player1s' players not played list.''' 
def remove_player_not_played(player1, player2):
    for index in range(len(player1.players_not_played)):
        if player2.get_name() == player1.players_not_played[index].get_name():
            return player1.players_not_played.pop(index)

'''Checks if any of the generated games do not have scores. If they do not
prevent generating of more scores.'''    
def can_pair(match_history):
    can_continue = True
    games = []
    for index in range(1,len(match_history)):
        if not match_history[index].score_exists():
            can_continue = False
            games.append(index)
            
    return can_continue, games
    
'''Returns to the user a list of games with no score. '''
def pairing_not_ready(match_history, games_not_ready):
    print('You must enter all scores for the round before generating new pairings')
    print('The following games have no score: ')
    out_msg = ''
    for item in games_not_ready:
        out_msg += repr(match_history[item])
    print(out_msg)
    

#############
#Enter Score#
#############
'''Allows the user to enter scores for a Game.'''
def enter_scores(match_history, player_list):
    games_no_score = False
    score_to_enter = ''
    
    if (len(match_history) == 1):
        print('There are no games!!')
        return match_history
    
    for index in range(1,len(match_history)):
        if not match_history[index].score_exists():
            if not games_no_score:
                games_no_score = True
                print('The following games have no score: \n')
            print(match_history[index])
            
    while score_to_enter == '':
        game_number = input('Which game are you trying to enter a score for, enter to go back: ')
        if game_number == 'z':
            return match_history
        try:
            print(match_history[int(game_number)])
            if match_history[int(game_number)].score_exists():
                print('Score already exists!!')
                option = input("Would you like to edit this score? (y/n): ")
                if option == 'y' or option == 'Y':
                    match_history[int(game_number)].reset_score()
                else:
                    return match_history
            score_to_enter = input('Please enter a score, enter to go back: ')
            match_history[int(game_number)].set_score(score_to_enter)
        except:
            print('Invalid game. No score has been entered.')
            return match_history
    
    return match_history

#############
#PLAYER RANK#    
#############

'''Assigns points to players based on performance so far.'''
def resistance_dict(player_list):
    point_dict = {}
    points = len(player_list) - 1
    
    point_dict[player_list[0]] = points
    for index in range(1, len(player_list)):
        if player_list[index].match_percent() == player_list[index - 1].match_percent(): 
            point_dict[player_list[index]] = points
        else:
            points -= 1
            point_dict[player_list[index]] = points   
    return point_dict

'''If two players have the same match % then resistance needs to be calculated.'''
def resistance(player_list, point_dict):
    for index in range(1, len(player_list)):
        if player_list[index].match_percent() == player_list[index - 1].match_percent() and \
        player_list[index].set_percent() == player_list[index - 1].set_percent():
            calculate_resistance(player_list[index], point_dict)
            if player_list[index - 1].get_resistance() == 0:
                calculate_resistance(player_list[index - 1], point_dict)

'''Calculates the resistance for an individual player.'''                
def calculate_resistance(player, point_dict):
    resistance_points = 0
    for person in player.players_beaten:
        if person.get_name() == '**Bye**':
            resistance_points += 0
        else:
            resistance_points += point_dict[person]
    player.set_resistance(resistance_points)
    
'''Resets Resistance for every player.'''
def wipe_resistance(player_list):
    for player in player_list:
        player.reset_resistance()
        
##########################
#Calculates Maximum Games#
##########################
'''Calculates the maximum number of games assuming no one replays anyone.'''
def calculate_max_games(player_list):
    number_of_players = len(player_list)
    #Guassian Series
    maximum_games = (number_of_players - 1)*(number_of_players) / 2
    return maximum_games

#################    
#Text Formatting#
#################
        
def print_player_rank(player_list):
    rank = 1
    wipe_resistance(player_list)
    player_list.sort()
    point_dict = resistance_dict(player_list)
    resistance(player_list, point_dict)
    player_list.sort()            
    for item in player_list:
        if item.get_name() == "**Bye**":
            pass
        else:
            print('{0}) {1}'.format(rank, item))
            rank += 1
    print()
    
def make_title(title):
    spaces = math.ceil(12 - len(title) / 2)
    side_buffer = 5
    title = '#' * side_buffer + ' ' * spaces + title + ' ' * spaces + '#' * side_buffer
    buffer = int((len(title))) * '#'
    title = buffer + '\n' + title + '\n' + buffer
    print(title)

def list_of_options():
    make_title('MAIN MENU')
    print('1. Generate Pairings')
    print('2. Enter Scores')
    print('3. Player Rankings')
    print('4. Match History')
    print('5. Exit')
    print()

def main():
    #entering players
    player_list = initialize()
    maximum_games = calculate_max_games(player_list) 
    #global variables
    pair_count = 0 
    match_history = ['Dummy']  
        
    #display list of options
    list_of_options()   
    try:
        option = int(input('Please select an option: '))
    except:
        option = 0
        print('Invalid Option!')
    print()
    while option != 5:
        if option == 1:
            #generate_pairings
            print('GENERATE PAIRINGS')
            if len(match_history) - 1 == maximum_games:
                print('\n!!!Maximum games reached!!!\n')
            else:
                can_continue, games = can_pair(match_history)
                if can_continue:
                    match_history, pair_count = make_pairs(match_history, pair_count, player_list)
                else:
                    pairing_not_ready(match_history, games)
        elif option == 2:
            #enter scores
            print('ENTER SCORES')
            match_history = enter_scores(match_history, player_list)
            print()
        elif option == 3:
            #player rankings
            print('PLAYER RANKINGS')
            print_player_rank(player_list)
        elif option == 4:
            #print match_history
            print('MATCH HISTORY')
            for item in match_history[1:]:
                print(item)
        elif option == 6:
            print('Player 1 not played list')
            print(player_list[0])
            print(player_list[0].players_not_played)
        list_of_options()    
        try:
            option = int(input('Please select an option: '))
        except:
            option = 0
        print()
    if option == 5:
        print('EXITING...')
        
main()
    