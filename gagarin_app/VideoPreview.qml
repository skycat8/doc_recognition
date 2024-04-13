import QtQuick 2.0
import QtMultimedia 5.0

Item {
    id: videoPreview
    property alias source : player.source
    signal closed

    MediaPlayer {
        id: player
        autoPlay: true

        //switch back to viewfinder after playback finished
        onStatusChanged: {
            if (status == MediaPlayer.EndOfMedia)
                videoPreview.closed();
        }
    }

    VideoOutput {
        source: player
        anchors.fill : parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: {
            videoPreview.closed();
        }
    }
}

