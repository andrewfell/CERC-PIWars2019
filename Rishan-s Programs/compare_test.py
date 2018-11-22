import random
def big(a,b,c):
    if c >= b and c >= a:
        biggest_val = c
        biggest = "c"
    if b >= a and b >= c:
        biggest_val = b
        biggest = "b"
    if a >= b and a >= c:
        biggest_val = a
        biggest = "a"
    if a == b and a == c:
        biggest_val = c
        biggest = "c"
    return biggest

while True:
    a = random.randint(0,10)
    b = random.randint(0,10)
    c = random.randint(0,10)
    print('a:',a,' b:',b,'c:',c)
    value = big(a,b,c)
    print(value)