import numpy as np
import pandas as pd
from sklearn.cluster import FeatureAgglomeration
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVR
from tpot.builtins import OneHotEncoder, StackingEstimator
from tpot.export_utils import set_param_recursive
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=27)

# Average CV score on the training set was: -3.9977339888795447
exported_pipeline = make_pipeline(
    make_union(
        FunctionTransformer(copy),
        OneHotEncoder(minimum_fraction=0.15, sparse=False, threshold=10)
    ),
    FeatureAgglomeration(affinity="cosine", linkage="complete"),
    LinearSVR(C=10.0, dual=True, epsilon=0.01, loss="epsilon_insensitive", tol=0.01)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 27)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
