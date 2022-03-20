#import win32ui
#import win32con

class Font:
    HEIGHT = 'height'
    WIDTH = 'width'
    FONT = 'font'
    font = {}
    def __init__(self, height, width, name, weight):
        self.font[self.HEIGHT] = height
        self.font[self.WIDTH] = width
        '''
        self.font[self.FONT] = win32ui.CreateFont({
            'name': name,
            'height': self.font[self.HEIGHT],
            'width': self.font[self.WIDTH],
            'weight': weight
        })
        '''
    def getFont(self):
        return self.font[self.FONT]
    def getHeight(self):
        return self.font[self.HEIGHT]
    def getWidth(self):
        return self.font[self.WIDTH]
        
class fontH1Bold(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(
            self, 
            height=scale_factor*font_scale, 
            width=150, 
            name=self.ARIAL, 
            #weight=win32con.FW_EXTRABOLD)

class fontH2Bold(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(
            self, 
            height=int(scale_factor*font_scale*.75), 
            width=150, 
            name=self.ARIAL, 
            #weight=win32con.FW_BOLD)

class fontCourierBold(Font):
    COURIER_NEW = 'Courier New'

    def __init__(self, scale_factor, font_scale):
        Font.__init__( 
            self, 
            height=int(scale_factor*font_scale*0.3), 
            width=75, 
            name=self.COURIER_NEW, 
            #weight=win32con.FW_BOLD 
            )

class fontArial24Bold(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__( 
            self, 
            height=int(scale_factor*font_scale*.4), 
            width=150, 
            name=self.ARIAL, 
            #weight=win32con.FW_BOLD 
            )

class fontArial12(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(
            self, 
            height=int(scale_factor*font_scale*.2), 
            width=100, 
            name=self.ARIAL, 
            #weight=win32con.FW_NORMAL
            )

class fontArial9(Font):
    ARIAL = 'arial'

    def __init__(self, scale_factor, font_scale):
        Font.__init__(
            self, 
            height=int(scale_factor*font_scale*.15), 
            width=75, 
            name=self.ARIAL, 
            #weight=win32con.FW_NORMAL
            )

class FontBuilder:
    H1Bold='H1BOLD'
    H2Bold='H2BOLD'
    COURIERBOLD='COURIERBOLD'
    ARIAL24BOLD='ARIAL24BOLD'    
    ARIAL12='ARIAL12'
    ARIAL9='ARIAL9'

    def __init__(self, scale_factor, font_scale):
        self.scale_factor = scale_factor
        self.font_scale = font_scale

    def get(self, fontType):
        match fontType.upper():
            case self.H1Bold:
                return fontH1Bold(self.scale_factor, self.font_scale)
            case self.H2Bold:
                return fontH2Bold(self.scale_factor, self.font_scale)
            case self.COURIERBOLD:
                return fontCourierBold(self.scale_factor, self.font_scale)
            case self.ARIAL24BOLD:
                return fontArial24Bold(self.scale_factor, self.font_scale)
            case self.ARIAL12:
                return fontArial12(self.scale_factor, self.font_scale)
            case self.ARIAL9:
                return fontArial9(self.scale_factor, self.font_scale)
        return fontArial12(self.scale_factor, self.font_scale)
