import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: qsTr("Sales Data Analysis")

    ColumnLayout {
        anchors.fill: parent
        spacing: 10

        Button {
            text: qsTr("Calculate and Display Data")
            onClicked: backend.calculate_and_send_data()
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            TextArea {
                id: resultArea
                wrapMode: TextArea.WrapAtWordBoundaryOrAnywhere
                readOnly: true
                font.family: "Courier"
                font.pointSize: 12
                text: backend.result_data // Bind to backend.result_data property
            }
        }
    }
}
