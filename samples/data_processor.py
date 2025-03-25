# This Python file contains intentional code quality issues

# Poor function name and no docstring
def fn(l):
    r = []
    for i in range(len(l)):
        if l[i] > 0:
            r.append(l[i] * 2)
        else:
            r.append(0)
    return r

# Hard-coded values and magic numbers
def calculate_score(answers):
    total = 0
    for answer in answers:
        if answer.correct:
            total += 10  # Magic number
        elif answer.partially_correct:
            total += 5   # Magic number
        else:
            total -= 2   # Magic number
            
    # Hard-coded grade boundaries
    if total >= 90:
        return "A"
    elif total >= 80:
        return "B"
    elif total >= 70:
        return "C"
    elif total >= 60:
        return "D"
    else:
        return "F"

# Overly complex function with too many responsibilities
def process_user_data(data):
    # Validate data
    if not data or "users" not in data:
        return {"error": "Invalid data format"}
    
    # Process users
    processed_users = []
    for user in data["users"]:
        # Data validation
        if "name" not in user or "email" not in user:
            continue
        
        # Email validation - complex regex in-line
        import re
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user["email"]):
            continue
        
        # Format user data
        formatted_user = {
            "display_name": user["name"].title(),
            "contact": user["email"].lower(),
            "joined_date": user.get("joined", "N/A"),
            "role": user.get("role", "user"),
            "active": user.get("status", "inactive") == "active"
        }
        
        # Calculate permissions
        permissions = []
        if formatted_user["role"] == "admin":
            permissions = ["read", "write", "delete", "manage"]
        elif formatted_user["role"] == "editor":
            permissions = ["read", "write"]
        else:
            permissions = ["read"]
        
        formatted_user["permissions"] = permissions
        processed_users.append(formatted_user)
    
    # Generate statistics
    stats = {
        "total_users": len(processed_users),
        "active_users": sum(1 for user in processed_users if user["active"]),
        "roles": {}
    }
    
    for user in processed_users:
        role = user["role"]
        if role in stats["roles"]:
            stats["roles"][role] += 1
        else:
            stats["roles"][role] = 1
    
    return {
        "processed_users": processed_users,
        "statistics": stats
    } 