from src.types import Action
from typing import Dict, List, Optional, Union


def apply_action_to_value(
	action: Action,
	value: Union[int, float, str],
) -> Union[int, float, str]:
	if len(action.keys()) > 1:
		raise Exception(
			"Too many actions '{}' were specified".format(", ".join(action.keys()))
		)

	set = action.get("set")

	# Specyfing set will replace the current value with the one passed to set
	if set is not None:
		return set
	else:
		raise Exception(
			"Unexpected '{}' action was specified".format(list(action.keys())[0])
		)


def apply_actions_to_initial_value(
	actions: List[Action],
	initial_value: Dict[str, Union[int, float, str]],
):
	"""
	This function mutates the initial_value object passed to it
	"""
	for item in actions:
		if initial_value.get(item) is None:
			raise Exception(
				f"The key '{item}' is not defined in the initial value object"
			)

		initial_value[item] = apply_action_to_value(
			actions[item], initial_value[item]
		)
