from src.types import Action
from typing import Dict, Optional, Union


def apply_action_to_value(
	action: Action,
	value: Optional[Union[int, float, str]],
):
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
