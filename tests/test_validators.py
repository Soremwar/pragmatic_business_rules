from src.validators import plain_dictionary_schema
import jsonschema
from jsonschema.exceptions import ValidationError
import pytest


def test_plain_dictionary_schema():
	jsonschema.validate({}, plain_dictionary_schema)
	jsonschema.validate(
		{
			"string": "some string",
			"int": 1,
			"float": 2.5,
		},
		plain_dictionary_schema,
	)

	with pytest.raises(
		ValidationError,
		match="{} is not of type 'number', 'string'",
	):
		jsonschema.validate(
			{
				"an object": {},
			},
			plain_dictionary_schema,
		)
