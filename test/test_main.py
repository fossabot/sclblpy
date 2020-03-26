from sclblpy._bundle import _gzip_load, _gzip_delete
from sclblpy._jwt import _get_user_details
from sclblpy.main import remove_credentials, upload, endpoints, delete_endpoint, _set_toolchain_URL, _set_admin_URL, \
    list_models, start_print, stop_print, _toggle_debug_mode

import numpy as np
from sklearn import svm
from sklearn import datasets

# Script settings:
RUN_TESTS = False  # Prevent unintended testing
DEBUG_MODE = False  # Set debug to true; meaning print stack traces.
ADMIN_URL = "http://localhost:8008"  # Location of admin for this testmau
TOOLCHAIN_URL = "http://localhost:8010"  # Location of toolchain for this test


def test_upload():
    """ Test the upload function"""

    # Start fitting a simple model
    clf = svm.SVC()
    X, y = datasets.load_iris(return_X_y=True)
    clf.fit(X, y)

    print("# 1: Simple upload, no docs etc; should fail:")
    upload(clf, np.empty(0))


    print("# 2: Docs, no example; should fail:")
    docs = {}
    docs['name'] = "Name of model"
    docs['documentation'] = "A long .md thing...."
    upload(clf, np.empty(0), docs=docs)

    print("# 3: Example, no docs")
    row = X[130, :]
    upload(clf, row)

    print("# 4: All args")
    upload(clf, row, docs=docs)

    # Test saving and loading:
    print("# 5: Test loading and retrieving:")
    upload(clf, row, docs=docs, _keep=True)
    obj = _gzip_load()
    _gzip_delete()
    mod = obj['fitted_model']
    pred = mod.predict(row.reshape(1, -1))
    assert pred == [2], "Prediction is not correct."


def test_remove_credentials():
    """ Test of get user details"""
    _get_user_details()
    remove_credentials(True)


def test_endpoints():
    """ Test endpoint() function """
    endpoints()


def test_delete_endpoint():
    """ Test deleting an endpoint """
    cfid = ""
    ep = endpoints()
    try:
        cfid = ep[0]['cfid']
    except Exception as e:
        # Effectively there was no endpoint...
        print("No endpoints to remove; test not run.")

    if cfid:
        delete_endpoint(cfid)


def test_setting_URLs():
    """ Test url setters: """
    _set_toolchain_URL(TOOLCHAIN_URL)
    _set_admin_URL(ADMIN_URL)


def test_user_utils():
    start_print()
    list_models()
    stop_print()
    list_models()
    start_print()


# Run tests
if __name__ == '__main__':

    if not RUN_TESTS:
        print("Not running tests.")
        exit()

    print("Running simple functional tests of main.py")
    print("===============================")

    if DEBUG_MODE:
        _toggle_debug_mode()

    test_user_utils()
    test_setting_URLs()

    test_upload()
    test_remove_credentials()

    # test_endpoints()
    test_delete_endpoint()

    print("===============================")
    print("All tests passed.")
