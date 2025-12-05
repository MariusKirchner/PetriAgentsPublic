# PetriAgents
Combination of Agent-based modeling with Petri net simulations 

Final product will be a program with a GUI interface for creation of Agent based simulations with multiple types of agents that each have their own behaviours and corresponding Petri nets. Finished simulation includes custom flow of molecules in the environment, inflow of these into the bacteria and behaviour depending on the Petri nets of each agent. 

## Requirements
- PetriAgents works with NetLogo 6.3 [1]
- PetriAgents requires JDK 1.8 
- PetriAgents requires NL4PY [2] to be installed with your Python distribution
- PetriAgents requires python-libsbml [3] to be installed with your Python distribution
- PetriAgents requires statsmodels [5] to be installed with your Python distribution

## Installation
Clone the GitHub repository. 

Run main.py in a Python environment that has the requirements mentioned before installed.

On first startup the program asks for the location of your NetLogo installation. This parameter will be saved in config.xml. If you ever want to change the NetLogo version, you can delete that config.xml and select the new folder on restart or directly change the config.xml.

## Theoretical considerations
A paper is currently in preparation for submission and will be linked in upon publication.

## Usage
Run main.py in a Python environment that has the requirements mentioned before installed.

To be written. For now check the example Petri nets (.sbml files) for reference and load your own .sbml files in. To create the .sbml files we recommend using [MonaLisa](https://github.com/MolBIFFM/MonaLisa) [4]. Behavioural places and environmental places have to be called Beh_PlaceName and Env_PlaceName. The environment places are representing molecules that are also available in the medium. The behavioural places are representing agents behaviour. Currently Move, Repl (Replication), Death and Tumble are implemented.

For data plotting, use FullPlot.py.
You might have to change some parameters in FullPlot.py to fit your simulation parameters (such as NumberOfBacs, maximum and minimum coordinates and which plots you want to create.)


## Work in Progress

### Known Issues
- Multiple species have the same color per default, should rotate through colors.
- The GUI is currently very prone to errors, if you do not use it how it was intended to use. This will be improved upon in further iterations. If there are problems, feel free to message us and we will help as fast as we can.

### Features to be implemented
- Compartment-Agents mode: Makes simulations possible in which an agent is a compartment and therefore restricts molecules and potentially other agents from crossing its space.
- Change variables: Allow for dynamic or static changes in the agents variables (for example movement speed or speed of replication etc.).
- Change connected behaviours: Currently behavioural places are detected by name from .sbml only, this will be freely changeable in the PetriAgents interface.
- Permeability compartments: Currently compartments strictly block molecules from crossing its border. This should be connected to a certain probability to represent permeability. Potentially implement a concentration gradient check here.
- Start-conditions: Currently environment molecules are receiving an area and a random number between 0 and x on each of the patches in that area. This should be defineable more precisely.

### Runtime optimization
- Do as much as possible in NL, as API can be slow, only Petri net calculation and interface in Python => in each tick there should be one API Call per agent, reducable to one call for all agents (faster that way).
- Modularize the NetLogo Project creation

## Release History
- 2022-2025               Various pre-Release versions
- 5th of December 2025    Version 1.0.0 Release

## Authors
This work was written by Marius Kirchner during his PhD student time at the group of Prof. Dr. Ina Koch.
Authors with significant impact on this work were Marius Kirchner, Marcus Keßler, Jörg Ackermann, Christoph Welsch, Ivan Dikic and Ina Koch.

## Funding
The work was funded by the Hessian Ministry of Higher Education, Research and the Arts (HMWK) for the LOEWE Research Cluster ACLF-I (Marius Kirchner, Marcus Keßler, Christoph Welsch, Ivan Dikic and Ina Koch) (Project P6, P12, P13, P14, Z2 and Z3) and the EnABLE Cluster (to Marius Kirchner, Christoph Welsch, Ivan Dikic and Ina Koch).

## References

[1] Wilensky, U. (1999). NetLogo. http://ccl.northwestern.edu/netlogo/. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL.

[2] Gunaratne, C., & Garibay, I. (2021). NL4Py: Agent-based modeling in Python with parallelizable NetLogo workspaces. SoftwareX, 16, 100801.

[3] Benjamin J. Bornstein, Sarah M. Keating, Akira Jouraku, and Michael Hucka (2008) LibSBML: An API Library for SBML. Bioinformatics, 24(6):880–881, doi:10.1093/bioinformatics/btn051.

[4] Jens Einloft, Jörg Ackermann, Joachim Nöthen, Ina Koch, MonaLisa—visualization and analysis of functional modules in biochemical networks, Bioinformatics, Volume 29, Issue 11, June 2013, Pages 1469–1470, https://doi.org/10.1093/bioinformatics/btt165.

[5] https://github.com/statsmodels/statsmodels
