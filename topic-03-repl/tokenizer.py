# tokenizer

"""
break character stream into tokens, provide a list of tokens

    tokens = tokenize(string_of_code)
"""

import re

patterns = [
    ["\(", "("],
    ["\)", ")"],
    ["\*", "*"],
    ["\/", "/"],
    ["\+", "+"],
    ["\-", "-"],
    ["print", "print"],
    ["\!", "!"],
    ["\%", "%"],
    ["(\d*\.\d+)|(\d+\.\d*)|(\d+)", "number"],
    ["[A-Za-z_][A-Za-z0-9_]*","identifier"],
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])


def tokenize(characters):
    tokens = []
    position = 0
    while position < len(characters):
        for pattern, tag in patterns:
            match = pattern.match(characters, position)
            if match:
                break
        assert match
        # update position for next match
        token = {
            "tag": tag,
            "value": match.group(0),
            "position": position,
        }
        position = match.end()
        tokens.append(token)
    for token in tokens:
        if token["tag"] == "number":
            if "." in token["value"]:
                token["value"] = float(token["value"])
            else:
                token["value"] = int(token["value"])
    token = {
        "tag": "end",
        "value": "",
        "position": position,
    }
    tokens.append(token)
    return tokens


def test_simple_tokens():
    print("testing simple tokens")
    assert tokenize("") == [{"tag": "end", "value": "", "position": 0}]
    assert tokenize("*")[0]["tag"] == "*"
    tokens = tokenize("*+")
    assert tokens == [
        {"tag": "*", "value": "*", "position": 0},
        {"tag": "+", "value": "+", "position": 1},
        {"tag": "end", "value": "", "position": 2},
    ]
    tokens = tokenize("*/+-()print!%")                                               # testing ! and % token
    assert tokens == [
        {"tag": "*", "value": "*", "position": 0},
        {"tag": "/", "value": "/", "position": 1},
        {"tag": "+", "value": "+", "position": 2},
        {"tag": "-", "value": "-", "position": 3},
        {"tag": "(", "value": "(", "position": 4},
        {"tag": ")", "value": ")", "position": 5},
        {"tag": "print", "value": "print", "position": 6},
        {"tag": "!", "value": "!", "position": 11},
        {"tag": "%", "value": "%", "position": 12},
        {"tag": "end", "value": "", "position": 13},
    ]
    tokens = tokenize("123")
    assert tokens == [
        {"tag": "number", "value": 123, "position": 0},
        {"tag": "end", "value": "", "position": 3},
    ]
    tokens = tokenize("123.45")
    assert tokens == [
        {"tag": "number", "value": 123.45, "position": 0},
        {"tag": "end", "value": "", "position": 6},
    ]
    tokens = tokenize("123.")
    assert tokens == [
        {"tag": "number", "value": 123.0, "position": 0},
        {"tag": "end", "value": "", "position": 4},
    ]
    tokens = tokenize(".25")
    assert tokens == [
        {"tag": "number", "value": 0.25, "position": 0},
        {"tag": "end", "value": "", "position": 3},
    ]

def test_identifier():
    tokens = tokenize("x")
    assert tokens == [
        {"tag": "identifier", "value": "x", "position": 0},
        {"tag": "end", "value": "", "position": 1},
    ]
    tokens = tokenize("xyz")
    assert tokens == [
        {"tag": "identifier", "value": "xyz", "position": 0},
        {"tag": "end", "value": "", "position": 3},
    ]    
    tokens = tokenize("xyz_0")
    assert tokens == [
        {"tag": "identifier", "value": "xyz_0", "position": 0},
        {"tag": "end", "value": "", "position": 5},
    ]
    tokens = tokenize("xyz_0+++")
    assert tokens[0] == {"tag": "identifier", "value": "xyz_0", "position": 0}

def test_tokenize_expression():
    print("testing tokenize expression")
    tokens = tokenize("(3.5+40)/5-(3.*.4)")
    assert tokens == [
        {"tag": "(", "value": "(", "position": 0},
        {"tag": "number", "value": 3.5, "position": 1},
        {"tag": "+", "value": "+", "position": 4},
        {"tag": "number", "value": 40, "position": 5},
        {"tag": ")", "value": ")", "position": 7},
        {"tag": "/", "value": "/", "position": 8},
        {"tag": "number", "value": 5, "position": 9},
        {"tag": "-", "value": "-", "position": 10},
        {"tag": "(", "value": "(", "position": 11},
        {"tag": "number", "value": 3.0, "position": 12},
        {"tag": "*", "value": "*", "position": 14},
        {"tag": "number", "value": 0.4, "position": 15},
        {"tag": ")", "value": ")", "position": 17},
        {"tag": "end", "value": "", "position": 18},
    ]
    tokens = tokenize("-(-3.5+40)/5-(3.*.4)")
    assert tokens == [
        {"tag": "-", "value": "-", "position": 0},
        {"tag": "(", "value": "(", "position": 1},
        {"tag": "-", "value": "-", "position": 2},
        {"tag": "number", "value": 3.5, "position": 3},
        {"tag": "+", "value": "+", "position": 6},
        {"tag": "number", "value": 40, "position": 7},
        {"tag": ")", "value": ")", "position": 9},
        {"tag": "/", "value": "/", "position": 10},
        {"tag": "number", "value": 5, "position": 11},
        {"tag": "-", "value": "-", "position": 12},
        {"tag": "(", "value": "(", "position": 13},
        {"tag": "number", "value": 3.0, "position": 14},
        {"tag": "*", "value": "*", "position": 16},
        {"tag": "number", "value": 0.4, "position": 17},
        {"tag": ")", "value": ")", "position": 19},
        {"tag": "end", "value": "", "position": 20},
    ]


if __name__ == "__main__":
    test_simple_tokens()
    test_identifier()
    test_tokenize_expression()
    print("done.")
