import yaml


# small class to define a license node, which makes up
# a license expression tree
class LicNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.right = right
        self.left = left

    def __str__(self, level=0):
        ret = "\t" * level + self.value + "\n"
        if type(self.left) is LicNode:
            ret += self.left.__str__(level + 1)
        elif self.left:
            ret += "\t" * (level + 1) + self.left + "\n"

        if type(self.right) is LicNode:
            ret += self.right.__str__(level + 1)
        elif self.right:
            ret += "\t" * (level + 1) + self.right + "\n"

        return ret


# Builds an expression tree from the given expression.
# This allows us to effectively parse and manipulate the
# expression while maintaining the logical relationships.
# Simple text parsing simply doesn't work well for complicated
# license expressions.
#
# The idea is to build a binary tree where each node can either
# be another expression or, if a leaf node, just the license ID.
#
# For example, for the expression A AND B AND (C OR D),
# the tree should look like:
#   AND
#  /  \
# A   AND
#    /   \
#   B    OR
#       /  \
#      C    D
#
# This function automatically takes care to remove standalone exceptions
# while building the tree. The new expression without the standalone exceptions
# can then be produced by rendering the tree back into text form.
def create_exp_tree(exp=None, exception_list=[], ignore_list=[]):
    if not exp:
        return

    left = None
    right = None
    new_node = LicNode()
    sub_exp = None
    rhs = None

    exp = exp.strip()
    exp_spl = exp.split(" ")
    exp_spl = [x.strip() for x in exp_spl]

    # Handle holes in expression at beginning
    while exp_spl[0] == "AND" or exp_spl[0] == "OR":
        del exp_spl[0]

        if not exp_spl:
            return

    # get the left side
    if exp_spl[0].startswith("("):
        # find the end paranthesis and recurse inside
        i = 0
        open_paran = 0
        for char in exp:
            i += 1

            if char == "(":
                open_paran += 1
            elif char == ")":
                open_paran -= 1

            if open_paran == 0:
                break

        sub_exp = exp[1 : i - 1]
        left = create_exp_tree(sub_exp, exception_list, ignore_list)
        rhs = exp[i + 1 :]
    else:
        # Normal license ID, no paranthesis
        if len(exp_spl) > 1 and exp_spl[1] == "WITH":
            # if first field is a valid license ID, then check exception
            if (
                exp_spl[0] not in exception_list
                and exp_spl[0] not in ignore_list
            ):
                if (
                    exp_spl[2] in exception_list
                    and exp_spl[2] not in ignore_list
                ):
                    left = LicNode(value=" ".join(exp_spl[0:3]))
                else:
                    # ignore exception as it's not a proper exception or it's supposed to be ignored
                    left = LicNode(value=exp_spl[0])

            rhs = " ".join(exp_spl[3:])
        else:
            # don't add standalone exceptions. It's ok to have a hole here
            if (
                exp_spl[0] not in ignore_list
                and exp_spl[0] not in exception_list
            ):
                left = LicNode(value=exp_spl[0])

            rhs = " ".join(exp_spl[1:])

    if not rhs:
        return left

    # get the connector, i.e AND/OR
    exp_spl = rhs.strip().split(" ")
    try:
        new_node.left = left
        new_node.value = exp_spl[0]
    except IndexError:
        # If only one symbol in the expression, just return it. We're at the end of the recursion
        return left

    # remove connector string, and parse only the right hand side past this point
    rhs = " ".join(exp_spl[1:])

    if rhs:
        # parse the right side
        sub_exp = rhs
        right = create_exp_tree(sub_exp, exception_list, ignore_list)
        new_node.right = right

    # deal with holes - if we have only one side of the expression,
    # then we can pass the existing child node up the tree
    if new_node.right and new_node.left:
        return new_node
    elif not new_node.right and new_node.left:
        new_node = new_node.left
    elif not new_node.left and new_node.right:
        new_node = new_node.right
    else:
        return None

    return new_node


# Convert the expression tree to text form
def render_exp_tree(exp_tree=None, parent_value="", string=""):
    if exp_tree is None:
        return

    sub_str = ""
    lhs = render_exp_tree(exp_tree.left, exp_tree.value, string)
    rhs = render_exp_tree(exp_tree.right, exp_tree.value, string)

    if exp_tree.value == "AND":
        sub_str = f"{lhs} {exp_tree.value} {rhs}"
        if parent_value == "OR":
            sub_str = f"({sub_str})"
    elif exp_tree.value == "OR":
        sub_str = f"{lhs} {exp_tree.value} {rhs}"
        if parent_value == "AND":
            sub_str = f"({sub_str})"
    else:
        sub_str = exp_tree.value

    return f"{string} {sub_str}".strip()


# Tests the expression tree API, validates that reading/rendering
# is accurate.
#
# input_yaml=<path to yaml holding test cases>
# exception_list = list of all license exceptions
# ignore_list = list of all license IDs which can be ignored
def __test_exp_tree__(input_yaml=None, exception_list=[], ignore_list=[]):
    test_exps = None
    with open(input_yaml, "r") as input_y:
        test_exps = yaml.safe_load(input_y)

    i = 0
    for tst_case in test_exps:
        result_node = create_exp_tree(
            test_exps[tst_case]["input"], exception_list, ignore_list
        )
        result_str = render_exp_tree(result_node, "")
        expected = test_exps[tst_case]["expected"]
        if expected:
            expected = expected.strip()

        if result_str == expected:
            print(f"Sucessfully passed test case {i}")
        else:
            print(
                f"Test {i} failed!\n\tResult: {result_str}\n"
                + f"\tExpected Result: {test_exps[tst_case]['expected']}"
            )

        #    print(f"Result tree:\n{result_node}")

        i += 1
