import dwin
import time
import speech_recognition as sr
import re

def remove_accents(input_str):
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỈỉỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỴỵỶỷỸỹ'
    s0 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaEeEeEeEeEeEeEeEeIiIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyYy'    
    s = ""
    print(input_str.encode('utf-8'))
    for c in input_str:
        if c in s1:
            s += s0[s1.index(c)]
        else:
            s += c
    return s

class MenuItem:
    def __init__(self, name:str, vp:int, unit_price:int):
        self.name : str = name
        self.vp : int = vp
        self.quantity : int = 0
        self.unit_price : int = unit_price
        self.total_price : int = 0


class MenuSelection: 
    def __init__(self, port:str="/dev/ttyAMA0", baudrate:int=115200, button_order:int=0x4000, button_yes:int=0x3000, button_mic:int=0x5000, text_order:int=0x6000):
        self.dwin = dwin.dwin(port=port, baudrate=baudrate)
        self.menu_items = {}
        self.button_order = button_order
        self.button_yes = button_yes
        self.button_mic = button_mic
        self.text_order = text_order

    def add_menu_item(self, name:str, vp:int, unit_price:int):
        if name not in self.menu_items:
            self.menu_items[name] = MenuItem(name, vp, unit_price)

    def startOrder(self):
        self.dwin.switchPage(1)

    def resetOrder(self):
        self.dwin.switchPage(0)

    def order(self, UseMic:bool=False):
        text_order_str = ""
        total_price:int = 0
        if not UseMic:
            for name in self.menu_items:
                self.menu_items[name].quantity = self.dwin.readDataVP(self.menu_items[name].vp)
                if self.menu_items[name].quantity == 0:
                    continue
                self.dwin.setDataVP(self.menu_items[name].vp, 0)    
                item = self.menu_items[name]
                self.menu_items[name].total_price = item.quantity * item.unit_price
                total_price += self.menu_items[name].total_price

                text_order_str += f"{remove_accents(item.name)}: {item.quantity} x {item.unit_price}k = {item.total_price}k\r\n"
        else:
            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
            content = recognizer.recognize_google(audio, language='vi-VN')
            print(content)
            pattern = r'(\d+)\s+([^\d,]+)'
            matches = re.findall(pattern, content)
            self.dwin.switchPage(4)
            for match in matches:
                quantity = int(match[0])
                item_name = match[1].strip()
                for predefined_item in self.menu_items:
                    if predefined_item in item_name:
                        text_order_str += f"{remove_accents(predefined_item)}: {quantity} x {self.menu_items[predefined_item].unit_price}k = {quantity * self.menu_items[predefined_item].unit_price}k\r\n"
                        total_price += quantity * self.menu_items[predefined_item].unit_price
                        break
            
        text_order_str += f"Tong tien: {total_price}k"
        # self.dwin.setTextVP(self.text_order, text_order_str)
        #take the date and time
        bill_info_str = f"{time.strftime('%d/%m/%Y')}\r\n{time.strftime('%H:%M:%S')}\r\n"
        # self.dwin.setTextVP(self.bill_info, bill_info_str)
        self.dwin.setTextVP(self.text_order, bill_info_str + text_order_str)

        return (bill_info_str + text_order_str)

            
        
