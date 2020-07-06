from refactor import download
from evaluator import ScoreEvaluator
import json
import numpy as np

alpha = 1.15
beta = 1.05


class Driver:
    def __init__(self):
        self.raw_case_map = {}
        self.student_case_map = {}
        self.case_student_map = {}
        self.case_difficulty = {}

    def score_evaluator_driver(self):
        file = open('../test_data.json')
        test_data = json.loads(file.read())

    def pre_deal(self):
        for case_id in self.raw_case_map.keys():
            time_list = [raw_case.time for raw_case in self.raw_case_map[case_id]]
            line_list = [raw_case.line for raw_case in self.raw_case_map[case_id]]
            time_average = np.average(time_list)
            time_var = np.var(time_list)
            line_average = np.average(line_list)
            line_var = np.var(line_list)


if __name__ == '__main__':
    pass
