# This object will match any object with no nested properties and all items being
# either strings or numbers
plain_dictionary_schema = {
	"additionalProperties": False,
	"patternProperties": {
		".+": {
			"type": [
				"number",
				"string",
			]
		},
	},
	"type": "object",
}
