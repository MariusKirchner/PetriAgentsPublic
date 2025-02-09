breed [flagella flagellum] 
 
 
patches-own [ 
	 compartmentID 
	 ] 

directed-link-breed [connectors connector] 
 
globals [
	 local-color 
	 flagella-size 
	 local-time 
	 timeinterval-per-tick 
	 bacteria-velocity 
	 flowspeed 
	 newIndividuals 
	 deadIndividuals 
	 ] 
 
to setup 
	 clear-globals 
	 clear-ticks 
	 clear-turtles 
	 clear-patches 
	 clear-drawing 
	 clear-output 
	 reset-ticks 
	 set timeinterval-per-tick 1 
	 set bacteria-velocity 0.3 
	 set flowspeed 0.1 
	 set newIndividuals [] 
	 set deadIndividuals [] 
	 set-default-shape flagella "flagella" 
	 set flagella-size 1 
	 updateView 
end 

to setCompartment [x y newCompartmentID] 
	 ask patch x y [ 
	 	 set compartmentID newCompartmentID 
	 ] 
end 
to setCompartmentAll [listOfCommands] 
	 foreach listOfCommands [ 
	 	 [content] -> 
	 	 setCompartment (item 0 content) (item 1 content) (item 2 content) 
	 ] 
end 
to make-flagella 
	 let flagella-shape (word "flagella" 1) 
	 hatch 1 [ 
	 	 set breed flagella 
	 	 set color blue 
	 	 set label "" 
	 	 set shape "flagella-4" 
	 	 bk 0.5 
	 	 set size 1 
	 	 create-connector-from myself [ 
	 	 	 set hidden? true 
	 	 	 tie 
	 	 ] 
	 ] 
end 
 
to go 
	 ask flagella with [not any? my-links][die] 
	 patchdiffusion 
	 tick 
	 set local-time ticks * timeinterval-per-tick 
	 updateView 
end 

to patchdiffusion 
	 let tempList [] 
	 ask patches [ 
	 ] 
end 
to updateView 
	 ask patches [ 
