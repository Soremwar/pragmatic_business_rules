from .action import apply_actions_to_initial_value
from .asserts import assert_single_conditional
from .condition import evaluate_conditional
from .types import Rule
from .validators import plain_dictionary_schema
from jsonschema.exceptions import ValidationError
from typing import Dict, List, Union
import jsonschema


# TODO
# Use jsonschema to validate rules
def process_rules(
	rules: List[Rule],
	variables: Dict[str, Union[int, float, str]],
	initial_value: Dict[str, Union[int, float, str]],
) -> Dict[str, Union[int, float, str]]:
	value = initial_value.copy()

	try:
		jsonschema.validate(variables, plain_dictionary_schema)
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'variables': {validation_error.message}"
		) from validation_error

	try:
		jsonschema.validate(initial_value, plain_dictionary_schema)
	except ValidationError as validation_error:
		raise Exception(
			f"Invalid input for 'initial_value': {validation_error.message}"
		) from validation_error

	for rule in rules:
		actions = rule.get("actions")
		conditions = rule.get("conditions")

		# Make sure the condition has at least one usable condition
		assert_single_conditional(conditions)

		all = conditions.get("all")
		any = conditions.get("any")

		conditional = all if all is not None else any
		type = "all" if all is not None else "any"

		if evaluate_conditional(conditional, variables, type):
			apply_actions_to_initial_value(actions, value)

	return value


# import json

# f = open("rules.json")
# data: List[Rule] = json.load(f)

# process_rules(data, {
# 	"DiasMoraInternos": 1.0,
# 	"DiasMoraExternos": 1.0,
# })
