# CMake generated Testfile for 
# Source directory: /scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile
# Build directory: /scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(NFLiteralSet "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_nfliteralset")
set_tests_properties(NFLiteralSet PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;100;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(NormalForm "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_normalform")
set_tests_properties(NormalForm PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;101;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(Horn "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_horn")
set_tests_properties(Horn PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;102;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(Schoning "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_schoning")
set_tests_properties(Schoning PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;103;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(Assign "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_assign")
set_tests_properties(Assign PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;104;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(UnitProp "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_unitprop")
set_tests_properties(UnitProp PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;105;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(Resolution "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/build/test/test_resolve")
set_tests_properties(Resolution PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;106;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
add_test(CNFCompress "test_cnfcompress.h")
set_tests_properties(CNFCompress PROPERTIES  _BACKTRACE_TRIPLES "/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;107;add_test;/scratch/illner/job_9760050.meta-pbs.metacentrum.cz/pccompile/CMakeLists.txt;0;")
subdirs("lib")
subdirs("test")
subdirs("bin")
