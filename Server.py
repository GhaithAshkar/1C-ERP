import sys
from PySide6.QtCore import QObject, Slot, QUrl, Property, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import pandas as pd
from collections import defaultdict


class Backend(QObject):
    summaryChanged = Signal()

    def __init__(self):
        super().__init__()
        self.files_data = []
        self._summary = "No data loaded yet"

    @Property(str, notify=summaryChanged)
    def summary(self):
        return self._summary

    @Slot(str)
    def readFiles(self, fileUrls):
        try:
            self.files_data = []
            urls = fileUrls.split(',')
            for url in urls:
                local_path = QUrl(url).toLocalFile()
                df = pd.read_excel(
                    local_path,
                    skiprows=4,  # Skip header rows
                    usecols=[1, 5]  # Product name and quantity columns
                )
                self.files_data.append(df)
                print(f"Successfully loaded file: {local_path}")

            print(f"Total files processed: {len(self.files_data)}")
            self.calculateAverages()

        except Exception as e:
            self._summary = f"Error processing files: {str(e)}"
            self.summaryChanged.emit()

    def calculateAverages(self):
        try:
            if not self.files_data:
                self._summary = "No files loaded"
                self.summaryChanged.emit()
                return

            # Initialize data structure for tracking products
            product_data = defaultdict(lambda: {
                'total_quantity': 0,
                'appearances': 0,
                'monthly_values': []
            })

            # Process each file (month)
            for df in self.files_data:
                processed_products = set()  # Track products in current file

                for _, row in df.iterrows():
                    product_name = str(row.iloc[0]).strip()
                    if pd.notna(row.iloc[1]) and pd.notna(product_name):
                        try:
                            quantity = float(row.iloc[1])
                            product_data[product_name]['total_quantity'] += quantity
                            if product_name not in processed_products:
                                product_data[product_name]['appearances'] += 1
                                processed_products.add(product_name)
                            product_data[product_name]['monthly_values'].append(quantity)
                        except (ValueError, TypeError):
                            continue

            # Format results
            summary_lines = ["Product Sales Analysis\n", "=" * 50 + "\n"]

            # Sort products by average sales
            sorted_products = sorted(
                product_data.items(),
                key=lambda x: x[1]['total_quantity'] / x[1]['appearances'] if x[1]['appearances'] > 0 else 0,
                reverse=True
            )

            for product, data in sorted_products:
                avg = data['total_quantity'] / data['appearances'] if data['appearances'] > 0 else 0
                summary_lines.extend([
                    f"Product: {product}\n",
                    f"Total Sales: {data['total_quantity']:.2f}\n",
                    f"Appears in {data['appearances']} of {len(self.files_data)} files\n",
                    f"Average per appearance: {avg:.2f}\n",
                    f"Monthly values: {', '.join(f'{v:.2f}' for v in data['monthly_values'])}\n",
                    "-" * 50 + "\n\n"
                ])

            self._summary = "".join(summary_lines)
            self.summaryChanged.emit()

        except Exception as e:
            self._summary = f"Error calculating averages: {str(e)}"
            self.summaryChanged.emit()


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = Backend()

    engine.rootContext().setContextProperty("backend", backend)
    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())