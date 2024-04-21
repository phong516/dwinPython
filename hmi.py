import dwin

data_quantity_1 = 0x5000
button_increase_1 = 0x3000

class MenuItem:
    def __init__(self, name:str, vp:int, unit_price:int):
        self.name = name
        self.vp = vp
        self.quanity = 0
        self.unit_price = unit_price
        self.total_price = 0


class MenuSelection: 
    def __init__(self, port:str="/dev/ttyAMA0", baudrate:int=115200, button_order:int=0x4000, text_order:int=0x6000):
        self.dwin = dwin.dwin(port=port, baudrate=baudrate)
        self.menu_items = {}
        self.button_order = button_order
        self.text_order = text_order
        self.total_price = 0

    def add_menu_item(self, name:str, vp:int, unit_price:int):
        if name not in self.menu_items:
            self.menu_items[name] = MenuItem(name, vp, unit_price)
            self.dwin.setDataVP(vp, 0)

    def order(self):
        text_order_str = ""
        for name in self.menu_items:
            self.menu_items[name].quantity = self.dwin.readDataVP(self.menu_items[name].vp)
            item = self.menu_items[name]
            self.menu_items[name].total_price = item.quantity * item.unit_price
            self.total_price += self.menu_items[name].total_price

            text_order_str += f"{item.name}: {item.quantity} x {item.unit_price} = {item.total_price}\r\n"

        text_order_str += f"Total price: {self.total_price}"
        self.dwin.setTextVP(self.text_order, text_order_str)