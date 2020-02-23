# Utility functions (internal)
from sclblpy import *
import inspect
import json


def __model_supported(obj) -> bool:
    """Checks whether the supplied model is supported.

    """
    if not SUPPORTED_MODELS:
        __load_supported_models()

    try:
        model_name: str = __get_model_name(obj)
        model_base: str = __get_model_package(obj)
    except:
        raise ModelSupportError("Unable to retrieve model details")

    if (model_base in SUPPORTED_MODELS and
            model_name in SUPPORTED_MODELS[model_base]):
        return True
    else:
        return False


def __get_model_package(obj):
    """Gets the package name of a model object.

    Args:
        obj: a fitted model object
    """
    mod = inspect.getmodule(obj)
    base, _sep, _stem = mod.__name__.partition('.')
    return base


def __get_model_name(obj):
    return type(obj).__name__


def __load_supported_models():
    print("loading supported models..")
    global SUPPORTED_MODELS
    try:
        with open(CURRENT_FOLDER + "/supported.json", "r") as f:
            SUPPORTED_MODELS = json.load(f)
            print("opening file...")
    except FileNotFoundError:
        raise ModelSupportError("Unable to find list of supported models.")
