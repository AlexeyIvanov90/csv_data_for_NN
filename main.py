import sys
import gui

app = gui.QApplication(sys.argv)
qb = gui.Absolute()
qb.load_path()
qb.show()
sys.exit(app.exec())
