import QtQuick 2.0

Item {
    id: button

    property string source: "images/toolbutton.png"

    signal clicked

    property string text
    property color color: "white"

    width : 80
    height: 60

    opacity: 1

    BorderImage {
        id: buttonImage
        source: parent.source
        width: button.width; height: button.height
    }
    MouseArea {
        id: mouseRegion
        anchors.fill: buttonImage
        onClicked: { button.clicked(); }
        onHoveredChanged: {
            if(containsMouse)
                parent.opacity = 0.5
            else
                parent.opacity = 1.0
        }
    }
    Text {
        id: btnText
        anchors.fill: buttonImage
        anchors.margins: 5
        text: button.text
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        elide: Text.ElideRight
        color: button.color
        font.bold: true
        style: Text.Raised
        styleColor: "black"
        font.pixelSize: 14
    }
}
