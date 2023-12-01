from distutils.dir_util import copy_tree
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.request import urlretrieve
from zipfile import ZipFile

from cookiecutter.vcs import clone


def write_custom_config(user_input_config):
    if not user_input_config:
        return

    tmp = TemporaryDirectory()
    tmp_zip = None

    print(user_input_config)

    # if not absolute, test if local path relative to parent of created directory
    if not user_input_config.startswith("/"):
        test_path = Path("..") / user_input_config
    else:
        test_path = Path(user_input_config)

    # check if user passed a local path
    if test_path.exists() and test_path.is_dir():
        local_path = test_path

    elif test_path.exists() and test_path.endswith(".zip"):
        tmp_zip = test_path

    # check if user passed a url to a zip
    elif user_input_config.startswith("http") and (
        user_input_config.split(".")[-1] in ["zip"]
    ):
        tmp_zip, _ = urlretrieve(user_input_config)

    # assume it is a VCS uri and try to clone
    else:
        clone(user_input_config, clone_to_dir=tmp)
        local_path = tmp

    if tmp_zip:
        with ZipFile(tmp_zip, "r") as zipf:
            zipf.extractall(tmp)
            local_path = tmp

    # write whatever the user supplied into the project
    copy_tree(local_path, ".")

    tmp.cleanup()
