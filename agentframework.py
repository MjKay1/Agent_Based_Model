import random
import requests
import bs4

r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})

class Agents():

    
    #set x and y coordinates
    def __init__ (self,environment,agents, x=None, y=None):
        if (x == None):
            self._x = random.randint(0,99)
            print("X Data not found, Random integer used")
        else:
            self._x = x
        if (y == None):
            self._y = random.randint(0,99)
            print("Y Data not found, Random integer used")
        else:
            self._y = y
        self.environment=environment
        self.store=0
        self.agents=agents
        
    def getx(self):
        return self._x
    def gety(self):
        return self._y
  
 
    def setx(self, value):
        self._x = value
    def sety(self, value):
        self._y = value


    def delx(self):
        del self._x
    def dely(self):
        del self._y


    x = property(getx, setx, delx, "I am the 'x' Value")
    y = property(gety, sety, dely, "I am the 'y' Value")
        

    #move x and y 1 step 
    def move (self):
        if random.random() < 0.5:
            self._x = (self._x + 1) % 100
        else:
            self._x = (self._x - 1) % 100
            
        if random.random() < 0.5:
            self._y = (self._y + 1) % 100
        else:
            self._y = (self._y - 1) % 100
            
    
    def eat(self): # can you make it eat what is left?
        if self.environment[self.y][self.x] > 10:
            self.environment[self.y][self.x] -= 10
            self.store += 10
            
    
    def share_with_neighbours(self, neighbourhood):
        # Loop through the agents in self.agents .
        for agent in self.agents:
            # Calculate the distance between self and the current other agent:
            distance = self.distance_between(agent) 
            # If distance is less than or equal to the neighbourhood
            if distance <= neighbourhood:
                # Sum self.store and agent.store .
                sum = self.store + agent.store
                # Divide sum by two to calculate average.
                average = sum / 2
                # self.store = average
                self.store = average
                # agent.store = average
                agent.store = average
                
               # print("sharing " + str(distance) + " " + str(average))
            # End if
        # End loop
        #find distances
    def distance_between(self, agent):
        return(((self.x-agent.x)**2)+((self.y-agent.y)**2))**.5
            
        
        
        
        
