# PetriAgents
Combination of Agent-based modeling with Petri net simulations 

Final product will be an easy to use GUI interface for creation of Agent based simulations with multiple types of agents that each have their own behaviours and corresponding Petri nets. Finished simulation includes custom flow of molecules in the environment, inflow of these into the bacteria depending on the concentration and behaviour depending on the Petri nets of each agent. 

## Requirements
- PetriAgents works with NetLogo 6.3 [1]
- PetriAgents requires JDK 1.8 
- PetriAgents requires NL4PY [2] to be installed with your Python distribution
- PetriAgents requires python-libsbml [3] to be installed with your Python distribution
- PetriAgents requires statsmodels [5] to be installed with your Python distribution

## Installation
Clone the github repository. 

In Backend/NetLogoConnection/NetLogoExecution.py in Line 23 or 27 (depending on if you are on Windows or MacOS/Linux) change the path to your local NetLogo installation.

## Theoretical considerations
To be written.

## Usage
Run main.py in a Python environment that has the requirements mentioned before installed.

To be written. For now check the example Petri nets (.sbml files) for reference and load your own .sbml files in. To create the .sbml files we recommend using [MonaLisa](https://github.com/MolBIFFM/MonaLisa) [4]. Behavioural places and environmental places have to be called Beh_PlaceName and Env_PlaceName. The environment places are representing molecules that are also available in the medium. The behavioural places are representing agents behaviour. Currently Move, Repl (Replication), Death and Size are implemented.



## Work in Progress

### Known Issues
- Edge detection is not optimal for agents.
- Save/Load Project is currently not fully functional.
- Flow settings are currently not changing the actual flow of molecules.
- Flow and diffusion are not effecting the agents, maybe this will become a setting for the flow at least.
- Multiple species have the same color per default, should rotate through colors.
- Molecules can be moved multiple times in each step, as patches are checked one by one. Take a snapshot of current state and then apply diffusion.
- Agents have flagella per-default and their behaviour is sometimes wrong, maybe we will just delete them.
- The GUI is currently very prone to errors, if you do not use it how it was intended to use. This will be improved upon in further iterations. If there are problems, feel free to message us and we will help as fast as we can.

### Features to be implemented
- Allow user to easily set their NetLogo installation through the GUI and save that setting.
- Compartment-Agents mode: Makes simulations possible in which an agent is a compartment and therefore restricts molecules and potentially other agents from crossing its space.
- Inflow/Outflow: Implement possibility to define timepoints and inflow/outflow amounts of Environment-Molecules to simulate inflow/outflow of the system.
- Data extraction: Make extraction of molecule and agent composition at certain time intervals possible (directly to .csv). Potentially also extract agents position and variables at certain time.
- Change variables: Allow for dynamic or static changes in the agents variables (for example movement speed or speed of replication etc.).
- Change connected behaviours: Currently behavioural places are detected by name from .sbml only, this will be freely changeable in the PetriAgents interface.
- Permeability compartments: Currently compartments strictly block molecules from crossing its border. This should be connected to a certain probability to represent permeability. Potentially implement a concentration gradient check here.
- Start-conditions: Currently environment molecules are receiving an area and a random number between 0 and x on each of the patches in that area. This should be defineable more precisely.


### Runtime optimization
- Do as much as possible in NL, as API can be slow, only Petri net calculation and interface in Python => in each tick there should be one API Call per agent, reducable to one call for all agents (faster that way).
- Modularize the NetLogo Project creation

## References

[1] Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

[2] Gunaratne, C., & Garibay, I. (2021). NL4Py: Agent-based modeling in Python with parallelizable NetLogo workspaces. SoftwareX, 16, 100801.

[3] Benjamin J. Bornstein, Sarah M. Keating, Akira Jouraku, and Michael Hucka (2008) LibSBML: An API Library for SBML. Bioinformatics, 24(6):880–881, doi:10.1093/bioinformatics/btn051.

[4] Jens Einloft, Jörg Ackermann, Joachim Nöthen, Ina Koch, MonaLisa—visualization and analysis of functional modules in biochemical networks, Bioinformatics, Volume 29, Issue 11, June 2013, Pages 1469–1470, https://doi.org/10.1093/bioinformatics/btt165.

[5] https://github.com/statsmodels/statsmodels
