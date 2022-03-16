import win32ui
import win32con

class fontH1Bold:
    HEIGHT = 'height'
    WIDTH = 'width'
    FONT = 'font'
    ARIAL = 'arial'
    def __init__(self, scale_factor, font_scale):
        self.font[self.HEIGHT] = scale_factor * font_scale
        self.font[self.WIDTH] = 175
        self.font[self.FONT] = win32ui.CreateFont({
            'name': self.ARIAL,
            'height': self.font[self.HEIGHT],
            'width': self.font[self.WIDTH],
            'weight': win32con.FW_EXTRABOLD
        })
    def getFont(self):
        return self.font

class PrintRepository:
    def __inti__(self):
        pass

    def printTest(self):
        
