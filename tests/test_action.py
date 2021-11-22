from src.action import apply_actions_to_initial_value, apply_action_to_item
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
			apply_action_to_item(action, "unknown key", 0)

	def test_assert_action_type(self):
		invalid_action = "unknown"

		with pytest.raises(
			Exception,
			match=f"Unexpected '{invalid_action}' action was specified",
		):
			apply_action_to_item({invalid_action: 1}, "unknown key", 0)

	def test_assert_comparable_item_type(self):
		invalid_item = "some item"
		original_value = 0
		new_value = "asd"

		with pytest.raises(
			Exception,
			match="'set' action type differs from initial value type: The value '{}' to compare for variable '{}' doesn't match the defined variable type of '{}'"
			.format(
				new_value,
				invalid_item,
				type(original_value).__name__,
			),
		):
			apply_action_to_item({"set": new_value}, invalid_item, original_value)


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
