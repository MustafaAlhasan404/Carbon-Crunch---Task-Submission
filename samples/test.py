# app.py
def calculate_total(orders):
    """Calculate the total value of all orders.
    
    Args:
        orders: List of order dictionaries containing 'value' keys
        
    Returns:
        total: The sum of all order values
    """
    total = 0
    for order in orders:
        total += order["value"]
    return total