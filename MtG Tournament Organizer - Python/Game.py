class Game:
    def __init__(self, player1, player2, pair_count):
        self.__player1 = player1
        self.__player2 = player2
        self.__pair_count = pair_count
        self.__score = None
        if self.__player2.get_name() == '**Bye**':
            self.set_score('2:0')
        elif self.__player1.get_name() == '**Bye**':
            self.set_score('0:2')
        
    def __repr__(self):
        if not self.__score:
            out_str = 'Game: {0}\n{1} \n{2}\nScore: {3}\n'.format(self.__pair_count, self.__player1, self.__player2, 'MISSING')
        else:
            out_str = 'Game: {0}\n{1} \n{2}\nScore: {3}:{4}\n'.format(self.__pair_count, self.__player1, self.__player2, self.__score[0], self.__score[2])
        return out_str
        
    def get_player1(self):
        return self.__player1
        
    def get_player2(self):
        return self.__player2
        
    def set_score(self, score):
        self.__score = score
        
        try:
            total_matches = int(self.__score[0]) + int(self.__score[2])
        except:
            self.__score = None
            print('Incorrect score format')
            return
            
        self.__player1.set_matches_played(total_matches)
        self.__player2.set_matches_played(total_matches)
        
        self.__player1.set_matches_won(int(self.__score[0]))
        self.__player2.set_matches_won(int(self.__score[2]))
        
        self.__player1.set_set_total(1)
        self.__player2.set_set_total(1)
        
        if self.__score[0] == self.__score[2]:
            self.__player1.set_set_won(.5)
            self.__player2.set_set_won(.5)
            
        elif self.__score[0] > self.__score[2]:
            self.__player1.set_set_won(1)
            self.__player2.set_set_won(0)
            self.__player1.players_beaten.append(self.__player2)
            
        elif self.__score[0] < self.__score[2]:
            self.__player1.set_set_won(0)
            self.__player2.set_set_won(1)
            self.__player2.players_beaten.append(self.__player1)
    
    def reset_score(self):
        try:
            total_matches = int(self.__score[0]) + int(self.__score[2])
        except:
            self.__score = None
            print('Incorrect score format')
            return
            
        self.__player1.set_matches_played(total_matches * -1)
        self.__player2.set_matches_played(total_matches * -1)
        
        self.__player1.set_matches_won(int(self.__score[0]) * -1)
        self.__player2.set_matches_won(int(self.__score[2]) * -1)
        
        self.__player1.set_set_total(-1)
        self.__player2.set_set_total(-1)
        
        if self.__score[0] == self.__score[2]:
            self.__player1.set_set_won(-.5)
            self.__player2.set_set_won(-.5)
            
        elif self.__score[0] > self.__score[2]:
            self.__player1.set_set_won(-1)
            self.__player2.set_set_won(0)
            index = self.__player1.players_beaten.index(self.__player2)
            self.__player1.players_beaten.pop(index)
            
        elif self.__score[0] < self.__score[2]:
            self.__player1.set_set_won(0)
            self.__player2.set_set_won(-1)
            index = self.__player2.players_beaten.index(self.__player1)
            self.__player2.players_beaten.pop(index)
        self.__score = None
            
    def score_exists(self):
        if self.__score:
            return True
        else:
            return False