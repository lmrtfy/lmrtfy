import numpy as np
import random
from lmrtfy.annotation import result, variable

# Random walk towards PMF

difficulty = variable(1, 'difficulty')
domain_expertise = variable(5, 'domain_expertise')
runway_months = variable(12, 'runway', unit='Months')  # Months
ship_every = variable(1, 'ship_every', unit='Days')
talking_to_customer = variable(5, 'talking_to_customer')


days_per_month = 30 


bad_luck = result(12 * random.random(), 'bad_luck', unit='Months')  # 12 Months of setbacks
max_time_to_pmf = result(difficulty * 3 * (2 - domain_expertise/5) + bad_luck, 'max_time_to_pmf', unit='Months')
print(bad_luck, max_time_to_pmf)


start = max_time_to_pmf * days_per_month * np.random.rand(2)
stop = max_time_to_pmf * days_per_month * np.random.rand(2)
points = list()
points.append(start)
hit_pmf = False
shots_on_goal = 0


for i in range(int(runway_months * days_per_month // ship_every)):
    shots_on_goal += 1
    customer_feedback = stop-points[-1]
    customer_feedback /= np.linalg.norm(customer_feedback)
    customer_feedback *= (talking_to_customer/5 * np.sqrt(ship_every))
    
    angle = 2*np.pi*random.random()
    direction = np.asarray((np.cos(angle),np.sin(angle)), dtype=np.float64)
    new_point = points[-1] + ship_every * direction + customer_feedback
    points.append(new_point)

    if np.linalg.norm(new_point-stop) < 10.:
        hit_pmf = True
        break


points = np.asarray(points, dtype=np.float64)

message = "PMF Reached"
if not hit_pmf:
    message = "End of Runway"


print(result(hit_pmf, 'pmf_hit'), 
      result(shots_on_goal, 'shots_on_goal'), 
      result(ship_every*shots_on_goal, 'time_elapsed', unit='Days'), 
      result(np.linalg.norm(start-stop), 'initial_time_distance_to_pmf', unit='Days'), 
      result(np.linalg.norm(stop-points[-1,:]), 'time_distance_to_pmf_in_the_end', unit='Days'),
      result(message, 'conclusion'))
