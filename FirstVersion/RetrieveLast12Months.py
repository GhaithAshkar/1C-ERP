from PySide6.QtCore import QObject, Signal, Slot
import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, Property

# Mock data for the last 12 months
mock_1c_data = {
    "January": [
        {"id": "1", "name": "Laptop", "quantity": 150},
        {"id": "2", "name": "TV", "quantity": 100}
    ],
    "February": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "March": [
        {"id": "1", "name": "Laptop", "quantity": 180},
        {"id": "2", "name": "TV", "quantity": 90}
    ],

    "April": [
        {"id": "1", "name": "Laptop", "quantity": 170},
        {"id": "2", "name": "TV", "quantity": 100}
    ],

    "May": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "June": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "July": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "August": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "September": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "October": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "November": [
        {"id": "1", "name": "Laptop", "quantity": 200},
        {"id": "2", "name": "TV", "quantity": 120}
    ],

    "December": [
        {"id": "1", "name": "Laptop", "quantity": 800},
        {"id": "2", "name": "TV", "quantity": 120}
    ]

}

class Backend(QObject):
    dataChanged = Signal()  # Signal to notify QML about data updates

    def __init__(self):
        super().__init__()
        self._result_data = ""

    @Property(str, notify=dataChanged)
    def result_data(self):
        return self._result_data

    @result_data.setter
    def result_data(self, value):
        if self._result_data != value:
            self._result_data = value
            self.dataChanged.emit()

    @Slot()
    def calculate_and_send_data(self):
        """Calculate yearly averages and analyze monthly sales"""
        try:
            print("DEBUG: Starting calculation...")  # Debug statement

            # Step 1: Calculate yearly averages for each product
            product_stats = {}
            for month_data in mock_1c_data.values():
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
                pid: stats["total_quantity"] / stats["count"]
                for pid, stats in product_stats.items()
            }

            # Step 2: Analyze each month's data
            result_table = []
            result_table.append("Month | Product Name | Monthly Sales | Yearly Average | % Change | Status")
            result_table.append("-" * 70)
            for month_name, products in mock_1c_data.items():
                for product in products:
                    pid = product["id"]
                    monthly_sales = product["quantity"]
                    yearly_avg = yearly_averages[pid]
                    percentage_change = ((monthly_sales - yearly_avg) / yearly_avg) * 100

                    status = (
                        "Green" if percentage_change >= 10 else
                        ("Red" if percentage_change <= -10 else "Neutral")
                    )

                    result_table.append(f"{month_name} | {product['name']} | {monthly_sales} | "
                                        f"{round(yearly_avg, 2)} | {round(percentage_change, 2)}% | {status}")

            # Step 3: Format the result for display in QML
            self.result_data = "\n".join(result_table)
            print("DEBUG: Result data prepared.")  # Debug statement

        except Exception as e:
            self.result_data = f"Error: {str(e)}"
            print(f"DEBUG: Error occurred - {str(e)}")  # Debug statement


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("RL12M.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
