import random
import graphviz

# Function to generate random decisions
def generate_random_decisions(num_decisions, num_outcomes):
    decisions = {}
    for i in range(num_decisions):
        decision_key = f'D{i+1}'
        outcomes = {}
        remaining_probability = 1.0
        for j in range(num_outcomes):
            outcome_key = f'{decision_key}O{j+1}'
            if j == num_outcomes - 1:
                probability = remaining_probability
            else:
                probability = round(random.uniform(0.1, remaining_probability), 2)
                remaining_probability -= probability
            gain_loss = random.randint(-100, 100)
            outcomes[outcome_key] = {'probability': probability, 'gain_loss': gain_loss}
        decisions[decision_key] = outcomes
    return decisions

# Generate random decisions
random.seed(42)
decisions = generate_random_decisions(3, 3)

# Calculate statistical expectations
def calculate_expectation(decision):
    return sum(outcome['probability'] * outcome['gain_loss'] for outcome in decision.values())

expectations = {key: calculate_expectation(value) for key, value in decisions.items()}

# Identify the decision with maximal gain
max_gain_decision = max(expectations, key=expectations.get)

# Calculate the expectations considering only losses
def calculate_loss_expectation(decision):
    return sum(outcome['probability'] * outcome['gain_loss'] for outcome in decision.values() if outcome['gain_loss'] < 0)

loss_expectations = {key: calculate_loss_expectation(value) for key, value in decisions.items()}

# Identify the decision with minimal loss (most positive value)
min_loss_decision = min(loss_expectations, key=loss_expectations.get)

print(f"Decision with maximal gain: {max_gain_decision} with expectation {expectations[max_gain_decision]}")
print(f"Decision with minimal loss: {min_loss_decision} with expectation {loss_expectations[min_loss_decision]}")

# Print all expectation values
print("\nAll Expectation Values (Gains):")
for decision, expectation in expectations.items():
    print(f"{decision}: {expectation}")

print("\nAll Expectation Values (Losses):")
for decision, expectation in loss_expectations.items():
    print(f"{decision}: {expectation}")

# Visualize the probability tree using Graphviz
def plot_tree(decisions, max_gain_decision, min_loss_decision):
    dot = graphviz.Digraph(comment='Probability Tree')
    
    root = 'Root'
    dot.node(root)
    
    for decision, outcomes in decisions.items():
        node_attr = {}
        # Highlight max gain in yellow
        if decision == max_gain_decision:
            node_attr = {'style': 'filled', 'fillcolor': 'yellow'}
        # Highlight minimal loss in red
        elif decision == min_loss_decision:
            node_attr = {'style': 'filled', 'fillcolor': 'red'}
        
        dot.node(decision, **node_attr)
        dot.edge(root, decision)
        for outcome, attributes in outcomes.items():
            dot.node(outcome, label=f'{outcome}\nP={attributes["probability"]}\nG/L={attributes["gain_loss"]}')
            dot.edge(decision, outcome)
    
    return dot

# Plot and visualize the tree with highlighted decisions
tree = plot_tree(decisions, max_gain_decision, min_loss_decision)
tree.render('probability_tree', format='png', cleanup=True)
tree.view()

"""
Decision with maximal gain: D2 with expectation -12.729999999999993
Decision with minimal loss: D1 with expectation -76.38

All Expectation Values (Gains):
D1: -76.38
D2: -12.729999999999993
D3: -73.57000000000001

All Expectation Values (Losses):
D1: -76.38
D2: -34.17999999999999
D3: -73.57000000000001
probability_tree.pdf
"""