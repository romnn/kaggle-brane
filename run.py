#!/usr/bin/env python3
import base64
import traceback
import os
import sys
import yaml
import kaggle

from functools import wraps
from kaggle.api.kaggle_api_extended import KaggleApi

"""
implemented kaggle API wrappers
    - competitions {list, files, download, submit, submissions, leaderboard}
    - datasets {list, files, download, create, version, init, metadata, status}
    - kernels {list,init,push,pull,output,status}

not covered by this package as of now
    - config {view, set, unset}
"""


def _is_set(val):
    return str(val).lower() in ["y", "yes", "true", "t"]


def authenticate():
    api = KaggleApi()
    api.authenticate()
    return api


def wrap_error(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return True, f(*args, **kwargs), ""
        except Exception as e:
            trace = traceback.format_exc()
            return False, None, trace

    return decorated


@wrap_error
def list_competitions(api, env):
    competition = env.get("COMPETITION")
    if competition is None:
        raise ValueError("must specify competition")
    # optional
    group = env.get("GROUP")
    category = env.get("CATEGORY")
    sort_by = env.get("SORT_BY")
    page = int(env.get("PAGE", 1))
    search = env.get("SEARCH")
    return api.competitions_list(
        group=group, category=category, sort_by=sort_by, page=page, search=search
    )


@wrap_error
def list_competition_files(api, env):
    competition = env.get("COMPETITION")
    if competition is None:
        raise ValueError("must specify competition")
    return api.competition_list_files(competition)


@wrap_error
def download_competition(api, env):
    competition = env.get("COMPETITION")
    if competition is None:
        raise ValueError("must specify competition")
    # optional
    dest = env.get("DESTINATION")
    return api.competition_download_files(competition, path=dest)


@wrap_error
def submit_competition(api, env):
    file_name = env.get("FILE_NAME")
    if file_name is None:
        raise ValueError("must specify file name")
    competition = env.get("COMPETITION")
    if competition is None:
        raise ValueError("must specify competition")
    # optional
    message = env.get("MESSAGE", "")
    quiet = _is_set(env.get("QUIET", ""))
    return api.competition_submit(
        file_name=file_name, message=message, competition=competition, quiet=quiet
    )


@wrap_error
def competition_submissions(api, env):
    competition = env.get("COMPETITION")
    if competition is None:
        raise ValueError("must specify competition")
    return api.competition_submissions(competition)


@wrap_error
def competition_leaderboard(api, env):
    competition = env.get("COMPETITION")
    if competition is None:
        raise ValueError("must specify competition")

    # optional
    download = _is_set(env.get("DOWNLOAD", ""))
    quiet = _is_set(env.get("QUIET", ""))
    dest = env.get("DESTINATION")

    if download:
        # this does not work because of
        api.competition_leaderboard_download(competition, path=dest, quiet=quiet)
        return None
    return api.competition_leaderboard_view(competition)


@wrap_error
def list_dataset(api, env):
    # optional
    sort_by = env.get("SORT_BY")
    size = env.get("SIZE")
    file_type = env.get("FILE_TYPE")
    license_name = env.get("LICENSE_NAME")
    tag_ids = env.get("TAG_IDS")
    search = env.get("SEARCH")
    user = env.get("USER")
    mine = env.get("MINE")
    page = int(env.get("PAGE", 1))
    max_size = int(env.get("MAX_SIZE", 100000))
    min_size = int(env.get("MIN_SIZE", 0))

    return api.dataset_list(
        sort_by=sort_by,
        size=size,
        file_type=file_type,
        license_name=license_name,
        tag_ids=tag_ids,
        search=search,
        user=user,
        mine=mine,
        page=page,
        max_size=max_size,
        min_size=min_size,
    )


@wrap_error
def list_dataset_files(api, env):
    dataset = env.get("DATASET")
    if dataset is None:
        raise ValueError("must specify dataset")
    return api.dataset_list_files(dataset)


@wrap_error
def download_dataset(api, env):
    dataset = env.get("DATASET")
    if dataset is None:
        raise ValueError("must specify dataset")

    # optional
    dest = env.get("DESTINATION")
    file_name = env.get("FILE_NAME")
    unzip = _is_set(env.get("UNZIP", ""))
    force = _is_set(env.get("FORCE", ""))
    quiet = _is_set(env.get("QUIET", ""))

    if file_name is None:
        api.dataset_download_files(
            dataset, path=dest, unzip=unzip, force=force, quiet=quiet
        )
    else:
        api.dataset_download_file(
            dataset, file_name, path=dest, force=force, quiet=quiet
        )
    return None


@wrap_error
def create_dataset(api, env):
    folder = env.get("FOLDER") or os.getcwd()
    # optional
    public = _is_set(env.get("PUBLIC", ""))
    quiet = _is_set(env.get("QUIET", ""))
    convert_to_csv = _is_set(env.get("CONVERT_TO_CSV", ""))
    dir_mode = env.get("DIR_MODE")

    return api.dataset_create_new(
        folder=folder,
        public=public,
        quiet=quiet,
        convert_to_csv=convert_to_csv,
        dir_mode=dir_mode,
    )


@wrap_error
def dataset_version(api, env):
    folder = env.get("FOLDER") or os.getcwd()
    # optional
    version_notes = env.get("VERSION_NOTES")
    quiet = _is_set(env.get("QUIET", ""))
    convert_to_csv = _is_set(env.get("CONVERT_TO_CSV", ""))
    delete_old_versions = _is_set(env.get("DELETE_OLD_VERSIONS", ""))
    dir_mode = env.get("DIR_MODE")

    return self.dataset_create_version(
        folder,
        version_notes,
        quiet=quiet,
        convert_to_csv=convert_to_csv,
        delete_old_versions=delete_old_versions,
        dir_mode=dir_mode,
    )


@wrap_error
def init_dataset(api, env):
    folder = env.get("FOLDER") or os.getcwd()
    api.dataset_initialize(folder)


@wrap_error
def dataset_metadata(api, env):
    dataset = env.get("DATASET")
    if dataset is None:
        raise ValueError("must specify dataset")

    # optional
    dest = env.get("DESTINATION")
    update = _is_set(env.get("UPDATE", ""))

    if update:
        api.dataset_metadata_update(dataset, path=dest)
    else:
        meta_file = api.dataset_metadata(dataset, path=dest)


@wrap_error
def dataset_status(api, env):
    dataset = env.get("DATASET")
    if dataset is None:
        raise ValueError("must specify dataset")

    return api.dataset_status(dataset)


@wrap_error
def list_kernel(api, env):
    dataset = env.get("DATASET")
    if dataset is None:
        raise ValueError("must specify dataset")

    page = int(env.get("PAGE", 1))
    page_size = int(env.get("PAGE_SIZE", 36))
    search = env.get("SEARCH")
    mine = env.get("MINE")
    competition = env.get("COMPETITION")
    parent_kernel = env.get("PARENT_KERNEL")
    user = env.get("USER")
    language = env.get("LANGUAGE")
    kernel_type = env.get("KERNEL_TYPE")
    output_type = env.get("OUTPUT_TYPE")
    sort_by = env.get("SORT_BY")

    return api.kernels_list(
        page=page,
        page_size=page_size,
        search=search,
        mine=mine,
        dataset=dataset,
        competition=competition,
        parent_kernel=parent_kernel,
        user=user,
        language=language,
        kernel_type=kernel_type,
        output_type=output_type,
        sort_by=sort_by,
    )


@wrap_error
def init_kernel(api, env):
    folder = env.get("FOLDER") or os.getcwd()
    return api.kernels_initialize(folder)


@wrap_error
def push_kernel(api, env):
    folder = env.get("FOLDER") or os.getcwd()
    return api.kernels_push(folder)


@wrap_error
def pull_kernel(api, env):
    kernel = env.get("KERNEL")
    if kernel is None:
        raise ValueError("must specify kernel")
    dest = env.get("DESTINATION")
    metadata = env.get("METADATA")
    quiet = _is_set(env.get("QUIET", ""))

    return api.kernels_pull(kernel, path=dest, metadata=metadata, quiet=quiet)


@wrap_error
def kernel_output(api, env):
    kernel = env.get("KERNEL")
    if kernel is None:
        raise ValueError("must specify kernel")
    dest = env.get("DESTINATION")
    force = _is_set(env.get("FORCE", ""))
    quiet = _is_set(env.get("QUIET", ""))

    return api.kernels_output(kernel, path=dest, force=force, quiet=quiet)


@wrap_error
def kernel_status(api, env):
    kernel = env.get("KERNEL")
    if kernel is None:
        raise ValueError("must specify kernel")
    return api.kernels_status(kernel)


@wrap_error
def debug_auth(api, env):
    return dict()
    return dict(
        kaggle_username=env.get("KAGGLE_USERNAME"), kaggle_key=env.get("KAGGLE_KEY")
    )

if __name__ == "__main__":
    print(yaml.dump({"output": "test"}))

if False:
    if len(sys.argv) < 3:
        print(yaml.dump({
            **{"success": False, "error": 'must provide a command and a subcommand, e.g. "competitions list"'},
        }, sort_keys=True))
    else:
        command = sys.argv[1]
        subcommand = sys.argv[2]
        functions = {
            "debug": {
                "auth": debug_auth,
            },
            "competitions": {
                "list": list_competitions,
                "files": list_competition_files,
                "download": download_competition,
                "submit": submit_competition,
                "submissions": competition_submissions,
                "leaderboard": competition_leaderboard,
            },
            "datasets": {
                "list": list_dataset,
                "files": list_dataset_files,
                "download": download_dataset,
                "create": create_dataset,
                "version": dataset_version,
                "init": init_dataset,
                "metadata": dataset_metadata,
                "status": dataset_status,
            },
            "kernels": {
                "list": list_kernel,
                "init": init_kernel,
                "push": push_kernel,
                "pull": pull_kernel,
                "output": kernel_output,
                "status": kernel_status,
            },
        }
        api = authenticate()
        func = functions[command][subcommand]
        success, output, error = func(api, os.environ)
        print(yaml.dump({"output": {
            **{"success": success, "error": error},
            **output
        }}, sort_keys=True))
