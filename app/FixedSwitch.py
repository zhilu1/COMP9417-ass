class FixedSwitch:
    def __init__(self):
        self.steps = 1

    def getAction(self):
        if self.steps >= 10:
            self.steps = 1
            return 0b11  # switch both
        else:
            self.steps += 1
            return 0b00  # switch neither

    def learn(self, reward, newstate):
        # Fixed policy doesn't learn
        pass

    def saveResult(self):
        pass
