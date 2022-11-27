import json

with open('states.json') as f:
    state_data = json.load(f)
print('Original JSON Keys: ', [state.keys() for state in state_data['states']][0])
for state in state_data['states']:
    del state['area_codes']
print('\nModified JSON Keys: ', [state.keys() for state in state_data['states']][0])
with open('new_statefile.json', 'w') as f:
    json.dump(state_data, f, indent=2)
with open('new_statefile.json') as f:
    state_data = json.load(f)
print('\nReloaded JSON keys: ', [state.keys() for state in state_data['states']][0])