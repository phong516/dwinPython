from hmi import MenuSelection
import time

if __name__ == "__main__":
    menu = MenuSelection(port="/dev/ttyUSB0")
    menu.add_menu_item("Snack", 0x5000, 5)
    menu.add_menu_item("Water", 0x5001, 5)
    menu.add_menu_item("Hamburger", 0x5002, 15)
    menu.add_menu_item("Coke", 0x5003, 10)
    menu.add_menu_item("BanhMi", 0x5004, 10)
    menu.add_menu_item("Milk", 0x5005, 10)
    menu.add_menu_item("Pho", 0x5006, 10)
    menu.add_menu_item("IceCream", 0x5007, 10)
    while True:
        time.sleep(0.1)
        keyCode = menu.dwin.listenLastByte()
        if (keyCode == None):
            continue
        print(keyCode)
        match keyCode:
            case menu.button_order:
                print("order")
                menu.order()
            case 0x4001 | 0x4002 | 0x4003 | 0x4004:
                time.sleep(2)
                menu.dwin.switchPage(1)