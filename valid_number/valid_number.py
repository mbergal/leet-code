import re
def _or(*args:str):
    return "(" + "|".join([f"({x})" for x in args]) + ")"

def _optional(re: str):
    return f"({re})?"

def _one_or_more(re: str):
    return f"({re})+"

sign = r"[\+\-]"
integer=_optional(sign) + _one_or_more(r"\d")
decimal_number = _optional(sign) + _or(
    _one_or_more(r"\d") + r"\.",
    _one_or_more(r"\d") + r"\." + _one_or_more(r"\d"),
    r"\." + _one_or_more(r"\d")
)
number = _or(decimal_number,integer) + _optional("[eE]"+integer)


def is_valid_number(str: str):
    return re.fullmatch(number, str) is not None

# A decimal number or an integer.
# (Optional) An 'e' or 'E', followed by an integer.

# A decimal number can be split up into these components (in order):

# (Optional) A sign character (either '+' or '-').
# One of the following formats:
# One or more digits, followed by a dot '.'.
# One or more digits, followed by a dot '.', followed by one or more digits.
# A dot '.', followed by one or more digits.
# An integer can be split up into these components (in order):

# (Optional) A sign character (either '+' or '-').
# One or more digits.

# decimal_number|integer[e|E]integer
# decimal_number=[+-](\d+\.)|(\d+\.\d+)|(\.\d+)

def main():
    """
    >>> re.fullmatch(sign, "+")[0]
    '+'
    >>> re.fullmatch(sign, "-")[0]
    '-'
    >>> re.fullmatch(sign, "*")
    >>> re.fullmatch(integer, "1")[0]
    '1'
    >>> re.fullmatch(integer, "1111")[0]
    '1111'
    >>> re.fullmatch(integer, "+1111")[0]
    '+1111'
    >>> re.fullmatch(integer, "-1111")[0]
    '-1111'
    >>> re.fullmatch(decimal_number, "1.")[0]
    '1.'
    >>> re.fullmatch(decimal_number, "1.1")[0]
    '1.1'
    >>> re.fullmatch(decimal_number, ".1")[0]
    '.1'
    >>> re.fullmatch(decimal_number, "-.1")[0]
    '-.1'
    >>> re.fullmatch(decimal_number, "+1.1")[0]
    '+1.1'
    >>> is_valid_number("+1.1E1")
    True
    >>> is_valid_number("2")
    True
    >>> is_valid_number("0089")
    True
    >>> is_valid_number("-0.1")
    True
    >>> is_valid_number("+3.14")
    True
    >>> is_valid_number("4.")
    True
    >>> is_valid_number("-.9")
    True
    >>> is_valid_number("2e10")
    True
    >>> is_valid_number("-90E3")
    True
    >>> is_valid_number("3e+7")
    True
    >>> is_valid_number("+6e-1")
    True
    >>> is_valid_number("53.5e93")
    True
    >>> is_valid_number("-123.456e789")
    True
    >>> is_valid_number("0")
    True
    >>> is_valid_number("e")
    False
    >>> is_valid_number(".")
    False
    >>> is_valid_number("abc")
    False
    >>> is_valid_number("1a")
    False
    >>> is_valid_number("1e")
    False
    >>> is_valid_number("1e")
    False
    >>> is_valid_number("e3")
    False
    >>> is_valid_number("99e2.5")
    False
    >>> is_valid_number("--6")
    False
    >>> is_valid_number("-+3")
    False
    >>> is_valid_number("95a54e53")
    False

    
    
    """

if __name__ == "__main__":
    import doctest
    doctest.testmod()
