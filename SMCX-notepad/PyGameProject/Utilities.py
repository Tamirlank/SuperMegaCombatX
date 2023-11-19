def clamp_number(num, a, b):
    if num < a:
        num = a
    elif num > b:
        num = b
    return num

def clamp_number_loop(num, a, b):
    if num > b:
        num = a
    elif num < a:
        num = b
    return num