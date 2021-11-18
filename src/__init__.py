from .condition import assert_single_conditional, evaluate_conditional
from .types import Rule
from typing import Dict, List, Union


# TODO
# Use jsonschema to validate rules and variables
def process_rules(
	rules: List[Rule],
	variables: Dict[str, Union[int, float, str]]
):
	for rule in rules:
		actions = rule.get("actions")
		conditions = rule.get("conditions")

		# Make sure the condition has at least one usable condition
		assert_single_conditional(conditions)

		all = conditions.get("all")
		any = conditions.get("any")

		conditional = all if all is not None else any
		type = "all" if all is not None else "any"

		result = evaluate_conditional(conditional, variables, type)
		print(result)

import json
f = open("rules.json")
data: List[Rule] = json.load(f)

process_rules(
	data,
	{
		"DiasMoraInternos": 1.0,
		"DiasMoraExternos": 1.0,
	}
)