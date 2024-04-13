#ifndef QRECOGNITIONTASKPOSTER_H
#define QRECOGNITIONTASKPOSTER_H

#include <QThread>

class QRecognitionTaskPoster : public QThread
{
    Q_OBJECT
public:
    explicit QRecognitionTaskPoster(const QString &_apiurl,
                                    const QString &_filename,
                                    bool _delete_after,
                                    QObject *parent=nullptr);
signals:
    void replyReady(int http_status, const QByteArray &body);
protected:
    void run() override;
private:
    QString apiurl, filename;
    bool delete_after;
};

#endif // QRECOGNITIONTASKPOSTER_H
