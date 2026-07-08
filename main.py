# This is a sample Python script.
from classes.Shotgun import Shotgun


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def main():
    print("Buckshot Roulette Lite")
    shotgun = Shotgun()
    print(shotgun)
    shotgun.load_shells(1,2)
    print(shotgun)
    shotgun.invert_shell()
    print(shotgun)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
