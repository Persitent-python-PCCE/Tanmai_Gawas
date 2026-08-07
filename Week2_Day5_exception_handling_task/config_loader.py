def load_config(path):
    """Read and print each line of an application config file."""
    # TODO:
    # 1) open(path) raises FileNotFoundError if the file is missing -
    # handle it with a clear message.
    # 2) Reading can raise OSError (IOError is an alias for it) - handle it too.
    # 3) Use 'finally' to ALWAYS print: "config load attempt finished".
    try:
        f = open(path, "r")
        for line in f:
            print(line.strip())
        f.close()
    except FileNotFoundError as fe:
        print("File Not Found",fe)
    except IOError as ie:
        print("Cannot Read File",ie)
    finally:
        print("config load attempt finished")

# - Test cases -
load_config("app.config") # may or may not exist
load_config("does_not_exist.cfg") # must be handled gracefully