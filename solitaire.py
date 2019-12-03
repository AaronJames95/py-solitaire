from tkinter import *
import random
import math

class Card(object):
    def __init__(self,canvas,value,suit):
        self.radius = 20
        self.value = value
        self.suit = suit
        self.canvas = canvas
        self.color = "white"

    def move(self, canvas):
        pass

    def draw(self):
        '''
        (cX,cY,r) = (self.cX,self.cY,self.radius)
        color = self.color
        self.canvas.create_oval(cX-r,cY-r,cX+r,cY+r,fill=color)
        '''
        print (self.value,'of',self.suit)

class Deck(object):
    def __init__(self,canvas):
        self.size = 52
        self.deck = []
        self.values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.suits = ['clubs','diamonds','hearts','spades']
        self.canvas = canvas
        self.makeDeck()

    def makeDeck(self):
        #makes a card for each combo of values and suits, puts them into the deck
        for v in self.values:
            for s in self.suits:
                card = Card(self.canvas,v,s)
                self.deck.append(card)
        random.shuffle(self.deck)
        for card in self.deck:
            card.draw()
        assert (len(self.deck) == self.size)
        
    def drawShape(self):
        (cX,cY,r) = (self.cX,self.cY,self.radius)
        color = self.color
        self.canvas.create_oval(cX-r,cY-r,cX+r,cY+r,fill=color)

class Circle(object):
    def __init__(self,canvas):
        self.radius = 20
        self.canvas = canvas
        self.color = "white"
        
    def drawShape(self):
        (cX,cY,r) = (self.cX,self.cY,self.radius)
        color = self.color
        self.canvas.create_oval(cX-r,cY-r,cX+r,cY+r,fill=color)

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

class Animation(object):

    def mousePressed(self,event):
        self.shooter.changeAngle(event.x,event.y)
        self.redrawAll()
    
    def keyPressed(self,event):
        if event.keysym == "space":
            self.isShot = True
        if event.keysym == "h":
            self.helpUp = not self.helpUp
        self.redrawAll()
    
    def timerFired(self):
        winGame = False
        for target in self.targets:
            target.cY += target.speed
            if target.cY > 520:
                target.reset()
            if self.isShot:
                self.bullet.moveBullet(self.shooter.angle,self.bulletSpeed)
            if self.bullet.cX < -5 or self.bullet.cX > 505 or self.bullet.cY < 0:
                self.bullet = Bullet(canvas) 
                self.isShot = False
            if self.bullet.isHit(target) and not winGame:
                self.bullet = Bullet(canvas)
                target.reset()
                self.isShot = False
                self.score += 1
                print (self.score)
            if self.score == 25:
                winGame = True
        if winGame:
            self.targets.append(Target(canvas))
            
        self.redrawAll()
        delay = 10 # milliseconds
        canvas.after(delay, self.timerFired) # pause, then call timerFired again
    
    def redrawAll(self):
        canvas.delete(ALL)
        canvas.create_rectangle(0,0, 502, 502, fill = 'white') 
        self.shooter.drawShooter() 
        for target in self.targets:
            target.drawTarget()
        self.bullet.drawBullet()
        if self.helpUp:
            self.drawHelp()
        
    
    def init(self):
        Deck(canvas)
        self.targets = [Target(canvas),Target(canvas)]
        self.shooter = Shooter(canvas)
        self.bullet = Bullet(canvas)
        self.bulletSpeed = 15
        self.isShot = False
        self.score = 0
        self.helpUp = False
        
    def drawHelp(self):
        canvas.create_text(250,240,text = "Use mouse to aim")
        canvas.create_text(250,250,text = "Press Space to shoot")
        canvas.create_text(250,260,text = "Get to 25 Points!")
              
    
    def run(self):
        global canvas
        root = Tk()
        canvas = Canvas(root, width=500, height=500)
        canvas.pack()
        self.init()
        input('PAUSE (line 152)')
        root.bind("<Button-1>", lambda event: self.mousePressed(event))
        root.bind("<Key>", lambda event: self.keyPressed(event))
        self.timerFired()
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

animation = Animation()
animation.run()