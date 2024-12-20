import graphviz

# Define static values for gain example
gain_decisions = {
    'D1': {
        'D1O1': {'probability': 0.4, 'gain_loss': 50},
        'D1O2': {'probability': 0.6, 'gain_loss': 70}
    },
    'D2': {
        'D2O1': {'probability': 0.3, 'gain_loss': 40},
        'D2O2': {'probability': 0.7, 'gain_loss': 30}
    },
    'D3': {
        'D3O1': {'probability': 0.5, 'gain_loss': 60},
        'D3O2': {'probability': 0.5, 'gain_loss': 80}
    }
}

# Define static values for loss example
loss_decisions = {
    'D1': {
        'D1O1': {'probability': 0.4, 'gain_loss': -50},
        'D1O2': {'probability': 0.6, 'gain_loss': -70}
    },
    'D2': {
        'D2O1': {'probability': 0.3, 'gain_loss': -40},
        'D2O2': {'probability': 0.7, 'gain_loss': -30}
    },
    'D3': {
        'D3O1': {'probability': 0.5, 'gain_loss': -60},
        'D3O2': {'probability': 0.5, 'gain_loss': -80}
    }
}

# Calculate statistical expectations
def calculate_expectation(decision):
    return sum(outcome['probability'] * outcome['gain_loss'] for outcome in decision.values())

gain_expectations = {key: calculate_expectation(value) for key, value in gain_decisions.items()}
loss_expectations = {key: calculate_expectation(value) for key, value in loss_decisions.items()}

# Identify the decision with maximal gain
max_gain_decision = max(gain_expectations, key=gain_expectations.get)

# Identify the decision with minimal loss (most positive value)
min_loss_decision = max(loss_expectations, key=loss_expectations.get)

print(f"Decision with maximal gain: {max_gain_decision} with expectation {gain_expectations[max_gain_decision]}")
print(f"Decision with minimal loss: {min_loss_decision} with expectation {loss_expectations[min_loss_decision]}")

# Print all expectation values
print("\nAll Expectation Values (Gains):")
for decision, expectation in gain_expectations.items():
    print(f"{decision}: {expectation}")

print("\nAll Expectation Values (Losses):")
for decision, expectation in loss_expectations.items():
    print(f"{decision}: {expectation}")

# Visualize the probability tree using Graphviz
def plot_tree(decisions, optimal_decision, title):
    dot = graphviz.Digraph(comment=title)
    
    root = 'Root'
    dot.node(root)
    
    for decision, outcomes in decisions.items():
        node_attr = {'style': 'filled', 'fillcolor': 'yellow'} if decision == optimal_decision else {}
        dot.node(decision, **node_attr)
        dot.edge(root, decision)
        for outcome, attributes in outcomes.items():
            dot.node(outcome, label=f'{outcome}\nP={attributes["probability"]}\nG/L={attributes["gain_loss"]}')
            dot.edge(decision, outcome)
    
    return dot

# Plot and visualize the gain tree
gain_tree = plot_tree(gain_decisions, max_gain_decision, 'Gain Probability Tree')
gain_tree.render('gain_probability_tree', format='png', cleanup=True)
gain_tree.view()

# Plot and visualize the loss tree
loss_tree = plot_tree(loss_decisions, min_loss_decision, 'Loss Probability Tree')
loss_tree.render('loss_probability_tree', format='png', cleanup=True)
loss_tree.view()

"""
Decision with maximal gain: D3 with expectation 70.0
Decision with minimal loss: D2 with expectation -33.0

All Expectation Values (Gains):
D1: 62.0
D2: 33.0
D3: 70.0

All Expectation Values (Losses):
D1: -62.0
D2: -33.0
D3: -70.0
loss_probability_tree.pdf
"""