class FixedSwitch:
    def getAction(self, state):
        if state.steps >= 10:
            state.steps = 1
            return 0b11  # switch both
        else:
            return 0b00  # switch neither

    def learn(self, reward, newstate):
        # Fixed policy doesn't learn
        pass

    def saveResult(self):
        pass
