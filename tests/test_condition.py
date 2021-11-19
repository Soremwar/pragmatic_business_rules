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

	def test_invalid_type(self):
		variable = "123"
		value = {}
		with pytest.raises(
			Exception,
			match="The value '{}' has a type '{}' which is not valid for a condition value"
			.format(
				value,
				type(value).__name__,
			)
		) as e:
			evaluate_condition(
				{
					"name": variable,
					"operator": "equal_to",
					"value": value,
				},
				{
					variable: {},
				},
			)

	def test_string_equal_to(self):
		variable = "some variable"
		value = "some value"

		assert evaluate_condition(
			{
				"name": variable,
				"operator": "equal_to",
				"value": value,
			},
			{
				variable: value,
			},
		)

		assert not evaluate_condition(
			{
				"name": variable,
				"operator": "equal_to",
				"value": value,
			},
			{
				variable: value + " other",
			},
		)

	def test_invalid_string_operator(self):
		variable = "123"
		operator = "invalid operator"
		with pytest.raises(
			Exception,
			match=f"The operator '{operator}' is not valid for string operations"
		) as e:
			evaluate_condition(
				{
					"name": variable,
					"operator": operator,
					"value": "123",
				},
				{
					variable: "asd",
				},
			)

	def test_invalid_number_operator(self):
		variable = "number variable"
		operator = "invalid operator"
		with pytest.raises(
			Exception,
			match=f"The operator '{operator}' is not valid for number operations"
		) as e:
			evaluate_condition(
				{
					"name": variable,
					"operator": operator,
					"value": 0,
				},
				{
					variable: 1,
				},
			)
