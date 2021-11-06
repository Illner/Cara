# Import
import io
import sys

# Variables
a = 0
o = 0
l = 0
size = 0

ratio_dict = {}
rh_name = None
rh_io_string = None
mapping = {0: 0}

circuit_path = sys.argv[1]
fold_path = sys.argv[2]
file_name = sys.argv[3]

with open(circuit_path, "r") as file:
    for i, line in enumerate(file.readlines()):
        temp = line.split(" ")

        if line.startswith("C") or line.startswith("nnf"):
            continue

        if line.startswith("p cnf"):
            number_of_variables = int(temp[2])
            number_of_clauses = int(temp[3])

            ratio = number_of_clauses / number_of_variables
            ratio_dict[i] = ratio

            rh_io_string.writelines(line)
            continue

        if not line.startswith("A") and not line.startswith("O") and not line.startswith("L") and not line.startswith("R"):
            line_temp = ""

            for v in temp:
                vv = int(v)

                m = mapping[abs(vv)]
                m = m if vv >= 0 else -m

                if line_temp == "":
                    line_temp = f"{m}"
                else:
                    line_temp = f"{line_temp} {m}"

            rh_io_string.writelines(f"{line_temp}\n")
            continue

        if rh_io_string is not None:
            with open(fr"{fold_path}\{file_name}.{rh_name}.cnf", "w") as file:
                file.write(rh_io_string.getvalue())

            rh_io_string = None
            rh_name = None
            mapping = {0: 0}

        if line.startswith("A"):
            a += 1
            if len(temp) >= 3:
                size += int(temp[1])

        elif line.startswith("O"):
            o += 1
            if len(temp) >= 4:
                size += int(temp[2])

        elif line.startswith("L"):
            l += 1

        elif line.startswith("R"):
            rh_name = str(i + 1)
            rh_io_string = io.StringIO()

            nv = int(temp[2])

            for j in range(1, nv + 1):
                mapping[j] = int(temp[2 + j])

print(f"Size: {size}")
print(f"A: {a}, O: {o}, L: {l}")

# print(sorted(ratio_dict, key=ratio_dict.get))
