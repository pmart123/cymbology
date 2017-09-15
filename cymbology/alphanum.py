import string
from types import MappingProxyType

# character map
CHAR_MAP = MappingProxyType(
    dict(zip(string.digits + string.ascii_uppercase, range(0, 36)))
)
