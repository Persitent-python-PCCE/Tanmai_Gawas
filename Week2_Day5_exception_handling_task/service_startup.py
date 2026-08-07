def get_json_parser():
    """Use the faster 'orjson' library if installed, else fall back."""
    # TODO: 'import orjson' raises ImportError (ModuleNotFoundError) when it
    # isn't installed. Handle it, print "orjson not available - falling
    # back to standard json", and import the built-in json instead.
    try:
        import orjson
        return orjson
    except ModuleNotFoundError:
        print("orjson not available - falling back to standard json")
        import json
        return json

class ReportService:
    def __init__(self):
        self.connected = False # connection not opened yet
    def run_query(self):
        if not self.connected:
            raise RuntimeError("Database connection not established.")
        return "query results"


def generate_report(service):
    """TODO: call service.run_query() inside try/except RuntimeError,
    print the error message, and keep the program running."""
    try:
        res = service.run_query()
        print(res)
    except RuntimeError as e:
        print(e)


# - Test cases -
get_json_parser() # handled > standard json fallback
generate_report(ReportService()) # RuntimeError handled, no crash
