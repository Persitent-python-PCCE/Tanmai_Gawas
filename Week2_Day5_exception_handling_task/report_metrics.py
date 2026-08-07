def average_order_value(total_revenue, num_orders):
    """Return the average revenue per order for a reporting period."""
    # TODO: total_revenue / num_orders raises ZeroDivisionError when a# period has 0 orders. Handle it and return 0.0 instead of crashing.
    try:
        avg = total_revenue / num_orders
        return round(avg, 2)
    except ZeroDivisionError:
        return 0.0
    
def project_revenue(current_revenue, growth_rate, periods): 
    """Project revenue compounding at 'growth_rate' over N periods."""
    # TODO: with a very large 'periods', the result raises OverflowError.
    # Handle OverflowError, and add a general ArithmeticError safety net.
    try:
        projected = current_revenue * (1.0 + growth_rate) ** periods
        return round(projected, 2)
    except OverflowError:
        print("Error: Revenue projection is too large to calculate.")
        return None
    except ArithmeticError:
        print("Error: An arithmetic error occurred during calculation.")
        return None
    
# - Test cases (do not change) -
print(average_order_value(15000, 120)) # 125.0
print(average_order_value(15000, 0)) # must NOT crash > 0.0
print(project_revenue(50000, 0.08, 5)) # normal projection
print(project_revenue(1e6, 8.0, 100000)) # must NOT crash (overflow)
