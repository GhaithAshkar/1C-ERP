# import sys
# from PySide6.QtCore import QObject, Slot, QUrl, Property, Signal
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtQml import QQmlApplicationEngine
# import pandas as pd
# from collections import defaultdict


# class Backend(QObject):
#     summaryChanged = Signal()
#
#     def __init__(self):
#         super().__init__()
#         self.files_data = []
#         self._summary = "No data loaded yet"
#
#     @Property(str, notify=summaryChanged)
#     def summary(self):
#         return self._summary
#
#     @Slot(str)
#     def readFiles(self, fileUrls):
#         try:
#             self.files_data = []
#             urls = fileUrls.split(',')
#             for url in urls:
#                 local_path = QUrl(url).toLocalFile()
#                 df = pd.read_excel(
#                     local_path,
#                     skiprows=4,  # Skip header rows
#                     usecols=[1, 5]  # Product name and quantity columns
#                 )
#                 self.files_data.append(df)
#                 print(f"Successfully loaded file: {local_path}")
#
#             print(f"Total files processed: {len(self.files_data)}")
#             self.calculateAverages()
#
#         except Exception as e:
#             self._summary = f"Error processing files: {str(e)}"
#             self.summaryChanged.emit()
#
#     def calculateAverages(self):
#         try:
#             if not self.files_data:
#                 self._summary = "No files loaded"
#                 self.summaryChanged.emit()
#                 return
#
#             # Initialize data structure for tracking products
#             product_data = defaultdict(lambda: {
#                 'total_quantity': 0,
#                 'appearances': 0,
#                 'monthly_values': []
#             })
#
#             # Process each file (month)
#             for df in self.files_data:
#                 processed_products = set()  # Track products in current file
#
#                 for _, row in df.iterrows():
#                     product_name = str(row.iloc[0]).strip()
#                     if pd.notna(row.iloc[1]) and pd.notna(product_name):
#                         try:
#                             quantity = float(row.iloc[1])
#                             product_data[product_name]['total_quantity'] += quantity
#                             if product_name not in processed_products:
#                                 product_data[product_name]['appearances'] += 1
#                                 processed_products.add(product_name)
#                             product_data[product_name]['monthly_values'].append(quantity)
#                         except (ValueError, TypeError):
#                             continue
#
#             # Format results
#             summary_lines = ["Product Sales Analysis\n", "=" * 50 + "\n"]
#
#             # Sort products by average sales
#             sorted_products = sorted(
#                 product_data.items(),
#                 key=lambda x: x[1]['total_quantity'] / x[1]['appearances'] if x[1]['appearances'] > 0 else 0,
#                 reverse=True
#             )
#
#             for product, data in sorted_products:
#                 avg = data['total_quantity'] / data['appearances'] if data['appearances'] > 0 else 0
#                 summary_lines.extend([
#                     f"Product: {product}\n",
#                     f"Total Sales: {data['total_quantity']:.2f}\n",
#                     f"Appears in {data['appearances']} of {len(self.files_data)} files\n",
#                     f"Average per appearance: {avg:.2f}\n",
#                     f"Monthly values: {', '.join(f'{v:.2f}' for v in data['monthly_values'])}\n",
#                     "-" * 50 + "\n\n"
#                 ])
#
#             self._summary = "".join(summary_lines)
#             self.summaryChanged.emit()
#
#         except Exception as e:
#             self._summary = f"Error calculating averages: {str(e)}"
#             self.summaryChanged.emit()
#

import sys
from PySide6.QtCore import QObject, Slot, QUrl, Property, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import pandas as pd


class Backend(QObject):
    summaryChanged = Signal()

    def __init__(self):
        super().__init__()
        self.monthly_data = {}  # Format: {product: [month1_sales, month2_sales,...]}
        self.yearly_averages = {}
        self.summary = "No data loaded yet"
        self.report_data = []  # Stores generated report data for searching

    @Property(str, notify=summaryChanged)
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value
        self.summaryChanged.emit()

    @Slot(str)
    def readFiles(self, fileUrls):
        try:
            urls = fileUrls.split(',')
            if len(urls) != 12:
                raise ValueError("Exactly 12 monthly files are required.")

            print("DEBUG: Starting to process files...")

            # Process each file and extract data
            for month_index, url in enumerate(urls):
                local_path = QUrl(url).toLocalFile()
                df = pd.read_excel(local_path, skiprows=4, usecols=[1, 5])  # Product name and quantity columns

                for _, row in df.iterrows():
                    product_name = str(row.iloc[0]).strip().lower()  # Normalize product name to lowercase
                    if pd.notna(row.iloc[1]) and pd.notna(product_name):
                        quantity = float(row.iloc[1])
                        if product_name not in self.monthly_data:
                            self.monthly_data[product_name] = [0.0] * 12
                        self.monthly_data[product_name][month_index] = quantity

            # Print all processed products for debugging
            print("DEBUG: Processed Products:")
            for product in self.monthly_data.keys():
                print(f"Product: {product}, Monthly Sales: {self.monthly_data[product]}")

            # Calculate yearly averages
            for product, monthly_sales in self.monthly_data.items():
                self.yearly_averages[product] = sum(monthly_sales) / 12
                print(f"DEBUG: Product: {product}, Yearly Average: {self.yearly_averages[product]}")

            self.summary = "Files processed successfully. Yearly averages calculated."
        except Exception as e:
            self.summary = f"Error processing files: {str(e)}"
            self.summaryChanged.emit()

    @Slot(int)
    def generateReport(self, target_month):
        try:
            if target_month < 0 or target_month > 11:
                raise ValueError("Invalid month index. Must be between 0 and 11.")

            print(f"DEBUG: Generating report for month index {target_month}...")

            report_lines = ["Product Name | Monthly Sales | Yearly Average | % Change | Status"]
            self.report_data.clear()  # Clear previous report data

            for product, sales in self.monthly_data.items():
                monthly_sale = sales[target_month]
                avg = self.yearly_averages[product]
                change = ((monthly_sale - avg) / avg) * 100 if avg != 0 else 0

                # Determine status based on percentage change
                if change >= 10:
                    status = "Green"
                elif change <= -10:
                    status = "Red"
                else:
                    status = "Neutral"

                report_line = f"{product} | {monthly_sale:.2f} | {avg:.2f} | {change:+.2f}% | {status}"
                report_lines.append(report_line)

                # Store data for search functionality
                self.report_data.append({
                    "product": product,
                    "monthly_sales": monthly_sale,
                    "yearly_avg": avg,
                    "change": change,
                    "status": status
                })

            # Print the generated report for debugging
            print("DEBUG: Generated Report:")
            for line in report_lines:
                print(line)

            # Update summary with the generated report
            self.summary = "\n".join(report_lines)
        except Exception as e:
            self.summary = f"Error generating report: {str(e)}"
            self.summaryChanged.emit()

    @Slot(str)
    def searchProduct(self, product_name):
        try:
            normalized_name = product_name.strip().lower()  # Normalize input
            result_lines = ["Product Name | Monthly Sales | Yearly Average | % Change | Status"]
            found_product = False

            print(f"DEBUG: Searching for product '{normalized_name}'...")

            for record in self.report_data:
                if record["product"] == normalized_name:  # Compare normalized names
                    found_product = True
                    result_lines.append(
                        f"{record['product']} | {record['monthly_sales']:.2f} | {record['yearly_avg']:.2f} | "
                        f"{record['change']:+.2f}% | {record['status']}"
                    )
                    break

            if not found_product:
                result_lines.append(f"No results found for '{product_name}'.")

            # Print search results for debugging
            print("DEBUG: Search Results:")
            for line in result_lines:
                print(line)

            # Clear screen and display only the searched product details
            self.summary = "\n".join(result_lines)
        except Exception as e:
            self.summary = f"Error searching for product: {str(e)}"

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    backend = Backend()

    engine.rootContext().setContextProperty("backend", backend)
    engine.load("RL12M.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())