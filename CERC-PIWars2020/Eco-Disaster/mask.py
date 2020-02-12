import numpy as np

lower_black = [330/2, (50*2.55), (50*2.55)]
upper_black = [360/2, (100*2.55), (100*2.55)]
lower_black2 = [0/2, (10*2.55), (10*2.55)]
upper_black2 = [20/2, (30*2.55), (70*2.55)]

#Red:
lower_red1 = [325/2, (55*2.55), (50*2.55)]
upper_red1 = [365/2, (100*2.55), (100*2.55)]

lower_red2 = [0/2, (55*2.55), (50*2.55)]
upper_red2 = [10/2, (80*2.55), (80*2.55)]
#Blue:
lower_blue = [61/2, (0*2.55), (60*2.55)]
upper_blue = [190/2, (50*2.55), (100*2.55)]
#Green:
lower_green = [80/2, (40*2.55), (40*2.55)]
upper_green = [120/2, (80*2.55), (90*2.55)]
#Yellow:
lower_yellow = [40/2, (60*2.55), (60*2.55)]
upper_yellow = [55/2, (100*2.55), (100*2.55)]

# create NumPy arrays from the boundaries
lower_red1 = np.array(lower_red1, dtype = "uint8")
upper_red1 = np.array(upper_red1, dtype = "uint8")
lower_red2 = np.array(lower_red2, dtype = "uint8")
upper_red2 = np.array(upper_red2, dtype = "uint8")
lower_green = np.array(lower_green, dtype = "uint8")
upper_green = np.array(upper_green, dtype = "uint8")
lower_blue = np.array(lower_blue, dtype = "uint8")
upper_blue = np.array(upper_blue, dtype = "uint8")
lower_yellow = np.array(lower_yellow, dtype = "uint8")
upper_yellow = np.array(upper_yellow, dtype = "uint8")
