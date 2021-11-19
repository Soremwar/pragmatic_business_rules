from typing import Any, Dict, List, Literal, Optional, Union
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


def assert_comparable_type(value: Any, variable_name: str, variable_value: Any):
	# Ints and floats are comparable
	if type(value) in [int, float] and type(variable_value) in [int, float]:
		return

	if type(value) != type(variable_value):
		raise Exception(
			"The value '{}' to compare for variable '{}' doesn't match the defined variable type of '{}'"
			.format(
				value,
				variable_name,
				type(variable_value).__name__,
			)
		)


# By this point, the incoming conditions and variables have to have been already validated
# for correct value types
def evaluate_condition(
	condition: Condition,
	variables: Dict[str, Union[int, float, str]],
) -> bool:
	condition_name = condition.get("name")
	condition_operator = condition.get("operator")
	condition_value = condition.get("value")

	# Validate variable exists and matches type
	if condition_name not in variables:
		raise Exception(f"Variable '{condition_name}' not defined")

	variable: Union[str, int, float] = variables.get(condition_name)

	assert_comparable_type(
		condition_value,
		condition_name,
		variables.get(condition_name),
	)

	if type(condition_value) == str:
		if condition_operator == "equal_to":
			return condition_value == variable
		else:
			raise Exception(
				f"The operator '{condition_operator}' is not valid for string operations"
			)
	elif type(condition_value) == int or type(condition_value) == float:
		if condition_operator == "equal_to":
			return condition_value == variable
		else:
			raise Exception(
				f"The operator '{condition_operator}' is not valid for number operations"
			)
	else:
		raise Exception(
			"The value '{}' has a type '{}' which is not valid for a condition value"
			.format(
				condition_value,
				type(condition_value).__name__,
			)
		)


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
