# Mission 1a

As you gaze towards the console, something doesn't look quite right; *All of the drone logs are jumbled!* If they can't be fixed, the whole mission will be in vain. You try to decipher the logs, and you see a file full of `JSON` objects ***(your puzzle input)***. Maybe there is some way to filter them and reorder them again? Here is what one of them looks like:
```json
{
    "id": 32,
    "sig_value": 764324,
    "importance": "low",
    "link": {
        "up": "jwt",
        "down": "lap",
        "left": "ffm",
        "right": "van"
    },
    "valid": true,
    "category": [
        "entertainment",
        "elephants",
        "hall",
        "demotion"
    ]
}
```
We only care about certain logs for our purpose. Specifically, we care about logs that have an importance of ***medium or greater*** (they can have an importance of ***low, medium or high***), that are valid (so they contain ***"valid": true***), and that include either ***"drone"***, ***"status"*** or ***"temperature"***
Take for example, the logs below;
```json
[
    {
        "id": 432,
        "importance": "medium",
        "link": {
            "up": "das",
            "down": "eru",
            "left": "nme",
            "right": "ksa"
        },
        "sig_value": 26767,
        "valid": true,
        "category": [
            "drone",
            "thrusters"
        ]
    },
    {
        "id": 12,
        "importance": "low",
        "link": {
            "up": "dsa",
            "down": "bvc",
            "left": "dtg",
            "right": "wer"
        },
        "sig_value": 890,
        "valid": true,
        "category": [
            "status",
            "navigation"
        ]
    },
    {
        "id": 89,
        "importance": "low",
        "link": {
            "up": "xcv",
            "down": "fes",
            "left": "ndg",
            "right": "grq"
        },
        "sig_value": 212,
        "valid": false,
        "category": [
            "news",
            "federation"
        ]
    },
    {
        "id": 45,
        "importance": "high",
        "link": {
            "up": "rew",
            "down": "sss",
            "left": "vcx",
            "right": "aav"
        },
        "sig_value": 43244,
        "valid": true,
        "category": [
            "drone",
            "status"
        ]
    },
    {
        "id": 67,
        "importance": "high",
        "link": {
            "up": "eru",
            "down": "das",
            "left": "mcm",
            "right": "wqw"
        },
        "sig_value": 46290,
        "valid": true,
        "category": [
            "brewery"
        ]
    }
]
```
- The first log matches everything, so **we keep it**.
- The second has a low importance, so **we ignore it**.
- The third has a low importance, is marked with "valid": false and is not in a category we are interested in, so **we ignore it**.
- The fourth log matches everything, so **we keep it**.
- The fifth log is not in a category we are interested in, so **we ignore it**.

The engineers have predicted the drone misbehaving so they gave it a special *speculative tree log correction* system. For our logs, we need to give it a "correction base" number, and it will figure out the rest. This number is generated from the logs you have in the following way: *starting with the log with the **lowest** id and ending with the one with the **highest**, we multiply its **sig_value** by the **number of kept logs we have used so far** (including this one)*. Then we **add all of those together**.

In the example above, the correction base number is
```
43244 * 1 + 26767 * 2 = 96778
```
***What is the correction base number for the logs of your drone?***