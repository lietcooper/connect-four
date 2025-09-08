class ScoreKeeper:
    """A class for keeping scores"""

    def __init__(self, name, file="scores.txt"):
        self.name = name
        self.FILE = file
        self.scores = {}
        self.load_score()

    def load_score(self):
        scores = open(self.FILE, 'r')
        for score in scores.readlines():
            if len(score) > 2:  # If file not empty
                name, point = score.strip().split()
                self.scores[name] = int(point)
        scores.close()
        for key, value in self.scores.items():
            print(key + '\t' + str(value))

    def save_score(self, win=True):
        if self.name in self.scores:
            if win:
                self.scores[self.name] += 1
            else:
                self.scores[self.name] += 0
        else:
            if win:
                self.scores[self.name] = 1
            else:
                self.scores[self.name] = 0
        self.scores = dict(sorted(self.scores.items(),
                                  key=lambda item: item[1],
                                  reverse=True))
        with open(self.FILE, 'w') as f:
            lines = []
            for key, value in self.scores.items():
                line = key + "\t" + str(value) + "\n"
                lines.append(line)
            f.writelines(lines)
