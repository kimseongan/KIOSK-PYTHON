import time
import os
from tkinter import *


class Sandwich:
    def __init__(self):
        self.Smenu = {
            "햄에그치즈 샌드위치": 7500,
            "크래미 와사비 샌드위치": 8000,
            "핫치킨 샌드위치": 6500,
            "치킨텐더 샌드위치": 7500,
            "데리야끼치킨 샌드위치": 7500
        }

    def SW_menu(self):
        return self.Smenu

class Coffee:
    def __init__(self):
        self.Cmenu = {
            "아메리카노": 4000,
            "카페라테": 3000,
            "카푸치노": 4000,
            "바닐라라테": 4500
        }

    def C_menu(self):
        return self.Cmenu

    def toppings(self, toppings_list):
        total_charge = 0
        toppings_prices = {
            "펄": 700,
            "휘핑크림": 500,
            "초코칩": 1000,
            "설탕": 0
        }
        for topping in toppings_list:
            if topping in toppings_prices:
                total_charge += toppings_prices[topping]
        return total_charge

class Discount(Coffee):
    def __init__(self):
        super().__init__()

    def take_out(self, total_price):
        discounted_price = total_price * 0.90
        return discounted_price

class Display:
   
    def display_menu(menu):
        for item, price in menu.items():
            print(f"{item}: {price}원")

def write_receipt(order, toppings_list, total, discounted):
    receipt_path = "receipt.txt"
    with open(receipt_path, "w", encoding="utf-8") as f:
        f.write("<<<<<<<<<<<영수증>>>>>>>>>>>>>>>>\n")
        f.write(f"주문 날짜/시간: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("주문 내역:\n")
        for i, item in enumerate(order, 1):
            f.write(f"{i}. {item}\n")
        if toppings_list:
            f.write("\n추가 토핑:\n")
            for topping in toppings_list:
                f.write(f"- {topping}\n")
        f.write(f"\n총 금액: {total}원\n")
        if discounted:
            f.write(f"할인 적용된 총 금액: {discounted:.0f}원\n")

    # 메모장으로 영수증 파일 실행
    os.system(f"notepad.exe {receipt_path}")

def kiosk():
    coffee_instance = Discount()
    sandwich_instance = Sandwich()

    def show_menu():
        sandwich_menu = sandwich_instance.SW_menu()
        coffee_menu = coffee_instance.C_menu()

        menu_text = "샌드위치 메뉴:\n"
        for item, price in sandwich_menu.items():
            menu_text += f"{item}: {price}원\n"

        menu_text += "\n커피 메뉴:\n"
        for item, price in coffee_menu.items():
            menu_text += f"{item}: {price}원\n"
        
        menu_text +="\n주문을 하실려면, 창을 단아주세요!"

        menu_label.config(text=menu_text)

    root = Tk()
    root.title("Kiosk")

    menu_label = Label(root, text="", justify=LEFT, padx=20, pady=20)
    menu_label.pack()

    show_menu()

    root.mainloop()

    order = []
    while True:
        choice = input("원하는 메뉴를 입력하세요 (다음을 입력하려면 '다음' 입력): ")
        if choice in coffee_instance.C_menu() or choice in sandwich_instance.SW_menu():
            order.append(choice)
            print(f"{choice} 추가되었습니다.\n")
        elif choice == "다음":
            break
        else:
            print("잘못된 선택입니다. 다시 시도하세요.")

    if order:
        print("음료에 추가할 토핑을 선택하세요:")
        toppings_list = []
        while True:
            topping = input("추가할 토핑을 입력하세요 (펄, 휘핑크림, 초코칩, 설탕 중 선택, 다음을 입력하려면 '다음' 입력): ").strip().lower()
            if topping in ["펄", "휘핑크림", "초코칩", "설탕"]:
                toppings_list.append(topping)
                print(f"{topping}이(가) 추가되었습니다.\n")
            elif topping == "다음":
                break
            else:
                print("잘못된 선택입니다. 다시 시도하세요.")

        extra_charge = coffee_instance.toppings(toppings_list)

        print("주문이 완료되었습니다:")
        for item in order:
            print(f"- {item}")
        total = sum([coffee_instance.C_menu().get(item, 0) for item in order]) + sum([sandwich_instance.SW_menu().get(item, 0) for item in order]) + extra_charge
        print(f"\n추가된 토핑 금액: {extra_charge}원")
        take_out = input("테이크아웃 하시겠습니까? (예/아니오): ").strip().lower()
        if take_out == "예":
            discounted_total = coffee_instance.take_out(total)
            print(f"테이크아웃 할인 적용된 총 금액: {discounted_total:.0f}원")
        else:
            discounted_total = None
            print(f"총 금액: {total}원")
        
        receipt = input("영수증 출력하시겠습니까? (예/아니오)").strip().lower()
        if receipt == "예":
            write_receipt(order, toppings_list, total, discounted_total)
        else:
            try:
                os.remove('receipt.txt')
            except FileNotFoundError:
                pass

        print("\n주문을 준비 중입니다. 잠시만 기다려 주세요...")
        time.sleep(3)
        print("주문이 나왔습니다.")
        
    else:
        print("주문이 취소되었습니다.")

if __name__ == "__main__":
    kiosk()
