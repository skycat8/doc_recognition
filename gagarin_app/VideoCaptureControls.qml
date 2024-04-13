import QtQuick 2.0
import QtMultimedia 5.4

FocusScope {
    property Camera camera
    property bool previewAvailable : false

    property int buttonsPanelWidth: buttonPaneShadow.width

    signal previewSelected
    signal photoModeSelected
    id : captureControls

    Rectangle {
        id: buttonPaneShadow
        width: bottomColumn.width + 16
        height: parent.height
        anchors.top: parent.top
        anchors.right: parent.right
        color: Qt.rgba(0.08, 0.08, 0.08, 1)

        Column {
            anchors {
                right: parent.right
                top: parent.top
                margins: 8
            }

            id: buttonsColumn
            spacing: 8

            FocusButton {
                camera: captureControls.camera
                visible: camera.cameraStatus == Camera.ActiveStatus && camera.focus.isFocusModeSupported(Camera.FocusAuto)
            }

            CameraButton {
                text: "Record"
                visible: camera.videoRecorder.recorderStatus == CameraRecorder.LoadedStatus
                onClicked: camera.videoRecorder.record()
            }

            CameraButton {
                id: stopButton
                text: "Stop"
                visible: camera.videoRecorder.recorderStatus == CameraRecorder.RecordingStatus
                onClicked: camera.videoRecorder.stop()
            }

            CameraButton {
                text: "View"
                onClicked: captureControls.previewSelected()
                //don't show View button during recording
                visible: camera.videoRecorder.actualLocation && !stopButton.visible
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

            CameraListButton {
                model: QtMultimedia.availableCameras
                onValueChanged: captureControls.camera.deviceId = value
            }

            CameraButton {
                text: "Switch to Photo"
                onClicked: captureControls.photoModeSelected()
            }

            CameraButton {
                id: quitButton
                text: "Quit"
                onClicked: Qt.quit()
            }
        }
    }


    ZoomControl {
        x : 0
        y : 0
        width : 100
        height: parent.height

        currentZoom: camera.digitalZoom
        maximumZoom: Math.min(4.0, camera.maximumDigitalZoom)
        onZoomTo: camera.setDigitalZoom(value)
    }
}
