# monthly_analysis.py

from yearly_average import calculate_yearly_averages, mock_yearly_data

def get_all_product_ids(data):
    """Get a list of all unique product IDs across all months."""
    all_products = {}
    for month_data in data.values():
        for product in month_data:
            all_products[product["id"]] = product["name"]
    return all_products


def analyze_monthly_data(yearly_data, month_name, yearly_averages):
    """Analyze sales for a specific month against yearly averages."""
    if month_name not in yearly_data:
        raise ValueError(f"Month '{month_name}' not found in the dataset.")

    # Get all unique products across all months
    all_products = get_all_product_ids(yearly_data)

    # Get the specific month's data
    month_data = {product["id"]: product for product in yearly_data[month_name]}

    result_table = []
    result_table.append("Product Name | Monthly Sales | Yearly Average | % Change | Status")
    result_table.append("-" * 60)

    for pid, name in all_products.items():
        monthly_sales = month_data.get(pid, {"quantity": 0})["quantity"]
        yearly_avg = yearly_averages.get(pid, 0)
        percentage_change = ((monthly_sales - yearly_avg) / yearly_avg) * 100 if yearly_avg != 0 else 0

        status = (
            "Green" if percentage_change >= 10 else
            ("Red" if percentage_change <= -10 else "Neutral")
        )

        result_table.append(f"{name} | {monthly_sales} | "
                            f"{round(yearly_avg, 2)} | {round(percentage_change, 2)}% | {status}")

    return "\n".join(result_table)


if __name__ == "__main__":
    # Calculate yearly averages first
    yearly_averages = calculate_yearly_averages(mock_yearly_data)

    # Analyze sales for January (default)
    report = analyze_monthly_data(mock_yearly_data, "January", yearly_averages)
    print(report)
