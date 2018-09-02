from tkinter import *
import random
import time
import math
from scipy import spatial
import pandas as pd
"""
Setup Background Pane
"""
root = Tk()
width = 1200
height = 600
w = Canvas(root, width=1200, height=600)
w.pack()
#Create the top text showing number of Zoa in our system
toptext = w.create_text([20,20], text=(str(0)))

"""
Helper Functions
"""
#Euclidean Distance, takes in two lists of list, returns a float
def eudist(unit1,unit2):
    return math.sqrt((unit1[0]-unit2[0])**2+(unit1[1]-unit2[1])**2)
#Cosine Similarity
def cosine(ls1, ls2):
    return 1 - spatial.distance.cosine(ls1,ls2)

#Convert a vector to unit, return a tuple
def toUnit(vector):
    size = math.sqrt(vector[0]**2+vector[1]**2)
    if(size == 0):
        return (0,0)
    return (vector[0]/size, vector[1]/size)

#Make sure zoa doesn't go beyond screen
def screenxy(vector):
    x,y = vector
    if(x>1190):
        x = 1185
    if(y>590):
        y = 585
    if(x<10):
        x = 15
    if(y<10):
        y = 15
    return (x,y)

#Return average of a list
def average(l):
    if(len(l)==0):
        return 0
    return sum(l) / float(len(l))
"""
Global Variable
"""
# A list containing all food in the system
foodls = []

#A list containing all zoa in the system
zoanls = []

#Rate of progress, the higher, the slower
rate = 0.5

#These variables are for statistics
#The program will create a csv file.
#Use the graph visualizer jupyter notebook for visualization
numfoo = []
numls = []
velocityavg = []
healthavg = []
sightavg = []
generationavg = []
sizeavg = []
eatavg = []
min1 = []
min2 = []
min3 = []
min4 = []
min5 = []
min6 = []
max1 = []
max2 = []
max3 = []
max4 = []
max5 = []
max6 = []

"""
EcoSystem is the manager class.
"""
class EcoSystem:
    def __init__(self):
        self.id = 0
        self.zid = 0
        self.count = 0
        self.stamp = 0
    """
    Provide the statistics over time in a .csv format
    """
    def calcstat(self):
        vls = []
        hls = []
        sls = []
        genls = []
        sizels = []
        eatls = []
        for zoa in zoanls:
            vtemp, maxhtemp, htemp, stemp, gen, sizetemp, mode = zoa.genetic()
            numeaten = zoa.getEat()
            vls.append(vtemp)
            hls.append(zoa.getMaxHealth())
            sls.append(stemp)
            genls.append(gen)
            sizels.append(sizetemp)
            eatls.append(numeaten)
        numfoo.append(len(foodls))
        numls.append(len(zoanls))
        velocityavg.append(average(vls))
        healthavg.append(average(hls))
        sightavg.append(average(sls))
        generationavg.append(average(genls))
        sizeavg.append(average(sizels))
        eatavg.append(average(eatls))
        min1.append(min(vls))
        min2.append(min(hls))
        min3.append(min(sls))
        min4.append(min(genls))
        min5.append(min(sizels))
        min6.append(min(eatls))
        max1.append(max(vls))
        max2.append(max(hls))
        max3.append(max(sls))
        max4.append(max(genls))
        max5.append(max(sizels))
        max6.append(max(eatls))
        df1 = pd.DataFrame({'NumZoa':numls})
        df0 = pd.DataFrame({'NumFood':numfoo})
        df2 = pd.DataFrame({'Velo':velocityavg})
        df3 = pd.DataFrame({'MaxHealth':healthavg})
        df4 = pd.DataFrame({'Sight':sightavg})
        df5 = pd.DataFrame({'Gen':generationavg})
        df6 = pd.DataFrame({'Size':sizeavg})
        df7 = pd.DataFrame({'minVelo':min1})
        df8 = pd.DataFrame({'minMaxHealth':min2})
        df9 = pd.DataFrame({'minSight':min3})
        df10 = pd.DataFrame({'minGen':min4})
        df11 = pd.DataFrame({'minSize':min5})
        df12 = pd.DataFrame({'maxVelo':max1})
        df13 = pd.DataFrame({'maxMaxHealth':max2})
        df14 = pd.DataFrame({'maxSight':max3})
        df15 = pd.DataFrame({'maxGen':max4})
        df16 = pd.DataFrame({'maxSize':max5})
        df17 = pd.DataFrame({'NumEaten':eatavg})
        df18 = pd.DataFrame({'minNumEaten':min6})
        df19 = pd.DataFrame({'maxNumEaten':max6})
        df = [df1,df0, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df13,df14,df15,df16,df17, df18,df19]
        result = pd.concat(df, axis=1, sort=False)
        result.to_csv('dataset.csv', index = False)
        """
        print("===============")
        print("Stamp", self.stamp)
        print("Number",numls[-1])
        print("Velo avg", velocityavg[-1]," Minimum: " ,min(vls), "Max: ", max(vls))
        print("health avg", healthavg[-1]," Minimum: " ,min(hls), "Max: ", max(hls))
        print("sight avg", sightavg[-1]," Minimum: " ,min(sls), "Max: ", max(sls))
        print("generation avg", generationavg[-1]," Minimum: " ,min(genls), "Max: ",max(genls))
        print('size avg', sizeavg[-1]," Minimum: " ,min(sizels), "Max: ", max(sizels))
        print('Eat avg', eatavg[-1]," Minimum: " ,min(eatls), "Max: ", max(eatls))
        """
    """
    Add food to a system. The location is randomize unless provided.
    """
    def addFood(self, x = -1, y = -1):
        if(x == -1 or y == -1):
            x = random.randint(10,1190)
            y = random.randint(10,590)
        food = Food(self.id,x,y)
        self.id+=1
        foodls.append(food)
    """
    Add Zoan to a system. A list of genetic is optional.
    Genetic is of format(velocity, maxhealth, health, sight, generation, size, method of food searching)
    """
    def addZoan(self, genetic = (3,180,180,50,0,10, 'min')):
        x = random.randint(10,1190)
        y = random.randint(10,590)
        zoa = Zoan(self.zid,x,y,genetic[0],genetic[1],genetic[2],genetic[3],genetic[4], genetic[5], genetic[6])
        self.zid+=1
        zoanls.append(zoa)
        zoa.move_zoan()
    """
    Dynamically add food to the system, also activate reproduction of Zoa
    """
    def process(self):
        self.reproduce()

        """
        Every uneaten food has a 10 percent change to generate another food nearby
        """
        if(len(foodls)<400):
            for food in foodls:
                rand = random.randint(1,100)
                if(rand<10):
                    redo = True
                    while(redo):
                        redo = False
                        xt, yt = food.location()
                        randx = random.randint(-30,30)
                        randy = random.randint(-30,30)
                        xt, yt = screenxy((xt+randx, yt+randy))
                        #Prevent food from spawning in the same spot.
                        for food in foodls:
                            locfood = food.location()
                            dist = eudist(locfood,(xt, yt))
                            if(dist<10):
                                redo = True
                    self.addFood(xt,yt)
        """
        Randomly add food all over the system. Only active if there are
        fewer than 21 foods in the system.
        """
        rand = random.randint(1,100)
        if(rand<24-len(foodls)/100):
            for i in range(10):
                self.addFood()
        #Add food immediately once all food is gone
        #Uncomment this is you plan to have a competitive system
        #if(len(foodls)<20):
        #    for i in range(20-len(foodls)):
        #        self.addFood()

        """
        Activate the statistics part, ignore this
        """
        self.count+=1
        if(self.count%5==0):
            self.stamp+=1
            self.calcstat()
            self.count = 0

        #Configure the toptext which tell the number of Zoa
        w.itemconfigure(toptext, text=(str(len(zoanls))))

        #recursion with delay
        w.after(int(rate*500), self.process)

    """
    Every Zoa has a change to reproduce with mutation
    """
    def reproduce(self):
        for zoa in zoanls:
            rand = random.randint(1,120)
            """
            The chance is higher for healthy zoa
            """
            if(rand<1+zoa.getHealth()/40 and not zoa.isHibernate()):
                vtemp,maxhtemp ,htemp, stemp, gen, sizetemp, foodmode = zoa.genetic()
                r1 = random.randint(-1,1) #Velocity
                r2 = random.randint(-10,10) #maxhealth
                r3 = random.randint(-15,15) #Sight
                r4 = random.randint(-3,3) #Size
                #Make sure size is not negative or zero
                sz =sizetemp+r4
                if(sz<1):
                     sz = 1
                #Add Zoa
                self.addZoan((vtemp+r1,maxhtemp+r2, htemp+r2, stemp+r3, gen+1,sz, foodmode))
"""
Class food represent the green food in the system
"""
class Food:
    def __init__(self, foodid ,locx, locy, energy = 40):
        self.id = foodid
        self.energy = energy
        self.size = 6
        self.locx = locx
        self.locy = locy
        self.vx = random.randint(-1,1)
        self.vy = random.randint(-1,1)
        self.body = w.create_oval([locx+self.size,locy+self.size,locx-self.size,locy-self.size], fill = 'Green')
        #self.move_food()

    #Return the location
    def location(self):
        return (self.locx, self.locy)
    #Delete the shape from the GUI
    def eaten(self):
        w.delete(self.body)
    #Return the Energy
    def getEnergy(self):
        return self.energy
    #make food move.
    def move_food(self):
        #self.evolve()
        if(self.locx+self.vx>1190):
            self.vx = -1*self.vx
        if(self.locy+self.vy>590):
            self.vy = -1*self.vy
        if(self.locx+self.vx<10):
            self.vx = -1*self.vx
        if(self.locy+self.vy<10):
            self.vy = -1*self.vy
        self.locx = self.locx+self.vx
        self.locy = self.locy+self.vy
        w.move(self.body, self.vx, self.vy)
        w.after(int(rate*200), self.move_food)
"""
Class Zoan models the Zoa.
See readme for more details.
"""
class Zoan:
    def __init__(self, zid ,locx, locy, v = 5, maxhealth = 400, health = 400, sight = 200,  gen = 0, size=10, foodmode= 'min'):
        self.velocity = v
        self.alive = True
        self.health = health
        self.maxhealth = maxhealth
        self.hibernate = False
        self.form = 0
        self.v = (0.01,0.01)
        self.gen = gen
        self.sight = sight
        self.id = zid
        self.size = size
        self.locx = locx
        self.locy = locy
        self.color = 'red'
        self.foodmode = foodmode
        self.numeaten = 0
        if(self.foodmode == 'vector'):
            self.color = 'blue'

        #Number of rankings Zoa with foodmode 'vector' will consider
        self.foodlimit = 5
        self.body = w.create_oval([locx+self.size,locy+self.size,locx-self.size,locy-self.size], fill = self.color)
        self.ssight = w.create_oval([locx+self.sight,locy+self.sight,locx-self.sight,locy-self.sight], outline = 'grey', state ='normal')
        self.text = w.create_text([self.locx,self.locy], text=(str(self.gen)))
    #Return how many food this Zoa has eaten
    def getEat(self):
        return self.numeaten
    #Return the genetics of the Zoa
    def genetic(self):
        return (self.velocity,self.maxhealth ,self.health, self.sight, self.gen, self.size, self.foodmode)
    #Return the current health of Zoa
    def getHealth(self):
        return self.health
    #Return the maximum health of Zoa
    def getMaxHealth(self):
        return self.maxhealth

    """
    Move the Zoa towards the food
    """
    def move_zoan(self):
        deltax, deltay = self.search_food()
        if(self.locx+deltax>1190):
            deltax = -1*deltax
            tx, ty = self.v
            self.v = (tx*-1, ty)
        if(self.locy+deltay>590):
            deltay = -1*deltay
            tx, ty = self.v
            self.v = (tx, ty*-1)
        if(self.locx+deltax<10):
            deltax = -1*deltax
            tx, ty = self.v
            self.v = (tx*-1, ty)
        if(self.locy+deltay<10):
            deltay = -1*deltay
            tx, ty = self.v
            self.v = (tx, ty*-1)

        self.locx = self.locx+deltax
        self.locy = self.locy+deltay
        #Move the shapes in GUI
        w.move(self.body, deltax, deltay)
        w.move(self.ssight, deltax, deltay)
        w.move(self.text, deltax, deltay)
        """
        Calculate Energy Loss from Moving
        """
        if(self.hibernate):
            self.health -= 1
        else:
            self.health -= 3+int(self.velocity/1.5)
        """
        Zoa with negative health DIES!
        """
        if(self.health<0):
            self.die()
            self.alive =  False
        if(self.alive):
            w.after(int(rate*50), self.move_zoan)
    """
    Determine the direction the Zoa is heading
    """
    def search_food(self):
        found = False
        #Founded-Food List
        ffls = []
        aggvector = [0,0]
        min = 100000000
        count2 = 0
        vx = 0
        vy = 0
        """
        Check all food in the System
        """
        for food in foodls:
            locfood = food.location()
            dist = eudist(locfood,(self.locx, self.locy))
            """
            In 'minimum distance' mode, the zoa moves towards the closest food
            """
            if(self.foodmode == 'min'):
                if(dist<self.sight and dist<min):
                    found = True
                    min = dist
                    vx, vy  = toUnit((locfood[0]-self.locx,locfood[1]-self.locy))
                    vx = vx * self.velocity
                    vy = vy * self.velocity
            else:
                """
                In vector-alignment mode, the zoa calculates the aggregate vector
                for all food in its sight, then the zoa ranks n-closest foods based
                on ranking of closeness and cosinesimilarity of the direction to the
                vector. A Zoa only considers the first 30 foods in its sight because it
                is stupid(For better performance).
                """
                if(dist<self.sight and count2 < 30):
                    count2+=1
                    found = True
                    #Make an aggregate vector of all food in its sight
                    ffls.append((food,dist,(locfood[0]-self.locx, locfood[1]-self.locy)))
                    vec = toUnit(((locfood[0]-self.locx)*(self.sight-dist), (locfood[1]-self.locy)*(self.sight-dist)))
                    aggvector = (aggvector[0]+ vec[0],aggvector[1]+vec[1])

            #eat food
            if(dist<self.size):
                self.health+=food.getEnergy()
                if(self.health>self.maxhealth):
                    self.health = self.maxhealth
                self.numeaten+=1
                food.eaten()
                w.itemconfig(self.body, fill="red")
                foodls.remove(food)

        """
        Calculate the vector-supportd rankings
        """
        if(self.foodmode == 'vector' and found == True):
            ffls.sort(key=lambda tup: tup[1])
            #bestfood = ffls[0][0]
            max = -100
            limit = self.foodlimit if self.foodlimit<len(ffls) else len(ffls)
            for i in range(limit):
                tempfood = ffls[i][0]
                locfood = tempfood.location()
                foodvector = [locfood[0]-self.locx,locfood[1]-self.locy]
                score = (self.foodlimit-i)*2/self.foodlimit +cosine(foodvector,aggvector)+0.5*cosine(foodvector,self.v)
                if(score>max):
                    max = score
                    bestfood = tempfood
            locfood = bestfood.location()
            vx, vy  = toUnit((locfood[0]-self.locx,locfood[1]-self.locy))
            w.itemconfig(self.body, fill="blue")
            vx = vx * self.velocity
            vy = vy * self.velocity
            if(vx == 0):
                vx=0.01
            if(vy==0):
                vy=0.01
            self.v = (vx,vy)
        """
        Zoa can enter 'hibernate' mode, where it moves mindlessly(randomly) in a direction
        until it comes across a food in its sight. The hibernate mode uses less energy.
        """
        if(found == False and self.hibernate == False):
            self.hibernate = True
            #w.itemconfig(self.body, fill="orange")
            vx, vy  = toUnit((random.randint(10,1190)-self.locx,random.randint(10,590)-self.locy))
            vx = vx * self.velocity
            vy = vy * self.velocity
            self.v = (vx, vy)
        else:
            if(found == True):
                self.hibernate = False
                #w.itemconfig(self.body, fill=self.color)
            else:
                vx, vy = self.v
        return vx, vy
    """
    The Zoa is dead. Noooo!
    Remove Zoa from Zoa list and remove its GUI
    """
    def die(self):
        for zoa in zoanls:
            if(zoa.getid()==self.id):
                zoanls.remove(zoa)
        #w.itemconfig(self.body, fill="blue")
        w.delete(self.body)
        w.delete(self.ssight)
        w.delete(self.text)
    def isHibernate(self):
        return self.hibernate
    def getid(self):
        return self.id

if __name__ == '__main__':
    """
    Initial Setup
    """
    ecoSys = EcoSystem()
    for i in range(50):
        ecoSys.addFood()
    for i in range(5):
        ecoSys.addZoan((3,260,260,50,0,10, 'min'))
        ecoSys.addZoan((3,190,190,50,0,10, 'vector'))

    ecoSys.process()
    root.mainloop()
