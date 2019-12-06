from tkinter import *
from PIL import ImageTk,Image  

import random
import math

#Canvas is global -\_(",)_/-

class Card(object):
    def __init__(self,value,suit):
        self.value = value
        self.suit = suit
        #MOD
        self.isFaceUp = True#False
        self.color = "white"
        self.backColor = 'blue'
        self.size = 50
        self.phi = (1.0 + 5.0**0.5) / 2

    def flip(self):
        self.isFaceUp = not self.isFaceUp

    def move(self, cx, cy):
        self.cx, self.cy = cx, cy
        assert(type(self.cx) == int and type(self.cy) == int)
    
    def getRect(self, size = 50):
        #width and height radius (wr, wh)
        #return topleft and bottomright coords
        #copy
        wr = size / 2
        hr = int(wr * self.phi)
        x1, x2 = self.cx - wr, self.cx + wr
        y1, y2 = self.cy - hr, self.cy + hr
        return (x1, y1),(x2, y2)

    def drawRect(self,p1,p2,color,w):
        canvas.create_rectangle(p1[0], p1[1], 
                                p2[0], p2[1],
                                fill = color, width = w)
        pass
        
    def drawCard(self):
        #copy
        size = self.size
        p1, p2 = self.getRect()
        self.drawRect(p1,p2,self.color,2)
        color = 'black'
        if self.isFaceUp:
            if self.suit == '♦' or self.suit == '♥': color = 'red'
            name = '' + self.value + self.suit            
            canvas.create_text(self.cx - (size/2), self.cy - (size*self.phi/2), 
                               anchor = NW, text = name, fill = color, font = 10)
        else:
            p1, p2 = self.getRect(size-6)
            self.drawRect(p1,p2,self.backColor,2)

class Deck(object):
    def __init__(self):
        self.size = 52
        self.deck = []
        self.values = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
        self.suits = ['C','D','H','S']
        self.suits = ['♠','♦','♥','♣']
        self.makeDeck()

    def makeDeck(self):
        #makes a card for each combo of values and suits, puts them into the deck
        for v in self.values:
            for s in self.suits:
                card = Card(v,s)
                self.deck.append(card)
        random.shuffle(self.deck)
        assert(len(self.deck) == self.size)

    def deal(self):
        return self.deck.pop()
    
    def rotate(self):
        pass


class Stack(object):
    def __init__(self, column = 0):
        self.stack = []
        self.column = column
        
    def len(self):
        return len(self.stack)
        
    def push(self,item):
        #adds item to top of stack
        #basically asserts item is a Card
        assert(type(item.suit) == str)
        if self.isLegal(item):
            self.stack.append(item)
        #returns if operation was successful or not
        return self.isLegal(item)

    def top(self):
        return self.stack[-1]
        
    def pop(self):
        # removes and returns item from top of stack
        return self.stack.pop(-1)

    def isLegal(self,item):
        return True

    def add(self, items):
        #pushes list of items to the stack
        for item in items:
            self.push(item)
    
    def remove(self, items):
        #pushes list of items to the stack
        new = []
        #can't remove more items than exist
        assert (items <= len(self.stack))
        for item in range(items):
            new.append(self.stack.pop())
        return new

    def isPointInBB(self,x,y,p1,p2):
        return (p1[0] < x and x < p2[0] and
                p1[1] < y and y < p2[1])

    def cut(self, stack, itemNum):
        #puts the top 'itemNum' of items in current stack onto the new one
        tempStack = Stack()
        tempStack.add(stack.remove(toRemove))



class  MixedStack(Stack):
    def __init__(self, column):
        super(MixedStack, self).__init__(column)
        #self.column = column
        
    def isLegal(self,item):
        return True

    def getStackBB(self):
        p1, fake = self.stack[0].getRect()
        fake, p2 = self.stack[-1].getRect()
        return p1,p2
    
    def getTopClicked(self,x,y):
        #for each card in stack
        for card_i in range(len(self.stack)):
            #inverse of card index to go backwards through list
            card_i_reversed = len(self.stack) - 1 - card_i
            card = self.stack[card_i_reversed]
            p1, p2 = card.getRect()
            if card.isFaceUp and self.isPointInBB(x,y,p1,p2):
                return card_i_reversed
        return False

    def clicked(self, x ,y):
        card_i = self.getTopClicked(x,y)
        print('col:',self.column,'card_i:',card_i)
        card = self.stack[card_i]
        print(card.value,card.suit)
        toRemove = len(self.stack) - card_i

    def draw(self,start):
        #draws stack starting at a center point, building downwards
        vertSpacer = 20
        x = start[0]
        for cardPos in range(self.len()):
        #goes through each card in the current mixed stack
            y = start[1] + vertSpacer*cardPos
            self.stack[cardPos].move(x,y)
            self.stack[cardPos].drawCard()
        
class  OrderedStack(Stack):
    def __init__(self, column):
        super(OrderedStack, self).__init__(column)
        #self.column = column
        
    def isLegal(self,item):
        return True

class  DragStack(MixedStack):
    def __init__(self, column = 7):
        super(DragStack, self).__init__(column)
        #self.column = column
        
    def isLegal(self,item):
        return True
    
    #need draw method

class Animation(object):

    def mousePressed(self,event):
        x, y = event.x, event.y
        yMid = self.mixed[0].getStackBB()[0][1]
        #print ("Lower?",y > yMid)
        if y < yMid:
            #something was clicked in top half of screen
            pass
        else:
            #something clicked in lower half of screen
            for stack in self.mixed:
                bb = stack.getStackBB()
                #bb is tuple of bounding box corners TopLeft,BottomRight
                if self.isPointInBB(x,y,bb[0],bb[1]): 
                    self.mixedStackClicked(x,y,stack)
        self.redrawAll()
    
    def mixedStackClicked(self, x, y, stack):
        if self.dragging:
            pass
        else:
            if type(stack.getTopClicked(x,y)) == int:
                stack.clicked(x,y)
    
                #OK fuck need a new "dragstack" obj that can draw itself relative to mouse
                #self.dragStack.add(tempStack.remove(toRemove)))
    
    def keyPressed(self,event):
        if event.keysym == "space":
            self.isShot = True
        if event.keysym == "h":
            self.helpUp = not self.helpUp
        self.redrawAll()

    

    def isPointInBB(self,x,y,p1,p2):
        #determines if a point is in a bounding box
        #TESTNEEDED
        return (p1[0] < x and x < p2[0] and
                p1[1] < y and y < p2[1])

    
    def timerFired(self):
        
        '''
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
        '''

        self.redrawAll()
        delay = 10 # milliseconds
        canvas.after(delay, self.timerFired) # pause, then call timerFired again
    
    def redrawAll(self):
        canvas.delete(ALL)
        canvas.create_rectangle(0,0, 
                                self.width + 1, self.height + 1, 
                                fill = self.backgroundColor) 
        self.drawStacks()
        Test().testStack()
        
    def getBB(self, cx, cy):
        #gets card shaped bounding box at cx,cy
        self.cx, self.cy = cx, cy
        assert(type(self.cx) == int and type(self.cy) == int)
        size = 50
        phi = (1.0 + 5.0**0.5) / 2
        wr = size / 2
        hr = int(wr * phi)
        x1, x2 = cx - wr, cx + wr
        y1, y2 = cy - hr, cy + hr
        return (x1, y1),(x2, y2)    
        
    def init(self):
        self.deck = Deck()
        self.backgroundColor = 'green'
        self.dragging = False
        self.dragStack = MixedStack(7)
        self.makeStacks()
        #Test().testSetup(self.mixed)

    def makeStacks(self):
        self.temp = Stack()
        self.mixed = [MixedStack(i) for i in range(7)]
        self.ordered = [OrderedStack(i) for i in range(4)]
        for i in range(7):
            for stack in self.mixed:
                if stack.column >= i:
                    stack.push(self.deck.deal())
                    #MOD
                    if stack.column == i: pass#stack.stack[-1].flip()

    

    def drawStacks(self):
        spacer = 100
        left = 90
        mixedHeight = 200
        for stackCol in range(len(self.mixed)):
        #iterates through each stack in the list of mixed stacks
            x = left + spacer*stackCol
            self.mixed[stackCol].draw((x,mixedHeight))
        
    def drawHelp(self):
        canvas.create_text(250,240,text = "Use mouse to aim")
        canvas.create_text(250,250,text = "Press Space to shoot")
        canvas.create_text(250,260,text = "Get to 25 Points!")
              
    
    def run(self):
        global canvas
        root = Tk()
        self.width, self.height = 800, 600
        canvas = Canvas(root, width = self.width, height = self.height)
        canvas.pack()
        self.init()
        root.bind("<Button-1>", lambda event: self.mousePressed(event))
        root.bind("<Key>", lambda event: self.keyPressed(event))
        self.timerFired()
        root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

class Test(object):
    def __init__(self):
        #self.runTests()
        pass

    def runTests(self):
        self.testStack()
        #self.testCard()
        print('Tests Passed')
        pass

    def testStack(self):
        card1 = Card('A','diamonds')
        card2 = Card('2','spades')
        stack = Stack()
        stack.push(card1)
        assert(stack.len() == 1)
        stack.push(card2)
        assert(stack.len() == 2)
        pop = stack.pop()
        assert(stack.len() == 1) 
        assert(pop.suit == 'spades')
        assert(pop.value == '2')
        pop = stack.pop()
        assert(stack.len() == 0 and pop.suit == 'diamonds' and pop.value == 'A')
        stack.add([card1,card2])
        assert(stack.len() == 2)
        assert(stack.top().suit == 'spades')
        pop = stack.pop()
        assert(pop.suit == 'spades' and pop.value == '2')
        stack.push(card2)
        assert(stack.len() == 2)
        stack.remove(2)
        assert(stack.len() == 0)
        self.testGetStackBB()
 

    def testSetup(self,mixed):
        for stack in mixed:
            for card in stack.stack:
                print(card.value,card.suit,card.isFaceUp)


    def testCard(self):
        card = Card('A','S')
        card.move(400,300)
        card.drawCard()
        
        card2 = Card('10', 'H')
        card2.move(200,300)
        card2.flip()
        card2.drawCard()
        pass

    def testGetStackBB(self):
        card1 = Card('A','diamonds')
        card2 = Card('2','spades')
        stack = MixedStack(0)
        card1.move(200,200)
        stack.push(card1)
        assert(card1.getRect() == stack.getStackBB())
   
        


    def testDeck(self):
        pass

animation = Animation()
animation.run()