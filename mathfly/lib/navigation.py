from dragonfly import Key

def text_nav(modifier, direction, n50, extreme):
    k = ""
    if extreme:
        if direction in ["left", "up"]:
            k = k + "home"
        else:
            k = k + "end"
        if direction in ["up", "down"]:
            k = "c-" + k
    else:
        k = str(direction) + ":" + str(n50)
    if modifier:
        k = str(modifier) + k.replace("c-", "")
    Key(k).execute()