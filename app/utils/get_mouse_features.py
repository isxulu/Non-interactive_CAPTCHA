import numpy as np
import pandas as pd


def get_speed_features(dist_x, dist_y, t):
    # calculate the speed
    speed_x = dist_x / t
    speed_y = dist_y / t
    speed = np.sqrt(np.square(dist_x) + np.square(dist_y)) / t
    # calculate the mean, std, max, min, median, 25%, 75% of the speed
    speed_mean = speed.mean()
    speed_std = speed.std()
    speed_max = speed.max()
    speed_min = speed.min()
    speed_median = speed.median()
    speed_25 = speed.quantile(0.25)
    speed_75 = speed.quantile(0.75)
    # calculate the covariance and corelation of the speed
    speed_cov = np.cov(speed_x, speed_y)[0, 1]
    # calculate the correlation of the speed_x and speed_y
    speed_corr = np.corrcoef(speed_x, speed_y)[0, 1]
    return speed_mean, speed_std, speed_max, speed_min, speed_median, speed_25, speed_75, speed_cov, speed_corr

def get_acceleration_features(speed, t):
    # calulate the acceleration
    acceleration = 2 * speed.diff(1).dropna() / np.square(t)
    # calculate the mean, std, max, min, median, 25%, 75% of the acceleration
    acceleration_mean = acceleration.mean()
    acceleration_std = acceleration.std()
    acceleration_max = acceleration.max()
    acceleration_min = acceleration.min()
    acceleration_median = acceleration.median()
    acceleration_25 = acceleration.quantile(0.25)
    acceleration_75 = acceleration.quantile(0.75)
    return acceleration_mean, acceleration_std, acceleration_max, acceleration_min, acceleration_median, acceleration_25, acceleration_75

# def get_entropy(data):
#     num_entries = len(data)
#     label_counts = {}
#     for feat_vector in data:
#         current_label = feat_vector[-1]
#         if current_label not in label_counts.keys(): label_counts[current_label] = 0
#         label_counts[current_label] += 1
#     shannon_entropy = 0.0
#     for key in label_counts:
#         prob = float(label_counts[key]) / num_entries
#         shannon_entropy -= prob * np.log(prob, 2)
#     return shannon_entropy

def get_training_data_features(data, indices):
    # create a dataframe to store the features
    features = pd.DataFrame()

    for idx in indices:
        # fetch a specific trace
        trace = data[data.id == idx]
        if len(trace) < 2: continue
        # start to add features
        trace.index = range(len(trace))
        # calculate the time interval
        interval = trace[['x', 'y', 't']].diff(1).dropna().copy()
        # calculate the displacement and speed
        dist_x, dist_y, time = interval.x, interval.y, interval.t
        speed = np.sqrt(np.square(dist_x) + np.square(dist_y)) / time
        # calculate the speed and acceleration features
        speed_features = get_speed_features(dist_x, dist_y, time)
        accel_features = get_acceleration_features(speed, time)
        # calculate the maximum and minimum time interval
        time_max, time_min = time.max(), time.min()
        # calculate difference between the target and the mean x, y coordinate of the trace
        target_x, target_y = trace.target_x[0], trace.target_y[0]
        x_mean, y_mean = trace.x.mean(), trace.y.mean()
        x_diff, y_diff = target_x - x_mean, target_y - y_mean
        # # calculate the entropy of the x, y coordinate
        # x_entropy = get_entropy(trace.x)
        # y_entropy = get_entropy(trace.y)
        # calculate the distance between the target and the start point
        start_x, start_y = trace.x[0], trace.y[0]
        start_dist = np.sqrt(np.square(target_x - start_x) + np.square(target_y - start_y))
        # calculate the distance between the target and the end point
        end_x, end_y = trace.x[len(trace) - 1], trace.y[len(trace) - 1]
        end_dist = np.sqrt(np.square(target_x - end_x) + np.square(target_y - end_y))
        # calculate the distance between the start point and the end point
        start_end_dist = np.sqrt(np.square(start_x - end_x) + np.square(start_y - end_y))

        # add the features to the dataframe
        trace_feats = pd.DataFrame(index=[0])
        trace_feats['id'] = idx
        trace_feats['speed_mean']     = speed_features[0]
        trace_feats['speed_std']      = speed_features[1]
        trace_feats['speed_max']      = speed_features[2]
        trace_feats['speed_min']      = speed_features[3]
        trace_feats['speed_median']   = speed_features[4]
        trace_feats['speed_25']       = speed_features[5]
        trace_feats['speed_75']       = speed_features[6]
        trace_feats['speed_cov']      = speed_features[7]
        trace_feats['speed_corr']     = speed_features[8]
        trace_feats['accel_mean']     = accel_features[0]
        trace_feats['accel_std']      = accel_features[1]
        trace_feats['accel_max']      = accel_features[2]
        trace_feats['accel_min']      = accel_features[3]
        trace_feats['accel_median']   = accel_features[4]
        trace_feats['accel_25']       = accel_features[5]
        trace_feats['accel_75']       = accel_features[6]
        trace_feats['time_max']       = time_max
        trace_feats['time_min']       = time_min
        trace_feats['x_diff']         = x_diff
        trace_feats['y_diff']         = y_diff
        # trace_feats['x_entropy']      = x_entropy
        # trace_feats['y_entropy']      = y_entropy
        trace_feats['start_dist']     = start_dist
        trace_feats['end_dist']       = end_dist
        trace_feats['start_end_dist'] = start_end_dist
        # add the label to the dataframe
        trace_feats['label']          = trace.label[0]

        # concatenate the features
        features = pd.concat([features, trace_feats])

    return features

def get_testing_data_features(data):
    # create a dataframe to store the features
    features = pd.DataFrame()

    # fetch a specific trace
    trace = data
    if len(trace) < 2: return None
    # start to add features
    trace.index = range(len(trace))
    # calculate the time interval
    interval = trace[['x', 'y', 't']].diff(1).dropna().copy()
    # calculate the displacement and speed
    dist_x, dist_y, time = interval.x, interval.y, interval.t
    speed = np.sqrt(np.square(dist_x) + np.square(dist_y)) / time
    # calculate the speed and acceleration features
    speed_features = get_speed_features(dist_x, dist_y, time)
    accel_features = get_acceleration_features(speed, time)
    # calculate the maximum and minimum time interval
    time_max, time_min = time.max(), time.min()
    # calculate difference between the target and the mean x, y coordinate of the trace
    target_x, target_y = trace.target_x[0], trace.target_y[0]
    x_mean, y_mean = trace.x.mean(), trace.y.mean()
    x_diff, y_diff = target_x - x_mean, target_y - y_mean
    # # calculate the entropy of the x, y coordinate
    # x_entropy = get_entropy(trace.x)
    # y_entropy = get_entropy(trace.y)
    # calculate the distance between the target and the start point
    start_x, start_y = trace.x[0], trace.y[0]
    start_dist = np.sqrt(np.square(target_x - start_x) + np.square(target_y - start_y))
    # calculate the distance between the target and the end point
    end_x, end_y = trace.x[len(trace) - 1], trace.y[len(trace) - 1]
    end_dist = np.sqrt(np.square(target_x - end_x) + np.square(target_y - end_y))
    # calculate the distance between the start point and the end point
    start_end_dist = np.sqrt(np.square(start_x - end_x) + np.square(start_y - end_y))

    # add the features to the dataframe
    trace_feats = pd.DataFrame(index=[0])
    trace_feats['speed_mean']     = speed_features[0]
    trace_feats['speed_std']      = speed_features[1]
    trace_feats['speed_max']      = speed_features[2]
    trace_feats['speed_min']      = speed_features[3]
    trace_feats['speed_median']   = speed_features[4]
    trace_feats['speed_25']       = speed_features[5]
    trace_feats['speed_75']       = speed_features[6]
    trace_feats['speed_cov']      = speed_features[7]
    trace_feats['speed_corr']     = speed_features[8]
    trace_feats['accel_mean']     = accel_features[0]
    trace_feats['accel_std']      = accel_features[1]
    trace_feats['accel_max']      = accel_features[2]
    trace_feats['accel_min']      = accel_features[3]
    trace_feats['accel_median']   = accel_features[4]
    trace_feats['accel_25']       = accel_features[5]
    trace_feats['accel_75']       = accel_features[6]
    trace_feats['time_max']       = time_max
    trace_feats['time_min']       = time_min
    trace_feats['x_diff']         = x_diff
    trace_feats['y_diff']         = y_diff
    # trace_feats['x_entropy']      = x_entropy
    # trace_feats['y_entropy']      = y_entropy
    trace_feats['start_dist']     = start_dist
    trace_feats['end_dist']       = end_dist
    trace_feats['start_end_dist'] = start_end_dist

    # concatenate the features
    features = pd.concat([features, trace_feats])

    return features