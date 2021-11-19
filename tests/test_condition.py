import pytest
from src.condition import assert_single_conditional, evaluate_condition


class TestAssertSingleConditional:

	def test_single_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' and 'any' properties can't be specified for the same conditional"
		) as e:
			assert_single_conditional({"all": [], "any": []})

	def test_valid_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' or 'any' properties were not found in the conditional"
		) as e:
			assert_single_conditional({})


class TestEvaluateCondition:

	def test_variable_exists(self):
		variable = "xyz"
		with pytest.raises(
			Exception, match=f"Variable '{variable}' not defined"
		) as e:
			evaluate_condition(
				{
					"name": variable,
					"operator": "equal_to",
					"value": "something"
				},
				{},
			)

	def test_variable_matches_type(self):
		variable_name = "abc"
		variable_value = 1
		condition_value = "a string"
		with pytest.raises(
			Exception,
			match="The value '{}' to compare for variable '{}' doesn't match the defined variable type of '{}'"
			.format(
				condition_value,
				variable_name,
				type(variable_value).__name__,
			)
		) as e:
			evaluate_condition(
				{
					"name": variable_name,
					"operator": "equal_to",
					"value": condition_value,
				},
				{
					variable_name: variable_value,
				},
			)
