from hmi import MenuSelection
import time

if __name__ == "__main__":
    menu = MenuSelection()
    menu.add_menu_item("Snack", 0x5000, 5)
    menu.add_menu_item("Water", 0x5001, 5)
    menu.add_menu_item("Hamburger", 0x5002, 15)
    menu.add_menu_item("Coke", 0x5003, 10)
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