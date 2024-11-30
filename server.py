import sys
from PySide6.QtCore import QObject, Slot, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import pandas as pd
from collections import defaultdict


class Backend(QObject):
    def __init__(self):
        super().__init__()
        self.files_data = []

    @Slot(str)
    def readFiles(self, fileUrls):
        try:
            self.files_data = []
            urls = fileUrls.split(',')
            for url in urls:
                local_path = QUrl(url).toLocalFile()
                df = pd.read_excel(local_path)
                print(f"\nReading file: {local_path}")
                print(f"Columns found: {df.columns.tolist()}")
                self.files_data.append(df)
                print(f"Successfully read file: {local_path}")

            print(f"\nTotal files processed: {len(self.files_data)}")
            self.calculate_averages()

        except Exception as e:
            print(f"Error processing files: {str(e)}")

    def calculate_averages(self):
        try:
            if not self.files_data:
                print("No files loaded")
                return

            df_sample = self.files_data[0]
            product_col = df_sample.columns[0]
            count_col = df_sample.columns[1]

            print(f"\nUsing columns: Product='{product_col}', Count='{count_col}'")

            # Dictionary to store counts for each product
            product_counts = defaultdict(list)

            # Collect all counts for each product across all files
            for df in self.files_data:
                for _, row in df.iterrows():
                    product_name = str(row[product_col])
                    count_value = float(row[count_col])
                    product_counts[product_name].append(count_value)

            # Calculate and display averages
            print("\nProduct Averages Across All Files:")
            print("-" * 60)

            # Create summary with averages
            summary_data = []
            total_files = len(self.files_data)

            for product, counts in product_counts.items():
                total_count = sum(counts)
                avg = total_count / total_files  # Average based on total number of files
                summary_data.append({
                    'Product': product,
                    'Total Count': total_count,
                    'Number of Files': total_files,
                    'Average': avg,
                    'Monthly Values': counts
                })

            # Sort by average value
            summary_data.sort(key=lambda x: x['Average'], reverse=True)

            # Print detailed summary
            for item in summary_data:
                print(f"Product: {item['Product']}")
                print(f"Monthly Values: {item['Monthly Values']}")
                print(f"Total Count: {item['Total Count']}")
                print(f"Number of Files: {item['Number of Files']}")
                print(f"Average: {item['Average']:.2f}")
                print("-" * 60)

        except Exception as e:
            print(f"Error calculating averages: {str(e)}")
            print("Detailed error information:")
            import traceback
            print(traceback.format_exc())


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())