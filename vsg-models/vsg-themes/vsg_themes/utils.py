import os
from os.path import abspath
from os.path import dirname
from typing import AnyStr

import yaml

from vsg_themes.analysis.theme_transformer import ThemeTransformer


# -------------------------------------------
# Generic Logic
def get_root_dir() -> AnyStr:
    """Get root directory of this package

    Returns:
        AnyStr: path in the host machine of the package

    Examples:
        Expected results when calling this function

        >>> get_root_dir() #doctest: +ELLIPSIS
        '/...'
    """
    return dirname(dirname(abspath(__file__)))


# -------------------------------------------
# Get Settings Configuration
def get_settings():
    config_file = os.path.join(
        get_root_dir(), '../../config/config_services.yaml'
    )
    with open(config_file, 'r') as fd:
        settings = yaml.safe_load(fd)

    return settings


# class to load models
class VSGThemesModels:
    def __init__(self, method):
        self.method = method
        self.model = None

    def load_all_models(self) -> None:
        if self.method == "transformer":
            self.model = ThemeTransformer()
        else:
            raise NotImplemented(f"{self.method} is not yet implemented at the API level.")


if __name__ == "__main__":
    import doctest
    failures, tests = doctest.testmod(verbose=True, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)
    print(f"{__file__}: Tests: {tests}; Failures: {failures}")
