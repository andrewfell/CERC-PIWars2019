import mypkg

trig_pin_l = 15
echo_pin_l = 14
echo_pin_r = 23
trig_pin_r = 18
while True:
    print('#=========================================#')
    mypkg.get_pulse_time(trig_pin_r, echo_pin_r)
    mypkg.calc_dist_cm(trig_pin_r, echo_pin_r)
    print('#=========================================#')
    print('#-----------------------------------------#')
    mypkg.get_pulse_time(trig_pin_l, echo_pin_l)
    mypkg.calc_dist_cm(trig_pin_l, echo_pin_l)
    print('#-----------------------------------------#')

