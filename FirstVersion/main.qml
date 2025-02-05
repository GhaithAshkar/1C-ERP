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
        }

        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            TextArea {
                width: parent.width
                text: backend.result_data
                readOnly: true
                font.family: "Monospace"
                font.pointSize: 11
                wrapMode: TextArea.NoWrap
            }
        }
    }
}
