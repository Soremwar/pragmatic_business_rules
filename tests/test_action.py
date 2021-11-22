from src.action import apply_actions_to_initial_value, apply_action_to_value
import pytest


class TestApplyActionToValue:

	def test_assert_single_action(self):
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


class TestApplyActionToInitialValue:

	def test_assert_item_defined_in_initial_value(self):
		item = "some key"

		with pytest.raises(
			Exception,
			match=f"The key '{item}' is not defined in the initial value object"
		):
			apply_actions_to_initial_value(
				{
					item: {
						"set": 10
					},
				},
				{},
			)
