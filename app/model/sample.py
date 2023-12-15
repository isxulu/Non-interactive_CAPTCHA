import sys, pickle
import numpy as np
import xgboost as xgb
import pandas as pd

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from utils import get_testing_data_features

def parse_trace(raw):

    raw_list = raw.split(',')
    tgt_coor = raw_list[-3:]

    traces = []
    for i in range(len(raw_list) // 3):
        pts = raw_list[i*3: i*3+3]
        trace = [0, *map(lambda x: float(x), pts), *map(lambda x: float(x), tgt_coor[:2])]    # ['id', 'x', 'y', 't', 'tgt_x', 'tgt_y']
        traces.append(trace)

    trace_pd = pd.DataFrame(traces, columns=['id', 'x', 'y', 't', 'target_x', 'target_y'])
    feature = get_testing_data_features(trace_pd)
    return feature

def judge_mouse_trace(trace, model):
    try:
        dtest = xgb.DMatrix(parse_trace(trace))
        # calculate the prediction
        pred = model.predict(dtest)
        # convert the raw prediction to 0, 1 label
        pred[pred >= 0.5] = 1
        pred[pred <  0.5] = 0
        if pred[0] == 0: print('fail')
        else: print('pass')
    except Exception as e:
        print(e)


# load pretrained xgboost model
# loaded_model = pickle.load(open("./app/model/pima.pickle.dat", "rb"))
loaded_model = pickle.load(open("./app/model/model.pkl", "rb"))
# parse the trace and predict

judge_mouse_trace(sys.argv[1], model=loaded_model)
