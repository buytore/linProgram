import pulp

# Instantiate our problem class
# answer to this is:
# Food | #1 | #2 | Cost
#  1   | 2  | 0  | 20
#  2   | 0  | 1  | 10
#  3   | 3  | 2  | 31
#  4   | 1  | 2  | 11
#  5   | 2  | 1  | 12
model = pulp.LpProblem("Diet Minimize problem", pulp.LpMinimize)

X1 = pulp.LpVariable('X1', lowBound=0, cat='Integer')
X2 = pulp.LpVariable('X2', lowBound=0, cat='Integer')
X3 = pulp.LpVariable('X3', lowBound=0, cat='Integer')
X4 = pulp.LpVariable('X4', lowBound=0, cat='Integer')
X5 = pulp.LpVariable('X5', lowBound=0, cat='Integer')

Y1 = pulp.LpVariable('Y1', cat='Binary')
Y2 = pulp.LpVariable('Y2', cat='Binary')
Y3 = pulp.LpVariable('Y3', cat='Binary')
Y4 = pulp.LpVariable('Y4', cat='Binary')
Y5 = pulp.LpVariable('Y5', cat='Binary')

# Objective function
#model += 30000 * A + 45000 * B, "Profit"
model += 20 * X1 + 10 * X2 + 31 * X3 + 11 * X4 + 12 * X5, "Cost"

# Constraints
model += 2 * X1 + 0 * X2 + 3 * X3 + 1 * X4 + 2 * X5 >= 21
model += 0 * X1 + 1 * X2 + 2 * X3 + 2 * X4 + 1 * X5 >= 12
model += X1 >= 2 * Y1
model += X2 >= 2 * Y2
model += X3 >= 2 * Y3
model += X4 >= 2 * Y4
model += X5 >= 2 * Y5
model += Y1 + Y2 + Y3 + Y4 + Y5 >= 3

# Solve our problem
model.solve()
pulp.LpStatus[model.status]

# Print our decision variable values
print "Food X1 = {}".format(X1.varValue)
print "Food X2 = {}".format(X2.varValue)
print "Food X3 = {}".format(X3.varValue)
print "Food X4 = {}".format(X4.varValue)
print "Food X5 = {}".format(X5.varValue)

# Print our objective function value
print pulp.value(model.objective)