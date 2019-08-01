import numpy as np
import pandas as pd
import os.path



#if os.path.exists('test.txt'):
#	q_table = pd.read_csv('test.txt', names=['switch', 'no_switch'])

state = str([1,1,1,1])
state_2 = str([2,2,2,2])

action_space=[0, 1]

q_table = pd.DataFrame(columns=action_space, dtype=np.float64)
new_row_1 = pd.Series([1,1], index=q_table.columns, name=state)
new_row_2 = pd.Series([1,1], index=q_table.columns, name=state_2)
#q_table = q_table.append(new_row_1)

print(q_table)
q_table = q_table.append(new_row_1)
q_table = q_table.append(new_row_2)
print(q_table)
#with open('test.txt', 'w') as f:
#	for row in q_table:
#		f.write(str(row))
for row in q_table:
	print(row)		
#f.close()
#print(q_table)



