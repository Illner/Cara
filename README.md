# Cara
**Backdoor Decomposable Monotone Circuits (BDMC) compiler**

## Language and packages
Python 3.9.1

## Arguments
Cara [-h] [-ct {D_BDMC,SD_BDMC}] [-ss {MiniSAT,Glucose,Lingeling,CaDiCal}] [-cc {C2D,NONE}] [-il {BCP,IMPLICIT_BCP,BACKBONE,NONE}] [-dd | -sd] [-v] input_file output_file

positional arguments:
* **input_file**
  + The path of the input file which is in the DIMACS CNF format.
* **output_file**
  + The path of the output file where the circuit will be saved.

optional arguments:
+ **-h, --help**
  + show this help message and exit
+ **-ct {D_BDMC,SD_BDMC}, --circuit_type {D_BDMC,SD_BDMC}**
  + The circuit type into which the input formula will be compiled. (default: D_BDMC)
* **-ss {MiniSAT,Glucose,Lingeling,CaDiCal}, --sat_solver {MiniSAT,Glucose,Lingeling,CaDiCal}**
  + The SAT solver which will be used for compiling the circuit. (default: MiniSAT)
* **-cc {C2D,NONE}, --component_caching {C2D,NONE}**
  + Which component caching will be used for compiling the circuit. (default: C2D)
* **-il {BCP,IMPLICIT_BCP,BACKBONE,NONE}, --implied_literals {BCP,IMPLICIT_BCP,BACKBONE,NONE}**
  + Which method will be used for deriving implied literals at every decision node. (default: BCP)
* **-dd, --dynamic_decomposition**
  + A dynamic decomposition approach will be used for compiling. (default: True)
* **-sd, --static_decomposition**
  + A static decomposition approach will be used for compiling. (default: False)
* **-v, --version**
  + show program's version number and exit

## High-level overview
![alt text](images/high-level_overview.png)

## Modules
![alt text](images/modules.png)
