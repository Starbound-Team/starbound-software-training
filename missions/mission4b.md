# Mission 4b

The drone made it to the sample site, but it took the scenic route to get there. Every tick drains its battery, and it will have to make this trip again and again *(alien plants don't sample themselves)*. Your team's `MAIN` clearly wasn't written with this terrain in mind.

The preloaded functions are burned into the drone's memory, so **you can't change them**, but **you can rewrite `MAIN`**. Your new `MAIN` can call the functions in **any order, as many times as you like**, but it can only call functions; it can't run `F`, `L` or `R` on its own. Everything else works as before: the drone starts on `S` facing east, an `F` into a tree is still skipped for free, and the drone stops the moment it reaches `E`.

In the example, the best you can do is:
```
MAIN: C A C A A
```
which takes the drone along this route:
```maze
start       C: tick 2   A: tick 5
#########   #########   #########
#>.#.#..#   #.v#.#..#   #..#.#..#
#....#.##   #....#.##   #..>.#.##
#.#.....#   #.#.....#   #.#.....#
#......E#   #......E#   #......E#
#########   #########   #########

C: tick 7   A: tick 11  A: tick 13
#########   #########   #########
#..#.#..#   #..#.#..#   #..#.#..#
#...v#.##   #....#.##   #....#.##
#.#.....#   #.#.....#   #.#.....#
#......E#   #....>.E#   #......>#
#########   #########   #########
```
The drone follows the same path as before, but turns right more cheaply. `B` turns right with three `L`s, while `C` uses a single `R`. Both run into the same trees after one square, and **`C`'s two extra `F`s are skipped for free**, so `C` takes `2` ticks where `B` took `4`. Swapping both of those `B`s for `C` saves `4` ticks, and the last `A` moves the drone two squares east onto `E`, just like `B` did. The drone reaches the sample site after **`13` ticks**. No other `MAIN` gets there faster.

***What is the fewest number of ticks your drone needs to reach the sample site?***
