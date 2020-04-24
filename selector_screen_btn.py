from RPi import GPIO
import signal
import time


from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


class Selector_screen_btn:

    def __init__(self, select_btn, down_btn, up_btn):
        GPIO.setmode(GPIO.BCM)

        self.selected = False
        self.index = 0
        
        self.font = ImageFont.load_default()   
        
        self.select_btn = select_btn
        self.down_btn = down_btn
        self.up_btn = up_btn
        
        GPIO.setup(select_btn,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(down_btn,GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(up_btn,GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(select_btn, GPIO.FALLING, callback=self.select_btn_callback, bouncetime=100)
        GPIO.add_event_detect(down_btn, GPIO.FALLING, callback=self.down_btn_callback, bouncetime=100)
        GPIO.add_event_detect(up_btn, GPIO.FALLING, callback=self.up_btn_callback, bouncetime=100)
        
        i2c = busio.I2C(SCL, SDA)
        self.disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
         
        # Clear display.
        self.disp.fill(0)
        self.disp.show()
         
        self.width = self.disp.width
        self.height = self.disp.height
        self.image = Image.new("1", (self.width, self.height))
         
        draw = ImageDraw.Draw(self.image)
         
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

    def select_btn_callback(self, channel):
        self.selected = True
        
    def down_btn_callback(self, channel):
        self.index = self.index - 1
        
    def up_btn_callback(self, channel):
        self.index = self.index + 1
        
    def clear_screen(self): 
         
        draw = ImageDraw.Draw(self.image)
        
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
      
        # Display image.
        self.disp.image(self.image)
        self.disp.show()
        time.sleep(0.1)

    def draw_text_screen(self, lines, scrollbar = False, scrollPercent = 0): 

        
        while(len(lines)<4):
            lines.append(" ")
         
        draw = ImageDraw.Draw(self.image)
        
        draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)
        # Write four lines of text.
        
        x = 0
        padding = -2
        top = padding
        bottom = self.height - padding
        
        draw.text((x, top + 0), lines[0], font=self.font, fill=255)
        draw.text((x, top + 8), lines[1], font=self.font, fill=255)
        draw.text((x, top + 16), lines[2], font=self.font, fill=255)
        draw.text((x, top + 25), lines[3], font=self.font, fill=255)
        
        if scrollbar:
            draw.rectangle([self.width-5, 0, self.width-1,  self.height-1], fill=0, outline=255, width=1)
                    
            heightScroll = int(scrollPercent*((self.height-4)/100))
            
            draw.line([self.width-6, 0, self.width-6,  self.height], fill=0, width=1)
            draw.rectangle([self.width-5, heightScroll, self.width-1,  heightScroll+4], fill=255, outline=255, width=1)
     
        # Display image.
        self.disp.image(self.image)
        self.disp.show()
        
    
    def draw_text_screen_wait_select(self, lines): 
        self.draw_text_screen(lines)
        while(self.selected == False):
            time.sleep(0.1)
        self.selected = False
    
    
    def draw_text_screen_two_choices_selector(self, lines, choices): 
        
        self.selected = False
        self.index = 0
        
        while(len(lines)<2):
            lines.append(" ")

        while self.selected == False:
            if self.index < 0:
                self.index = 0
            if self.index > 1:
                self.index = 1
            
            to_draw = lines.copy()

            if self.index == 0:
                txt = ">"+choices[0]+"< "+choices[1]
            else:
                txt = choices[0]+" >"+choices[1]+"<"
                
            txt = self.add_center_padding_text(txt)
            
            to_draw.append(txt)
            
            self.draw_text_screen(to_draw)
                
            time.sleep(0.1)
        
        self.selected = False
        return (self.index,choices[self.index])
    
    def draw_text_with_delay(self, lines, delay):    
        
        while(len(lines)<3):
            lines.append(" ")
            
        for i in range(delay, -1, -1):      
            time.sleep(1)
            to_draw = lines.copy()
            
            to_draw.append(str(i)+"s")
            self.draw_text_screen(to_draw)
        
    def draw_text_screen_selector(self, lines, scrollbar = False):
        
        self.selected = False
        self.index = 0

        while self.selected == False:
            if self.index < 0:
                self.index = 0
            if self.index >= len(lines):
                self.index = len(lines)-1
                
            if self.index+4 > len(lines):
                to_draw = lines[len(lines)-4:len(lines)]
                if len(lines)<4:
                    to_draw[self.index] = "> "+to_draw[self.index]
                else:
                    to_draw[4-(len(lines)-self.index)] = "> "+to_draw[4-(len(lines)-self.index)]
                self.draw_text_screen(to_draw, scrollbar, self.index/(len(lines)-1)*100)
            else:
                to_draw = lines[self.index:self.index+4]
                to_draw[0] = "> "+to_draw[0]
                self.draw_text_screen(to_draw, scrollbar, self.index/(len(lines)-1)*100 )
                
            
            
            time.sleep(0.1)
        
        self.selected = False
        return (self.index,lines[self.index])
        
    def draw_text_screen_selector_with_title(self, title, lines):
        
        self.selected = False
        self.index = 0

        while self.selected == False:
            if self.index < 0:
                self.index = 0
            if self.index >= len(lines):
                self.index = len(lines)-1
                
            if self.index+3 > len(lines):
                to_draw = lines[len(lines)-3:len(lines)]
                if len(lines)<3:
                    to_draw[self.index] = "> "+to_draw[self.index]
                else:
                    to_draw[3-(len(lines)-self.index)] = "> "+to_draw[3-(len(lines)-self.index)]
                self.draw_text_screen([title]+to_draw)
            else:
                to_draw = lines[self.index:self.index+3]
                to_draw[0] = "> "+to_draw[0]
                
                self.draw_text_screen([title]+to_draw)
            time.sleep(0.1)
        
        self.selected = False
        return (self.index,lines[self.index])
        
    def add_center_padding_text(self, text):
    
        textWidth = self.font.getsize(text)[0]
        while textWidth<self.width :
            text = " "+text + " "
            textWidth = self.font.getsize(text)[0]
        return text
    
    def add_right_padding_text(self, text):
        
        textWidth = self.font.getsize(" " + text)[0]
        while textWidth<self.width :
            text = " " + text
            textWidth = self.font.getsize(" " + text)[0]
        return text
        
    
