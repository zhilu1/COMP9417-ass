# COMP9417-ass

## Setup
modules used in saved to requirements.txt
After activate virtualenv, run 
```
pip install -r requirements.txt
```

Run
```
python TrafficSimulator.py
```
to execute the project
A window running the traffic simulator will be shown
## Important Modules

#### numpy, pandas
Generating useful data structures and processing data.

#### matplotlib, plotting
ploting results

#### tkinter
draw the intersection and simulate traffic on canvas

## File Structure

#### TrafficSimulator.py
File containing main function and traffic simulating
It does the drawing  and call functions in helper files
 to perform the learning in traffic simulator

#### Car.py, Light.py
Files containing car class and light class in order to do operations like creation,
switching lights, moving cars conveniently

#### Qlearning.py, FixedSwitch.py
Files containing algorithms

#### GlobalVars.py
File containing global variables and constants that are used in other files.
