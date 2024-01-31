from guardrails import Guard
from pydantic import BaseModel, Field
from validator import CsvMatch


class ValidatorTestObject(BaseModel):
    test_val: str = Field(
        validators=[
            CsvMatch(csv="header1,header2\nrow1col1,row1col2\n", on_fail="exception")
        ]
    )


TEST_OUTPUT = """
header1,header2
row1col1,row1col2
"""


guard = Guard.from_pydantic(output_class=ValidatorTestObject)

raw_output, guarded_output, *rest = guard.parse(TEST_OUTPUT)

print("validated output: ", guarded_output)


TEST_FAIL_OUTPUT = """
header1,header2
row1col1
"""

try:
  guard.parse(TEST_FAIL_OUTPUT)
  print ("Failed to fail validation when it was supposed to")
except (Exception):
  print ('Successfully failed validation when it was supposed to')