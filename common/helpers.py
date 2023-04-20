def get_last_translation(chain):
    print("In here", chain.steps)
    for step in reversed(chain.steps[:chain.current_step]):
        print("step: ", step)
        if step["type"] == "translate":
            return step["output"]