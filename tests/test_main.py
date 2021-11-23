from pragmatic_business_rules import process_rules
import pytest


class TestProcessRules:

	def test_assert_rule_schema(self):
		with pytest.raises(
			Exception,
			match="Invalid input for 'rules': 'actions' is a required property",
		):
			process_rules(
				[
					{
						"conditions": {
							"all": [],
						},
					},
				],
				{},
			)

		with pytest.raises(
			Exception,
			match="Invalid input for 'rules': The provided type for the action is invalid",
		):
			process_rules(
				[
					{
						"actions": {
							"unknown rule": {
								"set": True,
							},
						},
						"conditions": {
							"all": [],
						},
					},
				],
				{},
			)

		with pytest.raises(
			Exception,
			match="Invalid input for 'rules': The provided operator for the condition is invalid",
		):
			process_rules(
				[
					{
						"actions": {},
						"conditions": {
							"all": [{
								"name": "variable",
								"operator": "invalid operator",
								"value": 1,
							}],
						},
					},
				],
				{},
			)

	def test_assert_variable_schema(self):
		with pytest.raises(
			Exception,
			match="Invalid input for 'variables': {} is not of type 'null', 'number', 'string'",
		):
			process_rules(
				[],
				{
					"an object": {},
				},
			)

	def test_assert_single_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' and 'any' properties can't be specified for the same conditional"
		):
			process_rules(
				[
					{
						"actions": {},
						"conditions": {
							"all": [],
							"any": []
						},
					},
				],
				{},
			)

	def test_assert_valid_conditional(self):
		with pytest.raises(
			Exception,
			match="'all' or 'any' properties were not found in the conditional"
		):
			process_rules(
				[
					{
						"actions": {},
						"conditions": {},
					},
				],
				{},
			)

	def test_apply_no_action(self):
		item_name = "single key"
		current_item_value = 42.12
		expected_item_value = 99
		variable_name = "some variable"
		variable_value = "xyz"

		result = process_rules(
			[
				{
					"actions": {
						item_name: {
							"set": expected_item_value
						}
					},
					"conditions": {
						"any": [{
							"name": variable_name,
							"operator": "equal_to",
							"value": variable_value + "abc",
						}],
					}
				},
			],
			{
				item_name: current_item_value,
				variable_name: variable_value,
			},
		)

		assert result.get(item_name) == current_item_value

	def test_apply_single_action(self):
		item_name = "single key"
		item_value = 1
		variable_name = "some variable"
		variable_value = 77

		result = process_rules(
			[
				{
					"actions": {
						item_name: {
							"set": item_value
						}
					},
					"conditions": {
						"any": [{
							"name": variable_name,
							"operator": "equal_to",
							"value": variable_value,
						}],
					}
				},
			],
			{
				item_name: item_value - 1,
				variable_name: variable_value,
			},
		)

		assert result.get(item_name) == item_value

	def test_not_apply_invalid_condition(self):
		item_name = "single key"
		current_item_value = 0
		expected_item_value = 1
		variable_name = "some variable"
		variable_value = 77

		result = process_rules(
			[
				{
					"actions": {
						item_name: {
							"set": expected_item_value
						}
					},
					"conditions": {
						"any": [{
							"name": variable_name,
							"operator": "less_than",
							"value": variable_value,
						}],
					}
				},
			],
			{
				item_name: expected_item_value - 1,
				variable_name: variable_value,
			},
		)

		assert result.get(item_name) == current_item_value

	def test_apply_multiple_actions(self):
		item_1_name = "some item name"
		item_1_value = 1
		item_2_name = "some other item name"
		item_2_value = "asd"
		variable_1_name = "some variable"
		variable_1_value = 12
		variable_2_name = "other_variable"
		variable_2_value = 241.7

		result = process_rules(
			[
				{
					"actions": {
						item_1_name: {
							"set": item_1_value
						}
					},
					"conditions": {
						"any": [{
							"name": variable_1_name,
							"operator": "equal_to",
							"value": variable_1_value,
						}],
					}
				},
				{
					"actions": {
						item_2_name: {
							"set": item_2_value
						}
					},
					"conditions": {
						"all": [
							{
								"name": variable_1_name,
								"operator": "equal_to",
								"value": variable_1_value,
							},
							{
								"name": variable_2_name,
								"operator": "equal_to",
								"value": variable_2_value,
							},
						],
					}
				},
			],
			{
				item_1_name: item_1_value - 100,
				item_2_name: item_2_value + "123",
				variable_1_name: variable_1_value,
				variable_2_name: variable_2_value,
			},
		)

		assert result.get(item_1_name) == item_1_value
		assert result.get(item_2_name) == item_2_value
