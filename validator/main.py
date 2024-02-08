from typing import Any, Callable, Dict, Optional
from validator.parse_csv import parse_csv

from guardrails.validator_base import (
    FailResult,
    PassResult,
    ValidationResult,
    Validator,
    register_validator,
)


@register_validator(name="hyparam/valid_csv", data_type="string")
class CsvMatch(Validator):
    """Validates that a value matches a CSV text string.

    **Key Properties**

    | Property                      | Description                       |
    | ----------------------------- | --------------------------------- |
    | Name for `format` attribute   | `csv_match`                     |
    | Supported data types          | `string`                          |
    | Programmatic fix              | Generate a string that matches the regular expression |

    Args:
        delimiter: String delimiter for csv
    """  # noqa

    def __init__(
        self,
        delimiter: str = ",",
        on_fail: Optional[Callable] = None,
    ):
        super().__init__(on_fail=on_fail, delimiter=delimiter)
        self._delimiter = delimiter

    def validate(self, value: Any, metadata: Dict) -> ValidationResult:
        """Validates that value matches the provided regular expression."""
        try:
            rows = parse_csv(value)
        except Exception as e:
            return FailResult(
                error_message=f"Failed to parse CSV: {e}",
                fix_value="",
            )
        # TODO: Check that quoted strings match

        # Check that line lengths match
        first_row_length = len(rows[0])
        for row in rows:
            if len(row) != first_row_length:
                return FailResult(
                    error_message=f"CSV has rows of different lengths",
                    fix_value="",
                )

        return PassResult()

    def to_prompt(self, with_keywords: bool = True) -> str:
        return "results should match "
