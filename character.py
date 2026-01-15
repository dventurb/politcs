class Character:
    def __init__(self, name, index, charisma, aggressiveness, strategy, experience, cartoon, sound):
        self.name = name
        self.index = index
        self.charisma = charisma
        self.aggressiveness = aggressiveness
        self.strategy = strategy
        self.experience = experience
        self.cartoon = cartoon
        self.sound = sound

    def get_stats(self):
        return {
                "Charisma": self.charisma,
                "Aggressiveness": self.aggressiveness,
                "Strategy": self.strategy,
                "Experience": self.experience
                }

    
