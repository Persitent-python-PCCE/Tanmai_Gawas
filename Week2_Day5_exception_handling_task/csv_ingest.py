def parse_amount(raw):
    """Convert a raw text field (e.g. from a CSV) into a float amount."""
    # TODO: float(raw) raises ValueError for non-numeric text like 'N/A'.
    # Handle ValueError and return None for invalid input.
    try:
        return float(raw)
    except ValueError:
        return None


def column_total(values):
    """Sum a numeric column. A stray string entry raises TypeError."""
    # TODO: sum(values) raises TypeError if the column mixes numbers and text.
    # Handle TypeError and report that the column has a non-numeric value.
    try:
        return sum(values)
    except TypeError:
        print("The column has a non-numeric value.")
        return None


# - Test cases -
print(parse_amount("1999.50")) # 1999.5
print(parse_amount("N/A")) # handled > None
print(column_total([100, 250, 75])) # 425
print(column_total([100, "250", 75])) # handled, no crash