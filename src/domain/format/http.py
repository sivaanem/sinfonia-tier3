from pprint import PrettyPrinter

from src.lib.http import HTTPStatus


def status_code_repr(code: int) -> str:
    """Return HTTP status code along with its descriptive phrase.
    
    Example:
        200 -> 200 OK
    
    Args:
        code -- int: HTTP status code
        
    Return:
        str -- Status code representation
    """
    return f"{str(code)} {HTTPStatus(code).phrase}"


def json_repr(
        j: str,
        indent: int = 2,
        width: int = 90,
) -> str:
    """Prettify JSON string.
    
    Args:
        j -- str: JSON string
        indent -- int: Indent level (spaces) [default = 2]
        width -- int: Maximum line width (spaces) [default = 90]
        
    Return:
        str -- Prettified JSON string
    """    
    pp = PrettyPrinter(indent=2, width=90)
    return pp.format(j)


def json_repr(
        j: str,
        indent: int = 2,
        width: int = 90,
) -> str:
    """Prettify JSON string.
    
    Args:
        j -- str: JSON string
        indent -- int: Indent level (spaces) [default = 2]
        width -- int: Maximum line width (spaces) [default = 90]
        
    Return:
        str -- Prettified JSON string
    """    
    pp = PrettyPrinter(indent=indent, width=width)
    return pp.pformat(j)
