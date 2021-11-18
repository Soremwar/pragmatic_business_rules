# Necessary to allow circular dependencies in type anotations
from __future__ import annotations
from typing import Dict, List, Optional, Type, TypedDict, Union

class Condition(TypedDict):
	name: str
	operator: str
	value: Union[str, int]

class Conditional(TypedDict):
	all: Optional[List[Union[Conditional, Condition]]]
	any: Optional[List[Union[Conditional, Condition]]]


class Rule(TypedDict):
	actions: dict
	conditions: Conditional


# TODO
# Use jsonschema to validate rules and variables
def process_rules(
	rules: List[Rule],
	variables: Dict[str, Union[str, int]]
):
	counter = 0
	for rule in rules:
		if counter > 0:
			break

		any = rule.get("conditions").get("any")
		for condition in any[0].get("all"):
			condition_name = condition.get("name")

			# Validate variable exists and matches type
			if condition_name not in variables:
				raise Exception(f"Variable '{condition_name}' not defined")

			# TODO
			# Allow casting between ints and floats
			if type(condition.get("value")) != type(variables.get(condition_name)):
				raise Exception("The value '{}' to compare for variable '{}' doesn't match the defined variable type of '{}'".format(
					condition.get("value"),
					condition_name,
					type(variables.get(condition_name)).__name__,
				))

		counter += 1

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