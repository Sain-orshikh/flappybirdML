import config
import player

class Population:
    def __init__(self, size):
        self.players = []
        self.size = size
        for i in range(self.size):
            self.players.append(player.Player())

    def update_live_player(self):
        for p in self.players:
            if p.alive:
                p.look()
                p.think()
                p.draw(config.window)
                p.update(config.ground)
    
    #Returns true when all players die

    def extinct(self):
        for p in self.players:
            if p.alive:
                return False
        return True