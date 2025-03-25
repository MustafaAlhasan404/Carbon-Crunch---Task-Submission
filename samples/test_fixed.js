// This file contains several code quality issues to test the GitHub Actions workflow

// Poor function name and parameter naming
function fn(a, b) {
    var r = a + b;
    return r;
}

// Missing semicolons and inconsistent formatting
function calculateTotal(items) {
  var total = 0
  for(var i=0; i<items.length; i++) {
    total += items[i].price
  }
  return total
}

// Deeply nested conditionals
function processOrder(order, user) {
    if (order.status === 'new') {
        if (user.verified) {
            if (order.paymentMethod === 'credit') {
                if (order.items.length > 0) {
                    if (order.total < 1000) {
                        return 'Processing standard order';
                    } else {
                        if (user.premiumMember) {
                            return 'Processing premium order';
                        } else {
                            return 'Additional verification needed';
                        }
                    }
                } else {
                    return 'Empty order';
                }
            } else {
                return 'Alternative payment method';
            }
        } else {
            return 'User not verified';
        }
    } else {
        return 'Order already processed';
    }
} 