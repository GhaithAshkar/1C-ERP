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
        onAccepted: {
            backend.readFiles(selectedFiles.toString())
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        Button {
            Layout.fillWidth: true
            text: "Select Excel Files (Select all 12 months)"
            onClicked: fileDialog.open()
            height: 40
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            clip: true

            TextArea {
                width: parent.width
                text: backend.summary
                readOnly: true
                wrapMode: TextArea.Wrap
                font.family: "Consolas"
                font.pointSize: 10
                selectByMouse: true
            }
        }
    }
}