<<<<<<< Updated upstream
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    visible: true
    width: 1200
    height: 800
    title: "Product Sales Analyzer"

    FileDialog {
        id: fileDialog
        nameFilters: ["Excel files (*.xlsx)"]
        fileMode: FileDialog.OpenFiles
        onAccepted: backend.readFiles(selectedFiles.toString())
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        Button {
            Layout.fillWidth: true
            text: "Select Excel Files (All 12 Months)"
            onClicked: fileDialog.open()
        }

        ComboBox {
            id: monthSelector
            Layout.fillWidth: true
            model: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        }

        Button {
            Layout.fillWidth: true
            text: "Generate Report"
            onClicked: backend.generateReport(monthSelector.currentIndex)
        }

        TextField {
            id: searchField
            placeholderText: "Enter product name to search..."
            Layout.fillWidth: true
        }

        Button {
            Layout.fillWidth: true
            text: "Search Product"
            onClicked: backend.searchProduct(searchField.text)
=======
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "January Sales Report"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 20

        Button {
            Layout.alignment: Qt.AlignHCenter
            text: "Calculate January Report"
            onClicked: backend.calculate_january_report()
>>>>>>> Stashed changes
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            TextArea {
                width: parent.width
<<<<<<< Updated upstream
                text: backend.summary
                readOnly: true
                wrapMode: TextArea.WrapAtWordBoundaryOrAnywhere
                font.family: "Consolas"
                font.pointSize: 10
                selectByMouse: true
=======
                text: backend.result_data
                readOnly: true
                font.family: "Monospace"
                font.pointSize: 11
                wrapMode: TextArea.NoWrap
>>>>>>> Stashed changes
            }
        }
    }
}
