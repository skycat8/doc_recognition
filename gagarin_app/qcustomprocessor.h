#ifndef QCUSTOMPROCESSOR_H
#define QCUSTOMPROCESSOR_H

#include <QObject>
#include <QSettings>
#include <QQmlApplicationEngine>
#include <QCoreApplication>
#include <QTranslator>

#include "qsimplemaintenancetool.h"

class QCustomProcessor : public QObject
{
    Q_OBJECT
    Q_PROPERTY(QString language READ language WRITE setLanguage NOTIFY languageChanged)
    Q_PROPERTY(QString login READ login WRITE setLogin NOTIFY loginChanged)
    Q_PROPERTY(QString password READ password WRITE setPassword NOTIFY passwordChanged)
    Q_PROPERTY(QString srvurl READ srvurl WRITE setSrvurl NOTIFY srvurlChanged)
    Q_PROPERTY(QString method READ method WRITE setMethod NOTIFY methodChanged)
    // Update-related properties
    Q_PROPERTY(QString updtsrvurl READ updtsrvurl WRITE setUpdtsrvurl NOTIFY updtsrvurlChanged)
    Q_PROPERTY(float updtdownloadprogress READ updtdownloadprogress WRITE setUpdtdownloadprogress NOTIFY updtdownloadprogressChanged)
    // Bio
    Q_PROPERTY(QString appname READ appname NOTIFY appnameChanged)
    Q_PROPERTY(QString appversion READ appversion NOTIFY appversionChanged)
    Q_PROPERTY(QString appdescription READ appdescription NOTIFY appdescriptionChanged)
    Q_PROPERTY(QString appdisclaimer READ appdisclaimer NOTIFY appdisclaimerChanged)
    Q_PROPERTY(QString companyname READ companyname NOTIFY companynameChanged)
    Q_PROPERTY(QString companyaddress READ companyaddress NOTIFY companyaddressChanged)
    Q_PROPERTY(QString companyphone READ companyphone NOTIFY companyphoneChanged)
    Q_PROPERTY(QString companyfax READ companyfax NOTIFY companyfaxChanged)
    Q_PROPERTY(QString companyemail READ companyemail NOTIFY companyemailChanged)
    Q_PROPERTY(QDate   appreleasedate READ appreleasedate NOTIFY appreleasedateChanged)
    Q_PROPERTY(QString appuserguide READ appuserguide NOTIFY appuserguideChanged)

public:
    explicit QCustomProcessor(QQmlApplicationEngine *_qmlengine, QObject *parent = nullptr);
    ~QCustomProcessor();

    QString language() const;
    void setLanguage(const QString &_language);

    float updtdownloadprogress() const;
    void setUpdtdownloadprogress(const float _updtdownloadprogress);

    QString updtsrvurl() const;
    void setUpdtsrvurl(const QString &_updtsrvurl);

    QString srvurl() const;
    void setSrvurl(const QString &_srvurl);

    QString method() const;
    void setMethod(const QString &_method);

    QString login() const;
    void setLogin(const QString &_login);

    QString password() const;
    void setPassword(const QString &_password);

    QString appname() const;
    QString appversion() const;
    QString appdescription() const;
    QString appdisclaimer() const;
    QString companyname() const;
    QString companyaddress() const;
    QString companyphone() const;
    QString companyfax() const;
    QString companyemail() const;
    QString appuserguide() const;
    QDate   appreleasedate() const;

signals:
    void passwordChanged(const QString &_password);
    void loginChanged(const QString &_login);
    void updtsrvurlChanged(const QString &_url);
    void srvurlChanged(const QString &_url);
    void methodChanged(const QString &_method);
    void updtdownloadprogressChanged(float _value);
    void languageChanged(const QString &_language);
    void appdescriptionChanged(const QString &_value);
    void appdisclaimerChanged(const QString &_value);
    void companynameChanged(const QString &_value);
    void companyaddressChanged(const QString &_value);
    void companyphoneChanged(const QString &_value);
    void companyfaxChanged(const QString &_value);
    void companyemailChanged(const QString &_value);
    void appuserguideChanged(const QString &_value);
    void appnameChanged();
    void appversionChanged();
    void appreleasedateChanged();
    void askUpdateDialog(const QVariant &_appname, const QVariant &_version, const QVariant &_changelog);

public slots:
    void checkForUpdates();
    void processFile(const QString &filename, bool delete_after);

private slots:
    void __retranslate(const QString &_language);
    void __setupMaintenanceTool();
    void __update();

private:
    void updateAppInfo();

    QSettings *settings;
    QMap<QString,QVariant> smap;

    QQmlApplicationEngine *qmlengine;
    QTranslator translator;

    QSimpleMaintenanceTool qsmt;
    float m_updtdownloadprogress;

    struct AboutInfo {
        QString description;
        QString disclaimer;
        QString companyname;
        QString companyaddress;
        QString companyphone;
        QString companyfax;
        QString companyemail;
        QString userguide;
    } about;

    QString updatefilename, updateversion, updatechangelog;
};

#endif // QCUSTOMPROCESSOR_H
