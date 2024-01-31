from typing import Any, Callable, Dict, Optional
from validator.parse_csv import parse_csv

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="guardrails/csv_match", data_type="string")
class CsvMatch(Validator):
    """Validates that a value matches a CSV text string.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `csv_match`                     |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Generate a string that matches the regular expression |

    Args:
        csv: Str csv text contents
        delimiter: String delimiter for csv
    """  # noqa

    def __init__(
        self,
        csv: str,
        delimiter: str = ",",
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, csv=csv)
        self._csv = csv
        self._delimiter = delimiter

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        """Validates that value matches the provided regular expression."""

        try:
            csv = parse_csv(self._csv)
        except Exception as e:
            return FailResult(
                error_message=f"Failed to parse CSV: {e}",
                fix_value=self._csv,
            )
        # TODO: Check that quoted strings match

        # TODO: Check that line lengths match
        first_row_length = len(csv[0])
        for row in csv:
            if len(row) != first_row_length:
                return FailResult(
                    error_message=f"CSV has rows of different lengths",
                    fix_value=self._csv,
                )

        return PassResult()

    def to_prompt(self, with_keywords: bool = True) -> str:
        return "results should match " + self._regex
