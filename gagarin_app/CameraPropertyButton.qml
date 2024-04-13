import QtQuick 2.0
import QtMultimedia 5.0

Item {
    id: propertyButton
    property alias value : popup.currentValue
    property alias model : popup.model

    width : 80
    height: 60

    BorderImage {
        id: buttonImage
        source: "images/toolbutton.sci"
        width: propertyButton.width; height: propertyButton.height
    }

    CameraButton {
        anchors.fill: parent
        Image {
            anchors.centerIn: parent
            source: popup.currentItem.icon
        }

        onClicked: popup.toggle()
    }

    CameraPropertyPopup {
        id: popup
        anchors.right: parent.left
        anchors.rightMargin: 16
        anchors.top: parent.top
        visible: opacity > 0

        currentValue: propertyButton.value

        onSelected: popup.toggle()
    }
}

