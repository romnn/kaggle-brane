#!/usr/bin/env python3
import os
import sys
import yaml
from pprint import pprint

import kaggle_brane as kb

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            yaml.dump(
                {
                    "output": {
                        "status": {
                            "success": False,
                            "error": 'must provide a command and a subcommand, e.g. "competitions list"',
                        },
                    }
                },
            )
        )
    else:
        command = sys.argv[1]
        subcommand = sys.argv[2]
        functions = {
            "debug": {
                "auth": kb.debug_auth,
            },
            "competitions": {
                "list": kb.list_competitions,
                "files": kb.list_competition_files,
                "download": kb.download_competition,
                "submit": kb.submit_competition,
                "submissions": kb.competition_submissions,
                "leaderboard": kb.competition_leaderboard,
            },
            "datasets": {
                "list": kb.list_dataset,
                "files": kb.list_dataset_files,
                "download": kb.download_dataset,
                "create": kb.create_dataset,
                "version": kb.dataset_version,
                "init": kb.init_dataset,
                "metadata": kb.dataset_metadata,
                "status": kb.dataset_status,
            },
            "kernels": {
                "list": kb.list_kernel,
                "init": kb.init_kernel,
                "push": kb.push_kernel,
                "pull": kb.pull_kernel,
                "output": kb.kernel_output,
                "status": kb.kernel_status,
            },
        }
        try:
            api = kb.authenticate(os.environ)
        except Exception as e:
            if kb.DEBUG:
                raise e
            status = {"success": False, "error": str(e)}
            print(yaml.dump({"output": status}))

        func = functions[command][subcommand]
        if kb.DEBUG:
            print(func)
        success, output, error = func(api, os.environ)
        if kb.DEBUG:
            pprint(dict(success=success, output=output, error=error))
        output = output if output is not None else dict()
        status = {"success": success, "error": error}
        # status = {"status": status}
        print(
            yaml.dump(
                {
                    "output": {
                        **status,
                        **output,
                    }
                },
            )
        )
