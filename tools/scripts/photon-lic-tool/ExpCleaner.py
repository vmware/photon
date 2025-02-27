from common import cleanup_license_expression, get_exceptions_list, err_exit


class ExpCleaner:
    def clean_exp(self, license_expressions={}):
        exceptions_list = []

        if not license_expressions:
            err_exit("No license expression given")

        exceptions_list = get_exceptions_list()

        for key in license_expressions:
            lic_exp = license_expressions[key]
            new_exp = cleanup_license_expression(
                ignore_list=[], exception_list=exceptions_list, license_exp=lic_exp
            )

            print(f"\nFor {key}, original expression:\n{lic_exp}")
            print(f"\nNew expression:\n{new_exp}")
