from ConfigHelper import ConfigHelper
import win32ui
import win32con
from PrinterFonts import *

import json
config = ConfigHelper()
class PrintRepository:
    TEXT='text'
    FONT='font'
    ALIGN='align'
    CENTER='center'
    LEFT='left'
    RIGHT='right'
    
    def __init__(self):
        self.scale_factor = 30
        self.font_scale = 35
        self.y_direction_scale = -1

    def PrintDoc(self, printerName, title, lines):
        r=0
        c=0
        fontBld = FontBuilder(self.scale_factor, self.font_scale)
        dc = win32ui.CreateDC()
        dc.CreatePrinterDC(printerName)
        dc.SetMapMode(win32con.MM_TWIPS)
        dc.StartDoc(title)
        dc.StartPage()
        dc.SetTextColor(0x00000000)
        dc.SetBkMode(win32con.TRANSPARENT)
        print(lines)
        for line in lines:
            font = line[self.FONT]
            text = line[self.TEXT]
            dc.SelectObject(fontBld.get(font).getFont())
            dc.TextOut( 
                self.ALignment(
                    r, 
                    line[self.ALIGN], 
                    len(text)*fontBld.get(font).getWidth()
                ),
                c * self.y_direction_scale, 
                text)
            c = c +  fontBld.get(font).getHeight()
        
        dc.EndPage()
        dc.EndDoc()

    def ALignment(self, row, alignment, size ):
        widthPaper = config.getPaperWidthMW()
        leftSize = 0
        match alignment:
            case self.RIGHT:
                leftSize = widthPaper - size
                return leftSize
            case self.CENTER:
                leftSize = int((widthPaper - size)/2)
                return leftSize
        return row

    def PrintLine(self, text, font, align):
        return { self.TEXT: text, self.FONT: font, self.ALIGN: align}

    def printTest(self):
        x_y = 0, 0
        fontBld = FontBuilder(self.scale_factor, self.font_scale)
        print("Starting test...")    
        printerName = config.getPrinterName()
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

        dc.SelectObject(fontBld.get(FontBuilder.COURIERBOLD).getFont() )
        dc.TextOut(x_y[0], x_y[1] * self.y_direction_scale, "AGARRALA")
        x_y = x_y[0], x_y[1] + fontBld.get(FontBuilder.COURIERBOLD).getHeight()
        dc.EndPage()
        dc.EndDoc()


if __name__ == '__main__':   
    lines = []

    myPrn = PrintRepository()

    lines.append(myPrn.PrintLine("ABCDEM H1B",FontBuilder.H1Bold, PrintRepository.CENTER))
    lines.append(myPrn.PrintLine("ABCDEM H1B",FontBuilder.H1Bold, PrintRepository.LEFT))
    lines.append(myPrn.PrintLine("ABCDEM H1B",FontBuilder.H1Bold, PrintRepository.RIGHT))
    lines.append(myPrn.PrintLine("ABCDEM H2B",FontBuilder.H2Bold, PrintRepository.LEFT))
    lines.append(myPrn.PrintLine("ABCDEM COURIER_B",FontBuilder.COURIERBOLD, PrintRepository.CENTER))
    lines.append(myPrn.PrintLine("ABCDEM A24_B",FontBuilder.ARIAL24BOLD, PrintRepository.RIGHT))
    lines.append(myPrn.PrintLine("123",FontBuilder.ARIAL12, PrintRepository.RIGHT))
    lines.append(myPrn.PrintLine("ABCDEM A12",FontBuilder.ARIAL12, PrintRepository.LEFT))

    myPrn.PrintDoc(config.getPrinterName(), config.getTicketHeader(), lines)


