#!/usr/bin/env python3
"""
Ensure PuLP is installed: pip install pulp
"""
import pulp

def main():
    # Create the LP problem: maximize production
    problem = pulp.LpProblem("Beverage_Production", pulp.LpMaximize)

    # Decision variables: number of units to produce
    lemonade = pulp.LpVariable('Lemonade', lowBound=0, cat='Integer')
    juice = pulp.LpVariable('FruitJuice', lowBound=0, cat='Integer')

    # Objective: maximize total production
    problem += lemonade + juice, "Total_Units"

    # Constraints
    # Resource availability
    # 1) Water: 2 units per lemonade, 1 per juice, total <= 100
    problem += 2 * lemonade + 1 * juice <= 100, "Water_Constraint"
    # 2) Sugar: 1 unit per lemonade, total <= 50
    problem += 1 * lemonade <= 50, "Sugar_Constraint"
    # 3) Lemon juice: 1 unit per lemonade, total <= 30
    problem += 1 * lemonade <= 30, "LemonJuice_Constraint"
    # 4) Fruit puree: 2 units per juice, total <= 40
    problem += 2 * juice <= 40, "Puree_Constraint"

    # Solve
    solver = pulp.PULP_CBC_CMD(msg=False)
    problem.solve(solver)

    # Output results
    print(f"Status: {pulp.LpStatus[problem.status]}")
    print(f"Produce Lemonade: {int(lemonade.value())}")
    print(f"Produce Fruit Juice: {int(juice.value())}")
    print(f"Maximum total units: {int(pulp.value(problem.objective))}")

if __name__ == '__main__':
    main()
