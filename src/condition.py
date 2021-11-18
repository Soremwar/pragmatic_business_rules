from typing import Dict, List, Literal, Optional, Union
from .types import Condition, Conditional


def assert_single_conditional(conditional: Conditional):
	all = conditional.get("all")
	any = conditional.get("any")

	if all is not None and any is not None:
		raise Exception(
			"'all' and 'any' properties can't be specified for the same conditional"
		)
	elif all is None and any is None:
		raise Exception(
			"'all' or 'any' properties were not found in the conditional"
		)


def evaluate_condition(
	condition: Condition,
	variables: Dict[str, Union[int, float, str]],
):
	condition_name = condition.get("name")
	condition_value = condition.get("value")

	# Validate variable exists and matches type
	if condition_name not in variables:
		raise Exception(f"Variable '{condition_name}' not defined")

	variable: Union[str, int, float] = variables.get(condition_name)

	# TODO
	# Allow casting between ints and floats
	if type(condition_value) != type(variables.get(condition_name)):
		raise Exception(
			"The value '{}' to compare for variable '{}' doesn't match the defined variable type of '{}'"
			.format(
				condition_value,
				condition_name,
				type(variable).__name__,
			)
		)

	# TODO
	# Test other operators and validate string doesn't use operators other than equals
	return condition_value == variable


def evaluate_conditional(
	conditional: Optional[List[Union[Conditional, Condition]]],
	variables: Dict[str, Union[str, int]], type: Literal["all", "any"]
) -> bool:
	"""
	This function will evaluate the conditionals and return the boolean result for the entire group

	The evaluation process is different depending on the type:
	- all: All conditionals must be true
	- any: At least one conditional must be true
	"""
	if conditional is None:
		return False

	# Below there are checks that make sure to only refresh the result of the conditional
	# when the type it's set to is the correct one
	# The type "all" will only refresh the result if the result hasn't been marked as false
	# already, similarly the type "any" won't continue to process the conditionals if the result
	# has been marked as true

	# Make sure that the conditional contains items that can be evaluated
	# If no items were evaluated, mark the conditional as false
	evaluated_items = 0
	result = True
	for c in conditional:
		# If it contains a value, it's a simple condition
		if "value" in c:
			if type == "all" and result != False:
				result = evaluate_condition(c, variables)
			elif type == "any" and result != True:
				result = evaluate_condition(c, variables)
		else:
			assert_single_conditional(c)

			all = c.get("all")
			any = c.get("any")

			subconditional = all if all is not None else any
			subtype = "all" if all is not None else "any"

			if type == "all" and result != False:
				result = evaluate_conditional(subconditional, variables, subtype)
			elif type == "any" and result != True:
				result = evaluate_conditional(subconditional, variables, subtype)

		evaluated_items += 1

		# If one of the conditions returned false and the type is set to "all", stop evaluating and return
		if result == False and type == "all":
			break

		# If one of the conditions returned true and the type is set to "any", stop evaluating and return
		if evaluated_items > 0 and result == True and type == "any":
			break

	return result if evaluated_items > 0 else False
