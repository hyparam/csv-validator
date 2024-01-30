import re
import string
from typing import Any, Callable, Dict, Optional

import rstr

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

        # TODO: Check that line lengths match
        # TODO: Check that quoted strings match

        # Pad matching string on either side for fix
        # example if we are performing a regex search
        str_padding = (
            "" if self._match_type == "fullmatch" else rstr.rstr(string.ascii_lowercase)
        )
        self._fix_str = str_padding + rstr.xeger(self._regex) + str_padding

        if not getattr(p, self._match_type)(value):
            return FailResult(
                error_message=f"Result must match {self._regex}",
                fix_value=self._fix_str,
            )
        return PassResult()

    def to_prompt(self, with_keywords: bool = True) -> str:
        return "results should match " + self._regex
