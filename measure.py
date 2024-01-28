import egalitarion_bnb
import time
import random
import matplotlib.pyplot as plt

item_counts = []
measurments = []

for item_count in range(10, 20):
    start = time.time()
    player_one = [random.randrange(10) for _ in range(item_count)]
    player_two = [random.randrange(10) for _ in range(item_count)]
    egalitarion_bnb.egalitarion_allocation([player_one, player_two])
    end = time.time()
    measurment = end - start
    measurments.append(measurment)
    item_counts.append(item_count)
    print(item_count)
plt.plot(item_counts, measurments)
plt.show()
# print(measurments)
# print(item_counts)

