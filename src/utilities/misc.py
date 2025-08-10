def calculateState(logs):
    state = 0
    for log in logs:
        state += (log.get('state', 0))

    return state