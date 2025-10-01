class Player:
    def __init__(self, name) -> None:
        self.name = name
        self.health = 100
        self.mana = 10
        self.mana_regeneration = 1 # per second