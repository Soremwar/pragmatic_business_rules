from src.action import apply_action_to_value
import pytest


class TestApplyActionToResult:

	def test_assert_action_type(self):
		action = {"set": 1, "something_else": 2}

		with pytest.raises(
			Exception,
			match="Too many actions '{}' were specified".format(
				", ".join(action.keys())
			),
		):
			apply_action_to_value(action, 0)

	def test_assert_action_type(self):
		invalid_action = "unknown"

		with pytest.raises(
			Exception,
			match=f"Unexpected '{invalid_action}' action was specified",
		):
			apply_action_to_value({invalid_action: 1}, 0)
