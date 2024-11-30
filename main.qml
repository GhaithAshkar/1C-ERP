import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

ApplicationWindow {
    visible: true
    width: 400
    height: 200
    title: "Multiple Excel Files Uploader"

    FileDialog {
        id: fileDialog
        title: "Choose Excel Files"
        nameFilters: ["Excel files (*.xlsx)"]
        fileMode: FileDialog.OpenFiles

        onAccepted: {
            backend.readFiles(selectedFiles.join(','))
        }
    }

    Column {
        anchors.centerIn: parent
        spacing: 10

        Button {
            text: "Upload Excel Files"
            onClicked: fileDialog.open()
        }
    }
}