def parse_csv(text: str) -> list[list[str]]:
    """
    Parse CSV text into a nested list of rows and columns.

    Args:
    text (str): The CSV formatted string to be parsed.

    Returns:
    list[list[str]]: A nested list where each sublist represents a row and each string within a sublist represents a column.
    """
    rows = []
    row = []
    field = ''
    in_quotes = False
    previous_char_was_quote = False

    for char in text:
        if in_quotes and char == '"' and not previous_char_was_quote:
            # First quote, wait to see if it's escaped or end of field
            previous_char_was_quote = True
        elif in_quotes and char == '"' and previous_char_was_quote:
            # CSV escaped quote
            field += char
            previous_char_was_quote = False
        elif in_quotes and not previous_char_was_quote:
            # Append quoted character to field
            field += char
        else:
            # Not in quotes
            in_quotes = False
            previous_char_was_quote = False
            if char == ',':
                # Emit column
                row.append(field)
                field = ''
            elif char == '\n':
                # Emit row
                row.append(field)
                rows.append(row)
                row = []
                field = ''
            elif char == '"':
                in_quotes = True
            else:
                field += char

    # Handle last field and row, but skip empty last line
    if field or row:
        row.append(field)
        rows.append(row)

    return rows
