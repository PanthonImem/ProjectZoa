# Project Zoa

Project Zoa is a python-based ecosystem(Biology) simulation.

The GUI is based on Tkinter library. 

The goal is 1) to simulate and visualize highschool biology concepts such as natural selection, evolution, and population curve.
            2) to develop a somewhat intelligent Zoa AI, adjusting the parameter by genetic algorithm
            
## Running
Simply run the file EcoSystem.py
            
## Concepts: 
There are two type of objects in this ecosystem. 

1. Food:

A Food is represented with a green dot.

There are two means of default reproduction for Food.
1.1) normal reproduction : A Food has a chance to spawn another Food near the parent food
1.2) random addition : when the total quantity of Food is low, 15 Food will randomly be added to the system to keep the Zoa alive.

2. Zoa

A Zoa is represented with a red dot.

A Zoa has these characteristics, which can be passed to its offspring
- Velocity: how fast a zoa moves. Zoa with greater velocity loses more health when moving.
- Health: the 'fitness' function. A Zoa DIE if its health goes below zero.
- Max Health: the cap of health.
- Sight: The radius of the Zoa's observable environment. A zoa will only consider Food within its sight. 
- Size: The size of a zoa.
- Foodmode: See Zoa Food Search for more details.

Zoa Food Search: A zoa has two built-in modes. 
1)'Minimum Searching': A zoa moves toward the closest food in its sight
2)'Vector Alignment Searching': A zoa adds up all the possible vectors toward Foods in its sight, weighing closer Food more.
Then the Zoa ranks n of its closest food based on the distance and the cosine similarity between the aggregate vector and the 
vector towards each food. This is intended to serve as 
Note: A momentum factor has also been added to prevent the zoa from  being indecisive in the middle of a few Foods.
(Once it moves toward one food, the aggregate vector switches direction and so the Zoa oscillate)

Hibernation: When a Zoa can't find food in its sight, it picks a random direction and move there. 
Moving while in hibernation costs less health. 

Reproduction and Mutation: Any non-hibernated Zoa has a percentage chance to reproduce another Zoa with its genetic + a little random mutation. 

## Visualization

Simply run the Jupyter Notebook. Make sure you have the dataset.csv file generated.

