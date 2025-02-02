import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    width: 1200
    height: 800
    title: "Excel Sales Analyzer"
    Material.theme: Material.Dark
    Material.accent: Material.DeepPurple

    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#1e3c72" }
            GradientStop { position: 1.0; color: "#2a5298" }
        }

        ColumnLayout {
            anchors {
                fill: parent
                margins: 20
            }
            spacing: 20

            // Enhanced Header Section
            Rectangle {
                Layout.fillWidth: true
                height: 120
                color: "transparent"

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 8

                    Text {
                        text: "Sales Data Analysis"
                        font {
                            pixelSize: 42
                            family: "Segoe UI"
                            weight: Font.Light
                        }
                        color: "white"
                    }

                    Text {
                        text: "Upload and analyze your sales data across multiple periods"
                        font {
                            pixelSize: 16
                            family: "Segoe UI"
                        }
                        color: "#e0e0e0"
                        opacity: 0.8
                    }
                }
            }

            // Main Content Area with Cards
            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                color: "#ffffff"
                opacity: 0.95
                radius: 12

                layer.enabled: true
                layer.effect: DropShadow {
                    horizontalOffset: 0
                    verticalOffset: 4
                    radius: 12.0
                    samples: 17
                    color: "#40000000"
                }

                ColumnLayout {
                    anchors {
                        fill: parent
                        margins: 24
                    }
                    spacing: 20

                    // Upload Card
                    Rectangle {
                        Layout.fillWidth: true
                        height: 100
                        color: "#f8f9fa"
                        radius: 10
                        border.color: "#e0e0e0"
                        border.width: 1

                        RowLayout {
                            anchors {
                                fill: parent
                                margins: 20
                            }
                            spacing: 20

                            Button {
                                id: uploadButton
                                text: "Upload Excel Files"
                                Layout.preferredWidth: 220
                                Layout.preferredHeight: 50

                                background: Rectangle {
                                    radius: 10
                                    gradient: Gradient {
                                        GradientStop { position: 0.0; color: uploadButton.pressed ? "#1e3c72" : "#2a5298" }
                                        GradientStop { position: 1.0; color: uploadButton.pressed ? "#2a5298" : "#1e3c72" }
                                    }

                                    layer.enabled: true
                                    layer.effect: DropShadow {
                                        horizontalOffset: 0
                                        verticalOffset: 2
                                        radius: 8.0
                                        samples: 17
                                        color: "#40000000"
                                    }
                                }

                                contentItem: RowLayout {
                                    spacing: 10
                                    Text {
                                        text: "⬆"
                                        color: "white"
                                        font.pixelSize: 18
                                    }
                                    Text {
                                        text: uploadButton.text
                                        color: "white"
                                        font.pixelSize: 16
                                    }
                                }

                                onClicked: fileDialog.open()
                            }

                            ColumnLayout {
                                Layout.fillWidth: true
                                spacing: 4

                                Text {
                                    text: "Data Upload"
                                    font {
                                        pixelSize: 18
                                        weight: Font.Medium
                                    }
                                    color: "#2a5298"
                                }

                                Text {
                                    text: "Select multiple Excel files to analyze sales data across different periods"
                                    font.pixelSize: 14
                                    color: "#666666"
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }

                    // Results Area
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        color: "#f8f9fa"
                        radius: 10
                        border.color: "#e0e0e0"
                        border.width: 1

                        ColumnLayout {
                            anchors {
                                fill: parent
                                margins: 16
                            }
                            spacing: 12

                            Text {
                                text: "Analysis Results"
                                font {
                                    pixelSize: 18
                                    weight: Font.Medium
                                }
                                color: "#2a5298"
                            }

                            ScrollView {
                                Layout.fillWidth: true
                                Layout.fillHeight: true
                                clip: true

                                TextArea {
                                    id: resultArea
                                    text: backend.summary
                                    readOnly: true
                                    wrapMode: TextArea.Wrap
                                    font {
                                        family: "Consolas"
                                        pixelSize: 14
                                    }
                                    color: "#333333"
                                    padding: 16
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    FileDialog {
        id: fileDialog
        title: "Select Excel Files"
        nameFilters: ["Excel files (*.xlsx *.xls)"]
        fileMode: FileDialog.OpenFiles

        onAccepted: {
            backend.readFiles(selectedFiles.toString())
        }
    }
}