# Mission 1b

After pasting the number, you see the drone logs, and *they are still jumbled!* However, you remember that to serve the drone's *2D memory (**tm**)*, the log order no longer depends on their ids. Instead, the drone actually stores the logs ***as if they were objects on a 2D space***, in a **square grid**. *Their position on that grid is determined by the "link" element of the json object.* For example, look at the simplified logs below.
```json
[
    {
        "link": {
            "up": "aaa",
            "down": "bbb",
            "left": "ccc",
            "right": "ddd"
        }
    },
    {
        "link": {
            "up": "eee",
            "down": "fff",
            "left": "ddd",
            "right": "ggg"
        }
    }
]
```
If we were to place those logs on a grid, the second log would be to the **right** of the first one, since the first log's `right` link and the second log's `left` link are the same (`ddd`).

Here is another example:
```json
{
    "link": {
        "down": "das",
        "right": "ewq"
    }
}
```
We can tell that this log is in the **top-left corner** of the grid, since it doesn't link to a log above it or to its left.

The way we calculate the correction base number also changes. Instead of going from the lowest id to the highest, ***we start from the log in the top-left corner of the grid and end with the one in the bottom-right corner, reading a whole row from left to right before moving down to the next one***. Here are four logs that can be placed in a 2x2 grid:
```json
[
    {
        "link": {
            "down": "uuu",
            "right": "lll"
        },
        "sig_value": 7832
    },
    {
        "link": {
            "up": "uuu",
            "right": "rrr"
        },
        "sig_value": 243423
    },
    {
        "link": {
            "up": "ddd",
            "left": "rrr"
        },
        "sig_value": 545
    },
    {
        "link": {
            "down": "ddd",
            "left": "lll"
        },
        "sig_value": 1233
    }
]
```
The correction base number for these is
```
7832 * 1 + 1233 * 2 + 243423 * 3 + 545 * 4 = 742747
```
Under the new system, the drone needs the ***full log history*** (so even logs we previously ignored should be included). ***What is the correction base number for the logs of your drone with the new ordering?***
