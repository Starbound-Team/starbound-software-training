# Mission 4a

With the drill safely on its way down, you turn to the second mission that needs your input. The drone has to fly to a *sample site* and collect some of the local plant life, so you decide to see how it navigates this foreign planet.

The drone has to fly low to analyze alien samples, and since it had limited resources, your team needed to be careful when programming it. They decided to preload a set of **functions** that chain some of its movements together, to save on space and power. However, after you scan the planet surface, you see the terrain is rough with *martian trees* tall enough to block your flight. You have the preloaded functions from the drone's manual, as well as the terrain you scanned ***(your puzzle input)***. Here is an example:
```maze
A: FFLF
B: FFLLL
C: FFFR
MAIN: B A

#########
#S.#.#..#
#....#.##
#.#.....#
#......E#
#########
```
The drone starts on `S`, **facing east** (right), and the sample site is at `E`. Every `#` is a tree, and every `.` is open ground. Each function is a string of instructions:

- `F` moves the drone **forward** one square, which takes `1` tick. If there is a tree in the way, the drone's *hyper-proximity sensors* spot it and the drone **skips the `F`**: it stays where it is, and *no tick is spent*.
- `L` and `R` turn the drone **90°** to the left or right, without moving. Each turn takes `1` tick.

Inspecting the drone's program, you find `MAIN`, the function that calls all the others, in the order they are listed. **When `MAIN` runs out of functions to call, it starts over from the first one**, looping until the drone gets where it needs to go. The same sensors spot the sample site, so **the moment the drone reaches `E` it stops**, even in the middle of a function.

In the example, the drone (drawn as an arrow pointing the way it faces) is at the following positions after each call:
```maze
start       B: tick 4   A: tick 7
#########   #########   #########
#>.#.#..#   #.v#.#..#   #..#.#..#
#....#.##   #....#.##   #..>.#.##
#.#.....#   #.#.....#   #.#.....#
#......E#   #......E#   #......E#
#########   #########   #########

B: tick 11  A: tick 15  B: tick 17
#########   #########   #########
#..#.#..#   #..#.#..#   #..#.#..#
#...v#.##   #....#.##   #....#.##
#.#.....#   #.#.....#   #.#.....#
#......E#   #....>.E#   #......>#
#########   #########   #########
```
- **Call 1** (`B`, ticks `1` to `4`): the drone moves one square east. There is a tree in front of it, so **the second `F` is skipped** for free, and three left turns leave it facing south.
- **Call 2** (`A`, ticks `5` to `7`): one square south, then another tree, so the second `F` is skipped. The drone turns left to face east and moves one square east. `MAIN` has run out, but the drone hasn't reached `E` yet, **so `MAIN` starts over**.
- **Call 3** (`B`, ticks `8` to `11`): one square east, a skipped `F` into the next tree, and three left turns to face south.
- **Call 4** (`A`, ticks `12` to `15`): this time the way south is clear, so the drone moves two squares south, turns left to face east, and moves one square east.
- **Call 5** (`B`, ticks `16` and `17`): two squares east, the second one onto `E`. The drone stops right there, so the three `L`s at the end of `B` **never run**.

The drone reaches the sample site after **`17` ticks**. ***How many ticks does it take your drone to reach the sample site?***
