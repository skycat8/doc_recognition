#include "qrecognitiontaskposter.h"

#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QHttpMultiPart>
#include <QJsonParseError>
#include <QJsonObject>
#include <QUrl>
#include <QFile>
#include <QImage>
#include <QBuffer>
#include <QSslError>


QRecognitionTaskPoster::QRecognitionTaskPoster(const QString &_apiurl,
                                               const QString &_filename,
                                               bool _delete_after,
                                               QObject *parent) : QThread(parent),
    apiurl(_apiurl),
    filename(_filename),
    delete_after(_delete_after)
{ 
}

void QRecognitionTaskPoster::run()
{
    QHttpMultiPart *_fields = new QHttpMultiPart(QHttpMultiPart::FormDataType);

    QHttpPart _photo;
    _photo.setHeader(QNetworkRequest::ContentTypeHeader, "image/jpeg");
    _photo.setHeader(QNetworkRequest::ContentDispositionHeader, "form-data; name=\"photo\"; filename=\"photo.jpg\"");
    QFile *file = new QFile(filename);
    file->open(QIODevice::ReadOnly);
    _photo.setBodyDevice(file);
    file->setParent(_fields);
    _fields->append(_photo);
    QNetworkRequest _request(QUrl::fromUserInput(apiurl));
    QNetworkAccessManager nacm;
    QNetworkReply *_reply = nacm.post(_request, _fields);
    _reply->ignoreSslErrors(); // !!ACHTUNG!! - remove in production
    QObject::connect(_reply, SIGNAL(finished()), this, SLOT(quit()));
    QObject::connect(_reply,
                     &QNetworkReply::sslErrors,
                     this,
                     [](const QList<QSslError> &errors) {
        qInfo("WARNING! sslErrors in QRecognitionTaskPoster::run():");
        for(const auto &error: errors){
            qInfo(" - %s", error.errorString().toUtf8().constData());
        }
    });
    exec();

    int http_status = _reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
    QByteArray body = _reply->readAll();
    emit replyReady(http_status, body);
    if(delete_after)
        QFile::remove(filename);
    _fields->setParent(_reply);
    _reply->deleteLater();
}
