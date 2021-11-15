import pulp as pl
import other.environment as e
solver_list = pl.listSolvers(onlyAvailable=True)
print(solver_list)

print(e.is_64bit())
