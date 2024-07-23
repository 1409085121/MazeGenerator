class Connection:
    def __init__(self, map, visible=True):
        self.y2 = None
        self.x2 = None
        self.y1 = None
        self.x1 = None
        self.map = map
        self.parent1 = None
        self.parent2 = None
        self.visible = visible

    def bind(self, parent1, parent2):
        self.parent1 = parent1
        self.parent2 = parent2
        
        self.x1 = self.parent1.x
        self.y1 = self.parent1.y
        self.x2 = self.parent2.x
        self.y2 = self.parent2.y
        
        return self
