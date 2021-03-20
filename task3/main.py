from flask import Flask
from flask_restful import Api, Resource
from test import tests

app = Flask(__name__)
api = Api(app)


def appearance(intervals):
    pupil = intervals['pupil']
    tutor = intervals['tutor']
    time_sets_for_pupil = []
    time_sets_for_tutor = []
    i = 0
    while i < len(pupil) - 1:
        time_sets_for_pupil.extend(i for i in range(pupil[i], pupil[i + 1]))
        i += 2
    d = 0
    while d < len(tutor) - 1:
        time_sets_for_tutor.extend(i for i in range(tutor[d], tutor[d + 1]))
        d += 2
    time = 0
    for i in range(intervals['lesson'][0], intervals['lesson'][1]):
        if i in time_sets_for_pupil and i in time_sets_for_tutor:
            time += 1
    return time


def test(tests):
    for i, test in enumerate(tests):
        test_answer = appearance(test['data'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'
    return 1


class Result(Resource):
    def get(self):
        return {'answer': appearance(tests[0]['data'])}


api.add_resource(Result, '/api/result')


if __name__ == '__main__':
    if test(tests):
        app.run(debug=True)




