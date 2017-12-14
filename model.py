# -*- coding: utf-8 -*-
"""
Created on Mon Oct  9 10:17:59 2017

@author: gy17mjk
"""
"""
import matplotlib
print(matplotlib.rcParams['backend'])
matplotlib.use('Qt4Agg')
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

    fig.clear()
    global carry_on
    
    
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
    a = 0
    global carry_on #Not actually needed as we're not assigning, but clearer
    while (a < num_of_iterations) & (carry_on) :
        yield a			# Returns control and waits next call.
        a = a + 1
        

#animation = matplotlib.animation.FuncAnimation(fig, update, interval=1, 
#                                repeat=False, frames=num_of_iterations)
def run():
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



"""
#plotting a graph
matplotlib.pyplot.ylim(0, 99)
matplotlib.pyplot.xlim(0, 99)
for i in range(num_of_agents):
    matplotlib.pyplot.scatter(agents[i].x,agents[i].y)
"""
"""
#Assigning easterly and westerly points different colours
#find the east most point and assign to [a]
east=max(agents, key=operator.itemgetter(1))
#find the west most point and assign to [b]
west=min(agents, key=operator.itemgetter(1))
#pull the x and y co-ordinates from the listed [a] to colour the most easterly pink
matplotlib.pyplot.scatter(east[1],east[0],color='deeppink')
#pull the x and y co-ordinates from the listed [b] to colour the most westerly cyan
matplotlib.pyplot.scatter(west[1],west[0],color='cyan')
"""
"""
matplotlib.pyplot.imshow(environment)
matplotlib.pyplot.show()
"""

#print(agent.store)


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