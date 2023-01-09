
##################################################
# Main code of the Sensoric network research app #
# Made by Jakub Koterba, Karolina Bińka,         #
# Maciej Wrona, Hubert Wilga, Mateusz Tężyński   #
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
    print("Is it okey?")

    app = gui.QApplication(sys.argv)

    window = gui.Window()
    window.setFixedSize(1280,720)

    window.show()

    sys.exit(app.exec())

if __name__ =="__main__":
    main()
