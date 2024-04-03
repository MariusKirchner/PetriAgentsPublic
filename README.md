# PetriAgents
Combination of Agent Based Modeling with Petri net simulations 

Final Product will be an easy to use GUI interface for creation of AgentBased Simulations with multiple types of Agents that each have their own behaviours and corresponding Petri Nets. Finished simulation includes custom flow of molecules in the environment, inflow of these into the bacteria depending on the concentration (idk yet) and behaviour depending on the PetriNets of each Agent. 

Goal => do as much as possible in NL, as API can be slow, only petri net calculation and Interface in python => in each tick there should be one API Call per Agent, reducable to one call for all agents (faster that way)


TODO (Step by Step):
Cleanup the lists of things, they are NOT needed, only use dictionaries!

X Add bacteria into TKintertable

X Add Possibility to save Project into own file

X Add Possibility to load Project from own file

X Add possibility to delete bacteria species from TKintertable

Add possibility to see through behaviourPlaces from each Bacteria

Add possibility to edit these behaviours for each behaviourPlace

X Add table for environment Places, automatically add all Env_ Places from each Bacteria

Add possiblity to manually add or delete Environment Places from that list

Add possiblity to manually add concentrations of these environment places at certain time points and certain places

Add possiblity to change the flow at time points 

X Add NetLogoFile Creation (HUGE)

Add "AttributePlaces" to make them different from "Behaviours" for easier handling - (like size) - or change them to their behaviours (like "grow" -> size + 1)

Add possibility to add plots for anything needed into GUI

add graphic options for cells (colors, shapes etc.)

Add possibility into PetriNets (for demos) for molecules to change behaviour instead of fully inhibit it (like slow them down etc.)

Potentially make the bacteria species distinct by their shape while having their color change according to some attribute (let the user choose which attribute with which colors?)

Update the project save and load process for new data in the simulation

INCLUDE ALL SETTINGS! (HUGE HUGE)

X Add StartThisNetLogoSimulation 
(Combine with project save!)

Add possibility to add compartments, change the backend! Also change save and load!

Change ID system in the backend, maybe make individual ID's per object and get them from a big dict?

Runtime ideas:
Change the commands that are done in a loop into one large command (as API takes the longest time)

LongTermBugFixingTodo:
x prevent adding the same bacterianame

X prevent deleting nonexistent bacterianame

prevent illegal inputs for other entries

fix bug that prevents restarting a simulation from the same python program

X fix bug that happens when having a petri net with a token in it, some type of dict key error

X check if MOI change is really working? Same thing for Color, seems to not be written into the corresponding bacteria variable

fix continuities and implement non continuity for flow and cells!