import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import os

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyService"
    _svc_display_name_ = "My Background Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)  # Set a timeout (optional)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Replace with the path to your executable
        script_path = r'D:\laragon\www\python-web\desktop-app\notification\dist\cricketnotifier.exe'
        os.system(script_path)  # Run the executable

if __name__ == '__main__':
    servicemanager.Initialize()
    servicemanager.PrepareToHostSingle(MyService)
    servicemanager.StartServiceCtrlDispatcher()
