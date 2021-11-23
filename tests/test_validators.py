from jsonschema.exceptions import ValidationError
from pragmatic_business_rules.validators import variable_schema
import jsonschema
import pytest


def test_plain_dictionary_schema():
	jsonschema.validate({}, variable_schema)
	jsonschema.validate(
		{
			"string": "some string",
			"int": 1,
			"float": 2.5,
			"none": None
		},
		variable_schema,
	)

	with pytest.raises(
		ValidationError,
		match="{} is not of type 'null', 'number', 'string'",
	):
		jsonschema.validate(
			{
				"an object": {},
			},
			variable_schema,
		)
