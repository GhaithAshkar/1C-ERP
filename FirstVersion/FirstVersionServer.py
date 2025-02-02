from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)


mock_1c_data = {
    "2024-01": [
        {"id": "1", "name": "Laptop", "quantity": 150},
        {"id": "2", "name": "TV", "quantity": 100}
    ],
    "2024-02": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],
    "2024-03": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],
    "2024-04": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],
    "2024-05": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "2024-06": [
        {"id": "1", "name": "Laptop", "quantity": 180},
        {"id": "2", "name": "TV", "quantity": 90}
    ],

    "2024-07": [
        {"id": "1", "name": "Laptop", "quantity": 170},
        {"id": "2", "name": "TV", "quantity": 100}
    ],

    "2024-08": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "2024-09": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "2024-10": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "2024-11": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "2024-12": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ]



}


@app.route('/salesdata', methods=['GET'])
def get_sales_data():
    """Fetch all sales data or analyze specific month"""
    try:
        # Check if 'date' parameter is provided
        date = request.args.get('date')

        if date:
            # Analyze specific month
            return analyze_month(date)

        # Return all sales data
        return jsonify({
            "status": "success",
            "message": "Successfully retrieved all sales data.",
            "data": mock_1c_data
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


def analyze_month(date):
    """Analyze specific month compared to yearly average for each product"""
    try:
        # Validate date format
        try:
            parsed_date = datetime.strptime(date, "%Y-%m")  # Ensure date is in YYYY-MM format
        except ValueError:
            return jsonify({"status": "error", "message": "Invalid date format. Use YYYY-MM."}), 400

        # Extract year and month from the date
        year = date[:4]
        month = date[5:]

        # Filter data for the specified year
        yearly_data = {k: v for k, v in mock_1c_data.items() if k.startswith(year)}
        if not yearly_data or len(yearly_data) < 12:
            return jsonify({"status": "error", "message": f"Incomplete data for year {year}."}), 404

        # Get data for the specified month
        monthly_data = yearly_data.get(date)
        if not monthly_data:
            return jsonify({"status": "error", "message": f"No data found for {date}."}), 404

        # Calculate yearly averages and analyze each product
        product_stats = {}
        for month, products in yearly_data.items():
            for product in products:
                pid = product["id"]
                if pid not in product_stats:
                    product_stats[pid] = {
                        "name": product["name"],
                        "total_quantity": 0,
                        "count": 0
                    }
                product_stats[pid]["total_quantity"] += product["quantity"]
                product_stats[pid]["count"] += 1

        # Prepare analysis results for each product in the specified month
        results = []
        for product in monthly_data:
            pid = product["id"]
            stats = product_stats.get(pid)
            if not stats:
                continue

            monthly_sales = product["quantity"]
            yearly_avg = stats["total_quantity"] / stats["count"]  # Average per year (12 months)
            percentage_change = ((monthly_sales - yearly_avg) / yearly_avg) * 100

            results.append({
                "Product Name": stats["name"],
                "Monthly Sales": monthly_sales,
                "Yearly Average Sales": round(yearly_avg, 2),
                "% Change": round(percentage_change, 2),
                "Status": (
                    "Green" if percentage_change >= 10 else
                    ("Red" if percentage_change <= -10 else "Neutral")
                )
            })

        return jsonify({
            "status": "success",
            "message": f"Analysis for {date}",
            "data": results
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
