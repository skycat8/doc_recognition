import QtQuick 2.4
import QtQuick.Controls 2.1

Dialog {
    width: 350
    height: headerPane.height + column.height + 2*column.anchors.topMargin
    modal: true
    padding: 0
    topPadding: 0

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
            id: abouttoplabel
            text: qsTr("О программе")
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 10
        }
        Button {
            text: "✕"
            height: parent.height
            width: height
            flat: true
            anchors.right: parent.right
            anchors.verticalCenter: parent.verticalCenter
            onClicked: close()
        }
    }

    Column {
        id: column
        width: 0.8*parent.width
        x: (parent.width - width) / 2
        anchors.top: headerPane.bottom
        anchors.topMargin: 15
        spacing: 10
        Text {
            width: parent.width
            text: customsettings.companyname
            horizontalAlignment: Text.AlignHCenter
        }
        Pane { background.opacity: 0; padding: 2.5}
        Text {
            width: parent.width
            text: customsettings.appname + " v." + customsettings.appversion
            horizontalAlignment: Text.AlignHCenter
        }
        Text {
            width: parent.width
            text: qsTr("Дата релиза: ") + customsettings.appreleasedate.toLocaleDateString(Qt.locale(),Locale.ShortFormat)
            horizontalAlignment: Text.AlignHCenter
        }
        Text {
            width: parent.width
            text: customsettings.appdescription
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
        Text {
            width: parent.width
            text: customsettings.appdisclaimer
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
        }
        Row {
            width: parent.width
            spacing: 10
            Image {
                id: companyicon
                height: parent.height*0.8
                y: (parent.height - height) / 2
                fillMode: Image.PreserveAspectFit
                source: "Resources/manufacturer.svg"
            }
            Column {
                width: parent.width - companyicon.width
                spacing: 1.5
                Text {
                    text: customsettings.companyname
                    elide: Text.ElideRight
                    font.bold: true
                    width: parent.width
                }
                Text {
                    text: customsettings.companyaddress
                    elide: Text.ElideRight
                    width: parent.width
                }
                Text {
                    text: customsettings.companyphone
                    elide: Text.ElideRight
                    width: parent.width
                }
                Text {
                    text: customsettings.companyfax
                    elide: Text.ElideRight
                    width: parent.width
                }
                Text {
                    text: customsettings.companyemail
                    elide: Text.ElideRight
                    onLinkActivated: Qt.openUrlExternally(link)
                    linkColor: "grey"
                    width: parent.width
                }
            }           
        }
        Pane { background.opacity: 0; padding: 2.5}

        /*Row {
            x: (parent.width - width) / 2
            Text {
                id: userguideLink
                y: (parent.height - height) / 2
                text: customsettings.appuserguide
                linkColor: "grey"
                elide: Text.ElideRight
                //width: parent.width - userguideButton.width
                onLinkActivated: Qt.openUrlExternally(link)
            }
        }*/
    }
}
