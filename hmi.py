import dwin
import time

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
        self.quanity : int = 0
        self.unit_price : int = unit_price
        self.total_price : int = 0


class MenuSelection: 
    def __init__(self, port:str="/dev/ttyAMA0", baudrate:int=115200, button_order:int=0x4000, text_order:int=0x6000, bill_info:str=0x6001, mic:int=0x6002):
        self.dwin = dwin.dwin(port=port, baudrate=baudrate)
        self.menu_items = {}
        self.total_price = 0
        self.button_order = button_order
        self.text_order = text_order
        self.bill_info = bill_info
        self.mic = mic

    def add_menu_item(self, name:str, vp:int, unit_price:int):
        if name not in self.menu_items:
            self.menu_items[name] = MenuItem(name, vp, unit_price)
            # self.dwin.setDataVP(vp, 0)

    def order(self, UseMic:bool=False):
        text_order_str = ""

        if not UseMic:
            for name in self.menu_items:
                self.menu_items[name].quantity = self.dwin.readDataVP(self.menu_items[name].vp)
                if self.menu_items[name].quantity == 0:
                    continue
                item = self.menu_items[name]
                self.menu_items[name].total_price = item.quantity * item.unit_price
                self.total_price += self.menu_items[name].total_price

                text_order_str += f"{remove_accents(item.name)}: {item.quantity} x {item.unit_price}k = {item.total_price}k\r\n"
        else:
            with sr.Microphone() as source:
                audio = r.listen(source)
            content = r.recognize(audio, language='vi-VN')
            pattern = r'(\d+)\s+([^\d,]+)'
            matches = re.findall(pattern, content)
            
            for match in matches:
                quantity = int(match[0])
                item_name = match[1].strip()
                for predefined_item in self.menu_items:
                    if predefined_item in item_name:
                        text_order_str += f"{remove_accents(predefined_item)}: {quantity} x {self.menu_items[predefined_item].unit_price}k = {quantity * self.menu_items[predefined_item].unit_price}k\r\n"
                        self.total_price += quantity * self.menu_items[predefined_item].unit_price
                        break
                
        text_order_str += f"Tong tien: {self.total_price}k"
        print(text_order_str)
        self.dwin.setTextVP(self.text_order, text_order_str)
        #take the date and time
        bill_info_str = f"{time.strftime('%d/%m/%Y')}\r\n{time.strftime('%H:%M:%S')}\r\n"
        self.dwin.setTextVP(self.bill_info, bill_info_str)

        return (bill_info_str + text_order_str)

            
        
