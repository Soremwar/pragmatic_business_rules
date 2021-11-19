import pytest
from src.condition import assert_single_conditional

class TestAssertSingleConditional:
	def test_single_conditional(self):
		with pytest.raises(Exception, match="'all' and 'any' properties can't be specified for the same conditional") as e:
			assert_single_conditional({
				"all": [],
				"any": []
			})

	def test_valid_conditional(self):
		with pytest.raises(Exception, match="'all' or 'any' properties were not found in the conditional") as e:
			assert_single_conditional({})