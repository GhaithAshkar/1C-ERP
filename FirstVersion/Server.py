from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
import sys
from monthly_analysis import analyze_monthly_data, mock_yearly_data
from yearly_average import calculate_yearly_averages

class Backend(QObject):
    dataChanged = Signal()

    def __init__(self):
        super().__init__()
        self._result_data = ""
        self.yearly_averages = calculate_yearly_averages(mock_yearly_data)
        # Initialize with empty data (will be filled when Calculate is clicked)
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
    def calculate_january_report(self):
        """Generate the January sales report."""
        try:
            # Always analyze January data
            report = analyze_monthly_data(mock_yearly_data, "January", self.yearly_averages)
            self.result_data = report
        except Exception as e:
            self.result_data = f"Error: {str(e)}"


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    backend = Backend()
    engine.rootContext().setContextProperty("backend", backend)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
