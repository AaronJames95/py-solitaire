class Target(Circle):
    def __init__(self,canvas):
        super(Target, self).__init__(canvas)
        self.color = "red"
        self.cX = random.randint(20,480)
        self.cY = 40
        self.speed =2
        
    def reset(self):
        self.cX = random.randint(20,480)
        self.cY = 40
        
    def drawTarget(self):
        origRadius = self.radius
        self.drawShape()
        self.radius = self.radius *2/3
        self.color = 'white'
        self.drawShape()
        self.radius = self.radius/3
        self.color = 'red'
        self.drawShape()
        self.radius = origRadius