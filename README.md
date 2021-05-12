# Cara
**Backdoor Decomposable Monotone Circuits (BDMC) compiler**

## Language
Python 3.6+ (64 bit)

## Packages
* <a href="https://pypi.org/project/sortedcontainers/" target="_blank">sortedcontainers</a> 2.3.0 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/hypernetx/" target="_blank">hypernetx</a> 0.3.7 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/matplotlib/" target="_blank">matplotlib</a> 3.3.4 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/numpy/" target="_blank">numpy</a> 1.20.2 (Windows / Linux / macOS)
* <a href="https://pypi.org/project/kahypar/" target="_blank">kahypar</a> 1.1.6 (Linux / macOS)


* <a href="https://pypi.org/project/python-sat/" target="_blank">python-sat</a> 0.1.6.dev11 (Windows / Linux / macOS)
* <a href="https://github.com/Illner/pysat/" target="_blank">extended python-sat</a> 0.1.6.dev11 (Windows / Linux / macOS) (support VSIDS and VSADS decision heuristic)

You can install all required packages to central user packages repository using **pip install --user sortedcontainers==2.3.0 python-sat==0.1.6.dev11 hypernetx==0.3.7 matplotlib==3.3.4 numpy==1.20.2** kahypar==1.1.6

## Software
* <a href="http://glaros.dtc.umn.edu/gkhome/metis/hmetis/overview" target="_blank">hMETIS</a> 1.5.3 (Windows / Linux)
* <a href="https://www.cc.gatech.edu/~umit/software.html" target="_blank">PaToH</a> 3.3 (Linux / macOS)

## Cara
### Example
*cara.py -s -bc TWO_CNF -bc RENAMABLE_HORN_CNF input_file output_file*

### Arguments
positional arguments:
* **input_file**
  + path of the input file, which is in the DIMACS CNF format
* **output_file**
  + path of the output file, where the circuit will be saved in the DIMACS NNF format

optional arguments:
+ **-h, --help**
  + show this help message and exit
+ **-s, --smooth**
  + smooth the circuit (default: False)
+ **-p, --preprocessing**
  + find all backbone literals before the compilation (default: False)
+ **-uos, --use_one_solver**
  + use only one SAT solver for all components (default: False)
+ **-cc_abcp, --cc_after_bcp**
  + use component caching after BCP (default: False)
* **-bc {TWO_CNF,RENAMABLE_HORN_CNF}, --base_class {TWO_CNF,RENAMABLE_HORN_CNF}**
  + types of base classes in the circuit's leaves (literal leaves are mandatory) (default: None)
* **-dh {RANDOM,JEROSLOW_WANG_ONE_SIDED,JEROSLOW_WANG_TWO_SIDED,CLAUSE_REDUCTION,WEIGHTED_BINARIES,BACKBONE_SEARCH,DLCS,DLIS,DLCS_DLIS,EUPC}, --decision_heuristic {RANDOM,JEROSLOW_WANG_ONE_SIDED,JEROSLOW_WANG_TWO_SIDED,CLAUSE_REDUCTION,WEIGHTED_BINARIES,BACKBONE_SEARCH,DLCS,DLIS,DLCS_DLIS,EUPC}**
  + type of decision heuristic (default: CLAUSE_REDUCTION)
* **-dh_mdh {OK_SOLVER,POSIT_SATZ}, --dh_mixed_difference_heuristic {OK_SOLVER,POSIT_SATZ}**
  + type of mixed difference heuristic for the decision heuristic (clause reduction heuristic, exact unit propagation count heuristic) (default: OK_SOLVER)
* **-hpuf [0.01-0.49], --hp_ub_factor [0.01-0.49]**
  + balance factor that is used for hypergraph partitioning (hMETIS - UB factor, KaHyPar - epsilon) (default: 0.1)
* **-st [non-negative number or None], --subsumption_threshold [non-negative number or None]**
  + threshold (number of clauses) for applying subsumption (None for no limit) (default: 500)
* **-ncst [0.00-1.00], --new_cut_set_threshold [0.00-1.00]**
  + threshold for computing a new cut set (if the number of implied literals is at least x% of the component's number of variables) (default: 0.1)
* **-ss {MiniSAT,Glucose,Lingeling,CaDiCal}, --sat_solver {MiniSAT,Glucose,Lingeling,CaDiCal}**
  + type of SAT solver that will be used for compiling the circuit (default: MiniSAT)
* **-il {BCP,IMPLICIT_BCP,IMPLICIT_BCP_ITERATION,BACKBONE,NONE}, --implied_literals {BCP,IMPLICIT_BCP,IMPLICIT_BCP_ITERATION,BACKBONE,NONE}**
  + type of method that will be used for deriving implied literals at every decision node (default: BCP)
* **-il_ph {NONE,PROP_Z,CRA}, --il_preselection_heuristic {NONE,PROP_Z,CRA}**
  + type of preselection heuristic for implied literals (relevant only for IMPLICIT_BCP and IMPLICIT_BCP_ITERATION) (default: CRA)
* **-il_ph_cra_r [0.01-1.00], --il_ph_cra_rank [0.01-1.00]**
  + how many variables should be preselected (clause reduction approximation - rank) (default: 0.1)
* **-il_ph_prop_z_novlb [non-negative number or None], --il_ph_prop_z_number_of_variables_lower_bound [non-negative number or None]**
  + how many variables should be preselected (prop_z - lower bound) (None for no limit) (default: 10)
* **-il_ph_prop_z_dt [non-negative number], --il_ph_prop_z_depth_threshold [non-negative number]**
  + depth threshold (prop_z) (default: 5)
* **-fil {IMPLICIT_BCP,IMPLICIT_BCP_ITERATION,BACKBONE}, --first_implied_literals {IMPLICIT_BCP,IMPLICIT_BCP_ITERATION,BACKBONE}**
  + type of method that will be used for deriving implied literals after component decomposition (default: IMPLICIT_BCP)
* **-cc {NONE,STANDARD_CACHING_SCHEME,HYBRID_CACHING_SCHEME,BASIC_CACHING_SCHEME}, --component_caching {NONE,STANDARD_CACHING_SCHEME,HYBRID_CACHING_SCHEME,BASIC_CACHING_SCHEME}**
  + type of component caching that will be used for compiling the circuit (default: BASIC_CACHING_SCHEME)
* **-erc {NONE,SUBSUMPTION,UP_REDUNDANCY}, --eliminating_redundant_clauses {NONE,SUBSUMPTION,UP_REDUNDANCY}**
  + procedure that will be applied for determining redundant clauses (default: UP_REDUNDANCY)
* **-erc_t [non-negative number or None], --erc_threshold [non-negative number or None]**
  + threshold (number of clauses) for applying a procedure that eliminates redundant clauses (None for no limit) (default: 500)
* **-hps {HMETIS,PATOH,KAHYPAR,NONE}, --hp_software {HMETIS,PATOH,KAHYPAR,NONE}**
  + software used for hypergraph partitioning (default: PATOH (Linux / macOS), HMETIS (Windows))
* **-hpc {NONE,ISOMORFISM,ISOMORFISM_VARIANCE}, --hp_caching {NONE,ISOMORFISM,ISOMORFISM_VARIANCE}**
  + type of hypergraph partitioning caching (default: ISOMORFISM)
* **-hplnc [non-negative number or None], --hp_limit_number_of_clauses [non-negative number or None]**
  + threshold (number of clauses) for applying hypergraph partitioning caching (None for no limit) (default: 1000)
* **-hplnv [non-negative number or None], --hp_limit_number_of_variables [non-negative number or None]**
  + threshold (number of variables) for applying hypergraph partitioning caching (None for no limit) (default: 1000)
* **-cstc, --cut_set_try_cache**
  + compute a new cut set at every decision node that satisfies the limits for hypergraph partitioning caching (number of clauses/variables) (default: False)
+ **-hpvs {NONE,EQUIV_SIMPL}, --hp_variable_simplification {NONE,EQUIV_SIMPL}**
  + type of hypergraph partitioning variable simplification (default: EQUIV_SIMPL)
* **-ncstr [0.00-1.00], --new_cut_set_threshold_reduction [0.00-1.00]**
  + if the limits for hypergraph partitioning caching (number of clauses/variables) are satisfied, then the new_cut_set_threshold will be multiplied by x (default: 1)
* **-v, --version**
  + show program's version number and exit

## Cara - query
### Example
**Consistency** - *cara_query.py -co -a 1 -2 3 circuit_file*

**Validity** - *cara_query.py -va -a 1 -2 3 circuit_file*

**Clausal entailment** - *cara_query.py -ce -cl 1 -2 3 circuit_file*

**Model counting** - *cara_query.py -ct -a 1 -2 3 circuit_file*

**Minimum cardinality** - *cara_query.py -mc -o 1 -2 3 -d 4 5 circuit_file*

### Arguments
positional arguments:
* **circuit_file**
  + path of the circuit file, which is in the DIMACS NNF format
 
optional arguments:
+ **-h, --help**
  + show this help message and exit
+ **-co, --consistency**
  + consistency check (CO) (default: False)
+ **-va, --validity**
  + validity check (VA) (default: False)
+ **-ce, --clausal_entailment**
  + clausal entailment check (CE) (default: False)
+ **-ct, --model_counting**
  + model counting (CT) (default: False)
+ **-mc, --minimum_cardinality**
  + minimum cardinality (MC) (default: False)
+ **-a, --assumption [lit_1, lit_2, ...]**
  + assumption set (CO, VA, CT) (default: [])
+ **-cl, --clause [lit_1, lit_2, ...]**
  + clause (CE) (default: [])
+ **-o, --observation [lit_1, lit_2, ...]**
  + observation set (MC) (default: [])
+ **-d, --default [var_1, var_2, ...]**
  + default set (MC) (default: [])

## Modules
![alt text](images/modules.png)
