rishan = "apple"
def home():
    global rishan
    rishan = "orange"
    print("home Rishan = ",rishan)
    

def school():
    rishan = "banana"
    print("school Rishan = ",rishan)

def cerc():
    global rishan
    print("cerc rishan = ",rishan)

home()
school()
cerc()
