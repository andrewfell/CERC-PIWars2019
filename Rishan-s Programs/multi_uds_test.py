import mypkg

trig_pin_l = 15
echo_pin_l = 14
echo_pin_m = 17
trig_pin_m = 4
trig_pin_r = 18
echo_pin_r = 23

for i in range(4):
    r = mypkg.calc_dist_cm(trig_pin_r, echo_pin_r)
    l = mypkg.calc_dist_cm(trig_pin_l, echo_pin_l)
    m = mypkg.calc_dist_cm(trig_pin_m, echo_pin_m)
    print('#-----------------------------------------#')
    print(' l= ',l," m = ",m," r = ",r)
    print('#-----------------------------------------#')

