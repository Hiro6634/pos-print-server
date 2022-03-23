from operator import length_hint
from escpos.printer import Usb
from PIL import Image, ImageDraw, ImageFont

from ConfigHelper import ConfigHelper
from PrinterFonts import *

import json
config = ConfigHelper()


class PrnLine:
    def __init__(self, text='', font='', size=0, alignment='', resize=False, cmd='' ):
        self.text = text
        self.font = font
        self.size = size
        self.alignment = alignment
        self.resize = resize
        self.cmd=cmd

    def setCmd(self, cmd):
        self.cmd=cmd

    def getCmd(self):
        return self.cmd    

    def isCmd(self):
        return len(self.cmd) > 0

    def setText(self, text):
        self.text = text
    
    def getText(self):
        return self.text

    def setFont(self, font):
        self.font = font

    def getFont(self):
        return self.font

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def setAlignment( self, alignment ):
        self.alignment = alignment

    def getAlignment(self):
        return self.alignment

    def setResize(self, resize):
        self.resize = resize

    def getResize(self):
        return self.resize 

class PrintRepository:
    TEXT='text'
    FONT='font'
    ALIGN='align'
    CENTER='center'
    LEFT='left'
    RIGHT='right'
    LF = 'LF'
    CR = 'CR'
    CUT = 'CUT'

    VARELA_ROUND = 'VarelaRound'
    OPENS_SANS = 'OpenSans'
    MPLUS_ROUNDED_EB  = 'MPlusRoundedExtraBold'
    
    #TODO: Pasarlo al ConfigHelper
    font = 'OpenSans'
    font_size = 500
    text_align = LEFT
    prn_dpi = 203
    inches_width = 2.83465
    vendorId = 0x04b8
    productId = 0x0e15

    def __init__(self):
        self.scale_factor = 30
        self.font_scale = 35
        self.y_direction_scale = -1

        self.prn = Usb(self.vendorId, self.productId)

    def setSize(self, size ):
        self.font_size = size

    def setAlignment( self, alignment ):
        self.text_align = alignment.upper()

    def getTrueTypeFont(self, font, font_size):
        if font == 'VarelaRound':
            return ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/VarelaRound-Regular.ttf', font_size)
        elif font == 'MPlusRoundedExtraBold':
            return ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/MPLUSRounded1c-ExtraBold.ttf', font_size)
        else:    
            return ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/OpenSansCondensed-Light.ttf', font_size)

    def printLine(self, text_toprint, font='', size=-1, alignment='', resizing = False):
        font_size = self.font_size if size == -1 else size

        self.ttf = self.getTrueTypeFont( font, font_size )
        img = Image.new("L", (1,1))
        draw = ImageDraw.Draw(img)
        textSize = draw.textsize(text_toprint.strip(), spacing=4, font=self.ttf)
        # There is a bug in PIL that causes clipping of the fonts, 
        # it is described in https://stackoverflow.com/questions/1933766/fonts-clipping-with-pil
        # To avoid it, we'll add a generous +25% margin on the bottom:
        temp = list(textSize)
        temp[1] = int(temp[1] * 1.25)
        textsize = tuple(temp)

        img = Image.new("L", textSize, (255))
        draw = ImageDraw.Draw(img)
        draw.text((0, 0), text_toprint.strip(), (0), self.ttf)

        # To get rid of the unnecessary white space we've added earlier, we scan it pixel by pixel,
        # and leave only non-white rows and columns. Sadly, it is a compute-intensive task 
        # for a single board PC with ARM processor
        if( resizing ):
            print("Determining unused blank margins (this can take a while)..")
            nonwhite_positions = [(x,y) for x in range(img.size[0]) for y in range(img.size[1]) if img.getdata()[x+y*img.size[0]] != (255)] 
            rect = (min([x for x,y in nonwhite_positions]), min([y for x,y in nonwhite_positions]), max([x for x,y in nonwhite_positions]), max([y for x,y in nonwhite_positions])) # scans for unused margins of canvas
            img = img.crop(rect) # crops margins

        maxwidth = int(self.prn_dpi * self.inches_width)
        currwidth = img.size[0]
        currheight = img.size[1]

        scaling_ratio = maxwidth / currwidth

        if scaling_ratio < 1:
            img = img.resize((maxwidth,int(currheight * scaling_ratio)), Image.BILINEAR)

        nwidth, nheight = img.size
        margin = 5
        new_height = nheight + margin

        fix = Image.new("L", (nwidth, new_height), (255))
        fix.paste(img, (0, margin))
        img = fix

        # converts canvas to BW (better we do it here than rely on printer's firmware)
        img = img.convert('1')
        img.save( './p4.png' , dpi=(self.prn_dpi, self.prn_dpi)  )

        if alignment != '':
            self.prn.set(align=alignment) 
        else:
            self.prn.set(align=self.text_align) 
        print("Printing..")
        self.prn.image( './p4.png')

    def cut(self):
        self.prn.cut()
    
    def lf(self):
        self.prn.text("\n")

    def PrintDoc(self, printerName, title, lines ):
        for line in lines:
            if line.isCmd():
                if line.getCmd() == self.LF:
                    self.lf()
                elif line.getCmd() == self.CUT:
                    self.cut()
            else:
                self.printLine(line.getText(), alignment=line.getAlignment(), font=line.getFont(), size=line.getSize())


    def PrintLine(self, text='', font='', size=-1, align='', resize=False, cmd=''):
        return PrnLine( text = text, font = font, size = size, alignment = align, resize = resize, cmd = cmd )


if __name__ == '__main__':   
    lines = []
    
    myPrn = PrintRepository()
    '''
    lines.append(myPrn.PrintLine("ABCDEM H1B",FontBuilder.H1Bold, PrintRepository.CENTER))
    lines.append(myPrn.PrintLine("ABCDEM H1B",FontBuilder.H1Bold, PrintRepository.LEFT))
    lines.append(myPrn.PrintLine("ABCDEM H1B",FontBuilder.H1Bold, PrintRepository.RIGHT))
    lines.append(myPrn.PrintLine("ABCDEM H2B",FontBuilder.H2Bold, PrintRepository.LEFT))
    lines.append(myPrn.PrintLine("ABCDEM COURIER_B",FontBuilder.COURIERBOLD, PrintRepository.CENTER))
    lines.append(myPrn.PrintLine("ABCDEM A24_B",FontBuilder.ARIAL24BOLD, PrintRepository.RIGHT))
    lines.append(myPrn.PrintLine("123",FontBuilder.ARIAL12, PrintRepository.RIGHT))
    lines.append(myPrn.PrintLine("ABCDEM A12",FontBuilder.ARIAL12, PrintRepository.LEFT))

    myPrn.PrintDoc(config.getPrinterName(), config.getTicketHeader(), lines)
    '''
    #myPrn.printRpyTest("Hola Mundos!")
    print("Start Printing...")
    myPrn.setSize(40)
    #myPrn.setAlignment(myPrn.CENTER)
    myPrn.printLine(config.getTicketHeader(), font="VarelaRound", alignment=myPrn.CENTER, resizing=False)
    myPrn.lf()

    myPrn.setAlignment(myPrn.CENTER)
    myPrn.setSize(150)
    myPrn.printLine("HAMBURGESA",font='MPlusRoundedExtraBold', resizing=False)
    myPrn.lf()
    
    #myPrn.setAlignment(myPrn.RIGHT)
    myPrn.setSize(20)
    myPrn.printLine("2022-04-10 11:00:00.000", font="VarelaRound", alignment=myPrn.RIGHT, resizing=False )
    
    myPrn.lf()
    myPrn.cut()

    myPrn.setSize(40)
    #myPrn.setAlignment(myPrn.CENTER)
    myPrn.printLine(config.getTicketHeader(), font="VarelaRound", alignment=myPrn.CENTER, resizing=False)
    myPrn.lf()

    myPrn.setAlignment(myPrn.CENTER)
    myPrn.setSize(150)
    myPrn.printLine("HARUMAKI X3", font="MPlusRoundedExtraBold",resizing=False)
    myPrn.lf()

    #myPrn.setAlignment(myPrn.RIGHT)
    myPrn.setSize(20)
    myPrn.printLine("2022-04-10 11:00:00.000", font="VarelaRound", alignment=myPrn.RIGHT, resizing=False )
    
    myPrn.lf()
    
    myPrn.cut()
    myPrn.setSize(40)
    #myPrn.setAlignment(myPrn.CENTER)
    myPrn.printLine(config.getTicketHeader(), alignment=myPrn.CENTER, resizing=False)
    myPrn.lf()
    myPrn.setSize(25)
    #myPrn.setAlignment(myPrn.RIGHT)
    myPrn.printLine("HAMBURGUESA x 1 $180", alignment=myPrn.RIGHT, resizing=False)
    myPrn.printLine("HARUMAKI X3 x 1 $220", alignment=myPrn.RIGHT, resizing=False)
    #myPrn.setAlignment(myPrn.RIGHT)
    myPrn.printLine("=============================================", alignment=myPrn.RIGHT, resizing=False)
    myPrn.setSize(50)
    #myPrn.setAlignment(myPrn.RIGHT)
    myPrn.printLine("TOTAL $400", alignment=myPrn.RIGHT, resizing=False)

    #myPrn.setAlignment(myPrn.CENTER)
    myPrn.setSize(20)
    myPrn.printLine("HIRO SUYAMA           2022-04-10 11:00:00.000", alignment=myPrn.CENTER, resizing=False)

    print("Cutting")
    myPrn.cut()
