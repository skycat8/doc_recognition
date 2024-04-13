import QtQuick 2.4
import QtQuick.Controls 2.14

Dialog {
    id: dialog
    width: 350
    height: 350
    modal: true
    property string customtitle: "header"
    property string text: "some text\nsome text\nsome text\nsome text\nsome text\nsome text\nsome text\nsome text\n"
    property string color: "black"
    padding: 0
    topPadding: 0
    bottomPadding: 0

    Pane {
        id: headerPane
        width: parent.width
        height: 40
        padding: 0
        background: Rectangle {
            color: "grey"
            opacity: 0.35
        }
        Label {          
            text: dialog.customtitle
            anchors.left: parent.left
            anchors.leftMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width - closeB.width
            elide: Text.ElideRight           
        }
        Button {
            id: closeB
            text: "✕"
            height: parent.height
            width: height
            flat: true
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            onClicked: close()
        }
    }

    Pane {
        id: bodyPane
        width: parent.width
        height: parent.height - headerPane.height

        anchors.top: headerPane.bottom
        anchors.topMargin: 10

        ScrollView {
            id: view
            width: parent.width
            height: 0.9 *parent.height
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff
            ScrollBar.vertical.policy: ScrollBar.AsNeeded

            TextArea {
                readOnly: true
                wrapMode: TextEdit.WordWrap
                text: dialog.text
                color: dialog.color
            }
        }

        Button {
            id: rejectB
            text: qsTr("Ок")
            onClicked: close()
            flat: true
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 10
        }
    }
}
