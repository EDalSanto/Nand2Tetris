class LabelCounter():
    def __init__(self, labels):
        self.labels = labels
        self.counts = {}
        self._initialize_counts()

    def increment(self, label):
        self.counts[label] += 1

    def decrement(self, label):
        self.counts[label] -= 1

    def get(self, label):
        return self.counts[label]

    def reset_counts(self):
        self._initialize_counts()

    def _initialize_counts(self):
        for label in self.labels:
            self.counts[label] = 0
