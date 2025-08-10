def calculateState(logs):
    state = 0
    for log in logs:
        state += (log.get('state', 0))

    return state

def hasItems(list: list):
    return bool(not (len(list) == 0))