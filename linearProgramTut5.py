import pandas as pd
import pulp

factories = pd.DataFrame.from_csv('factory_variables.csv', index_col=['Month', 'Factory'])
demand = pd.DataFrame.from_csv('monthly_demand.csv', index_col=['Month'])

production = pulp.LpVariable.dicts("production",
                                   ((month, factory) for month, factory in factories.index),
                                   lowBound=0,
                                   cat='Integer')

factory_status = pulp.LpVariable.dicts("factory_status",
                                       ((month, factory) for month, factory in factories.index),
                                       cat='Binary')

model = pulp.LpProblem("Cost minimising scheduling problem", pulp.LpMinimize)

model += pulp.lpSum(
    [production[month, factory] * factories.loc[(month, factory), 'Variable_Costs'] for month, factory in
     factories.index]
    + [factory_status[month, factory] * factories.loc[(month, factory), 'Fixed_Costs'] for month, factory in
       factories.index]
)

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

model.solve()
pulp.LpStatus[model.status]

output = []
for month, factory in production:
    var_output = {
        'Month': month,
        'Factory': factory,
        'Production': production[(month, factory)].varValue,
        'Factory Status': factory_status[(month, factory)].varValue
    }
    output.append(var_output)
output_df = pd.DataFrame.from_records(output).sort(['Month', 'Factory'])
output_df.set_index(['Month', 'Factory'], inplace=True)
print output_df

# Print our objective function value (Total Costs)
print pulp.value(model.objective)
