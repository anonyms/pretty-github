# patterns.py

patterns = {
    "smiley": [
        "       ",  
        "  1 1  ",  
        "       ",  
        "   1   ",  
        " 1   1 ",  
        "  111  ",  
        "       "
    ],
    "heart": [
        " 1   1 ",  
        "111 111",  
        "1111111",  
        " 11111 ",  
        "  111  ",  
        "   1   ",  
        "       "
    ],
    "rocket": [
        "   1   ",  
        "  111  ",  
        "  1 1  ",  
        "  1 1  ",  
        "  111  ",  
        "   1   ",  
        "   1   "
    ],
    "lol_face": [
        " 1   1 ",  
        "       ",  
        "  111  ",  
        "       ",  
        " 1   1 ",  
        " 1 1 1 ",  
        "       "
    ]
}

def get_pattern(name):
    return patterns.get(name, None)