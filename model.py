# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 10:17:59 2017

@author: gy17mjk

Creates agents and assigns xy value, moves agents and interacts with environment and each other

the agents are created with xy values taken from the university of leeds website using webscraping,
if no data is found, random interger between 0 and 99 is used.
agents moves 1 step at a time in a random direction, 'eating' environment data and storing it 
(environment= any DEM/ list of values, needs to be loaded prior to running code and called in.txt), if they come within the distance set up
in neighbourhood, they will share their total store of data between each other.
Running code will bring up GUI, where model can be run, an animation will play and stop when condition met, either num_of_iterations reached
or max_store reached. Environment then stored (out.txt) and total.store appended to store.txt.

arguments-

num_of_agents -int
num_of_interations -int
neighbourhood -int/float
max_store -int/float
environment input (in.txt) -int/float
matplotlib.pyplot.ylim- int
matplotlib.pyplot.xlim- int

returns-

animation showing agents interacting with environment
environment output (out.txt) -int/float
total store of agents (store.txt) -float
"""


import matplotlib.pyplot
import matplotlib.animation
import agentframework
import csv
import random
import tkinter
import matplotlib.backends.backend_tkagg
import requests
import bs4


#get starting x,y values from website
r = requests.get('http://www.geog.leeds.ac.uk/courses/computing/practicals/python/agent-framework/part9/data.html')
content = r.text
soup = bs4.BeautifulSoup(content, 'html.parser')
td_ys = soup.find_all(attrs={"class" : "y"})
td_xs = soup.find_all(attrs={"class" : "x"})


#load in environment
f = open('in.txt', newline='')
environment = []
reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)
for row in reader:
    rowlist = []         		# A list of rows
    for value in row:				# A list of value
        rowlist.append(value)
    environment.append(rowlist)				# Floats
f.close() 	# Don't close until you are done with the reader;
		# the data is read on request.

#set amount of agents
num_of_agents = 10

#set amount of interations (steps)
num_of_iterations = 100

#set neighbourhood
neighbourhood = 20

#set max store for animation
max_store = 100000


agents = []


fig = matplotlib.pyplot.figure(figsize=(7,7))
ax = fig.add_axes([0,0,1,1])

#ax.set_autoscale_on(False)

#create set of variables in list, assign each of i a value
for i in range(num_of_agents):
    y= int(td_ys[i].text)
    x= int(td_xs[i].text)
    agents.append(agentframework.Agents(environment,agents, y, x))


carry_on = True


def update(frame_number):
    """
    until stopping condition is met it moves agents, makes them eat and share with neighbours
    and generates a frame of the animation. 
    
    stopping conditions are set as the num_of_iterations or if the max_store of agents is met.
    if value is less than these defined values it will repeat. on each repeat the agents preform
    a move funtion, an eat function and a share_with_neighbours function, the criteria for the
    stopping codition is then checked again, and the next frame for the animation is produced 
    (frame_number).
    
    arguments-
    
    num_of_iterations- int
    agents -int
    neighbourhood -float
    store- float
    max_store -float
    num_of_agents -int
    environment -int/float
    matplotlib.pyplot.ylim- int
    matplotlib.pyplot.xlim- int
    
    returns-
    
    store.txt- will also print "stopping condition met, total store = [VALUE]" when 
        stopping condition met this by max_store -float 
    frame in animation
    """
    fig.clear()
    global carry_on #makes animations continue until set otherwise.
    
    
#Randomly move 'j' times and eat
    for j in range(num_of_iterations):
        random.shuffle(agents)
        for agent in agents:
            agent.move()
            agent.eat()
            agent.share_with_neighbours(neighbourhood)
      
    
    #stopping condition is set to a max agent total store    
    total = 0
    for agent in agents:
        total += agent.store
    if total >= max_store:
        carry_on = False
        print("stopping condition met, total store =",total)
        with open('store.txt', 'a',) as f3:
            f3.write(str(total)+"\n")
        
    #plot scatter for frame    
    matplotlib.pyplot.ylim(0, 99)
    matplotlib.pyplot.xlim(0, 99)
    matplotlib.pyplot.imshow(environment)
    for i in range(num_of_agents):
        matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
        #print(agents[i].x,agents[i].y)

#check for repeat
def gen_function(b = [0]):
    """
    requires no setup
    """
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (a < num_of_iterations) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1
        

#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, repeat=False, frames=num_of_iterations)
def run():
    """
    requires no setup.
    """
    animation = matplotlib.animation.FuncAnimation(fig, update, frames=gen_function, repeat=False)
    canvas.show()


#build window
root = tkinter.Tk() 
root.wm_title("Model")
canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(fig, master=root)
canvas._tkcanvas.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

menu_bar = tkinter.Menu(root)
root.config(menu=menu_bar)
model_menu = tkinter.Menu(menu_bar)
menu_bar.add_cascade(label="Model", menu=model_menu)
model_menu.add_command(label="Run model", command=run) 


#export environment
f2 = open('out.txt', 'w', newline='') 
writer = csv.writer(f2, delimiter=' ')
for row in environment:		
	writer.writerow(row)		# List of values.
f2.close()


store=[]
for i in range(num_of_agents):
   store.append(agents[i].store)

store_sum=[sum(store)]


tkinter.mainloop()