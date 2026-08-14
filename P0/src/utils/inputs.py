def get_int_input(prompt, min_val=None, max_val=None, allow_blank=False):
    """Safely prompt and parse integer inputs from the console."""
    while True:
        val = input(prompt).strip()
        if allow_blank and not val:
            return None
        try:
            num = int(val)
            if min_val is not None and num < min_val:
                print(f"  [!] Please enter an integer >= {min_val}.")
                continue
            if max_val is not None and num > max_val:
                print(f"  [!] Please enter an integer <= {max_val}.")
                continue
            return num
        except ValueError:
            print("  [!] Invalid input. Please enter a valid integer.")

def get_float_input(prompt, min_val=None, allow_blank=False):
    """Safely prompt and parse decimal/float inputs from the console."""
    while True:
        val = input(prompt).strip()
        if allow_blank and not val:
            return None
        try:
            num = float(val)
            if min_val is not None and num < min_val:
                print(f"  [!] Please enter a number >= {min_val}.")
                continue
            return num
        except ValueError:
            print("  [!] Invalid input. Please enter a valid decimal number.")
