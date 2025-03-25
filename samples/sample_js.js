// This is a sample JavaScript file with some code quality issues

const User_Name = "John Doe";
const User_Age = 30;

function calculateTotal(items) {
    var sum = 0;
    for (var i = 0; i < items.length; i++) {
        sum = sum + items[i].price;
    }
    return sum;
}

const processOrder = async (order_id) => {
    const orderData = await fetch('https://api.example.com/orders/' + order_id)
    const data = orderData.json()
    
    const Total = calculateTotal(data.items)
    const Tax = Total * 0.1
    
    return {
        orderid: order_id,
        items: data.items,
        total: Total,
        tax: Tax,
        grandTotal: Total + Tax
    }
}

function renderItem(item) {
    console.log("Rendering item", item);
    return "<div class='item'>" + 
           "<h3>" + item.name + "</h3>" + 
           "<p>Price: $" + item.price + "</p>" + 
           "</div>";
} 