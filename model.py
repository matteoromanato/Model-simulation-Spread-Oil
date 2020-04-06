
from mesa import Model
from mesa.space import Grid
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from collections import defaultdict
from agents import Oil, Boat


class OilSpread(Model):
    def __init__ (self, height=20, width=20, initial_macchie= 1, qnt = 10, qnt_prop = 50,initial_barche= 1, power_boat = 3):
        
        self.height = height
        self.width = width
        self.initial_macchie = initial_macchie
        self.qnt = qnt
        self.qnt_prop = qnt_prop
        self.initial_barche = initial_barche
        self.power_boat=power_boat


        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=True)

       
        self.datacollector = DataCollector(
            {"Oil": lambda m: m.schedule.get_agent_count()
             #"Cane": lambda m: self.count_type(self, 0)
            })

        # Create macchie di petrolio
        for i in range(self.initial_macchie):          
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            macchia = Oil((x, y), self, qnt, qnt_prop)
            self.grid.place_agent(macchia, (x, y))
            self.schedule.add(macchia)

         # Create barchette pulisci mondo
        for i in range(self.initial_barche):          
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            barca = Boat((x, y), self, power_boat)
            self.grid.place_agent(barca, (x, y))
            self.schedule.add(barca)

        self.running = True
        self.datacollector.collect(self)

    

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        
        print ("il numero di agenti in gioco sono "+str(self.schedule.get_agent_count()))

        if self.schedule.get_agent_count() == self.initial_barche:
            self.running = False

      

