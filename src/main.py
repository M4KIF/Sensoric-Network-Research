##################################################
# Main code of the Sensoric network research app #
# Made by Jakub Koterba                          #
##################################################


###########
# Imports #
###########


# Main app structure
from packages.window import window_gui as gui

import sys


#################
# Main function #
#################


def main():

    app = gui.QApplication(sys.argv)

    window = gui.Window()
    window.setFixedSize(1368, 768)

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
