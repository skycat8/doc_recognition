QT += quick network multimedia svg widgets

android {
    QT += androidextras
}


TEMPLATE = app
CONFIG += c++14

TARGET = gagarin
VERSION = 0.0.0.1

DEFINES += APP_NAME=\\\"$${TARGET}\\\" \
           APP_VERSION=\\\"$${VERSION}\\\" \
           APP_DESIGNER=\\\"Alex.A.Taranov\\\"

win32: DEFINES += APP_RELEASE_DATE=\\\"$$system("echo %date%")\\\"
linux: DEFINES += APP_RELEASE_DATE=\\\"$$system("date +%d.%m.%Y")\\\"

SOURCES += \
    main.cpp \
    qcustomprocessor.cpp \
    qrecognitiontaskposter.cpp


HEADERS += \
    qcustomprocessor.h \
    qrecognitiontaskposter.h


include($${PWD}/../../QSimpleMaintenanceTool/qsimplemaintenancetool.pri)

RESOURCES += declarative-camera.qrc \
             $$files(Resources/*.png) \
             $$files(Resources/*.svg)

DEFINES += QT_MESSAGELOGCONTEXT \
           QT_NO_DEBUG_OUTPUT

android: include(/home/alex/Android/Sdk/android_openssl/openssl.pri)

TRANSLATIONS += English.ts

DISTFILES += \
    android/AndroidManifest.xml \
    android/build.gradle \
    android/gradle/wrapper/gradle-wrapper.jar \
    android/gradle/wrapper/gradle-wrapper.properties \
    android/gradlew \
    android/gradlew.bat \
    android/res/values/libs.xml

ANDROID_PACKAGE_SOURCE_DIR = $$PWD/android


