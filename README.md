# CaraCompiler
**(c)d-DNNF compiler**

**Backdoor Decomposable Monotone Circuits (BDMC) compiler**

<a href="https://dspace.cuni.cz/handle/20.500.11956/147674" target="_blank"> Diploma thesis (in Czech) </a>

## Language
Python 3.8+ (64 bit)

## Packages
* <a href="https://pypi.org/project/sortedcontainers/" target="_blank">sortedcontainers</a> 2.3.0 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/hypernetx/" target="_blank">hypernetx</a> 0.3.7 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/networkx/" target="_blank">networkx</a> 2.6.2 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/matplotlib/" target="_blank">matplotlib</a> 3.3.4 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/numpy/" target="_blank">numpy</a> 1.21.4 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/kahypar/" target="_blank">kahypar</a> 1.1.6 (Linux / macOS)
* <a href="https://pypi.org/project/kthread/" target="_blank">kthread</a> 0.2.2 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/PuLP/" target="_blank">PuLP</a> 2.5.1 (Windows / Linux / macOS)


* <a href="https://pypi.org/project/python-sat/" target="_blank">python-sat</a> 0.1.6.dev11 (Windows / Linux / macOS)
* <a href="https://github.com/Illner/pysat/" target="_blank">extended python-sat</a> 0.1.6.dev11 (Windows / Linux / macOS) (support VSIDS and VSADS decision heuristic)

You can install all required packages to central user packages repository using **pip install --user sortedcontainers==2.3.0 hypernetx==0.3.7 networkx==2.6.2 matplotlib==3.3.4 numpy==1.21.4 kthread==0.2.2** python-sat==0.1.6.dev11 kahypar==1.1.6 PuLP==2.5.1

## Software
* <a href="http://glaros.dtc.umn.edu/gkhome/metis/hmetis/overview" target="_blank">hMETIS</a> 1.5.3 (Windows / Linux)
* <a href="https://www.cc.gatech.edu/~umit/software.html" target="_blank">PaToH</a> 3.3 (Linux / macOS)
* <a href="https://gitlab.mff.cuni.cz/kucep6am/pccompile" target="_blank">PCCompile</a> (Linux)

## Cara
### Example
*cara.py -s -bc TWO_CNF -bc RENAMABLE_HORN_CNF input_file output_file*

## D4
### Example
*d4.py -s input_file output_file*

## Cara - query
### Example
**Consistency** - *cara_query.py -co -a 1 -2 3 circuit_file*

**Validity** - *cara_query.py -va -a 1 -2 3 circuit_file*

**Clausal entailment** - *cara_query.py -ce -cl 1 -2 3 circuit_file*

**Model counting** - *cara_query.py -ct -a 1 -2 3 circuit_file*

**Minimum cardinality** - *cara_query.py -mc -o 1 -2 3 -d 4 5 circuit_file*

## Modules
![alt text](images/modules.png)
