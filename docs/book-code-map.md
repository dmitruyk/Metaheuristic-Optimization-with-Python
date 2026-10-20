# Book code map

Source file: `Metaheuristic_Optimization_with_Python_Editorial_Edition.docx`.
Authors: Yuriy Romasevych, Viatcheslav Loveikin, and Dmytro Komarchuk.

Rendered-page estimates come from Word page-break markers. Word's document
property says 346 pages; the counter used here ends at 347. The implementation
brief's pages (p. 24, pp. 224–226, p. 231, pp. 289–298) do not match this file.
In this DOCX the ten-variable worked value 12.3901 is on rendered page 21,
Problem 1a is on rendered page 187, the cart-pole `penalty_terminal` line is
on rendered page 203, and Appendix B begins on rendered page 272.

Statuses: `verified` (executed and compared with a printed number, or parsed
and covered by `tests/`), `corrected-with-erratum` (behavior preserved except
for a documented change such as the random generator), `unverified` (present
in the manuscript, not numerically matched), `not-applicable` (prose,
explanation table, figure schematic, or Jupyter magic rather than a library function).

No row is blank. Result plots in Appendices A, C, and E stay `unverified`:
the full 100-run study was not repeated, and library figures are not substituted for the book's figures.

Review note, 2026-10-19: chapter-level status, tests, and notebooks are in
`docs/coverage-matrix.md`. Editor-facing before/after text is in
`docs/manuscript-replacements.md`. The reduced Generator study is not a reason
to change any Appendix C or Appendix E row from `unverified` to `verified`.

| ID | Rendered page | Kind | Status | Repo path | First line or caption |
| --- | --- | --- | --- | --- | --- |
| F001 | 10 | figure | unverified | not claimed to match a printed figure or table | Figure 1.1 — Graphical interpretation of the positions of particles on the surface of the objective function f(x)=x² |
| F002 | 10 | figure | unverified | not claimed to match a printed figure or table | Figure 1.2 — Graphical interpretation of the movement of a particle across the surface of the objective function f(x)=x² during the first four iterations |
| F003 | 11 | figure | unverified | not claimed to match a printed figure or table | Figure 1.3 — Graphical interpretation of the vector (pi-1 − xi-1) |
| F004 | 11 | figure | unverified | not claimed to match a printed figure or table | Figure 1.4 — Graphical interpretation of the vector (gi-1 − xi-1) |
| F005 | 11 | figure | unverified | not claimed to match a printed figure or table | Fig. 1.5 shows that the vector vi is obtained as the sum of three vectors, wvi-1, c1r1(pi-1 − xi-1), and c2r2(gi-1 − xi-1). It shows where the particle will move — it transitions f |
| F006 | 11 | figure | unverified | not claimed to match a printed figure or table | Figure 1.5 — Graphical interpretation of the rules for updating a particle’s position and velocity |
| C001 | 12 | table | unverified | not claimed to match a printed figure or table | Table 1.1 — Recommendations regarding swarm size K |
| T001 | 12 | table-3col | unverified | not claimed to match a printed figure or table | Authors |
| F007 | 13 | figure | unverified | not claimed to match a printed figure or table | Fig. 1.6 shows that at I=50 the PSO algorithm does not manage to converge. At I=100 the PSO algorithm only begins to converge. At I=200 the algorithm converged within approximately |
| F008 | 13 | figure | unverified | not claimed to match a printed figure or table | Figure 1.6 — Curves showing the reduction of the Griewank function using the PSO algorithm with swarm size K=25 for different values of the number of iterations I |
| F009 | 14 | figure | unverified | not claimed to match a printed figure or table | Figure 1.7 — Flowchart of the PSO algorithm |
| C002 | 15 | table | unverified | not claimed to match a printed figure or table | Table 1.2 ‒ Description of individual sections of the PSO function code in Python |
| T002 | 20 | explanation-table | not-applicable | no library object; explanation or non-Python content | Code |
| T003 | 21 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np def ObjectiveFunction(x): return float(np.sum(x**2) + np.sum(np.abs(x))) |
| T004 | 21 | code-listing | not-applicable | no library object; explanation or non-Python content | x = np.array([0.1, 0.2, 0.3, -0.2, 0.51, -0.2, 0, -0.2, -1.6, 2.0]) ObjectiveFunction(x) |
| T005 | 21 | table-1col | unverified | not claimed to match a printed figure or table | Dimension = 10 Vars = [f"x{i+1}" for i in range(Dimension)] DomainVarsList = [[-20, 20]] * 10 |
| T006 | 22 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as npfrom IPython.display import clear_output def PSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations): n = len(Vars) lb = np.array([d[ |
| T007 | 22 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 Iterations = 200 |
| T008 | 23 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = PSO(ObjectiveFunction, Vars, DomainVarsList, SwarmPopulation, Iterations) GBestCost, GBest, CostFunctionValues = OptimizationResult |
| T009 | 23 | code-listing | unverified | not claimed to match a printed figure or table | import matplotlib.pyplot as plt y = OptimizationResult[2] x = range(0, len(y)) plt.figure(figsize=(6, 4.5)) plt.semilogy(x, y, 'o', color='black', markersize=4) |
| F010 | 24 | figure | unverified | not claimed to match a printed figure or table | Figure 1.8 — Plot of the decrease of the objective function (1.13) using the PSO algorithm with swarm size K=25 (logarithmic scale) |
| T010 | 25 | table-1col | unverified | not claimed to match a printed figure or table | w, c1, c2 = 0.72, 1.19, 1.19 |
| T011 | 25 | table-1col | unverified | not claimed to match a printed figure or table | wMax, wMin, c1, c2 = 0.9, 0.4, 1.19, 1.19 |
| T012 | 25 | table-1col | unverified | not claimed to match a printed figure or table | w=(wMax-wMin)*(Iterations-step)/Iterations+wMin |
| F011 | 26 | figure | unverified | not claimed to match a printed figure or table | Figure 1.9 — Plot of the decrease of the objective function (1.13) using the LDW-PSO algorithm with swarm size K=25 (logarithmic scale) |
| F012 | 28 | figure | unverified | not claimed to match a printed figure or table | Figure 1.10 — Plot of the change in the quantities , wk, and  over the first ten iterations of the IA-PSO algorithm |
| T013 | 29 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def IAPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations): n = len(Vars) lb = np.array( |
| F013 | 30 | figure | unverified | not claimed to match a printed figure or table | Figure 1.11 — Plot of the decrease of the objective function (1.13) using the IA-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| F014 | 31 | figure | unverified | not claimed to match a printed figure or table | Figure 1.12 — Plots of the change in the quantities  and  when minimizing the objective function (1.13) using the BB-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| T014 | 32 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def BBPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations): n = len(Vars) lb = np.array( |
| F015 | 33 | figure | unverified | not claimed to match a printed figure or table | Figure 1.13 — Plot of the decrease of the objective function (1.13) using the BB-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| T015 | 34 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def VCTPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations, RC): n = len(Vars) lb = np.a |
| F016 | 34 | figure | unverified | not claimed to match a printed figure or table | Figure 1.14 — Plot of the decrease of the objective function (1.13) using the VCT-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| F017 | 35 | figure | unverified | not claimed to match a printed figure or table | Fig. 1.14 shows that the parameter RC has a direct effect on the result obtained. However, as with the LDW-PSO algorithm, this modification is not well suited to effectively minimi |
| F018 | 36 | figure | unverified | not claimed to match a printed figure or table | Figure 1.15 — Plot of the decrease of the objective function (1.13) using the ME-D-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| T016 | 36 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def BreakPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations, AcceptableRate, CostFuncVa |
| T017 | 36 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult =  MEDPSO(ObjectiveFunction, Vars, DomainVarsList, SwarmPopulation, Iterations, 0.01, [], []) GBestCost, GBest, CostFunctionValues = Optimiza |
| F019 | 38 | figure | unverified | not claimed to match a printed figure or table | Figure 1.16 — Ring topology of connections between particles |
| T018 | 39 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def RingPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations): n = len(Vars) lb = np.arra |
| F020 | 39 | figure | unverified | not claimed to match a printed figure or table | Fig. 1.17 shows that the Ring-PSO algorithm has slow convergence. This is a consequence of the fact that information about solutions to the problem spreads slowly through the swarm |
| F021 | 40 | figure | unverified | not claimed to match a printed figure or table | Figure 1.17 — Plot of the decrease of the objective function (1.13) using the Ring-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| F022 | 40 | figure | unverified | not claimed to match a printed figure or table | Figure 1.18 — vonNeumann-PSO topology of connections between particles with swarm size K =25 |
| T019 | 42 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def vonNeumannPSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations): n = len(Vars) lb = n |
| F023 | 43 | figure | unverified | not claimed to match a printed figure or table | Figure 1.19 — Plot of the decrease of the objective function (1.13) using the vonNeumann-PSO algorithm with swarm size K = 25 (logarithmic scale) |
| F024 | 43 | figure | unverified | not claimed to match a printed figure or table | Fig. 1.19 shows that the vonNeumann-PSO algorithm also has slow convergence. However, this modification, in many cases, shows a better result than the Ring-PSO algorithm. Applying  |
| T020 | 46 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np Vars = ['x1', 'x2', 'x3'] DomainVarsList = [(-20, 20), (-20, 20), (-20, 20)] def function(x): x1, x2, x3 = x return x1**2 + x2**2 + x3**2 Swa |
| T021 | 46 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | n = len(Vars) lb = np.array([d[0] for d in DomainVarsList]) ub = np.array([d[1] for d in DomainVarsList]) Position = lb + np.random.rand(SwarmPopulation, n) * ( |
| T022 | 47 | table-1col | unverified | not claimed to match a printed figure or table | print(Swarm) |
| T023 | 47 | table-1col | unverified | not claimed to match a printed figure or table | print(Swarm[0]) |
| T024 | 47 | table-1col | unverified | not claimed to match a printed figure or table | print(Swarm[3]) |
| T025 | 47 | table-1col | unverified | not claimed to match a printed figure or table | print(Swarm[-1]) |
| T026 | 48 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np x = np.array([2.2, -1.4, 0, -4.1]) v = np.array([-0.2, -0.1, 0.3, 3]) p = np.array([2.1, -1.7, 0.2, -3.8]) g = np.array([2, -1.5, -0.1, -4.1] |
| T027 | 48 | table-1col | unverified | not claimed to match a printed figure or table | vNew = w * v + c1 * r1 * (p - x) + c2 * r2 * (g - x) print(vNew) |
| T028 | 48 | table-1col | unverified | not claimed to match a printed figure or table | xNew = vNew + x print(xNew) |
| T029 | 49 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np Vars = ['x1', 'x2', 'x3'] DomainVarsList = [(-1, 1), (-1, 1), (-1, 1)] SwarmPopulation = 10 |
| T030 | 49 | code-listing | not-applicable | no library object; explanation or non-Python content | n = len(Vars) Position = np.random.uniform(-2, 2, size=(SwarmPopulation, n)) Velocity = np.random.uniform(-1, 1, size=(SwarmPopulation, n))Swarm = [] for k in r |
| T031 | 50 | table-1col | unverified | not claimed to match a printed figure or table | k = 0 print("Swarm[k] before boundary check:") print(Swarm[k]) for j in range(len(Vars)): if Swarm[k][0][j] < DomainVarsList[j][0]: Swarm[k][1][j] = 0 Swarm[k][ |
| T032 | 50 | table-1col | unverified | not claimed to match a printed figure or table | k = 1 print("Swarm[k] before boundary check:") print(Swarm[k]) for j in range(len(Vars)): if Swarm[k][0][j] < DomainVarsList[j][0]: Swarm[k][1][j] = 0 Swarm[k][ |
| T033 | 51 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np Vars = ['x1', 'x2', 'x3'] DomainVarsList = [(-2, 2), (-2, 2), (-2, 2)] def function(x): x1, x2, x3 = x return np.sin(x1**2) + np.sin(x2**2) + |
| T034 | 51 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | n = len(Vars) lb = np.array([d[0] for d in DomainVarsList]) ub = np.array([d[1] for d in DomainVarsList]) Position = lb + np.random.rand(SwarmPopulation, n) * ( |
| T035 | 51 | table-1col | unverified | not claimed to match a printed figure or table | GlobalBestCost = min(Swarm[k][4] for k in range(SwarmPopulation)) print("GlobalBestCost =", GlobalBestCost) |
| T036 | 51 | table-1col | unverified | not claimed to match a printed figure or table | PBestCost_all = [Swarm[k][4] for k in range(SwarmPopulation)] print(PBestCost_all) |
| T037 | 51 | table-1col | unverified | not claimed to match a printed figure or table | BestParticleNumber = PBestCost_all.index(GlobalBestCost) print(BestParticleNumber) |
| T038 | 51 | table-1col | unverified | not claimed to match a printed figure or table | print(Swarm[BestParticleNumber]) |
| T039 | 52 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np Dimension = 10 Vars = list(range(Dimension)) DomainVarsList = [(-500, 500)] * Dimension def ObjectiveFunction(x): return (np.sum(np.sqrt(np.a |
| T040 | 52 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 10 Iterations = 200 |
| T041 | 52 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = PSO(ObjectiveFunction, Vars, DomainVarsList, SwarmPopulation, Iterations) |
| F025 | 57 | figure | unverified | not claimed to match a printed figure or table | Figure 2.1 ‒ Graphical interpretation of the individual stages of constructing the donor vector v: a) computing the vector difference xr2-xr3; b) computing the weighted difference  |
| F026 | 57 | figure | unverified | not claimed to match a printed figure or table | Fig. 2.1, a shows that the vector difference xr2-xr3 is computed first (the operation in parentheses in expression (2.1)); the length of this difference is then changed by multiply |
| F027 | 57 | figure | unverified | not claimed to match a printed figure or table | Figure 2.2 ‒ Graphical interpretation of constructing the trial vector u |
| F028 | 58 | figure | unverified | not claimed to match a printed figure or table | Figure 2.3 ‒ Plots of the decrease of the Griewank function using the DE algorithm with population size K=25 for various numbers of iterations I |
| C003 | 59 | table | unverified | not claimed to match a printed figure or table | Table 2.1 shows the code of the DE algorithm together with an explanation of what each section of the code does. |
| F029 | 59 | figure | unverified | not claimed to match a printed figure or table | Figure 2.4 ‒ Flowchart of the DE algorithm |
| C004 | 60 | table | unverified | not claimed to match a printed figure or table | Table 2.1 ‒ Description of individual sections of the DE function's code in Python |
| T042 | 63 | explanation-table | not-applicable | no library object; explanation or non-Python content | Code |
| T043 | 65 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as npfrom IPython.display import clear_outputdef DE(function, Vars, DomainVarsList, Population, Iterations):    CostFunctionValues = []    CR, F =  |
| T044 | 65 | table-1col | unverified | not claimed to match a printed figure or table | Population = 25Iterations = 200 |
| T045 | 65 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = DE(ObjectiveFunction, Vars, DomainVarsList, Population, Iterations)GBestCost, GBest, CostFunctionValues = OptimizationResult |
| F030 | 65 | figure | unverified | not claimed to match a printed figure or table | Figure 2.5 ‒ Plot of the decrease of the objective function (1.13) using the DE algorithm with population size K=25 (on a logarithmic scale) |
| C005 | 66 | table | unverified | not claimed to match a printed figure or table | Table 2.2 lists several possible mutation schemes [3, 4]. In the notations of Table 2.2, the crossover operation is not indicated (by default, a binary operation is assumed, z=bin) |
| C006 | 66 | table | unverified | not claimed to match a printed figure or table | Table 2.2 ‒ Possible schemes for performing the mutation operation |
| T046 | 67 | table-2col | unverified | not claimed to match a printed figure or table | Algorithm notation |
| T047 | 68 | table-1col | unverified | not claimed to match a printed figure or table | i1 = BestDotNumber |
| T048 | 68 | code-listing | not-applicable | no library object; explanation or non-Python content | candidates = np.delete(AllIndexes, [k, i1]) i2, i3 = np.random.choice(candidates, 2, replace=False) |
| T049 | 68 | code-listing | not-applicable | no library object; explanation or non-Python content | candidates = np.delete(AllIndexes, k) i1, i2, i3 = np.random.choice(candidates, 3, replace=False) |
| T050 | 68 | code-listing | not-applicable | no library object; explanation or non-Python content | i1, i2, i3 = np.random.choice(candidates, 3, replace=False) |
| T051 | 69 | code-listing | not-applicable | no library object; explanation or non-Python content | i1, i2, i3 , i4, i5 = np.random.choice(candidates, 5, replace=False) |
| T052 | 69 | table-1col | unverified | not claimed to match a printed figure or table | DonorVector = Generation[i1] + F * (Generation[i2] - Generation[i3]) |
| T053 | 69 | table-1col | unverified | not claimed to match a printed figure or table | DonorVector = (Generation[i1] + F * (Generation[i2] - Generation[i3]) + F * (Generation[i4] - Generation[i5])) |
| T054 | 69 | code-listing | not-applicable | no library object; explanation or non-Python content | i2, i3 = np.random.choice(candidates, 2, replace=False) |
| T055 | 69 | code-listing | not-applicable | no library object; explanation or non-Python content | i2, i3, i4, i5 = np.random.choice(candidates, 4, replace=False) |
| T056 | 69 | table-1col | unverified | not claimed to match a printed figure or table | DonorVector = Generation[i1] + F * (Generation[i2] - Generation[i3]) |
| T057 | 69 | table-1col | unverified | not claimed to match a printed figure or table | DonorVector = (Generation[i1] + F * (Generation[i2] - Generation[i3]) + F * (Generation[i4] - Generation[i5])) |
| T058 | 70 | code-listing | not-applicable | no library object; explanation or non-Python content | i1=BestDotNumber candidates = np.delete(AllIndexes, [k, i1]) i2, i3, i4, i5 = np.random.choice(candidates, 4, replace=False) DonorVector = Generation[i1] + F *  |
| T059 | 70 | code-listing | not-applicable | no library object; explanation or non-Python content | i1=k i2 = BestDotNumber candidates = np.delete(AllIndexes, [i1, i2]) i3, i4 = np.random.choice(candidates, 2, replace=False) DonorVector = Generation[i1] + F *  |
| T060 | 70 | code-listing | not-applicable | no library object; explanation or non-Python content | i1=k i2 = BestDotNumber candidates = np.delete(AllIndexes, [i1, i2]) i3, i4 = np.random.choice(candidates, 2, replace=False) DonorVector = Generation[i1] + F*(G |
| T061 | 70 | code-listing | not-applicable | no library object; explanation or non-Python content | i2 = BestDotNumber i3 = k candidates = np.delete(AllIndexes, [i2, i3]) i1, i4, i5 = np.random.choice(candidates, 3, replace=False) DonorVector = Generation[i1]  |
| T062 | 71 | code-listing | not-applicable | no library object; explanation or non-Python content | i1=k i2 = BestDotNumber candidates = np.delete(AllIndexes, [i1, i2]) i3, i4 = np.random.choice(candidates, 2, replace=False) |
| T063 | 71 | code-listing | not-applicable | no library object; explanation or non-Python content | i1=k candidates = np.delete(AllIndexes, i1) i2, i3, i4 = np.random.choice(candidates, 3, replace=False) |
| F031 | 72 | figure | unverified | not claimed to match a printed figure or table | Figure 2.6 ‒ Plot of the decrease of the objective function (1.13) (on a logarithmic scale) using the DE algorithms with population size K=25: a) DE/rand/1; b) DE/rand/2; c) DE/bes |
| T064 | 73 | table-1col | unverified | not claimed to match a printed figure or table | CR, F = 0.5, 0.6 |
| T065 | 73 | table-1col | unverified | not claimed to match a printed figure or table | tau1, tau2 = 0.1, 0.1FLower, FUpper = 0.1, 0.9 |
| T066 | 73 | code-listing | not-applicable | no library object; explanation or non-Python content | i1, i2, i3 = np.random.choice(candidates, 3, replace=False) |
| T067 | 74 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | if np.random.rand() < tau1:F = FLower + np.random.rand() * (FUpper - FLower)if np.random.rand() < tau2:CR = np.random.rand() |
| F032 | 74 | figure | unverified | not claimed to match a printed figure or table | Figure 2.7 ‒ Plot of the decrease of the objective function (1.13) (on a logarithmic scale) using the SADE algorithm with population size K=25 |
| T068 | 77 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np xr1 = np.array([0.2, 0, -3.1, 5.6, -2.0])xr2 = np.array([1.1, -9.5, 2.9, -4.2, 2.1])xr3 = np.array([-2.1, 7.1, 1.1, -1.1, 0.5])F = 0.6 |
| T069 | 77 | table-1col | unverified | not claimed to match a printed figure or table | v = xr1 + F * (xr2 - xr3)print(v) |
| T070 | 78 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np x = np.array([1.2, 0.1, 0.5, -2.1, 6.2, 0.3, -2.2, 0.4, 9.3, 10.0])v = np.array([0.2, -0.2, 1.3, 2.3, 2.3, -0.3, -5.1, 0.3, 9.0, -4.6])CR = 0 |
| T071 | 78 | table-1col | unverified | not claimed to match a printed figure or table | TrialVector = [] |
| T072 | 78 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | for i in range(VarsLength):    iRand = np.random.choice(DimensionIndexes)    if np.random.rand() <= CR or iRand == i:        TrialVector.append(v[i])    else:   |
| T073 | 79 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np x = np.array([0.2, -0.9, 1.5])u = np.array([0.1, -0.2, 1.3])def function(x):    return float(np.sum(x**2)) |
| T074 | 79 | table-1col | unverified | not claimed to match a printed figure or table | if function(u) < function(x):    x = u.copy() |
| T075 | 79 | table-1col | unverified | not claimed to match a printed figure or table | print(x) |
| T076 | 82 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def DEBest1bin(function, Vars, DomainVarsList, Population, Iterations): CostFunctionValues = [] CR,  |
| T077 | 82 | table-1col | unverified | not claimed to match a printed figure or table | Population = 10Iterations = 100 |
| T078 | 82 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = DEBest1bin(ObjectiveFunction, Vars, DomainVarsList, Population, Iterations) |
| F033 | 86 | figure | unverified | not claimed to match a printed figure or table | Figure 3.1 ‒ Social hierarchy of wolves in a pack |
| F034 | 87 | figure | unverified | not claimed to match a printed figure or table | Figure 3.2 ‒ Illustration of the individual stages of constructing the vector x: a) determining the α-, β-, and δ-wolves among the whole pack; b) constructing the product vectors C |
| F035 | 88 | figure | unverified | not claimed to match a printed figure or table | Figure 3.3 ‒ Plots of the decrease of the Griewank function using the GWO algorithm with pack size K=25 for various numbers of iterations I |
| F036 | 89 | figure | unverified | not claimed to match a printed figure or table | Figure 3.4 ‒ Flowchart of the GWO algorithm |
| C007 | 90 | table | unverified | not claimed to match a printed figure or table | Table 3.1 ‒ Description of individual sections of the GWO function's code in Python |
| T079 | 94 | explanation-table | not-applicable | no library object; explanation or non-Python content | Code |
| T080 | 96 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def GWO(function, Vars, DomainVarsList, PackSize, Iterations): CostFunctionValues = [] lb = np.array |
| T081 | 96 | table-1col | unverified | not claimed to match a printed figure or table | PackSize = 25 Iterations = 200 |
| T082 | 96 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = GWO(ObjectiveFunction, Vars, DomainVarsList, PackSize, Iterations) |
| F037 | 96 | figure | unverified | not claimed to match a printed figure or table | Figure 3.5 ‒ Plot of the decrease of the objective function (1.13) using the GWO algorithm with pack size K=25 (on a logarithmic scale) |
| T083 | 97 | table-1col | unverified | not claimed to match a printed figure or table | a = 2 - 2 * (step / Iterations) |
| T084 | 97 | table-1col | unverified | not claimed to match a printed figure or table | a = 2 - 2 * (step / Iterations) ** 2 |
| F038 | 98 | figure | unverified | not claimed to match a printed figure or table | Figure 3.6 ‒ Plot of the change of the parameter a |
| F039 | 98 | figure | unverified | not claimed to match a printed figure or table | Figure 3.7 ‒ Plot of the decrease of the objective function (1.13) (on a logarithmic scale) using the mGWO algorithm with pack size K=25 |
| T085 | 101 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def EPDGWO(function, Vars, DomainVarsList, PackSize, Iterations): CostFunctionValues = [] lb = np.ar |
| F040 | 101 | figure | unverified | not claimed to match a printed figure or table | Figure 3.8 ‒ Plot of the decrease of the objective function (1.13) (on a logarithmic scale) using the EPD-GWO algorithm with pack size K=25 |
| T086 | 105 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np Vars = ['x1', 'x2', 'x3'] DomainVarsList = [(-20, 20), (-20, 20), (-20, 20)] def function(x): x1, x2, x3 = x return x1**2 + x2**2 + x3**2 Pac |
| T087 | 105 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | n = len(Vars) lb = np.array([d[0] for d in DomainVarsList]) ub = np.array([d[1] for d in DomainVarsList]) Pack = lb + np.random.rand(PackSize, n) * (ub - lb) |
| T088 | 105 | code-listing | not-applicable | no library object; explanation or non-Python content | WolvesCosts = np.array([function(x) for x in Pack], dtype=float) print(WolvesCosts) |
| T089 | 106 | code-listing | not-applicable | no library object; explanation or non-Python content | AlphaBetaDeltaCosts = np.argsort(WolvesCosts)[:3] |
| T090 | 106 | table-1col | unverified | not claimed to match a printed figure or table | AlphaWolfNumber = int(AlphaBetaDeltaCosts[0]) XAlpha = Pack[AlphaWolfNumber].copy() BetaWolfNumber = int(AlphaBetaDeltaCosts[1]) XBeta = Pack[BetaWolfNumber].co |
| T091 | 107 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np k = 0 a = 2 |
| T092 | 107 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | C1 = 2 * np.random.rand(len(Vars)) C2 = 2 * np.random.rand(len(Vars)) C3 = 2 * np.random.rand(len(Vars)) |
| T093 | 107 | code-listing | not-applicable | no library object; explanation or non-Python content | D1 = np.abs(C1 * XAlpha - Pack[k]) D2 = np.abs(C2 * XBeta - Pack[k]) D3 = np.abs(C3 * XDelta - Pack[k]) |
| T094 | 107 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | A1 = 2 * a * np.random.rand(len(Vars)) - a A2 = 2 * a * np.random.rand(len(Vars)) - a A3 = 2 * a * np.random.rand(len(Vars)) - a |
| T095 | 108 | table-1col | unverified | not claimed to match a printed figure or table | X1 = XAlpha - A1 * D1 X2 = XBeta - A2 * D2 X3 = XDelta - A3 * D3 print(X1) print(X2) print(X3) |
| T096 | 108 | code-listing | not-applicable | no library object; explanation or non-Python content | X = np.mean([X1, X2, X3], axis=0) print(X) |
| T097 | 110 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def GWOParameters(function, Vars, DomainVarsList, PackSize, Iterations): CostFunctionValues = [] A1D |
| T098 | 110 | table-1col | unverified | not claimed to match a printed figure or table | PackSize = 25 Iterations = 200 |
| T099 | 110 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = GWOParameters(ObjectiveFunction, Vars, DomainVarsList, PackSize, Iterations) BestWolvesCost, BestPosition, CostFunctionValues, A1D1List, A2 |
| T100 | 111 | code-listing | unverified | not claimed to match a printed figure or table | import matplotlib.pyplot as plt a_values = [item[0] for item in A1D1List] aA1D1 = [item[1] for item in A1D1List] aA2D2 = [item[1] for item in A2D2List] aA3D3 =  |
| T101 | 113 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import numpy as np from IPython.display import clear_output def mGWO(function, Vars, DomainVarsList, PackSize, Iterations): CostFunctionValues = [] lb = np.arra |
| T102 | 113 | table-1col | unverified | not claimed to match a printed figure or table | PackSize = 10 Iterations = 200 |
| T103 | 113 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = GWO(ObjectiveFunction, Vars, DomainVarsList, PackSize, Iterations) |
| C008 | 119 | table | unverified | not claimed to match a printed figure or table | Table 4.1 – Benchmarks, domains, global minimum value, and its location |
| T104 | 125 | table-6col | unverified | not claimed to match a printed figure or table | № |
| C009 | 125 | table | unverified | not claimed to match a printed figure or table | Table 4.2 – Benchmarks and some of their features |
| T105 | 127 | table-6col | unverified | not claimed to match a printed figure or table | № |
| T106 | 136 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np import plotly.graph_objects as go FunctionToShow = lambda x1, x2: x1 ** 2 * (1.0 + np.sin(x2)) + x2 ** 2 * (1.0 + np.sin(x1)) Vars = ["x1", " |
| T107 | 137 | code-listing | not-applicable | no library object; explanation or non-Python content | X1, X2 = np.meshgrid(np.linspace(DomainVarsList[0][0], DomainVarsList[0][1], 200), np.linspace(DomainVarsList[1][0], DomainVarsList[1][1], 200)) Z = function(np |
| T108 | 137 | code-listing | not-applicable | no library object; explanation or non-Python content | x_min, x_max = DomainVarsList[0] y_min, y_max = DomainVarsList[1] X1, X2 = np.meshgrid(np.linspace(x_min, x_max, 200), np.linspace(y_min, y_max, 200)) Z = funct |
| T109 | 138 | table-1col | unverified | not claimed to match a printed figure or table | Dimension = 10Population = 25Runs = 100Iterations = 500 |
| F041 | 141 | figure | unverified | not claimed to match a printed figure or table | Figure 5.1 ‒ Box-and-Whisker plot |
| T110 | 143 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | import io, time, contextlibimport numpy as npimport matplotlib.pyplot as plt# the optimizers call clear_output(); let us disable itclear_output = lambda *args,  |
| T111 | 143 | table-1col | unverified | not claimed to match a printed figure or table | Dimension = 30Ackley1Domain = [(-32.0, 32.0)] * DimensionVarsList = [f"x{i}" for i in range(1, Dimension + 1)] |
| T112 | 143 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | IterationNumber = 200SwarmPopulation = 25Runs = 30np.random.seed(2025)  # fixed seed: the results can be reproduced |
| T113 | 144 | table-1col | unverified | not claimed to match a printed figure or table | AlgorithOutputList = []for _ in range(Runs):    p = RunQuiet(RingPSO, Ackley1Function, VarsList, Ackley1Domain,                 SwarmPopulation, IterationNumber |
| T114 | 144 | table-1col | unverified | not claimed to match a printed figure or table | [3.16171, 2.8695, 3.48162, 3.16376, 3.45142, 2.72849, 2.73058, 2.89714, 3.61364, 3.25111, 3.48744, 4.90215, 3.14915, 2.73147, 2.95995, 3.03341, 2.66691, 3.37867 |
| T115 | 144 | code-listing | not-applicable | no library object; explanation or non-Python content | print(f"Maximum value: {np.max(AlgorithOutputList):.6g}")print(f"0.75-quantile: {np.quantile(AlgorithOutputList, 0.75):.6g}")print(f"Median: {np.median(Algorith |
| T116 | 145 | table-1col | unverified | not claimed to match a printed figure or table | Maximum value: 4.902150.75-quantile: 3.43323Median: 3.155430.25-quantile: 2.87641Minimum value: 2.25902Standard deviation: 0.527509 |
| T117 | 145 | table-1col | unverified | not claimed to match a printed figure or table | plt.figure(figsize=(4.5, 4.5))plt.boxplot(AlgorithOutputList, notch=True, patch_artist=True,            whis=(0, 100), showfliers=False,            boxprops=dic |
| F042 | 145 | figure | unverified | not claimed to match a printed figure or table | Figure 5.2 ‒ Box-and-Whisker plot built from the results of thirty independent runs of the Ring-PSO algorithm on the Ackley No. 1 benchmark: a) on a linear scale; b) on a logarithm |
| C010 | 147 | table | unverified | not claimed to match a printed figure or table | Table 5.1 ‒ Top 3 algorithms by median and minimum values |
| T118 | 159 | table-7col | unverified | not claimed to match a printed figure or table | Benchmark |
| C011 | 159 | table | unverified | not claimed to match a printed figure or table | Table 5.2 ‒ Sum of algorithm ranks by median and minimum values |
| T119 | 159 | table-15col | unverified | not claimed to match a printed figure or table | Indicator |
| T120 | 164 | table-1col | unverified | not claimed to match a printed figure or table | Dimension = 10HappyCatDomain = [(-2.0, 2.0)] * DimensionVars = [f"x{i}" for i in range(1, Dimension + 1)] |
| T121 | 164 | table-1col | unverified | not claimed to match a printed figure or table | Iterations = 100Population = 25Runs = 20 |
| T122 | 165 | table-1col | unverified | not claimed to match a printed figure or table | AlgorithOutputList = []for _ in range(Runs):    p = RunQuiet(DEBest, HappyCatFunction, Vars, HappyCatDomain,                 Population, Iterations)    Algorith |
| T123 | 165 | code-listing | not-applicable | no library object; explanation or non-Python content | print(f"Maximum value: {np.max(AlgorithOutputList):.6g}")print(f"0.75-quantile: {np.quantile(AlgorithOutputList, 0.75):.6g}")print(f"Median: {np.median(Algorith |
| T124 | 166 | table-1col | unverified | not claimed to match a printed figure or table | plt.figure(figsize=(4.5, 4.5)) plt.boxplot(AlgorithOutputList, notch=True, patch_artist=True, whis=(0, 100), showfliers=False, boxprops=dict(facecolor="#5E81B5" |
| T125 | 166 | table-1col | unverified | not claimed to match a printed figure or table | plt.figure(figsize=(4.5, 4.5)) plt.boxplot(AlgorithOutputList, notch=True, patch_artist=True, whis=(0, 100), showfliers=False, boxprops=dict(facecolor="#5E81B5" |
| T126 | 167 | table-1col | unverified | not claimed to match a printed figure or table | Iterations = 100Population = 10Runs = 5 |
| T127 | 167 | table-1col | unverified | not claimed to match a printed figure or table | start = time.perf_counter()for _ in range(Runs):    RunQuiet(DEBest, HappyCatFunction, Vars, HappyCatDomain,             Population, Iterations)print((time.perf |
| F043 | 172 | figure | unverified | not claimed to match a printed figure or table | Fig. 6.1 shows that a successful choice of the coefficients Ki, Kp, and Kd can ensure stability of the controlled plant (the variants in Fig. 6.1, a, b, c), while an unsuccessful c |
| F044 | 172 | figure | unverified | not claimed to match a printed figure or table | Figure 6.1 ‒ Transient-response plots of the plant in a closed-loop control system, with a PID controller, for various coefficient values: a) Ki=0.2, Kp=1, Kd=9; b) Ki=2, Kp=0.3, K |
| F045 | 172 | figure | unverified | not claimed to match a printed figure or table | Fig. 6.1 shows that the control dynamics are tied to the time coordinate: all the state variables are functions of time. In addition, constraint (6.4) and criterion (6.5) are also  |
| F046 | 174 | figure | unverified | not claimed to match a printed figure or table | Figure 6.2 ‒ Transient-response plots of the controlled plant, covered by feedback with a PID controller, for various coefficient values: a) the closed-loop system's transient proc |
| F047 | 174 | figure | unverified | not claimed to match a printed figure or table | Figure 6.3 ‒ Diagram of the mobile robot's environment with obstacles |
| F048 | 174 | figure | unverified | not claimed to match a printed figure or table | Figure 6.4 ‒ A possible solution to the problem of computing the mobile robot's trajectory |
| F049 | 175 | figure | unverified | not claimed to match a printed figure or table | Figure 6.5 ‒ Two-mass dynamic model of a hoist crane with a load on a flexible suspension |
| F050 | 177 | figure | unverified | not claimed to match a printed figure or table | Figure 6.6 ‒ Velocity of the crane's motion (red curve) and the difference between the positions of the crane and the load (black curve) for various coefficient values: a) A0=0, A1 |
| F051 | 177 | figure | unverified | not claimed to match a printed figure or table | Figure 6.7 ‒ Scheme of the mountain car motion control problem |
| F052 | 178 | figure | unverified | not claimed to match a printed figure or table | Figure 6.8 ‒ Structure of the artificial neural network for Problems 4a and 4b |
| F053 | 180 | figure | unverified | not claimed to match a printed figure or table | Figure 6.9 ‒ Plots of the car's control and state variables: a) position; b) velocity; c) control |
| F054 | 180 | figure | unverified | not claimed to match a printed figure or table | Figure 6.10 ‒ Dynamic model of the inverted pendulum (cart-pole) |
| T128 | 180 | table-2col | unverified | not claimed to match a printed figure or table |  |
| F055 | 180 | figure | unverified | not claimed to match a printed figure or table | Figure 6.11 ‒ Graphical illustration of the boundary conditions of the dynamic system's motion: a) initial state of the system; b) final state of the system |
| F056 | 183 | figure | unverified | not claimed to match a printed figure or table | Figure 6.12 ‒Plots of the system's state variables and control: a) position of the pendulum link; b) velocity of the pendulum link; c) position of the cart; d) velocity of the cart |
| F057 | 184 | figure | unverified | not claimed to match a printed figure or table | Figure 6.13 ‒ Diagram of the transformation of a constrained optimization problem into an objective-function minimization problem |
| F058 | 186 | figure | unverified | not claimed to match a printed figure or table | Figure 6.14 ‒ Dynamics of the search for the minimum of the function (6.27) |
| T129 | 186 | code-listing | unverified | not claimed to match a printed figure or table | # --- Setup: run once. Installs only the packages that are missing. --- import importlib.util, subprocess, sys REQUIRED = {                 # import name : pip  |
| F059 | 186 | figure | unverified | not claimed to match a printed figure or table | Figure 6.15 ‒ Graphical interpretation of reaching a neighborhood of the stability conditions XT |
| F060 | 186 | figure | unverified | not claimed to match a printed figure or table | Figure 6.16 ‒ Diagram of the closed-loop control system of a plant with a PID controller |
| T130 | 186 | code-listing | unverified | not claimed to match a printed figure or table | import sympy as sp s = sp.symbols("s") Ki, Kp, Kd = sp.symbols("Ki Kp Kd", real=True) # Transfer functions of the plant and PID controller Gp = 1 / ((s + 1) * ( |
| T131 | 186 | table-1col | unverified | not claimed to match a printed figure or table | # Close the series-connected model with unity negative feedback G_closed = sp.factor(G_series / (1 + G_series)) print(G_closed) |
| T132 | 188 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as np import sympy as sp from scipy import signal s = sp.symbols("s") Ki, Kp, Kd = sp.symbols("Ki Kp Kd", real=True) Gp = 1 / ((s + 1) * (1 + sp.Ra |
| T133 | 189 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as np import sympy as sp # ---------- 1. Symbolic preparation (run once) ---------- s = sp.symbols("s") Ki, Kp, Kd = sp.symbols("Ki Kp Kd", real=Tr |
| F061 | 190 | figure | unverified | not claimed to match a printed figure or table | Figure 6.17 ‒ Dynamics of the transient process for Ki=0.1, Kp=2, Kd=6 (a) and the placement of the system's poles (b) |
| F062 | 190 | figure | unverified | not claimed to match a printed figure or table | Fig. 6.18 shows that the dominant pole is located close to the imaginary axis Im. This causes a slow approach to the setpoint (Fig. 17, a), which is undesirable. This pole must be  |
| F063 | 190 | figure | unverified | not claimed to match a printed figure or table | Figure 6.18 ‒ Visual explanation of the construction of the penalty function PD |
| F064 | 191 | figure | unverified | not claimed to match a printed figure or table | Figure 6.19 ‒ Visual explanation of the construction of the penalty function PO |
| T134 | 192 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np# Circular obstacles: centers and radiip = np.array([[2.0, 2.0], [7.0, 3.0], [7.0, 7.5], [2.5, 7.0]])r = np.array([1.1, 1.4, 1.6, 1.5])obstacl |
| T135 | 192 | code-listing | unverified | not claimed to match a printed figure or table | # Cubic splines are implemented below with scipy.interpolate.CubicSpline.from scipy.interpolate import CubicSpline |
| T136 | 193 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as npfrom scipy.interpolate import CubicSplinedef ObjectiveFunction2(kx1, ky1, kx2, ky2, kx3, ky3):    """Length of a cubic-spline path plus penalt |
| F065 | 193 | figure | unverified | not claimed to match a printed figure or table | Figure 6.20 ‒ Discrete trajectories: a) one that crosses an obstacle; b) one that avoids all the obstacles |
| T137 | 195 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as np def ObjectiveFunction3(A0, A1, A2, A3, A4, A5, A6): L, g, v, T = 5.0, 9.81, 1.2, 3.0 t = np.arange(301) * 0.01 W = np.array([1, -4, 6, -4, 1] |
| F066 | 196 | figure | unverified | not claimed to match a printed figure or table | Figure 6.21 ‒ Plots of the crane's velocity and the difference between the positions of the crane and the load: a) constraint (6.16) violated; b) constraint (6.16) satisfied |
| T138 | 197 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as np def MountainCarStep(x, v, a): """One discrete transition of the mountain-car model.""" return np.array([x + v, v + 0.001*a - 0.0025*np.cos(3* |
| T139 | 197 | code-listing | unverified | not claimed to match a printed figure or table | def MountainCarANN(theta, x=None, v=None): """Feedforward ANN from Eq. (6.21); returns a number in (-pi/2, pi/2). Two equivalent ways to call it: MountainCarANN |
| T140 | 198 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | def ObjectiveFunction4a(params, step=MountainCarStep, T=200): """Problem 4a: number of steps needed to reach x > 0.5 (smaller is better).""" x, v, n = -0.5, 0.0 |
| T141 | 198 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction4b(params, step=MountainCarStep, T=200): """Problem 4b: steps needed to reach the flag and stop there.""" x, v, n = -0.5, 0.0, 1 for _ in r |
| F067 | 199 | figure | unverified | not claimed to match a printed figure or table | Figure 6.22 ‒ Plots of the car's state variables and control: a) position; b) velocity; c) control |
| T142 | 201 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as npdef CartPoleStep(phi, omega, x, v, F, dt=0.025):    """One explicit-Euler step of the cart-pole model used in the chapter."""    m, M, length, |
| T143 | 201 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np def CartPoleANN(theta, state=None): """Feedforward ANN for the cart-pole problem; returns a number in (-pi/2, pi/2). Two equivalent ways to c |
| T144 | 203 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | # ---------- Problem 5 data (constraints and tolerances of the problem) ---------- DT       = 0.025                                   # time step, s N_STEPS  =  |
| F068 | 205 | figure | unverified | not claimed to match a printed figure or table | Figure 6.23 ‒ Plots of the dynamic system's state variables and control: a) position of the pendulum link; b) velocity of the pendulum link; c) position of the cart; d) velocity of |
| C012 | 205 | table | unverified | not claimed to match a printed figure or table | Table 6.1 ‒ The number of iterations for each optimizer and variables domains for Problems 1-5 |
| T145 | 205 | table-8col | unverified | not claimed to match a printed figure or table | Problem |
| F069 | 205 | figure | unverified | not claimed to match a printed figure or table | Fig. 6.24 presents box-and-whisker charts for each objective function. For a more complete analysis, we give numerical estimates (Table 6.2) and the corresponding rating indicators |
| F070 | 208 | figure | unverified | not claimed to match a printed figure or table | Figure 6.24 ‒ Graphical representation of the optimization results for the objective functions corresponding to: a) Problem 1a; b) Problem 1b*; c) Problem 2; d) Problem 3; e) Probl |
| C013 | 208 | table | unverified | not claimed to match a printed figure or table | Table 6.2 ‒ Numerical representation of the results of minimizing the objective functions corresponding to Problems 1-5 |
| T146 | 208 | table-16col | unverified | not claimed to match a printed figure or table | Problem |
| C014 | 208 | table | unverified | not claimed to match a printed figure or table | Table 6.3 ‒ Top 3 algorithms by median and minimum values |
| T147 | 208 | table-7col | unverified | not claimed to match a printed figure or table | Problem |
| C015 | 209 | table | unverified | not claimed to match a printed figure or table | Table 6.4 ‒ Sum of algorithm ranks by median and minimum values |
| T148 | 209 | table-15col | unverified | not claimed to match a printed figure or table | Indicator |
| T149 | 213 | code-listing | unverified | not claimed to match a printed figure or table | import sympy as sps = sp.symbols("s")Ki, Kp, Kd = sp.symbols("Ki Kp Kd", real=True)Gp = 1/(1+s)**3Gc = Ki/s + Kp + Kd*s |
| T150 | 213 | table-1col | unverified | not claimed to match a printed figure or table | G_series = sp.factor(Gp * Gc)print(G_series) |
| T151 | 213 | table-1col | unverified | not claimed to match a printed figure or table | G_closed = sp.factor(G_series / (1 + G_series))print(G_closed) |
| T152 | 214 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np import sympy as sp from scipy import signal s = sp.symbols("s") Ki, Kp, Kd = sp.symbols("Ki Kp Kd", real=True) num_expr, den_expr = sp.fracti |
| T153 | 214 | table-1col | unverified | not claimed to match a printed figure or table | DomainVarsList = [[0.001, 50], [0.001, 50], [0.001, 50]]Vars = ["Ki", "Kp", "Kd"] |
| T154 | 214 | table-1col | unverified | not claimed to match a printed figure or table | Population = 20Iterations = 50 |
| T155 | 214 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = PSO(lambda x: ObjectiveFunction(*x), Vars, DomainVarsList, Population, Iterations) |
| T156 | 215 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np import matplotlib.pyplot as plt from scipy import signal Ki, Kp, Kd = OptimizationResult[1] num, den = get_coeffs(Ki, Kp, Kd) num = np.atleas |
| T157 | 216 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np p = np.array([[1, 3], [4, 2], [6, 3.5], [8, 1.8]], dtype=float) r = np.array([0.7, 1.0, 0.6, 0.9]) obstacle_count = len(r) obstacles = list(z |
| T158 | 216 | code-listing | unverified | not claimed to match a printed figure or table | from scipy.interpolate import CubicSpline |
| T159 | 217 | code-listing | unverified | not claimed to match a printed figure or table | from scipy.interpolate import CubicSpline def ObjectiveFunction(kx1, ky1, kx2, ky2, kx3, ky3): """Length of a cubic-spline path plus penalties for leaving the d |
| T160 | 217 | table-1col | unverified | not claimed to match a printed figure or table | Vars = ["kx1", "ky1", "kx2", "ky2", "kx3", "ky3"] DomainVarsList= [[0, 10], [0, 5], [0, 10], [0, 5], [0, 10], [0, 5]] |
| T161 | 217 | table-1col | unverified | not claimed to match a printed figure or table | Population = 25Iterations = 100 |
| T162 | 217 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = PSO(lambda x: ObjectiveFunction(*x), Vars, DomainVarsList, Population, Iterations) |
| T163 | 217 | code-listing | unverified | not claimed to match a printed figure or table | # Visualize the best trajectory returned by the optimizer. import numpy as np import matplotlib.pyplot as plt from matplotlib.patches import Circle from scipy.i |
| T164 | 220 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np import matplotlib.pyplot as plt from types import SimpleNamespace from scipy.linalg import expm from scipy.optimize import brentq def simulat |
| T165 | 220 | table-1col | unverified | not claimed to match a printed figure or table | Vars = ["t1", "t2", "t3"] DomainVarsList = [[0.01, 3], [0.01, 3], [0.01, 3]] |
| T166 | 220 | table-1col | unverified | not claimed to match a printed figure or table | Population = 25 Iterations = 500 |
| T167 | 220 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = PSO(lambda x: ObjectiveFunction(*x), Vars, DomainVarsList, Population, Iterations) |
| T168 | 221 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np import matplotlib.pyplot as plt t1, t2, t3 = OptimizationResult[1] F, l = 50000.0, 5.0 sol = simulate(t1, t2, t3, dt=0.005) t  = sol.t v1 = s |
| F071 | 223 | figure | unverified | not claimed to match a printed figure or table | Figure 6.25 ‒ Dynamic model of the Furuta pendulum |
| T169 | 225 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np def FurutaPendulumPlant(phi1, phi2, alpha1, alpha2, M, dt=0.02): """One explicit-Euler step of the Furuta-pendulum model (6.47). phi is measu |
| T170 | 225 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np def ANN(theta, inputs): """Five-neuron arctan network; theta contains 31 weights/biases.""" theta = np.asarray(theta, dtype=float) W = theta[ |
| T171 | 226 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np def ObjectiveFunction(*theta): """Furuta pendulum: minimise the control duration t_s (6.49). t_s is the first moment after which all four sta |
| T172 | 226 | table-1col | unverified | not claimed to match a printed figure or table | Vars = ["w111", "w121", "w131", "w141", "w112", "w122", "w132", "w142", "w113", "w123", "w133", "w143", "w114", "w124", "w134", "w144", "w115", "w125", "w135",  |
| T173 | 226 | table-1col | unverified | not claimed to match a printed figure or table | Population = 25Iterations = 2500 |
| T174 | 226 | table-1col | unverified | not claimed to match a printed figure or table | OptimizationResult = vonNeumannPSO(lambda x: ObjectiveFunction(*x), Vars, DomainVarsList, Population, Iterations) |
| T175 | 227 | code-listing | unverified | not claimed to match a printed figure or table | import numpy as np import matplotlib.pyplot as plt from scipy.signal import savgol_filter from scipy.interpolate import CubicSpline Delta_t, T = 0.02, 10.0 def  |
| F072 | 230 | figure | unverified | not claimed to match a printed figure or table | Figure 7.1 – Diagram of a three-link manipulator showing the desired position of the end effector pt (the robot's gripping element) |
| T176 | 230 | code-listing | verified | see `src/metaopt/` and `tests/test_examples_smoke.py` | import numpy as np def ObjectiveFunction5(x): alpha = np.asarray(x, dtype=float) return float(np.sqrt((2 / 5 * np.sum(np.cos(alpha)) - 1) ** 2 + (2 / 5 * np.sum |
| T177 | 231 | code-listing | not-applicable | no library object; explanation or non-Python content | Domain5Vars = [[-np.pi, np.pi] for _ in range(5)] Domain20Vars = [[-np.pi, np.pi] for _ in range(20)] Domain50Vars = [[-np.pi, np.pi] for _ in range(50)] |
| T178 | 231 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 500 OptimizationResult = PSO(ObjectiveFunction5, list(range(5)), Domain5Vars, SwarmPopulation, IterationNumber) |
| F073 | 231 | figure | unverified | not claimed to match a printed figure or table | Figure 7.2 ‒ Diagram of an I-shaped beam showing its geometric dimensions ‒ the variables of the objective function |
| T179 | 232 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): b, h, tw, tf = np.asarray(x, dtype=float) g1 = 2 * b * tw + tw * (h - 2 * tf) - 300 g2 = (18 * 10**4 * h) / (tw * (h - 2 * tf)**3 + 2  |
| T180 | 232 | table-1col | unverified | not claimed to match a printed figure or table | IShapedBeamVars = ["b", "h", "tw", "tf"] IShapedBeamDomain = [[10, 50], [10, 80], [0.9, 5], [0.9, 5]] |
| T181 | 233 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 100 OptimizationResult = PSO(ObjectiveFunction, IShapedBeamVars, IShapedBeamDomain, SwarmPopulation, IterationNumber) |
| F074 | 233 | figure | unverified | not claimed to match a printed figure or table | Figure 7.3 ‒ Diagram of the pressure vessel design problem |
| T182 | 234 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): nTs, nTh, R, L = np.asarray(x, dtype=float) Ts = np.floor(nTs + 0.5) * 0.0625 Th = np.floor(nTh + 0.5) * 0.0625 g1 = 0.0193 * R - Ts g |
| T183 | 234 | table-1col | unverified | not claimed to match a printed figure or table | PressureVesselVars = ["nTs", "nTh", "R", "L"] PressureVesselDomain = [[1, 1600], [1, 1600], [10, 200], [10, 240]] |
| T184 | 235 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 200 OptimizationResult = PSO(ObjectiveFunction, PressureVesselVars, PressureVesselDomain, SwarmPopulation, IterationNumbe |
| F075 | 235 | figure | unverified | not claimed to match a printed figure or table | Figure 7.4 ‒ Simplified diagram of a reinforced concrete beam |
| T185 | 235 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): nAs, nb, h = np.asarray(x, dtype=float) levels = np.array([6, 6.16, 6.32, 6.6, 7, 7.11, 7.2, 7.8, 7.9, 8, 8.4]) midpoints = (levels[:- |
| T186 | 235 | table-1col | unverified | not claimed to match a printed figure or table | ReinforcedConcreteBeamVars = ["nAs", "nb", "h"] ReinforcedConcreteBeamDomain = [[6, 8.4], [28, 40], [5, 10]] |
| T187 | 235 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 200 OptimizationResult = PSO(ObjectiveFunction, ReinforcedConcreteBeamVars, ReinforcedConcreteBeamDomain, SwarmPopulation |
| F076 | 236 | figure | unverified | not claimed to match a printed figure or table | Figure 7.5 ‒ Schematic representation of the robot manipulator's gripper mechanism [6] |
| T188 | 239 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): a, b, c, e, f, l, delta = np.asarray(x, dtype=float) z_min, z_max = 0, 25 y_min, y_max = 70, 150 z_values = np.arange(z_min, z_max + 1 |
| T189 | 239 | code-listing | not-applicable | no library object; explanation or non-Python content | RobotGripperVars = ["a", "b", "c", "e", "f", "l", "delta"] RobotGripperDomain = [[0, 150], [0, 150], [80, 300], [0, 100], [0, 150], [0, 300], [1, np.pi]] |
| T190 | 239 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 200 OptimizationResult = PSO(ObjectiveFunction, RobotGripperVars, RobotGripperDomain, SwarmPopulation, IterationNumber) |
| F077 | 242 | figure | unverified | not claimed to match a printed figure or table | Figure 7.6 ‒ Graphical representation of the optimization results for the objective functions corresponding to: a) Problem 1D=5; b) Problem 1D=20; c) Problem 1D=50; d) Problem 2; e |
| C016 | 243 | table | unverified | not claimed to match a printed figure or table | Table 7.1 ‒ Numerical representation of the results of minimizing the objective functions corresponding to Problems 1-5 |
| T191 | 243 | table-16col | unverified | not claimed to match a printed figure or table | Problem |
| C017 | 243 | table | unverified | not claimed to match a printed figure or table | Table 7.2 ‒ Top 3 algorithms by median and minimum objective-function values |
| T192 | 244 | table-7col | unverified | not claimed to match a printed figure or table | Problem |
| C018 | 244 | table | unverified | not claimed to match a printed figure or table | Table 7.3 ‒ Sum of algorithm ranks by median and minimum objective-function values |
| T193 | 244 | table-15col | unverified | not claimed to match a printed figure or table | Indicator |
| T194 | 247 | code-listing | unverified | not claimed to match a printed figure or table | def Penalty1(x): x1, x2, x3 = np.asarray(x, dtype=float) delta = 10**-10 h = x1**2 + x2**2 + x3**2 - 1 penalty_output = abs(h) if abs(h) >= delta else 0 return  |
| T195 | 247 | table-1col | unverified | not claimed to match a printed figure or table | Penalty1([0.1, 0.1, -0.5]) |
| T196 | 247 | table-1col | unverified | not claimed to match a printed figure or table | Penalty1([1, 10**-10, 0]) |
| T197 | 248 | code-listing | unverified | not claimed to match a printed figure or table | def Penalty2(x): x1, x2, x3 = np.asarray(x, dtype=float) delta = 10**-10 h = 5 * x1 + x2 - x3 penalty_output = abs(h) if abs(h) >= delta else 0 return float(10* |
| T198 | 248 | code-listing | unverified | not claimed to match a printed figure or table | def Penalty3(x): x1, x2, x3 = np.asarray(x, dtype=float) delta = 10**-10 h = x1 * x2 * x3 - 10 penalty_output = abs(h) if abs(h) >= delta else 0 return float(10 |
| T199 | 249 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): alpha1, alpha2, alpha3, L1, L2, L3 = np.asarray(x, dtype=float) x_end = L1 * np.cos(alpha1) + L2 * np.cos(alpha2) + L3 * np.cos(alpha3 |
| T200 | 249 | code-listing | not-applicable | no library object; explanation or non-Python content | Domain = [[-np.pi, np.pi] for _ in range(3)] + [[0.1, 1] for _ in range(3)] |
| T201 | 249 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 500 OptimizationResult = PSO(ObjectiveFunction, ["alpha1", "alpha2", "alpha3", "L1", "L2", "L3"], Domain, SwarmPopulation |
| F078 | 251 | figure | unverified | not claimed to match a printed figure or table | Figure 7.7 ‒ Diagram of the gearbox |
| T202 | 252 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): b, m, nz, l1, l2, d1, d2 = np.asarray(x, dtype=float) z = np.floor(nz + 0.5) g1 = 27 / (b * m**2 * z) - 1 g2 = 397.5 / (b * m**2 * z** |
| T203 | 252 | table-1col | unverified | not claimed to match a printed figure or table | Domain = [[2.6, 3.6], [0.7, 0.8], [17, 28], [7.3, 8.3], [7.3, 8.3], [2.9, 3.9], [5, 5.5]] |
| T204 | 252 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 500 OptimizationResult = PSO(ObjectiveFunction, ["b", "m", "nz", "l1", "l2", "d1", "d2"], Domain, SwarmPopulation, Iterat |
| F079 | 253 | figure | unverified | not claimed to match a printed figure or table | Figure 7.8 ‒ Diagram of the gear train |
| T205 | 254 | code-listing | unverified | not claimed to match a printed figure or table | def ObjectiveFunction(x): A, B, C, D = np.asarray(x, dtype=float) A = np.floor(A + 0.5) B = np.floor(B + 0.5) C = np.floor(C + 0.5) D = np.floor(D + 0.5) return |
| T206 | 254 | table-1col | unverified | not claimed to match a printed figure or table | Domain = [[12, 60], [12, 60], [12, 60], [12, 60]] |
| T207 | 254 | table-1col | unverified | not claimed to match a printed figure or table | SwarmPopulation = 25 IterationNumber = 100 OptimizationResult = PSO(ObjectiveFunction, ["A", "B", "C", "D"], Domain, SwarmPopulation, IterationNumber) |
| T208 | 270 | table-4col | unverified | not claimed to match a printed figure or table | № |
| T209 | 272 | table-1col | unverified | not claimed to match a printed figure or table | # LIBRARIES INSTALLATION %pip install tqdm joblib openpyxl ipywidgets %pip install numpy %pip install pandas %pip install matplotlib |
| T210 | 278 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | # BENCHMARKS AND DOMAINS import numpy as np def Ackley1Function(x): x = np.asarray(x, dtype=float) D = x.size return float(-20*np.exp(-0.2*np.sqrt(np.sum(x**2)/ |
| T211 | 292 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | # OPTIMIZERS import numpy as np from IPython.display import clear_output # PSO def PSO(function, Vars, DomainVarsList, SwarmPopulation, Iterations): n = len(Var |
| T212 | 297 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | # SETTINGS AND RUN - ALGORITHMS SEARCH PERFORMANCE import io, time, contextlib import numpy as np import pandas as pd # ---------- 0. Disable clear_output/print |
| T213 | 301 | code-listing | corrected-with-erratum | see `src/metaopt/` and `docs/errata.md` | # SETTINGS AND RUN - ALGORITHMS EXECUTION TIME import io, time, contextlib, os, pickle import numpy as np import pandas as pd # ---------- 0. Disable clear_outp |
| T214 | 304 | code-listing | unverified | not claimed to match a printed figure or table | # EXCEL EXPORT: average execution time import platform, datetime from openpyxl import Workbook from openpyxl.styles import Font, Alignment, Border, Side, Patter |
| T215 | 324 | table-16col | unverified | not claimed to match a printed figure or table | Benchmark |
| T216 | 325 | table-16col | unverified | not claimed to match a printed figure or table | Benchmark |
| T217 | 326 | table-16col | unverified | not claimed to match a printed figure or table | Benchmark |
| T218 | 327 | table-16col | unverified | not claimed to match a printed figure or table | Benchmark |
| T219 | 329 | code-listing | unverified | not claimed to match a printed figure or table | # LIBRARIES INSTALLATION import sys import numpy as np import matplotlib.pyplot as plt from matplotlib.patches import Patch from matplotlib.cbook import boxplot |
| T220 | 330 | code-listing | unverified | not claimed to match a printed figure or table | # SETTINGS # The plotting code works ONLY with the results of the efficiency experiment # (Section 5.1): the file raw_benchmark_results.npz (one number per run) |
| T221 | 331 | table-1col | unverified | not claimed to match a printed figure or table | # ALGORITHMS ORDER # Preferred order and colors for known algorithms (if present in the file). # Algorithms not in this list are picked up automatically and app |
| T222 | 332 | code-listing | not-applicable | no library object; explanation or non-Python content | # DATA data = np.load(DATA_PATH_RESOLVED) # Check that this is really the efficiency file: the keys must look like # "<problem>__<algorithm>", and every array m |
| T223 | 335 | code-listing | unverified | not claimed to match a printed figure or table | # PLOTS BUILD FUNCTIONS def build_boxplot(problem_idx: int, show: bool = False): problem_name = PROBLEM_INDEX_TO_NAME[problem_idx] safe_name = "".join(c if c.is |
| T224 | 335 | table-1col | unverified | not claimed to match a printed figure or table | # PLOTTING for p in problems: build_boxplot(p) |
| T225 | 335 | table-1col | unverified | not claimed to match a printed figure or table | # PLOTS SHOWING # Show the plot, with PREVIEW_INDEX set to the problem number you want to preview (1, 2, 3, ...). PREVIEW_INDEX = 1 build_boxplot(PREVIEW_INDEX, |
| T226 | 337 | table-15col | unverified | not claimed to match a printed figure or table | Algorithm |
| T227 | 347 | table-2col | unverified | not claimed to match a printed figure or table | Prerequisites for the Reader |

Rows: 324.
