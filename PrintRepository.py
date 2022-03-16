from ConfigHelper import ConfigHelper
import win32ui
import win32con
import json

class Font:
    HEIGHT = 'height'
    WIDTH = 'width'
    FONT = 'font'
    font = {}
    def __init__(self, height, width, name, weight):
        self.font[self.HEIGHT] = height
        self.font[self.WIDTH] = width
        self.font[self.FONT] = win32ui.CreateFont({
            'name': name,
            'height': self.font[self.HEIGHT],
            'width': self.font[self.WIDTH],
            'weight': weight
        })
    def getFont(self):
        return self.font[self.FONT]
    def getHeight(self):
        return self.font[self.HEIGHT]
    def getWidth(self):
        return self.font[self.WIDTH]
        
class fontH1Bold(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(self, height=scale_factor*font_scale, width=175, name=self.ARIAL, weight=win32con.FW_EXTRABOLD)

class fontH2Bold(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(self, height=scale_factor*font_scale, width=175, name=self.ARIAL, weight=win32con.FW_BOLD)

class fontH3(Font):
    COURIER_NEW = 'Courier New'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(self, height=int(scale_factor*font_scale/3.0), width=90, name=self.COURIER_NEW, weight=win32con.FW_BOLD)

class fontH4(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(self, height=int(scale_factor*font_scale/1.5), width=175, name=self.ARIAL, weight=win32con.FW_BOLD)

class FontBuilder:
    H1Bold='H1BOLD'
    H2Bold='H2BOLD'
    H3='H3'
    H4='H4'    
    def __init__(self, scale_factor, font_scale):
        self.scale_factor = scale_factor
        self.font_scale = font_scale

    def get(self, fontType):
        match fontType.upper():
            case self.H1Bold:
                return fontH1Bold(self.scale_factor, self.font_scale)
            case self.H2Bold:
                return fontH2Bold(self.scale_factor, self.font_scale)
            case self.H3:
                return fontH3(self.scale_factor, self.font_scale)
            case self.H4:
                return fontH4(self.scale_factor, self.font_scale)
        return fontH4(self.scale_factor, self.font_scale)



class PrintRepository:
    def __init__(self):
        self.config = ConfigHelper()
        self.scale_factor = 30
        self.font_scale = 35
        self.y_direction_scale = -1

    def Printdoc(self, printerName, title, lines):
        dc = win32ui.CreateDC()
        dc.CreatePrinterDC(printerName)
        dc.SetMapMode(win32con.MM_TWIPS)
        dc.StartDoc(title)
        dc.StartPage()
        dc.SetTextColor(0x00000000)
        dc.SetBkMode(win32con.TRANSPARENT)
        for line in lines:
            dc.SelectObject(FontBuilder.get(line['font']).getFont())
        dc.EndPage()
        dc.EndDoc()


    def TestPrintDoc(self):
        pass

    def printTest(self):
        x_y = 0, 0
        fontBld = FontBuilder(self.scale_factor, self.font_scale)
        print("Starting test...")    
        printerName = self.config.getPrinterName()
        print("Printer:" + printerName)
        dc = win32ui.CreateDC()
        dc.CreatePrinterDC(printerName)
        dc.SetMapMode(win32con.MM_TWIPS)
        dc.StartDoc("AJB-Ticekt")
        dc.StartPage()
        dc.SetTextColor(0x00000000)
        dc.SetBkMode(win32con.TRANSPARENT)
#        dc.SelectObject(myfont )
        dc.SelectObject(fontBld.get(FontBuilder.H1Bold).getFont() )
        #for i in range(len(samplePrintText)):
            #dc.TextOut(0, i*30*y_direction_scale, samplePrintText[i])
            #dc.MoveTo(0,i*y_direction_scale)
            #dc.LineTo(0,i*y_direction_scale)
        #dc.TextOut(x_y[0], x_y[1] * y_direction_scale, "HOLA MUNDO")

        dc.TextOut(x_y[0], x_y[1] * self.y_direction_scale, "HOLA MUNDO")
        x_y = x_y[0], x_y[1] + fontBld.get(FontBuilder.H1Bold).getHeight()

        dc.SelectObject(fontBld.get(FontBuilder.H2Bold).getFont() )
        dc.TextOut(x_y[0], x_y[1] * self.y_direction_scale, "ARACA LA CANA")
        x_y = x_y[0], x_y[1] + fontBld.get(FontBuilder.H2Bold).getHeight()

        dc.SelectObject(fontBld.get(FontBuilder.H3).getFont() )
        dc.TextOut(x_y[0], x_y[1] * self.y_direction_scale, "AGARRALA")
        x_y = x_y[0], x_y[1] + fontBld.get(FontBuilder.H3).getHeight()
        dc.EndPage()
        dc.EndDoc()


if __name__ == '__main__':   
    myPrn = PrintRepository()

    myPrn.printTest()

