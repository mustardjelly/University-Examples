class Player:
    def __init__(self, name):
        self.__name = name
        self.__matches_won = 0
        self.__matches_total = 0
        self.__set_won = 0
        self.__set_total = 0
        self.players_played = []
        self.players_beaten = []
        self.players_not_played = []
        self.__resistance = 0
        
    def __repr__(self):
        if self.__set_total == 0:
            out_str = 'NAME: {0} MATCH %: 0 SET %: 0 RESISTANCE: {1}'.format(self.__name, self.get_resistance())
        else:
            out_str = 'NAME: {0} MATCH %: {1} SET %: {2} RESISTANCE: {3}'.format(self.__name, round(self.match_percent() * 100, 2), round(self.__set_won / self.__set_total * 100, 2), self.get_resistance())
        
        return out_str
        
    def get_name(self):
        return self.__name
        
    def set_matches_won(self, score):
        self.__matches_won += score
        
    def set_matches_played(self, total):
        self.__matches_total += total
        
    def match_percent(self):
        try:
            return self.__matches_won / self.__matches_total
        except:
            return 0
            
    def set_percent(self):
        try:
            return self.__set_won / self.__set_total
        except:
            return 0
        
    def set_set_won(self, score):
        self.__set_won += score
        
    def get_resistance(self):
        return self.__resistance
        
    def set_set_total(self, total):
        self.__set_total += total
        
    def set_resistance(self, score):
        self.__resistance = score
        
    def reset_resistance(self):
        self.__resistance = 0
        
    def __lt__(self, other):
        try:
            if self.__set_won / self.__set_total > other.__set_won / other.__set_total:
                return True
            elif self.__set_won / self.__set_total == other.__set_won / other.__set_total:
                if self.__matches_won / self.__matches_total > other.__matches_won / other.__matches_total: 
                    return True
                elif self.__matches_won / self.__matches_total == other.__matches_won / other.__matches_total: 
                    if self.__resistance > other.__resistance:
                        return True
        except:
            return        
