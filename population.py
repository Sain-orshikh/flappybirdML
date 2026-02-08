import config
import player
import math
import species
import operator

class Population:
    def __init__(self, size):
        self.players = []
        self.generation = 1
        self.species = []
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

    def natural_selection(self):
        print('SPECIATE')
        self.speciate()

        print('CALCULATE FITNESS')
        self.calculate_fitness()

        print('KILL STALE SPECIES')
        self.kill_stale_species()

        print('SORT BY FITNESS')
        self.sort_species_by_fitness()

        print('CHILDREN FOR NEXT GEN')
        self.next_gen()

    def speciate(self):
        for s in self.species:
            s.players = []
        for p in self.players:
            add_to_species = False
            for s in self.species:
                if s.similarity(p.brain):
                    s.players.append(p)
                    add_to_species = True        
                    break
            if not add_to_species:
                self.species.append(species.Species(p))

    def calculate_fitness(self):
        for p in self.players:
            p.calculate_fitness()
        for s in self.species:
            s.calculate_average_fitness()

    def kill_stale_species(self):
        player_bin = []
        species_bin = []
        for s in self.species:
            if s.staleness >= 8:
                if len(self.species) > len(species_bin) + 1:
                    species_bin.append(s)
                    for p in s.players:
                        player_bin.append(p)
                else:
                    s.staleness = 0
        for p in player_bin:
            self.players.remove(p)
        for s in species_bin:
            self.species.remove(s)


    def sort_species_by_fitness(self):
        for s in self.species:
            s.sort_players_by_fitness()
        self.species.sort(key=operator.attrgetter('benchmark_fitness'), reverse=True)
        # Remove empty species
        self.species = [s for s in self.species if s.players]

    def next_gen(self):
        children = []

        if not self.species:
            print("WARNING: No species available, creating new population")
            for i in range(self.size):
                children.append(player.Player())
            self.players = children
            self.generation += 1
            return

        for s in self.species:
            children.append(s.champion.clone())
        
        children_per_species = math.floor((self.size - len(self.species)) / len(self.species))

        for s in self.species:
            for i in range(0, children_per_species):
                baby = s.offspring()
                if baby:
                    children.append(baby)
        
        while len(children) < self.size:
            baby = self.species[0].offspring()
            if baby:
                children.append(baby)

        self.players = []

        for child in children:
            self.players.append(child)

        self.generation +=1

    def extinct(self):
        for p in self.players:
            if p.alive:
                return False
        return True