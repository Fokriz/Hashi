import pygame, sys
import random



TypeLines = '|#-=' 
Numbers  = '12345678'
genLevel = 0
pobeda = False
class Dot():
    countOfDots = 0
    radius = 10
    def __init__(self, x = 0, y = 0, value = 1, genLvl = -1):
        Dot.countOfDots += 1
        self.x = x
        self.y = y
        self.value = value #Количесво соеденений в точке
        self.genLevel = genLvl
        self.count = self.value
        self.free = {
                'UP'    : True,
                'DOWN'  : True,
                'LEFT'  : True,
                'RIGHT' : True
                }
        self.connect = {
                'UP'    : 0,
                'DOWN'  : 0,
                'LEFT'  : 0,
                'RIGHT' : 0
                }
        self.lineTo = {
                'UP'    : 0,
                'DOWN'  : 0,
                'LEFT'  : 0,
                'RIGHT' : 0
        }
        
        self.connectVar = {
                'UP'    : 0,
                'DOWN'  : 0,
                'LEFT'  : 0,
                'RIGHT' : 0
        }
    
    def __str__(self):
        a = '\n\t'
        return 'Dot:' + a + 'countOfDots: ' + str(self.countOfDots) + a + 'x: ' + str(self.x) + a + 'y: ' + str(self.y) + a + 'value: ' + str(self.value) + a + 'count: ' + str(self.count) + a + 'free: ' + str(self.free) + a+ 'connect: ' + str(self.connect)
    
    def updateConnectVar(self):
        for i in self.lineTo:
            self.connectVar[i] = self.lineTo[i]
    
    def updateDot(self):
        self.free = {
                'UP'    : True,
                'DOWN'  : True,
                'LEFT'  : True,
                'RIGHT' : True
                }
        
    def updateCount(self):
        self.count = self.value
        for i in self.connect:
            self.count -= self.connect[i] 
    
    def cleanConnect(self):
        for i in self.connect:
            self.connect[i] = 0
    
    def updateConnect(self, table):
        if self.x > 0:
            if table.table[self.x - 1][self.y] == table.LINES['H']:
                self.connect['LEFT'] = 1
            elif table.table[self.x - 1][self.y] == table.LINES['HD']:
                self.connect['LEFT'] = 2
        if self.x < table.width - 1:
            if table.table[self.x + 1][self.y] == table.LINES['H']:
                self.connect['RIGHT'] = 1
            elif table.table[self.x + 1][self.y] == table.LINES['HD']:
                self.connect['RIGHT'] = 2
        if self.y > 0:
            if table.table[self.x][self.y - 1] == table.LINES['V']:
                self.connect['UP'] = 1
            elif table.table[self.x][self.y - 1] == table.LINES['VD']:
                self.connect['UP'] = 2
        if self.y < table.height - 1:
            if table.table[self.x][self.y + 1] == table.LINES['V']:
                self.connect['DOWN'] = 1
            elif table.table[self.x][self.y + 1] == table.LINES['VD']:
                self.connect['DOWN'] = 2
    
    def randomFree(self): #Случайная свободная сторона
        flag = False
        m = []
        for i in self.free:
            if self.free[i]:
                m.append(i)
                flag = True
        if flag:
            return m[random.randint(0, len(m) - 1)]
        else:
            return 'NO'
        
    def countOfFree(self):
        count = 0
        for i in self.free:
            count += int(self.free[i])
        return count
    
    def brokenDot(self):
        for i in self.free:
            self.free[i] = False
    
    def testLineTo(self, table):
        for i in self.lineTo:
            self.lineTo[i] = 0

        if self.free['LEFT']:
            for i in range(self.x - 1,-1,-1):
                if (table.table[i][self.y] == table.EMPTY) and (i != 0):
                    self.lineTo['LEFT'] += 1
                elif table.table[i][self.y] in Numbers:   
                    break
                else:
                    self.lineTo['LEFT'] = 0
                    break
                
        if self.free['RIGHT']:
            for i in range(self.x+1,table.width):
                if table.table[i][self.y] in Numbers:
                    self.lineTo['RIGHT'] = i - self.x - 1
                    break
                if table.table[i][self.y] in TypeLines:
                    break
        if self.free['UP']:
            for i in range(self.y - 1,-1,-1):
                if (table.table[self.x][i] == table.EMPTY) and (i != 0):
                    self.lineTo['UP'] += 1
                elif table.table[self.x][i] in Numbers:
                    break
                else:
                    self.lineTo['UP'] = 0
                    break
        if self.free['DOWN']:
            for i in range(self.y+1,table.height):
                if table.table[self.x][i] in Numbers:
                    self.lineTo['DOWN'] = i - self.y - 1
                    break
                if table.table[self.x][i] in TypeLines:
                    break                    
    
    def testOnBorders(self, table):
        if self.x < 2:
            self.free['LEFT'] = False
        if self.y < 2:
            self.free['UP'] = False
        if self.x > table.width - 3:
            self.free['RIGHT'] = False
        if self.y > table.height - 3:
            self.free['DOWN'] = False
    
    def testOnLines(self, table):
        if self.free['LEFT']:
            if table.table[self.x - 1][self.y] in TypeLines or table.table[self.x - 2][self.y] in TypeLines:
                self.free['LEFT'] = False
        if self.free['RIGHT']:
            if table.table[self.x + 1][self.y] in TypeLines or table.table[self.x + 2][self.y] in TypeLines:
                self.free['RIGHT'] = False
        if self.free['UP']:
            if table.table[self.x][self.y - 1] in TypeLines or table.table[self.x][self.y - 2] in TypeLines:
                self.free['UP'] = False
        if self.free['DOWN']:
            if table.table[self.x][self.y + 1] in TypeLines or table.table[self.x][self.y + 2] in TypeLines:
                self.free['DOWN'] = False

    def testOnNumbers(self, table):
        if self.free['LEFT']:
            if table.table[self.x - 1][self.y] in Numbers:
                self.brokenDot()
            if table.table[self.x - 2][self.y] in Numbers:
                self.free['LEFT'] = False
            if testOnNumberAround(table, self.x - 2, self.y):
                self.free['LEFT'] = False
        if self.free['RIGHT']:
            if table.table[self.x + 1][self.y] in Numbers:
                self.brokenDot()
            if table.table[self.x + 2][self.y] in Numbers:
                self.free['RIGHT'] = False
            if testOnNumberAround(table, self.x + 2, self.y):
                self.free['RIGHT'] = False
        if self.free['UP']:
            if table.table[self.x][self.y - 1] in Numbers:
                self.brokenDot()
            if table.table[self.x][self.y - 2] in Numbers:
                self.free['UP'] = False
            if testOnNumberAround(table, self.x, self.y - 2):
                self.free['UP'] = False
        if self.free['DOWN']:
            if table.table[self.x][self.y + 1] in Numbers:
                self.brokenDot()
            if table.table[self.x][self.y + 2] in Numbers:
                self.free['DOWN'] = False
            if testOnNumberAround(table, self.x, self.y + 2):
                self.free['DOWN'] = False
        
class GameTable():
    LINES = {
            'V'  : '|',
            'VD' : '#',
            'H'  : '-',
            'HD' : '='
            }
    EMPTY = ' '
    def __init__(self, height = 10, width = 10):
        self.height = height
        self.width = width
        self.table = [[self.EMPTY for i in range(height)] for j in range(width)]
    def __str__(self):
        s = ''
        for i in range(self.height):
            for j in range(self.width):
                s += self.table[j][i]
            s += '\n'
        return s
    
    def clean(self):
        for i in range(self.width):
            for j in range(self.height):
                if self.table[i][j] in TypeLines:
                    self.table[i][j] = self.EMPTY

def testFree(dot):
    maxNumber = 0
    for i in dot.free:
        if dot.free[i]:
            maxNumber += 2
    return maxNumber

def testConnect(dot):
    minNumber = 0
    for i in dot.connect:
        minNumber += dot.connect[i]
    return minNumber
    
def testOnNumberAround(table, x, y):
    if x > 0:
        if table.table[x - 1][y] in Numbers:
            return True
    if x < table.width - 1:
        if table.table[x + 1][y] in Numbers:
            return True
    if y > 0:
        if table.table[x][y - 1] in Numbers:
            return True
    if y < table.height - 1:
        if table.table[x][y + 1] in Numbers:
            return True
    return False
    

def distance(table, dot, choice):
    xp = 0
    yp = 0
    if choice == 'LEFT':
        xp = - 1
    elif choice == 'RIGHT':
        xp = 1
    elif choice == 'UP':
        yp = - 1
    elif choice == 'DOWN':
        yp = 1
    x = dot.x + xp
    y = dot.y + yp
    dis = 0
#    print(dot)
#    print('Distance:\n\tx: ' + str(x) + '\n\ty: ' + str(y) + '\n\tchoice: ' + choice)
    while (table.table[x][y] == table.EMPTY) and (x > 0) and (y > 0) and (x < table.width - 1) and (y < table.height - 1):
        x += xp
        y += yp
        dis += 1
    if table.table[x][y] in Numbers:
        dis -= 1
    else:
        if dis < 2:
            dis = 2
#    print('\tdis: ', dis)
    return dis

def makeConnect(table, dot, free, connect = ''):
    global dots
    H = 'H'
    V = 'V'
    if connect == 'Double':
        H = 'HD'
        V = 'VD'
    dis = distance(table, dot, free)
    if dis > 1:
        dis = random.randint(2, dis)
        disw = dis
        flag = True
        while (disw > 1) and (flag):
            if (free == 'LEFT') and (testOnNumberAround(table, dot.x - disw, dot.y)):
                disw -= 1
            elif (free == 'RIGHT') and (testOnNumberAround(table, dot.x + disw - 1, dot.y)):
                disw -= 1
            elif (free == 'UP') and (testOnNumberAround(table, dot.x, dot.y - disw)):
                disw -= 1
            elif (free == 'DOWN') and (testOnNumberAround(table, dot.x, dot.y + disw - 1)):
                disw -= 1
            else:
                flag = False
                
        if flag:
            dot.free[free] = False
        else:
            if disw > 2:
                disw -= 1
            dis = disw
            if free == 'LEFT':
                for j in range(dot.x - dis, dot.x):
                    table.table[j][dot.y] = table.LINES[H]
                dots.append(Dot(dot.x - dis, dot.y))
            elif free == 'RIGHT':
                for j in range(dot.x + 1, dot.x + dis):
                    table.table[j][dot.y] = table.LINES[H]
                dots.append(Dot(dot.x + dis, dot.y))
            elif free == 'UP':
                for j in range(dot.y - dis, dot.y):
                    table.table[dot.x][j] = table.LINES[V]
                dots.append(Dot(dot.x, dot.y - dis))
            elif free == 'DOWN':
                for j in range(dot.y + 1, dot.y + dis):
                    table.table[dot.x][j] = table.LINES[V]
                dots.append(Dot(dot.x, dot.y + dis))
            dots[dot.countOfDots - 1].genLevel = dot.genLevel + 1
            dots[dot.countOfDots - 1].testOnBorders(table)
            dots[dot.countOfDots - 1].testOnLines(table)
            dots[dot.countOfDots - 1].testOnNumbers(table)
            dots[dot.countOfDots - 1].updateConnect(table)
            if testFree(dots[dot.countOfDots - 1]):
                dots[dot.countOfDots - 1].value = testConnect(dots[dot.countOfDots - 1]) + random.randint(1, testFree(dots[dot.countOfDots - 1]))
            else:
                dots[dot.countOfDots - 1].value = testConnect(dots[dot.countOfDots - 1])
            table.table[dots[dot.countOfDots - 1].x][dots[dot.countOfDots - 1].y] = str(dots[dot.countOfDots - 1].value)
    else:
        dot.testOnBorders(table)
        dot.testOnLines(table)
        dot.testOnNumbers(table)
        dot.updateConnect(table)
        dot.updateCount()
#    print(table)
#    a = input()
        

def levelGen(table, dot):
    dot.testOnBorders(table)
    dot.testOnLines(table)
    dot.testOnNumbers(table)
    dot.updateConnect(table)
    dot.updateCount() 
    while dot.count:
        maxNumber = testFree(dot)
        free = dot.randomFree()
        if free != 'NO':
            if dot.count == maxNumber:
                makeConnect(table, dot, free, 'Double')
            elif dot.count > 1:
                if random.randint(0, 1):
                    makeConnect(table, dot, free, 'Double')
                else:
                    makeConnect(table, dot, free, 'One')
            elif dot.count == 1:
                makeConnect(table, dot, free, 'One')
        else:
            dot.value = testConnect(dot)
            table.table[dot.x][dot.y] = str(dot.value)
        dot.testOnLines(table)
        dot.updateConnect(table)
        dot.updateCount() 

def mainGen(table):
    global dots
    global genLevel
    flag = False
    for dot in dots:
        if dot.genLevel == genLevel:
            levelGen(table, dot)
            flag = True
    genLevel += 1
    if flag:
        mainGen(table)

pygame.init()
Buttons = [pygame.image.load('button_1.png'),pygame.image.load('button_2.png'),
pygame.image.load('button_3.png'),pygame.image.load('button_4.png')]

SelectButtons = [pygame.image.load('selectbutton_1.png'),pygame.image.load('selectbutton_2.png'),
pygame.image.load('selectbutton_3.png'),pygame.image.load('selectbutton_4.png')]

run = True
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Hashi Game")
win.fill((255,255,255))
while run:
    for i in range(4):
        win.blit(Buttons[i],(100,50*(i*2 +1)))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
	        run = False
	        sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x , y = event.pos
            if event.button == 1:
                if (x > 99) and (x < 401):
                    if (y > 49) and (y < 101):
                        width = 15
                        height = 15
                        run = False
                    if (y > 149) and (y < 201):
                        width = 25
                        height = 25
                        run = False
                    if (y > 249) and (y < 301):
                        width = 35
                        height = 35
                        run = False
                    if (y > 349) and (y < 401):
                        sys.exit()                
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos 
            if (x > 99) and (x < 401):
                if (y > 49) and (y < 101):
                    win.blit(SelectButtons[0],(100,50))
                if (y > 149) and (y < 201):
                    win.blit(SelectButtons[1],(100,150))
                if (y > 249) and (y < 301):
                    win.blit(SelectButtons[2],(100,250))
                if (y > 349) and (y < 401):
                    win.blit(SelectButtons[3],(100,350))              
        pygame.display.update()
Table = GameTable(height, width)	     
dots = []
dots.append(Dot(random.randint(0, Table.width - 1), 0))
dots[0].testOnBorders(Table)
dots[0].value = random.randint(3, testFree(dots[0]))
Table.table[dots[0].x][dots[0].y] = str(dots[0].value)
dots[0].genLevel = 0
mainGen(Table)

#print(Table)

playerTable = GameTable(Table.height, Table.width)
for i in range(Table.width):
    for j in range(Table.height):
        playerTable.table[i][j] = Table.table[i][j]
playerTable.clean()
for i in dots:
    i.updateDot()
    i.testOnBorders(playerTable)
    i.testLineTo(playerTable)
    i.updateConnectVar()

imageOnNumber = [pygame.image.load('num_1.jpg'),pygame.image.load('num_2.jpg'),
pygame.image.load('num_3.jpg'),pygame.image.load('num_4.jpg'),
pygame.image.load('num_5.jpg'),pygame.image.load('num_6.jpg'),
pygame.image.load('num_7.jpg'),pygame.image.load('num_8.jpg')]

imageOffNumber = [pygame.image.load('nonum_1.jpg'),pygame.image.load('nonum_2.jpg'),
pygame.image.load('nonum_3.jpg'),pygame.image.load('nonum_4.jpg'),
pygame.image.load('nonum_5.jpg'),pygame.image.load('nonum_6.jpg'),
pygame.image.load('nonum_7.jpg'),pygame.image.load('nonum_8.jpg')]

imageLine = {   'V' : pygame.image.load('V_line.jpg'),
                'VD': pygame.image.load('VD_line.jpg'),
                'H' : pygame.image.load('H_line.jpg'),
                'HD': pygame.image.load('HD_line.jpg')}

imageSelectNumber =  [pygame.image.load('Sel_1.jpg'),pygame.image.load('Sel_2.jpg'),
pygame.image.load('Sel_3.jpg'),pygame.image.load('Sel_4.jpg'),
pygame.image.load('Sel_5.jpg'),pygame.image.load('Sel_6.jpg'),
pygame.image.load('Sel_7.jpg'),pygame.image.load('Sel_8.jpg')]

r = 10

win = pygame.display.set_mode((Table.width*2*r,Table.height*2*r))

pygame.display.set_caption("Hashi Game")
win.fill((255,255,255))

def testOnWin():
    global Table
    global playerTable
    for i in range(Table.width):
        for j in range(Table.height):
            if Table.table[i][j] != playerTable.table[i][j]:
                return False
    return True
                
def drawWindow():
    global playerTable
    for i in dots:
	    win.blit(imageOnNumber[i.value-1],(i.x*2*r,i.y*2*r))
	    i.cleanConnect()
	    i.updateConnect(playerTable)
	    i.updateCount()
	    if i.count == 0:
	        win.blit(imageOffNumber[i.value-1],(i.x*2*r,i.y*2*r))
	    if (selectDot.x == i.x) and (selectDot.y == i.y):
	        win.blit(imageSelectNumber[selectDot.value-1],(selectDot.x*2*r,selectDot.y*2*r))
    for i in range(playerTable.width):
        for j in range(playerTable.height):
            if playerTable.table[i][j] in TypeLines:
                for t in playerTable.LINES:
                    if playerTable.table[i][j] == playerTable.LINES[t]:
                        win.blit(imageLine[t], (i*2*r, j*2*r))
	            
	       
    pygame.display.update()

def drawPossibleLine():
     if event.type == pygame.MOUSEMOTION:  
	        x , y = event.pos
	        flag = True                                            
	        for i in dots:
	            if (x//20 == i.x) and (y//20 == i.y) and (i.count != 0):
	                #print(i.x, i.y)
	                i.testLineTo(playerTable)
	                if i.lineTo['LEFT']:
	                    pygame.draw.rect(win,(97,91,91),((i.x - i.lineTo['LEFT'])*2*r,i.y*2*r+8, i.lineTo['LEFT']*2*r, 4))
	                if i.lineTo['RIGHT']:
	                    pygame.draw.rect(win,(97,91,91),((i.x+1)*2*r,i.y*2*r+8, i.lineTo['RIGHT']*2*r, 4))
	                if i.lineTo['UP']:
	                    pygame.draw.rect(win,(97,91,91),(i.x*2*r+8,(i.y - i.lineTo['UP'])*2*r, 4, i.lineTo['UP']*2*r))
	                if i.lineTo['DOWN']:
	                    pygame.draw.rect(win,(97,91,91),(i.x*2*r+8,(i.y+1)*2*r, 4, i.lineTo['DOWN']*2*r))
	                flag = False
	        if flag:
	            win.fill((255,255,255))
	            drawWindow()                    

def drawLine():
    global pobeda
    global selectDot
    global playerTable
    if event.type == pygame.MOUSEBUTTONDOWN:
        x , y = event.pos
        for i in dots:
            if (x//20 == i.x) and (y//20 == i.y):
                if event.button == 1:
                    if (selectDot.x == i.x):
                        if (selectDot.y - selectDot.connectVar['UP'] - 1) == i.y:
                            if selectDot.lineTo['UP'] != 0:
                                for j in range(i.y + 1, selectDot.y):
                                    if (playerTable.table[i.x][j] == playerTable.EMPTY) and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[i.x][j] = playerTable.LINES['V']
                            elif selectDot.connect['UP'] > 0:
                                for j in range(i.y + 1, selectDot.y):
                                    if (playerTable.table[i.x][j] == playerTable.LINES['V']) and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[i.x][j] = playerTable.LINES['VD']
                                    elif (playerTable.table[i.x][j] == playerTable.LINES['VD']):
                                        playerTable.table[i.x][j] = playerTable.EMPTY
                                    if (playerTable.table[i.x][j] == playerTable.LINES['V']) and ((i.count == 0) or (selectDot.count == 0)):
                                        playerTable.table[i.x][j] = playerTable.EMPTY
                        if ((selectDot.y + selectDot.connectVar['DOWN'] + 1) == i.y): 
                            if (selectDot.lineTo['DOWN'] != 0):
                                for j in range(selectDot.y + 1, i.y):
                                    if (playerTable.table[i.x][j] == playerTable.EMPTY)  and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[i.x][j] = playerTable.LINES['V']
                            elif selectDot.connect['DOWN'] > 0:
                                for j in range(selectDot.y + 1, i.y):
                                    if (playerTable.table[i.x][j] == playerTable.LINES['V']) and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[i.x][j] = playerTable.LINES['VD']
                                    elif (playerTable.table[i.x][j] == playerTable.LINES['VD']):
                                        playerTable.table[i.x][j] = playerTable.EMPTY   
                                    if (playerTable.table[i.x][j] == playerTable.LINES['V']) and ((i.count == 0) or (selectDot.count == 0)):
                                        playerTable.table[i.x][j] = playerTable.EMPTY
                    elif selectDot.y == i.y:
                        if (selectDot.x - selectDot.connectVar['LEFT'] - 1) == i.x:
                            if (selectDot.lineTo['LEFT'] != 0):
                                for j in range(i.x + 1, selectDot.x):
                                    if (playerTable.table[j][i.y] == playerTable.EMPTY) and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[j][i.y] = playerTable.LINES['H']
                            elif selectDot.connect['LEFT'] > 0:
                                for j in range(i.x + 1, selectDot.x):          
                                    if (playerTable.table[j][i.y] == playerTable.LINES['H']) and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[j][i.y] = playerTable.LINES['HD']
                                    elif (playerTable.table[j][i.y] == playerTable.LINES['HD']):
                                        playerTable.table[j][i.y] = playerTable.EMPTY
                                    if (playerTable.table[j][i.y] == playerTable.LINES['H']) and ((i.count == 0) or (selectDot.count == 0)):
                                        playerTable.table[j][i.y] = playerTable.EMPTY
                        if (selectDot.x + selectDot.connectVar['RIGHT'] + 1) == i.x:
                            if (selectDot.lineTo['RIGHT'] != 0):
                                for j in range(selectDot.x + 1, i.x):
                                   if (playerTable.table[j][i.y] == playerTable.EMPTY) and (i.count != 0) and (selectDot.count != 0):
                                       playerTable.table[j][i.y] = playerTable.LINES['H']
                            elif selectDot.connect['RIGHT'] > 0:
                                for j in range(selectDot.x + 1, i.x):      
                                    if (playerTable.table[j][i.y] == playerTable.LINES['H']) and (i.count != 0) and (selectDot.count != 0):
                                        playerTable.table[j][i.y] = playerTable.LINES['HD']
                                    elif (playerTable.table[j][i.y] == playerTable.LINES['HD']):
                                        playerTable.table[j][i.y] = playerTable.EMPTY
                                    if (playerTable.table[j][i.y] == playerTable.LINES['H']) and ((i.count == 0) or (selectDot.count == 0)):
                                        playerTable.table[j][i.y] = playerTable.EMPTY
                                           
                selectDot = i
                #print(playerTable)
                pobeda = testOnWin()
                
            
selectDot = Dot(-1, -1)
run = True
while run:

	for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        run = False
	        sys.exit()
	    drawPossibleLine()
	    drawLine()
	drawWindow()
	if pobeda:
	    run = False

YouWin = pygame.image.load('win.png')

win = pygame.display.set_mode((640,480))

pygame.display.set_caption("Hashi Game")
win.fill((255,255,255))
run = True
while run:
    for event in pygame.event.get():
	    if event.type == pygame.QUIT:
	        run = False
	        sys.exit()
    win.blit(YouWin,(0,0))
    pygame.display.update()
pygame.quit()            
            
