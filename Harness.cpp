#include <QCoreApplication>
#include <QProcess>
#include <QStringList>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    QProcess process;
    process.setProgram("TestApp.exe");
    if(argc == 2){
        QStringList args;
        args << argv[1];
        process.setArguments(args);
    }
    else if(argc > 2){
        return -1;
    }
    process.start();
    process.waitForFinished(100);
    return 0;
}
