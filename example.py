from selector_screen_btn import Selector_screen_btn
from time import sleep

#Creation of Screen Button Selector Object, using pin 20, 8 and 7
screen_btn = Selector_screen_btn(20, 8, 7)      


#Simple text
screen_btn.draw_text_screen(["Hello World","left", screen_btn.add_center_padding_text("center"), screen_btn.add_right_padding_text("right")])
sleep(2)

#Simple text Waiting for press of select button
screen_btn.draw_text_screen_wait_select(["Hello World", "standard","alignment", "press >select< button"])

#Simple text using center padding
screen_btn.draw_text_screen_wait_select(["Hello World", screen_btn.add_center_padding_text("center"), screen_btn.add_center_padding_text("alignment"), screen_btn.add_center_padding_text("press >select< button")])

#Delay GUI
screen_btn.draw_text_with_delay(["A delay GUI", "wait"], 5)

screen_btn.draw_text_with_delay(["Selector GUI", "following"], 3)
#Selector GUI with more than 4 lines (GUI only show 4 lines at a time)
choice = screen_btn.draw_text_screen_selector(["a", "b", "c", "d", "e", "f"])
print(choice) 
choice = screen_btn.draw_text_screen_selector(["a", "b", "c", "d", "e", "f"], True)
print(choice) 

#Selector GUI with more less than 4 lines (GUI only show 4 lines at a time)
choice = screen_btn.draw_text_screen_selector(["a", "b", "c"])
print(choice)

#Selector GUI with a Title
choice = screen_btn.draw_text_screen_selector_with_title("Selector GUI w Title", ["a", "b", "c", "d", "e", "f"])
print(choice)


screen_btn.draw_text_screen_two_choices_selector([screen_btn.add_center_padding_text("Two buttons selector")],["yes","no"])

screen_btn.clear_screen()