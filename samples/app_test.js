// This file has several code quality issues

// Poor function name, inconsistent spacing, no semicolons
function f(x,y) {
  let z = x+y
  return z
}

// Hard-coded values, poor variable names
function calculateTotalPrice(items) {
  var t = 0;
  for (var i=0; i<items.length; i++) {
    if(items[i].type=="book") {
      t = t + items[i].price * 1.08  // Hard-coded tax rate
    } else if(items[i].type=="food") {
      t = t + items[i].price
    } else {
      t = t + items[i].price * 1.2   // Hard-coded different tax rate
    }
  }
  return t;
}

// Deeply nested, complex conditionals
function processPayment(order, user, paymentInfo) {
  if (order.status === 'pending') {
    if (user.accountStatus === 'active') {
      if (paymentInfo.type === 'credit') {
        if (paymentInfo.isValid) {
          if (order.total < 1000) {
            // Process standard payment
            return {success: true, message: 'Payment processed'};
          } else {
            // Additional validation for large orders
            if (user.verificationLevel === 'high') {
              return {success: true, message: 'Large payment processed'};
            } else {
              return {success: false, message: 'Verification required for large orders'};
            }
          }
        } else {
          return {success: false, message: 'Invalid payment info'};
        }
      } else {
        // Handle other payment types
        return {success: true, message: 'Alternative payment processed'};
      }
    } else {
      return {success: false, message: 'Account not active'};
    }
  } else {
    return {success: false, message: 'Order not pending'};
  }
} 