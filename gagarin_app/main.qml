import QtQuick 2.4
import QtQuick.Controls 2.1
import QtQuick.Window 2.1
import QtQuick.Controls.Universal 2.3
import QtMultimedia 5.9
import QtQuick.Dialogs 1.0


ApplicationWindow {
    id: window
    visible: true
    width: 480
    height: 720
    title: customsettings.appname

    function customExit() {
        camera.stop()
        close()
        Qt.quit()
    }

    function openDrawer() {
        drawer.open()
    }

    function showUpdateDialog(_appname,_version,_changelog) {
        updatedialog.show(_appname,_version,_changelog)
    }

    property bool capturing_allowed: !busyIndicator.running

    property int videodevIndex: 0 // QtMultimedia.availableCameras.length > 1 ? 1 : 0

    property var listoflanguages: ["Русский", "English"]

    signal frameCaptured(string filename, bool delete_after)

    CustomAboutDialog {
        id: aboutdialog
        x: (window.width - width)   / 2
        y: (window.height - height) / 2
    }

    CustomDialog {
        objectName: "messageDialog"
        width: window.width * 0.9
        height: window.height * 0.9
        x: (window.width - width)   / 2
        y: (window.height - height) / 2
    }

    CustomUpdateDialog {
        id: updatedialog
        width: window.width * 0.9
        height: window.height * 0.9
        x: (window.width - width)   / 2
        y: (window.height - height) / 2
    }

    FileDialog {
        id: filedialog
        folder: shortcuts.pictures
        onAccepted: { frameCaptured(fileUrl.toString(), false)
            photoPreview.source = fileUrl
            stillControls.previewAvailable = true
            cameraUI.state = "PhotoPreview"
        }
    }


    BusyIndicator {
        id: busyIndicator
        z: 1
        objectName: "busyIndicator"
        width: window.width / 3
        height: width
        x: (window.width - width) / 2
        y: (window.height - height) / 2
        running: false
    }

    ProgressBar {
        id: updatedownloadprogressbar
        z: 1
        width: window.width*0.9
        x: (window.width - width) / 2
        y: window.height / 5
        value: customsettings.updtdownloadprogress
        visible: value > 0.01 && value < 0.99
        opacity: 0.5
        Label {
            text: qsTr("Загрузка обновлений:")
            anchors.bottom: parent.top
        }
    }


    Drawer {
        id: drawer
        width: 300
        height: window.height
        padding: 0
        edge: Qt.LeftEdge

        Button {
            id: closeB
            anchors.right: parent.right
            flat: true
            text: "<<" // ">>"
            opacity: 0.5
            onClicked: drawer.close()
        }

        Column {
            id: topColumn
            width: parent.width * 0.95
            y: 10 + closeB.height
            x: (parent.width - width)/2
            spacing: 10

            Label {
                width: parent.width
                text: qsTr("Выберите язык интерфейса:")
                elide: Text.ElideRight
            }
            ComboBox {
                flat: true
                width: parent.width
                model:  window.listoflanguages
                currentIndex: customsettings.language === model[0] ? 0 : 1
                onCurrentIndexChanged: customsettings.language = model[currentIndex]
            }

            Label {
                width: parent.width
                text: qsTr("Сервер:")
                elide: Text.ElideRight
            }
            TextField {
                width: 0.9*parent.width
                x: (parent.width - width)/2
                horizontalAlignment: Text.AlignHCenter
                text: customsettings.srvurl
                onAccepted: customsettings.srvurl = text
            }

            Label {
                width: parent.width
                text: qsTr("Эндпоинт:")
                elide: Text.ElideRight
            }
            ComboBox {
                model: ["/process", "/detect"]
                width: 0.9*parent.width
                x: (parent.width - width)/2
                currentIndex: customsettings.method === model[0] ? 0 : 1
                onCurrentValueChanged: customsettings.method = model[currentIndex]
            }

            Label {
                width: parent.width
                text: qsTr("Камера:")
                elide: Text.ElideRight
            }
            ComboBox {
                model: QtMultimedia.availableCameras
                width: 0.9*parent.width
                x: (parent.width - width)/2
                textRole: "displayName"
                currentIndex: videodevIndex
                onCurrentIndexChanged: videodevIndex = currentIndex
            }

        }

        Button {
            width: height
            text: qsTr("?")
            anchors.left: parent.left
            flat: true
            onClicked: aboutdialog.open()
        }
    }


    Rectangle {
        id : cameraUI

        width: window.width
        height: window.height

        color: "black"
        state: "PhotoCapture"

        states: [
            State {
                name: "PhotoCapture"
                StateChangeScript {
                    script: {
                        camera.captureMode = Camera.CaptureStillImage
                        camera.start()
                    }
                }
            },
            State {
                name: "PhotoPreview"
            },
            /*State {
                name: "VideoCapture"
                StateChangeScript {
                    script: {
                        camera.captureMode = Camera.CaptureVideo
                        camera.start()
                    }
                }
            },*/
            State {
                name: "VideoPreview"
                StateChangeScript {
                    script: {
                        camera.stop()
                    }
                }
            }
        ]

        Camera {
            id: camera
            captureMode: Camera.CaptureStillImage
            deviceId: QtMultimedia.availableCameras[videodevIndex].deviceId
            onDeviceIdChanged: console.log(QtMultimedia.availableCameras[videodevIndex].deviceId)

            imageCapture {
                resolution: "800x600"

                onImageCaptured: {
                    photoPreview.source = preview
                    stillControls.previewAvailable = true
                    cameraUI.state = "PhotoPreview"
                }

                onImageSaved: frameCaptured(path, true)
            }

            videoRecorder {
                 resolution: "640x480"
                 frameRate: 30
            }
        }

        PhotoPreview {
            id : photoPreview
            anchors.fill : parent
            onClosed: cameraUI.state = "PhotoCapture"
            visible: cameraUI.state == "PhotoPreview"
            focus: visible
        }

        VideoPreview {
            id : videoPreview
            anchors.fill : parent
            onClosed: cameraUI.state = "VideoCapture"
            visible: cameraUI.state == "VideoPreview"
            focus: visible

            //don't load recorded video if preview is invisible
            source: visible ? camera.videoRecorder.actualLocation : ""
        }

        VideoOutput {
            id: viewfinder
            visible: cameraUI.state == "PhotoCapture" || cameraUI.state == "VideoCapture"

            width: parent.width
            height: parent.height

            source: camera
            autoOrientation: true
        }

        PhotoCaptureControls {
            id: stillControls
            anchors.fill: parent
            camera: camera
            visible: cameraUI.state == "PhotoCapture"
            onPreviewSelected: cameraUI.state = "PhotoPreview"
            onVideoModeSelected: cameraUI.state = "VideoCapture"
        }

        /*VideoCaptureControls {
            id: videoControls
            anchors.fill: parent
            camera: camera
            visible: cameraUI.state == "VideoCapture"
            onPreviewSelected: cameraUI.state = "VideoPreview"
            onPhotoModeSelected: cameraUI.state = "PhotoCapture"
        }*/
    }
}
