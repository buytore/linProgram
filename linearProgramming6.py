import pandas as pd
import pulp

factories = pd.DataFrame.from_csv('factory_variables.csv', index_col=['Month', 'Factory'])
print factories

demand = pd.DataFrame.from_csv('monthly_demand.csv', index_col=['Month'])
print demand

# Production
production = pulp.LpVariable.dicts("production",
                                     ((month, factory) for month, factory in factories.index),
                                     lowBound=0,
                                     cat='Integer')

# Factory Status, On or Off
factory_status = pulp.LpVariable.dicts("factory_status",
                                     ((month, factory) for month, factory in factories.index),
                                     cat='Binary')

# Factory switch on or off
switch_on = pulp.LpVariable.dicts("switch_on",
                                    ((month, factory) for month, factory in factories.index),
                                    cat='Binary')

# Instantiate the model
model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)

# Select index on factory A or B
factory_A_index = [tpl for tpl in factories.index if tpl[1] == 'A']
factory_B_index = [tpl for tpl in factories.index if tpl[1] == 'B']

# Define objective function
model += pulp.lpSum(
    [production[m, f] * factories.loc[(m, f), 'Variable_Costs'] for m, f in factories.index]
    + [factory_status[m, f] * factories.loc[(m, f), 'Fixed_Costs'] for m, f in factories.index]
    + [switch_on[m, f] * 20000 for m, f in factory_A_index]
    + [switch_on[m, f] * 400000 for m, f in factory_B_index])

# Production in any month must be equal to demand
months = demand.index
for month in months:
    model += production[(month, 'A')] + production[(month, 'B')] == demand.loc[month, 'Demand']

# Production in any month must be between minimum and maximum capacity, or zero.
for month, factory in factories.index:
    min_production = factories.loc[(month, factory), 'Min_Capacity']
    max_production = factories.loc[(month, factory), 'Max_Capacity']
    model += production[(month, factory)] >= min_production * factory_status[month, factory]
    model += production[(month, factory)] <= max_production * factory_status[month, factory]

# Factory B is off in May
model += factory_status[5, 'B'] == 0
model += production[5, 'B'] == 0

for month, factory in factories.index:
    # In month 1, if the factory ison, we assume it turned on
    if month == 1:
        model += switch_on[month, factory] == factory_status[month, factory]

    # In other months, if the factory is on in the current month AND off in the previous month, switch on = 1
    else:
        model += switch_on[month, factory] >= factory_status[month, factory] - factory_status[ month -1, factory]
        model += switch_on[month, factory] <= 1 - factory_status[ month -1, factory]
        model += switch_on[month, factory] <= factory_status[month, factory]

model.solve()
print pulp.LpStatus[model.status]

output = []
for month, factory in production:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[(month, factory)].varValue,
        'Factory Status': factory_status[(month, factory)].varValue,
        'Switch On': switch_on[(month, factory)].varValue
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output).sort_values(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)
print output_df