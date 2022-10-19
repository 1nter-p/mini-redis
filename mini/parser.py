class DataType:
    """An enum for the data types in the Redis protocol.
    Maps type names to their corresponding byte.
    """

    SIMPLE_STRING = 43
    ERROR = 45
    INTEGER = 58
    BULK_STRING = 36
    ARRAY = 42


def parse_redis(data: bytes) -> str | int | list[str] | list[int]:
    """Parse the data according to the Redis protocol.
    Redis protocol reference: https://redis.io/docs/reference/protocol-spec/
    """

    if data.strip() == b"":
        return None

    # The first byte of data indicates the data type
    type_byte = data[0]

    if type_byte in (
        DataType.SIMPLE_STRING,
        DataType.ERROR,
        DataType.BULK_STRING,
    ):
        return data[1:].decode().strip()

    if type_byte == DataType.ARRAY:
        # Get the raw elements (unparsed bytes)
        raw_elems = data[2:].split(b"\r\n")

        # Parse each element
        parsed_elems = [raw_elem.decode() for raw_elem in raw_elems]

        # Remove any elements starting with $
        parsed_elems = [elem for elem in parsed_elems if not elem.startswith("$")]

        # Remove the first and last elements, which are empty strings
        parsed_elems.pop(-1)
        parsed_elems.pop(0)

        return parsed_elems

    if type_byte == DataType.INTEGER:
        return int(data[1:].decode().strip())

    # If we don't know what the data type is, raise a ValueError
    raise ValueError(f"unknown data type: {type_byte}")
