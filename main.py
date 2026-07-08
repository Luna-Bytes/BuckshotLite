from classes.Shotgun import Shotgun

def main():
    print("Buckshot Roulette Lite")
    shotgun = Shotgun()
    print(shotgun)
    shotgun.load_shells(1,2)
    print(shotgun)
    shotgun.invert_shell()
    print(shotgun)


if __name__ == '__main__':
    main()
