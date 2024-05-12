import dwin
import time
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
    def __init__(self, port:str="/dev/ttyAMA0", baudrate:int=115200, button_order:int=0x4000, text_order:int=0x6000, bill_info:str=0x6001):
        self.dwin = dwin.dwin(port=port, baudrate=baudrate)
        self.menu_items = {}
        self.total_price = 0
        self.button_order = button_order
        self.text_order = text_order
        self.bill_info = bill_info

    def add_menu_item(self, name:str, vp:int, unit_price:int):
        if name not in self.menu_items:
            self.menu_items[name] = MenuItem(name, vp, unit_price)
            # self.dwin.setDataVP(vp, 0)

    def order(self):
        text_order_str = ""
        for name in self.menu_items:
            self.menu_items[name].quantity = self.dwin.readDataVP(self.menu_items[name].vp)
            if self.menu_items[name].quantity == 0:
                continue
            item = self.menu_items[name]
            self.menu_items[name].total_price = item.quantity * item.unit_price
            self.total_price += self.menu_items[name].total_price

            text_order_str += f"{item.name}: {item.quantity} x {item.unit_price}k = {item.total_price}k\r\n"

        text_order_str += f"Total price: {self.total_price}k"
        print(text_order_str)
        self.dwin.setTextVP(self.text_order, text_order_str)
        #take the date and time
        bill_info_str = f"{time.strftime('%d/%m/%Y')}\r\n{time.strftime('%H:%M:%S')}\r\n"
        self.dwin.setTextVP(self.bill_info, bill_info_str)