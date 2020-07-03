class CaseData:
    def __init__(self, case_id, user_id, url, score, time, line):
        self.user_id = user_id
        self.case_id = case_id
        self.url = url
        self.score = score
        self.time = time
        self.line = line
        # [self.time, self.line] = ScoreEvaluator.getscore(url)

    def __str__(self):
        return 'user:' + str(self.user_id) + ' case:' + str(self.case_id) +' score:' + str(self.score) + ' time:' + str(self.time) + ' line:' + str(
            self.line)

    def copy(self):
        copy = CaseData(self.case_id, self.user_id, self.url, self.score, self.time, self.line)
        return copy
