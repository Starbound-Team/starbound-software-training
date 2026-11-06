# Mission 3a

As you slowly drift through the outer edge of the planet, relieved that the drone is finally working as intended, you decide to start looking at the missions the drone is assigned to complete *(it is a research project after all)*. Two of the missions however involve your input, in order to be completed optimally.

The first involves taking a peek under the surface of the foreign planet. Your drone is equipped with a *hyper-length drill* to dig through the surface, and *hyper-sonar sensors*, to allow for mapping the planet below the surface area (the drone's *hyper-frequency resonators* have been going crazy ever since you arrived, so you are sure it is worth studying). Your drone has generated one such map already ***(your puzzle input)***. Here is an example of what a map could look like:
```map
.AB...b..a
..a.A..B7b
b....7BA.a
.aBb..A.7.
...B..Aa.7
.a..7.b.AB
AB...b..7.
.7..B..a.b
7aAB.b....
...B.7..b.
A.b...B7..
A.B7a.b...
```
Inspecting closer, you realize that the artifacts the map has generated are thankfully not glitches. They are however *space-defining wormholes!* If your drill digs through a wormhole, it will **teleport to every matching wormhole on the layers above**. This means that **if there is more than one matching wormhole above the one we entered, the drill will exit through all of them simultaneously**. Take the below map as an example:
```map
....a..
..ab..A
a......
.......
```
If we start digging on the **first column**:
On dig `1`, the map will look as such:
```map
⌄...a..
..ab..A
a......
.......
```
On dig `2`:
```map
|...a..
⌄.ab..A
a......
.......
```
On dig `3`:
```map
|...⌄..
|.⌄b..A
a......
.......
```
If we continue digging, we can see that the drill will reach the end by dig `5`:
```map
|...|..
|.|b|.A
a.|.⌄..
..⌄....
```
If we instead entered through column `3`, the final map would look as such:
```map
..|.|..
..ab|.A
a...|..
....⌄..
```
so we would need `5` digs to reach the end. If we entered through column `5`, the wormhole would have nowhere to send the drill so it passes straight through it, reaching the end in only `4` digs:
```map
....|..
..ab|.A
a...|..
....⌄..
```
We are looking to find on **which column the drone should start digging to minimize the number of times we need to dig** in order to reach the layer of interest, so the drone can conserve as much energy as possible. If we see the first example again:
```map
.AB...b..a
..a.A..B7b
b....7BA.a
.aBb..A.7.
...B..Aa.7
.a..7.b.AB
AB...b..7.
.7..B..a.b
7aAB.b....
...B.7..b.
A.b...B7..
A.B7a.b...
```
The best start is **column 9**. It reaches the bottom in **16 digs**, and its route goes through 4 wormholes. Note that it digs straight through the `7` in layer 2, because there is no `7` above it.

The drone needs to understand how much energy to prepare to reach the target layer, along with knowing the column it needs to go to. Thankfully, all we have to give it is the **muplex**, which is **the multiplication result of the column and the amount of digs we needed to reach the bottom**. In the above example the muplex is **`9*16=144`**. If two columns could reach the end with the smallest amount of digging, **we would pick the one with the smallest muplex available**. The drone's *hyper-frequency resonators* seem to report that we only have to dig up to **layer 40** to collect the most interesting data. ***What is the muplex we need to give the drone, if we want to dig up to the 40th layer?*** 

*Note, if the drill gets teleported by a wormhole on the target layer (here 40), it still hasn't reached it; the drill has to rest on the target layer at the end.*