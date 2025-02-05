# yearly_average.py

mock_yearly_data = {
    "January": [
        {"id": "1", "name": "Laptop", "quantity": 20},
        {"id": "2", "name": "TV", "quantity": 1000}

    ],
    "February": [
        {"id": "1", "name": "Laptop", "quantity": 120},
        {"id": "2", "name": "TV", "quantity": 180},
        {"id": "3", "name": "Keyboard", "quantity": 110},
        {"id": "4", "name": "Mouse", "quantity": 190}
    ],
    "March": [
        {"id": "1", "name": "Laptop", "quantity": 130},
        {"id": "2", "name": "TV", "quantity": 190},
        {"id": "3", "name": "Keyboard", "quantity": 120},
        {"id": "4", "name": "Mouse", "quantity": 200}
    ],
    "April": [
        {"id": "1", "name": "Laptop", "quantity": 140},
        {"id": "2", "name": "TV", "quantity": 200},
        {"id": "3", "name": "Keyboard", "quantity": 130},
        {"id": "4", "name": "Mouse", "quantity": 210}
    ],
    "May": [
        {"id": "1", "name": "Laptop", "quantity": 150},
        {"id": "2", "name": "TV", "quantity": 220},
        {"id": "3", "name": "Keyboard", "quantity": 140},
        {"id": "4", "name": "Mouse", "quantity": 220}
    ],
    "June": [
        {"id": "1", "name": "Laptop", "quantity": 160},
        {"id": "2", "name": "TV", "quantity": 230},
        {"id": "3", "name": "Keyboard", "quantity": 150},
        {"id": "4", "name": "Mouse", "quantity": 230}
    ],
    "July": [
        {"id": "1", "name": "Laptop", "quantity": 170},
        {"id": "2", "name": "TV", "quantity": 240},
        {"id": "3", "name": "Keyboard", "quantity": 160},
        {"id": "4", "name": "Mouse", "quantity": 240}
    ],
    "August": [
        {"id": "1", "name": "Laptop", "quantity": 180},
        {"id": "2", "name": "TV", "quantity": 250},
        {"id": "3", "name": "Keyboard", "quantity": 170},
        {"id": "4", "name": "Mouse", "quantity": 250}
    ],
    "September": [
        {"id": "1", "name": "Laptop", "quantity": 190},
        {"id": "2", "name": "TV", "quantity": 260},
        {"id": "3", "name": "Keyboard", "quantity": 180},
        {"id": "4", "name": "Mouse", "quantity": 260}
    ],
    "October": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 270},
        {"id": "3", "name": "Keyboard", "quantity": 190},
        {"id": "4", "name": "Mouse", "quantity": 270}
    ],
    "November": [
        {"id": "1", "name": "Laptop", "quantity": 210},
        {"id": "2", "name": "TV", "quantity": 280},
        {"id": "3", "name": "Keyboard", "quantity": 200},
        {"id": "4", "name": "Mouse", "quantity": 280}
    ],
    "December": [
        {"id": "1", "name": "Laptop", "quantity": 220},
        {"id": "2", "name": "TV", "quantity": 290},
        {"id": "3", "name": "Keyboard", "quantity": 210},
        {"id": "4", "name": "Mouse", "quantity": 290}
        ]


}

def calculate_yearly_averages(data):
    """Calculate yearly averages for each product."""
    product_stats = {}

    for month_data in data.values():
        for product in month_data:
            pid = product["id"]
            if pid not in product_stats:
                product_stats[pid] = {
                    "name": product["name"],
                    "total_quantity": 0,
                    "count": 0
                }
            product_stats[pid]["total_quantity"] += product["quantity"]
            product_stats[pid]["count"] += 1

    yearly_averages = {
        #pid: stats["total_quantity"] / stats["count"]
        pid: stats["total_quantity"] / 12
        for pid, stats in product_stats.items()
    }

    return yearly_averages


if __name__ == "__main__":
    averages = calculate_yearly_averages(mock_yearly_data)
    print("Yearly Averages:", averages)