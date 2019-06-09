from random import random
from datetime import date
from datetime import datetime

x = random()
y = random() * 10
today = date.today()
time = datetime.now().time()
t_v = str(time)
unique_value = float(t_v.replace(':', '')) * random()
print(f'Random value from 0 to 1: {x}')
print(f'Random value from 0 to 10: {y}')
print(f"Today's Date: {today}, Current Time: {time}, Unique Value: {unique_value:.2f} ")