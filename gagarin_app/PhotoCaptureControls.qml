import QtQuick 2.0
import QtMultimedia 5.4

FocusScope {
    property Camera camera
    property bool previewAvailable : false

    property int buttonsPanelWidth: buttonPaneShadow.width

    signal previewSelected
    signal videoModeSelected
    id : captureControls

    Rectangle {
        id: buttonPaneShadow
        width: parent.width
        height: parent.height
        anchors.top: parent.top
        anchors.right: parent.right
        color: "transparent"

        Column {
            anchors {
                right: parent.right
                top: parent.top
                margins: 8
            }

            id: buttonsColumn
            spacing: 8          

            CameraButton {
                id: quitButton
                source: "images/toolbutton_red.png"
                text: qsTr("Выйти")
                onClicked: window.customExit()
            }

            /*CameraListButton {
                model: QtMultimedia.availableCameras
                onValueChanged: captureControls.camera.deviceId = value
            }

            CameraPropertyButton {
                id : wbModesButton
                value: CameraImageProcessing.WhiteBalanceAuto
                model: ListModel {
                    ListElement {
                        icon: "images/camera_auto_mode.png"
                        value: CameraImageProcessing.WhiteBalanceAuto
                        text: "Auto"
                    }
                    ListElement {
                        icon: "images/camera_white_balance_sunny.png"
                        value: CameraImageProcessing.WhiteBalanceSunlight
                        text: "Sunlight"
                    }
                    ListElement {
                        icon: "images/camera_white_balance_cloudy.png"
                        value: CameraImageProcessing.WhiteBalanceCloudy
                        text: "Cloudy"
                    }
                    ListElement {
                        icon: "images/camera_white_balance_incandescent.png"
                        value: CameraImageProcessing.WhiteBalanceTungsten
                        text: "Tungsten"
                    }
                    ListElement {
                        icon: "images/camera_white_balance_flourescent.png"
                        value: CameraImageProcessing.WhiteBalanceFluorescent
                        text: "Fluorescent"
                    }
                }
                onValueChanged: captureControls.camera.imageProcessing.whiteBalanceMode = wbModesButton.value
            }*/

        }

        Column {
            anchors {
                left: parent.left
                top: parent.top
                margins: 8
            }

            spacing: 8

            CameraButton {
                text: qsTr("Настройки")
                onClicked: window.openDrawer()
            }
        }

        Column {
            anchors {
                bottom: parent.bottom
                right: parent.right
                margins: 8
            }

            id: bottomColumn
            spacing: 8

            CameraButton {
                enabled: window.capturing_allowed
                text: qsTr("Посл.")
                onClicked: captureControls.previewSelected()
                visible: captureControls.previewAvailable
            }

            /*CameraButton {
                text: "Switch to Video"
                onClicked: captureControls.videoModeSelected()
            }*/

            FocusButton {
                camera: captureControls.camera
                visible: camera.cameraStatus == Camera.ActiveStatus && camera.focus.isFocusModeSupported(Camera.FocusAuto)
            }

            CameraButton {
                enabled: window.capturing_allowed
                text: qsTr("Снять")
                visible: camera.imageCapture.ready
                onClicked: camera.imageCapture.capture()
            }
        }

        Column {
            anchors {
                bottom: parent.bottom
                left: parent.left
                margins: 8
            }

            spacing: 8

            CameraButton {
                enabled: window.capturing_allowed
                text: qsTr("Файл")
                onClicked: filedialog.open()
            }
        }


    }

    ZoomControl {
        x : 0
        y : (parent.height - height) / 2
        width : 100
        height: parent.height / 1.5

        currentZoom: camera.digitalZoom
        maximumZoom: Math.min(4.0, camera.maximumDigitalZoom)
        onZoomTo: camera.setDigitalZoom(value)
    }
}
