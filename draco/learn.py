import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split


def train_model(X, test_size: float = 0.3, C: float = 1, quiet=False):
    """Given features X and labels y, train a linear model to classify them
    Args:
        X: a N x M matrix, representing feature vectors
        y: a N vector, representing labels
        test_size: the fraction of test data
    """

    X_train, X_dev = train_test_split(X, test_size=test_size, random_state=1)

    size = len(X_train)

    y_train = np.ones(size)

    # flip a few examples at random
    idx = np.ones(size, dtype=bool)
    idx[: int(size / 2)] = False
    np.random.shuffle(idx)

    X_train[idx] = -X_train[idx]
    y_train[idx] = -y_train[idx]

    clf = svm.LinearSVC(C=C, fit_intercept=False)
    clf.fit(X_train, y_train)

    if not quiet:
        print("Train score: ", clf.score(X_train, y_train))
        if test_size > 0:
            print("Dev score: ", clf.score(X_dev, np.ones(len(X_dev))))

    return clf
