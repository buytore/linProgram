import pulp

model = pulp.LpProblem("Diet Minimize problem", pulp.LpMinimize)

empName = {}
empAllHours = {}
# employee name A, B & C and their respective historical hours
employees = {'A': [0,0,6,7,3],
             'B': [0,4,7,0,5],
             'C': [4,0,0,2,7]}

tasks = [6, 0, 7, 4, 8]

for employee, historicalHours in employees.items():
    empName[employee] = pulp.LpVariable('X_' + employee, lowBound=0, cat='Integer')
    empAllHours[employee] = historicalHours + tasks

model += empName['A'] + empName['B'] + empName['C']

# constraint
for employee, hours in empAllHours.items():
    for workTime in hours:
        model += empAllHours[employee] <= 30
        ## SUM HOURS IN LIST USING INDEX VALUE and STEP ALONG THE LIST


# New Hours
X1 = pulp.LpVariable('X1', lowBound=0, cat='Integer')
X2 = pulp.LpVariable('X2', lowBound=0, cat='Integer')
X3 = pulp.LpVariable('X3', lowBound=0, cat='Integer')
X4 = pulp.LpVariable('X4', lowBound=0, cat='Integer')
X5 = pulp.LpVariable('X5', lowBound=0, cat='Integer')

# Historical Hours
Y1 = pulp.LpVariable('Y1', cat='Binary')
Y2 = pulp.LpVariable('Y2', cat='Binary')
Y3 = pulp.LpVariable('Y3', cat='Binary')
Y4 = pulp.LpVariable('Y4', cat='Binary')
Y5 = pulp.LpVariable('Y5', cat='Binary')

# Optimization
model += 20 * X1 + 20 * X2 + 20 * X3 + 20 * X4 + 20 * X5, "Cost"


# Constraints
model += X1 + X2 + X3 + X4 + X5 <= 30
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