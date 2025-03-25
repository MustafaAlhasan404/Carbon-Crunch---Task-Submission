"""Sample Python file with code quality issues"""

from math import *
import random

def CalculateTotal(orders):
    sum = 0
    for i in orders:
        sum += i["value"]
    return sum

class userProfile:
    def __init__(self, Name, Age):
        self.Name = Name
        self.Age = Age
    
    def printInfo(self):
        print(f"User: {self.Name}, Age: {self.Age}")
        return None

def process_order(orderID, items, apply_discount = False):
    # Calculate the total
    total = CalculateTotal(items)
    
    # Apply discount if needed
    if apply_discount == True:
        if total > 100:
            total = total * 0.9
        else:
            total = total * 0.95
    
    # Calculate tax
    tax = total * 0.1
    
    # Return the result
    return {
        "order_id": orderID,
        "total": total,
        "tax": tax,
        "grand_total": total + tax
    }

def generate_report():
    """Generate a sales report"""
    try:
        # Simulate loading data
        data = [{"id": 1, "value": 10}, {"id": 2, "value": 20}]
        result = process_order("ORD123", data)
        
        # Print the report
        print("====== REPORT ======")
        print(f"Order ID: {result['order_id']}")
        print(f"Total: ${result['total']}")
        print(f"Tax: ${result['tax']}")
        print(f"Grand Total: ${result['grand_total']}")
        print("====================")
    except:
        print("Error generating report") 