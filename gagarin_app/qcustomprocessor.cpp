#include "qcustomprocessor.h"

#include <QJsonDocument>
#include <QJsonObject>
#include <QQmlContext>
#include <QStandardPaths>
#include <QLocale>
#include <QDir>
#include <QTimer>
#include <QVariant>
#include <QDesktopServices>
#include <QDate>

#include "qrecognitiontaskposter.h"

QCustomProcessor::QCustomProcessor(QQmlApplicationEngine *_qmlengine, QObject *parent) : QObject(parent),
    qmlengine(_qmlengine),
	m_updtdownloadprogress(0)
{
    QDir _dir(QStandardPaths::writableLocation(QStandardPaths::GenericDataLocation).append("/%1").arg(APP_NAME));
    if(!_dir.exists())
        _dir.mkpath(_dir.absolutePath());
    settings = new QSettings(_dir.absolutePath().append("/%1.ini").arg(APP_NAME),QSettings::IniFormat,this);
    const auto list = settings->allKeys();
    for(const auto &key: list)
        smap.insert(key,settings->value(key));
    qmlengine->rootContext()->setContextProperty("customsettings",this);
    __retranslate(language());
    __setupMaintenanceTool();
    checkForUpdates();

    connect(this,SIGNAL(updtsrvurlChanged(QString)),this,SLOT(checkForUpdates()));
    connect(qmlengine->rootObjects().at(0),SIGNAL(frameCaptured(QString,bool)),this,SLOT(processFile(QString,bool)));
}



void QCustomProcessor::processFile(const QString &filename, bool delete_after)
{
    QString _filename = filename;
#ifndef Q_OS_ANDROID
    if(filename.contains("file://"))
        _filename = filename.section("file://",1,1);
#endif
    qInfo("%s -> %s", filename.toUtf8().constData(), _filename.toUtf8().constData());
    QObject *busyindicator = qmlengine->rootObjects().at(0)->findChild<QObject*>("busyIndicator");
    QObject *msgdialog = qmlengine->rootObjects().at(0)->findChild<QObject*>("messageDialog");
    QRecognitionTaskPoster *poster = new QRecognitionTaskPoster(QString("%1/gagarin/mercury%2").arg(srvurl(),method()), _filename, delete_after);
    connect(poster, &QThread::started, this, [busyindicator](){
       busyindicator->setProperty("running", true);
    });
    connect(poster, &QRecognitionTaskPoster::replyReady, this, [this, busyindicator, msgdialog](int http_status, const QByteArray &body){
        busyindicator->setProperty("running", false);

        QJsonObject json = QJsonDocument::fromJson(body).object();

        msgdialog->setProperty("customtitle",QString("POST %1").arg(method()));
        if(http_status == 0) {
            msgdialog->setProperty("color", "black");
            msgdialog->setProperty("text",tr("[0]\n\nНе удалось соединиться! Проверьте наличие подключения!"));
        } else if(http_status == 200) {
            msgdialog->setProperty("color", "black");
            msgdialog->setProperty("text",QString("[%1]\n\n%2").arg(QString::number(http_status),QJsonDocument(json).toJson()));
        } else {
            msgdialog->setProperty("color", "red");
            msgdialog->setProperty("text",QString("[%1]\n\n%2").arg(QString::number(http_status),QJsonDocument(json).toJson()));
        }
        QMetaObject::invokeMethod(msgdialog,"open");
    });
    connect(poster,SIGNAL(finished()),poster,SLOT(deleteLater()));
    poster->start();
}



QCustomProcessor::~QCustomProcessor()
{
    const auto list = smap.keys();
    for(const auto &key: list)
        settings->setValue(key,smap.value(key));
    qApp->quit();
    qInfo("I AM HERE IN QCustomProcessor::~QCustomProcessor()");
}

void QCustomProcessor::__retranslate(const QString &_language)
{
    if(_language == "Русский")
        QLocale::setDefault(QLocale(QLocale::Russian));
    else if(_language == "English")
        QLocale::setDefault(QLocale(QLocale::English,QLocale::UnitedKingdom));

    QCoreApplication::removeTranslator(&translator);
    bool _is_loaded = translator.load(QString(":/%1.qm").arg(_language));
    qDebug("%s %s",_language.toUtf8().constData(), _is_loaded ? "is loaded" : "is not loaded");
    QCoreApplication::installTranslator(&translator);
    updateAppInfo();
    if(qmlengine)
       qmlengine->retranslate();
}

QString QCustomProcessor::language() const
{
    return smap.value("Language","Русский").toString();
}

void QCustomProcessor::setLanguage(const QString &_language)
{
    if(language() != _language) {
        smap.insert("Language",_language);
        __retranslate(_language);
        emit languageChanged(_language);
    }
}

void QCustomProcessor::__setupMaintenanceTool()
{
    if(qmlengine) {
        connect(this,SIGNAL(askUpdateDialog(QVariant,QVariant,QVariant)),qmlengine->rootObjects().at(0),SLOT(showUpdateDialog(QVariant,QVariant,QVariant)));
        connect(qmlengine->rootObjects().at(0)->findChild<QObject*>("UpdateDialog"),SIGNAL(accepted()),this,SLOT(__update()));
    }
    connect(&qsmt,&QSimpleMaintenanceTool::checked,this,[this](const QList<smt::Version> &_versions){
        // If this slot is called then _versions list is not empty
        const smt::Version &_lastversion = _versions.at(0); // greatest available
        if(_lastversion.version > APP_VERSION) {            
            updateversion = _lastversion.version;
            updatechangelog = _lastversion.changelog;
            qsmt.download(_lastversion.url);
            connect(&qsmt,&QSimpleMaintenanceTool::downloadProgress,this,[this](const QString &_url, qint64 bytesReceived, qint64 bytesTotal){
                Q_UNUSED(_url)
                setUpdtdownloadprogress(static_cast<float>(bytesReceived)/bytesTotal);
            });
        }
    });
    connect(&qsmt,&QSimpleMaintenanceTool::downloaded,this,[this](const QString &_filename){
        qDebug("Downloaded to '%s'",_filename.toUtf8().constData());
        updatefilename = _filename;
        emit askUpdateDialog(APP_NAME,updateversion,updatechangelog);
    });
    connect(&qsmt,&QSimpleMaintenanceTool::error,[](QSimpleMaintenanceTool::ErrorType _errtype, const QString &_error) {
        Q_UNUSED(_errtype)
        qDebug("%s",_error.toUtf8().constData());
    });
}

float QCustomProcessor::updtdownloadprogress() const
{
    return m_updtdownloadprogress;
}

void QCustomProcessor::setUpdtdownloadprogress(const float _updtdownloadprogress)
{
    if(updtdownloadprogress() != _updtdownloadprogress) {
        m_updtdownloadprogress = _updtdownloadprogress;
        emit updtdownloadprogressChanged(_updtdownloadprogress);
    }
}

void QCustomProcessor::checkForUpdates()
{
    qsmt.check(QString("%1/updates.json").arg(updtsrvurl()));
}

void QCustomProcessor::__update()
{
    QDesktopServices::openUrl(QUrl::fromLocalFile(updatefilename));
    qApp->quit();
}

void QCustomProcessor::updateAppInfo()
{
    about.userguide = tr("<a href='https://188.225.24.25/gagarin/mercury/docs'>Инструкция</a>");
    emit appuserguideChanged(about.userguide);
    about.description = tr("Приложение предназначено для распознавания фото документов");
    emit appdescriptionChanged(about.description);
    about.disclaimer = tr("Все права принадлежат ООО \"SystemFailure\"");
    emit appdisclaimerChanged(about.disclaimer);
    about.companyname = tr("Systemfailure©");
    emit companynameChanged(about.companyname);
    about.companyaddress = tr("Россия ...");
    emit companyaddressChanged(about.companyaddress);
    about.companyphone = tr("тел.: +7(495)...");
    emit companyphoneChanged(about.companyphone);
    about.companyfax = tr("факс: +7(495)...");
    emit companyfaxChanged(about.companyfax);
    about.companyemail = tr("<a href='mailto:pi-null-mezon@yandex.ru?subject=Вопрос по программе %1'>e-mail</a>").arg(APP_NAME);
    emit companyemailChanged(about.companyemail);
}

QString QCustomProcessor::password() const
{
    return QByteArray::fromBase64(smap.value("Password").toByteArray(),QByteArray::OmitTrailingEquals);
}

void QCustomProcessor::setPassword(const QString &_password)
{
    if(_password != password()) {
        smap.insert("Password",_password.toUtf8().toBase64(QByteArray::OmitTrailingEquals));
        emit passwordChanged(_password);
    }
}

QString QCustomProcessor::login() const
{
    return smap.value("Login").toString();
}

void QCustomProcessor::setLogin(const QString &_login)
{
    if(_login != login()) {
        smap.insert("Login",_login);
        emit loginChanged(_login);
    }
}


QString QCustomProcessor::srvurl() const
{
    return smap.value("RecServer/Url","https://188.225.24.25").toString();
}

void QCustomProcessor::setSrvurl(const QString &_srvurl)
{
    if(updtsrvurl() != _srvurl) {
        smap.insert("RecServer/Url",_srvurl);
        emit srvurlChanged(_srvurl);
    }
}

QString QCustomProcessor::method() const
{
    return smap.value("UpdateServer/Method","/process").toString();
}

void QCustomProcessor::setMethod(const QString &_method)
{
    if(method() != _method) {
        smap.insert("UpdateServer/Method",_method);
        emit srvurlChanged(_method);
    }
}


QString QCustomProcessor::updtsrvurl() const
{
    return smap.value("UpdateServer/Url","https://pi-mezon.ru").toString();
}

void QCustomProcessor::setUpdtsrvurl(const QString &_updtsrvurl)
{
    if(updtsrvurl() != _updtsrvurl) {
        smap.insert("UpdateServer/Url",_updtsrvurl);
        emit updtsrvurlChanged(_updtsrvurl);
    }
}

QString QCustomProcessor::appname() const
{
    return APP_NAME;
}

QString QCustomProcessor::appversion() const
{
    return APP_VERSION;
}

QString QCustomProcessor::appdescription() const
{
    return about.description;
}

QString QCustomProcessor::appdisclaimer() const
{
    return about.disclaimer;
}

QString QCustomProcessor::companyname() const
{
    return about.companyname;
}

QString QCustomProcessor::companyaddress() const
{
    return about.companyaddress;
}

QString QCustomProcessor::companyphone() const
{
    return about.companyphone;
}

QString QCustomProcessor::companyfax() const
{
    return about.companyfax;
}

QString QCustomProcessor::companyemail() const
{
    return about.companyemail;
}

QString QCustomProcessor::appuserguide() const
{
    return about.userguide;
}

QDate QCustomProcessor::appreleasedate() const
{
    return QDate::fromString(APP_RELEASE_DATE,"dd.MM.yyyy");
}

