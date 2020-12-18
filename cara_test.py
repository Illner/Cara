import formula.cnf as cnf

path = r"D:\Storage\OneDrive\Škola\Vysoká škola\UK\Rozhodovací procedury a verifikace (NAIL094)\Cvičení\Úkoly\task1\example.cnf"

c = cnf.Cnf(path)
print(c)

# for i in range(c.number_of_clauses):
#     print(c.get_clause(i))

