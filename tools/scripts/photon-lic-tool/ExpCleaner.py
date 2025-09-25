from common import (
    cleanup_license_expression,
    get_exceptions_list,
    err_exit,
    running_in_container,
    read_license_from_file,
)
from DockerUtil import DockerUtil


class ExpCleaner:
    def clean_exp(self, file=None, stdin=None):
        exceptions_list = []
        license_expressions = {}

        docker_util = DockerUtil.detect()
        if docker_util is not None:
            mount_list, cmd = docker_util.build_clean_exp_docker_cmd(
                file=file, stdin=stdin
            )
            docker_util.run_docker_cmd(cmd=cmd, mount_list=mount_list)
            return

        # read from file
        if file:
            license_expressions = read_license_from_file(file)
        # read from stdin
        elif stdin:
            license_expressions["stdin"] = stdin
        else:
            err_exit("License expression must be provided!")

        exceptions_list = get_exceptions_list()

        for key in license_expressions:
            lic_exp = license_expressions[key]
            new_exp = cleanup_license_expression(
                ignore_list=[],
                exception_list=exceptions_list,
                license_exp=lic_exp,
            )

            print(f"\nFor {key}, original expression:\n{lic_exp}")
            print(f"\nNew expression:\n{new_exp}")
