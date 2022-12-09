import os
import socket
import subprocess
import sys
import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from NetWorkMonitorGUI import Ui_NetWorkMonitor


def timeFmt():
    return time.strftime('%m-%d_%H-%M-%S', time.localtime(time.time()))


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    # print(IP)
    route = IP.split(".")
    route = route[0] + "." + route[1] + "." + route[2] + "." + "1"
    return route


class main(QMainWindow, Ui_NetWorkMonitor):
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setupUi(self)
        self.process = ''
        self.ipList = []
        self.home_path = os.environ['HOME']
        self.logPath = self.home_path + "/Desktop/NetWorkLog/"
        self.host_gh.setText(extract_ip())
        # self.initDir()
        self.setWindowOpacity(0.9)
        self.startFlag = False
        self.pingPid1 = ''
        self.pingPid2 = ''
        self.pingPid3 = ''

    def errorMsgAlert(self, msg):
        QMessageBox.critical(self, "错误", msg)

    def initDir(self):
        if os.path.exists(self.logPath):
            pass
        else:
            os.mkdir(self.logPath, 0o755)

    @QtCore.pyqtSlot()
    def on_startBtn_clicked(self):
        self.startFlag = True
        self.initDir()
        self.ipList = []
        if self.host_fixture1.isChecked() or self.host_fixture2.isChecked() or self.host_gh.isChecked():
            if self.host_fixture1.isChecked():
                ip = self.host_fixture1.text()
                fileName = "{}Fixture1_{}.log".format(self.logPath, timeFmt())
                self.process = subprocess.Popen("ping --apple-time {} > {}".format(ip, fileName), shell=True,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(self.process.pid)
                self.ipList.append({'ip': ip, 'fileName': fileName})
            if self.host_fixture2.isChecked():
                ip = self.host_fixture2.text()
                fileName = "{}Fixture2_{}.log".format(self.logPath, timeFmt())
                self.process = subprocess.Popen("ping --apple-time {} > {}".format(ip, fileName), shell=True,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.ipList.append({'ip': ip, 'fileName': fileName})
                print(self.process.pid)
            if self.host_gh.isChecked():
                ip = self.host_gh.text()
                fileName = "{}GH_{}.log".format(self.logPath, timeFmt())
                self.process = subprocess.Popen("ping --apple-time {} > {}".format(ip, fileName), shell=True,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                self.ipList.append({'ip': ip, 'fileName': fileName})
            self.startBtn.setEnabled(False)
            print(self.process.pid)
        else:
            self.errorMsgAlert("请先选择需要Ping的ip！")

    @QtCore.pyqtSlot()
    def on_stopBtn_clicked(self):
        if self.process:
            self.process.kill()
            os.system("killall -9 ping")
            self.process = ''
            self.startBtn.setEnabled(True)
        else:
            self.errorMsgAlert("还没开始Ping！")

    @QtCore.pyqtSlot()
    def on_checkLogBtn_clicked(self):
        # print("ipList:", self.ipList)
        if self.ipList:
            for i in self.ipList:
                if os.path.exists(i["fileName"]):
                    os.system("open {}".format(i["fileName"]))
                else:
                    self.errorMsgAlert("log:\"{}\"不存在！".format(i["fileName"]))
        else:
            self.errorMsgAlert("没有log信息！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = main()
    MainWindow.show()
    sys.exit(app.exec_())
