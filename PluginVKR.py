import cutter
import json
from PySide2.QtCore import QObject, SIGNAL
from PySide2.QtWidgets import QAction, QLabel, QMessageBox, QMenu, QFileDialog

class MyDockWidget(cutter.CutterDockWidget):
    def __init__(self, parent, action):
        super(MyDockWidget, self).__init__(parent, action)
        self.setObjectName("MyDockWidget")
        self.setWindowTitle("PluginVKR")

        self._label = QLabel(self)
        self.setWidget(self._label)

        QObject.connect(cutter.core(), SIGNAL("seekChanged(RVA)"), self.update_contents)
        self.update_contents()

    def update_contents(self):
        disasm = cutter.cmd("pd 1").strip()

        instruction = cutter.cmdj("pdj 1")
        size = instruction[0]["size"]

        self._label.setText("Current disassembly:\n{}\nwith size {}".format(disasm, size))


class MyCutterPlugin(cutter.CutterPlugin):
    name = "PluginVKR"
    description = "Разметка в дизассемблере блоков кода после фаззинга"
    version = "1.0"
    author = "I.Eremin"
    action2 = None
    config = {}
    mainwindow = None
    
    def setupPlugin(self):
        pass

    def setupInterface(self, main):
        action = QAction("PluginVKR", main)
        action.setCheckable(True)
        
        # получить ссылку на секцию Edit(правка) главного меню приложения
        print(main.getMenuByType(cutter.MainWindow.MenuType.Edit)) # ОТЛАДКА
        mainMenu = main.getMenuByType(cutter.MainWindow.MenuType.Edit)

        # завести строку меню
        self.action2 = QAction("Запуск PluginVKR")
        # привязать к строке функцию (пока это лямбда-выражение)
        self.action2.triggered.connect(self.hilight)
        # поместить строку в меню
        mainMenu.addAction(self.action2)
        
        widget = MyDockWidget(main, action)
        main.addPluginDockWidget(widget, action)
        self.mainwindow = main

    def terminate(self):
        pass
    
    def hilight(self):
        # QMessageBox.information(self.mainwindow,
        #                         "Окно из плагина", "Текст сообщения")
        fileName = QFileDialog.getOpenFileName(self.mainwindow,
            caption="Открыть отчёт покрытия фаззинга",
            dir=".",
            filter="Текстовые файлы (*.txt *.json)")
        print(fileName)
        if fileName[0] is None:
            print("Exit")
            return
        file = open(fileName[0], "r")
        jsonReport = json.load(file)
        file.close()
        max_occurences = int(jsonReport["max_occurences"][1])
        print("max_occurences = ", max_occurences)
        
        core = cutter.core()
        highlighter = core.getBBHighlighter()
        # for key in jsonReport["bb"].keys():
        #     highlighter.highlight(0x1001deac8, "#FF0000")
        for key in jsonReport["bb"].keys():
            clr = 0xFF * int(jsonReport["bb"][key]) // max_occurences
            print(f"clr = {clr:x}")
            # color_string = 
            highlighter.highlight(int(key, base=16) + 0x140000000, f"#ff{clr:x}{clr:x}")
        return


def create_cutter_plugin():
    return MyCutterPlugin()