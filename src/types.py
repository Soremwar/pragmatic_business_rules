from __future__ import annotations
from typing import List, Optional, TypedDict, Union


class Condition(TypedDict):
	name: str
	operator: str
	value: Union[int, float, str]


class Conditional(TypedDict):
	all: Optional[List[Union[Conditional, Condition]]]
	any: Optional[List[Union[Conditional, Condition]]]


class Rule(TypedDict):
	actions: dict
	conditions: Conditional
