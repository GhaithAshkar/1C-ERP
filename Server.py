# # import sys
# # from PySide6.QtCore import QObject, Slot, QUrl
# # from PySide6.QtGui import QGuiApplication
# # from PySide6.QtQml import QQmlApplicationEngine
# # import pandas as pd
# # from collections import defaultdict
# #
# # class Backend(QObject):
# #     def __init__(self):
# #         super().__init__()
# #         self.files_data = []
# #
# #     @Slot(str)
# #     def readFiles(self, fileUrls):
# #         try:
# #             urls = fileUrls.split(',')
# #             for url in urls:
# #                 local_path = QUrl(url).toLocalFile()
# #                 df = pd.read_excel(local_path)
# #                 print(f"File: {local_path}")
# #                 print(f"Columns found: {df.columns.tolist()}")
# #                 self.files_data.append(df)
# #                 print(f"Successfully read file {local_path}")
# #             print(f"{len(self.files_data)} files processed")
# #         except Exception as e:
# #             print(f"Error processing files: {str(e)}")
# #
# #     def calculateAverages(self):
# #         try:
# #             if not self.files_data:
# #                 print("No files loaded")
# #                 return
# #
# #             df_sample = self.files_data[0]
# #             product_col = df_sample.columns[1]  # Assuming second column is product description
# #             count_col = df_sample.columns[5]    # Assuming sixth column is quantity
# #
# #             product_counts = defaultdict(list)
# #
# #             for df in self.files_data:
# #                 for _, row in df.iterrows():
# #                     product_name = str(row[product_col])
# #                     count_value = float(row[count_col])
# #                     product_counts[product_name].append(count_value)
# #
# #             summary_data = []
# #             total_files = len(self.files_data)
# #
# #             for product, counts in product_counts.items():
# #                 total_count = sum(counts)
# #                 avg = total_count / total_files
# #                 summary_data.append({
# #                     'Product': product,
# #                     'Total Count': total_count,
# #                     'Number of Files': total_files,
# #                     'Average': avg,
# #                     'Monthly Values': counts
# #                 })
# #
# #             summary_data.sort(key=lambda x: x['Average'], reverse=True)
# #
# #             print("Averages Across All Files")
# #             print("-" * 60)
# #             for item in summary_data:
# #                 print(f"Product: {item['Product']}")
# #                 print(f"Monthly Values: {item['Monthly Values']}")
# #                 print(f"Total Count: {item['Total Count']}")
# #                 print(f"Number of Files: {item['Number of Files']}")
# #                 print(f"Average: {item['Average']:.2f}")
# #                 print("-" * 60)
# #
# #         except Exception as e:
# #             print(f"Error calculating averages: {str(e)}")
# #             import traceback
# #             print(traceback.format_exc())
# #
# #
# # if __name__ == "__main__":
# #     app = QGuiApplication(sys.argv)
# #     engine = QQmlApplicationEngine()
# #     backend = Backend()
# #
# #     # Set context property to make backend accessible in QML
# #     engine.rootContext().setContextProperty("backend", backend)
# #
# #     # Load the main QML file
# #     engine.load("main.qml")
# #
# #     # Check if any root objects were loaded
# #     if not engine.rootObjects():
# #         sys.exit(-1)
# #
# #     # Start the application event loop
# #     sys.exit(app.exec())
#
# #______________________________________________________________
#
#
# import sys
# from PySide6.QtCore import QObject, Slot, QUrl, Property, Signal
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtQml import QQmlApplicationEngine
# import pandas as pd
# from collections import defaultdict
#
#
# class Backend(QObject):
#     # Signal to notify QML about data changes
#     summaryChanged = Signal()
#
#     def __init__(self):
#         super().__init__()
#         self.files_data = []
#         self._summary = "No data loaded yet. Please select Excel files."
#
#     @Property(str, notify=summaryChanged)
#     def summary(self):
#         return self._summary
#
#     @Slot(str)
#     def readFiles(self, fileUrls):
#         try:
#             # Clear previous data
#             self.files_data = []
#
#             # Split the URLs and process each file
#             urls = fileUrls.split(',')
#             for url in urls:
#                 local_path = QUrl(url).toLocalFile()
#                 print(f"Reading file: {local_path}")
#
#                 # Read Excel file with specific parameters
#                 df = pd.read_excel(
#                     local_path,
#                     engine='openpyxl'
#                 )
#
#                 self.files_data.append(df)
#                 print(f"Successfully loaded file: {local_path}")
#
#             print(f"Total files processed: {len(self.files_data)}")
#
#             # Calculate averages after loading all files
#             self.calculateAverages()
#
#         except Exception as e:
#             error_msg = f"Error processing files: {str(e)}"
#             print(error_msg)
#             self._summary = error_msg
#             self.summaryChanged.emit()
#
#     def calculateAverages(self):
#         try:
#             if not self.files_data:
#                 self._summary = "No files loaded"
#                 self.summaryChanged.emit()
#                 return
#
#             # Initialize data structures
#             product_counts = defaultdict(list)
#             summary_lines = ["Product Sales Analysis\n", "=" * 50 + "\n\n"]
#
#             # Process each file
#             for df in self.files_data:
#                 for _, row in df.iterrows():
#                     try:
#                         # Get product name and quantity
#                         product_name = str(row.iloc[1]).strip()  # Second column
#                         quantity = float(row.iloc[5])  # Sixth column
#
#                         if pd.notna(product_name) and pd.notna(quantity):
#                             product_counts[product_name].append(quantity)
#                     except (ValueError, IndexError) as e:
#                         print(f"Skipping row due to error: {e}")
#                         continue
#
#             # Calculate statistics
#             total_files = len(self.files_data)
#             summary_data = []
#
#             for product, quantities in product_counts.items():
#                 total = sum(quantities)
#                 average = total / total_files
#                 summary_data.append({
#                     'product': product,
#                     'total': total,
#                     'average': average,
#                     'monthly_values': quantities
#                 })
#
#             # Sort by average sales (descending)
#             summary_data.sort(key=lambda x: x['average'], reverse=True)
#
#             # Format output
#             for item in summary_data:
#                 summary_lines.extend([
#                     f"Product: {item['product']}\n",
#                     f"Monthly Average: {item['average']:.2f}\n",
#                     f"Total Annual: {item['total']:.2f}\n",
#                     f"Monthly Values: {', '.join(f'{v:.2f}' for v in item['monthly_values'])}\n",
#                     "-" * 50 + "\n\n"
#                 ])
#
#             # Update summary and notify QML
#             self._summary = "".join(summary_lines)
#             self.summaryChanged.emit()
#             print("Calculation completed successfully")
#
#         except Exception as e:
#             error_msg = f"Error calculating averages: {str(e)}"
#             print(error_msg)
#             self._summary = error_msg
#             self.summaryChanged.emit()
#
#
# if __name__ == "__main__":
#     app = QGuiApplication(sys.argv)
#     engine = QQmlApplicationEngine()
#
#     # Create and register backend
#     backend = Backend()
#     engine.rootContext().setContextProperty("backend", backend)
#
#     # Load QML
#     engine.load("main.qml")
#
#     if not engine.rootObjects():
#         sys.exit(-1)
#
#     sys.exit(app.exec())

#--------------------------------------------------


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