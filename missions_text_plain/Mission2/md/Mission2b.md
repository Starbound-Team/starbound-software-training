# Mission 2b

Now that you know how far off your camera's calibration is, you can use the drone's *hyper-photon calibrator* to have it calibrate itself. You still need to tell it how to calibrate each lens, however.

The calibrator is supposed to work by **either heating a lens or cooling it, by `1` at a time**. Testing it on the drone, however, shows that it's a bit imprecise: instead of changing the heat of only the lens you aim it at, **it also changes the heat of its immediate neighbours**. So if you heat up the second lens, the first and the third heat up too. Note that *the first lens neighbours the last*, because the lenses form a ring. Also, **the calibrator can still cause the temperatures to loop.** Each heat or cool you aim at a lens counts as one use, even though it changes three lenses.

Since every photon and every calibration just adds to a lens's state, *the order doesn't matter*: calibrating the camera before the test photo or after it gives the same result. So you can simply start from the lenses' final state and bring them all back to `0`.

Here is the first example from mission 2a. After its last frame, the lenses are:
```
2  1  3 -1  0 -2
```
Heating *lens `1`* also heats *lenses `6` and `2`*. Many calibrations make every lens neutral. For example, heating *lens `1`* twice, cooling *lens `2`* three times, heating *lens `5`* once and cooling *lens `6`* once works, and uses the calibrator **7 times**. This one is cheaper:
```
lens           1  2  3  4  5  6
start          2  1  3 -1  0 -2
2 heats at 1  +2 +2  .  .  . +2
3 heats at 2  +3 +3 +3  .  .  .
1 heat at 3    . +1 +1 +1  .  .
end            0  0  0  0  0  0
```
*Lenses `1` to `3`* are heated 7 times each, which loops them all the way round back to `0`. *Lens `6`* only gets warmed through *lens `1`*, its neighbour across the ring. That's **6 uses** of the calibrator, and no calibration uses fewer, so the answer for this example is **6**.

Here is the second example from mission 2a. After its last frame, the lenses are:
```
-2 -3  3  3  3  0  2  3  0
```
With 9 lenses, heating *lens `1`* changes *lenses `9`, `1` and `2`*, and heating *lens `9`* changes *lenses `8`, `9` and `1`*. One calibration that works is 3 heats at *lens `3`*, 1 heat at *lens `4`*, 3 heats at *lens `6`*, 3 cools at *lens `7`*, 2 cools at *lens `8`* and 2 heats at *lens `9`*, which uses the calibrator **14 times**. This one is cheaper:
```
lens           1  2  3  4  5  6  7  8  9
start         -2 -3  3  3  3  0  2  3  0
3 heats at 1  +3 +3  .  .  .  .  .  . +3
3 cools at 4   .  . -3 -3 -3  .  .  .  .
2 cools at 8   .  .  .  .  .  . -2 -2 -2
1 cool at 9   -1  .  .  .  .  .  . -1 -1
end            0  0  0  0  0  0  0  0  0
```
The very hot *lenses `3` to `5`* are cooled straight back to `0`. *Lenses `1` and `9`* both rely on the ring: *lens `1`* ends at `−2 + 3 − 1 = 0`, and *lens `9`* at `0 + 3 − 2 − 1 = 0`. That's **9 uses** of the calibrator, and no calibration uses fewer, so the answer for this example is **9**.

***What is the smallest number of calibrator uses that calibrates your camera?***
