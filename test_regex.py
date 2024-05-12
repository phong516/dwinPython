import re
import speech_recognition as sr

predefined_items = ['bánh mì', 'hamburger', 'coca']

def order(text:str):

    pattern = r'(\d+)\s+([^\d,]+)'
    matches = re.findall(pattern, text)

    quantities = []
    final_items = []

    for match in matches:
        quantity = int(match[0])
        item_name = match[1].strip()
        for predefined_item in predefined_items:
            if predefined_item in item_name:
                quantities.append(quantity)
                final_items.append(predefined_item)
                break
    input("Press to order")
    print("Input: ", text)     
    if not final_items:
        print("Vui lòng gọi các món trong menu")
    else:
        print("Quantities:", quantities)
        print("Final Items:", final_items)

r = sr.Recognizer()
while(True):
    input("Listen?")
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        content = r.recognize(audio, language='vi-VN')
        print("You said " + content)    # recognize speech using Google Speech Recognition
    except LookupError:                            # speech is unintelligible
        print("Could not understand audio") 

#order("Cho tôi 1 lon coca, 2 hamburger, 3 bánh mì")
