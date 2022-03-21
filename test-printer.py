
#!/usr/bin/env python3
debug = 0

import argparse
parser = argparse.ArgumentParser(description="Renders provided Unicode string as image and prints it on a POS printer")
parser.add_argument("-t", "--text", type=str, help="The text to print. For a multi-line text, prefix the parameter with the dollar sign: $'Мама\\nмыла раму' ")
parser.add_argument("-s", "--size", type=int, help="Override the auto font size (80 pt is recommended)")
parser.add_argument("-w", "--wrap", type=int, help="Force-wrap text lines at a given position (default: 50)")
parser.add_argument("-c", "--crop",  type=str, help="Cut paper roll after printing (default: yes)",
  choices=["yes","no"])
parser.add_argument("-f", "--font", type=str, help="The font to use (if omitted, the default font is Oswald)",
  choices=["Caveat","Roboto","JetBrainsMono","Oswald","Lato","OpenSans","OpenSansBold","Yanone"])

args = parser.parse_args()
text_toprint = args.text # works with Unicode!

word_wrap = 50
if args.wrap:
    try:
        word_wrap = int(args.wrap) # value from command line overrides default
    except ValueError:
        word_wrap = 50

import textwrap
if debug ==1:
    print("Initial text: ")
    print(str(text_toprint))
text_toprint = '\n'.join(['\n'.join(textwrap.wrap(line, word_wrap, break_long_words=True, replace_whitespace=False, expand_tabs=True)) for line in text_toprint.splitlines() if line.strip() != ''])
# Misc. cleanup:
text_toprint = text_toprint.replace("❏","*")
if debug ==1:
    print("Text processed by textwrap:")
    print(str(text_toprint))


prn_dpi = 203 # check out printer's specifications
inches_width = 2.83465 # width of the adhesive paper roll, in inches (72mm for 80mm roll)

length_list = text_toprint.split('\n')
max_line_length = 0

for i in length_list:
    max_line_length = max(max_line_length, len(i))
print("Longest line: {} chars".format(max_line_length))

# For the longer labels we'll reduce the font size, to bring the image size down and to improve the speed of the subsequent image manipulations.
# Tune those values for the font you are using:
if(max_line_length <= 2): font_size = 500
if(max_line_length > 2 and max_line_length <= 10): font_size = int(400 - max_line_length * 10.47)
if(max_line_length >= 11 and max_line_length < 20): font_size = int(200 - max_line_length * 5.21)
if(max_line_length >= 20 and max_line_length < 80): font_size = int(80 - max_line_length * 0.5)
if(max_line_length >= 80): font_size =  50 # font under 30 points is unreadable on my printer
    
if debug == 1:
    workdir = "/var/www/html" # saves image to the root dir of the web server, which allows debugging via web browser (install Nginx to easily access generated images)
else:
    workdir = "/var/www/tmp"

if args.size:
    try:
        font_size = int(args.size) # value from command line overrides auto font size
        print("Font size will be force-set by user to: {}pt".format(font_size))
    except ValueError:
        font_size = 80
        print("Font size reset to: {}pt".format(font_size))
else:
    print("Font size was automatically set to: {}pt".format(font_size))

print("Length of text: {} chars".format(len(text_toprint)))
print("{} lines in total".format(text_toprint.count('\n') + 1))

from PIL import Image, ImageDraw, ImageFont
if args.font == "JetBrainsMono":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/JetBrainsMono-1.0.3/ttf/JetBrainsMono-Regular.ttf', font_size) # get it from https://www.jetbrains.com/lp/mono/
elif args.font == "Lato":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Lato-Regular.ttf', font_size) # get it from https://github.com/google/fonts
elif args.font == "Roboto":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Roboto-Regular.ttf', font_size)
elif args.font == "OpenSans":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/OpenSansCondensed-Light.ttf', font_size)
elif args.font == "OpenSansBold":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/OpenSans-Bold.ttf', font_size)
elif args.font == "Caveat":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Caveat-Regular.ttf', font_size)
elif args.font == "Yanone":
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/YanoneKaffeesatz-Regular.ttf', font_size)
else:
    ttf=ImageFont.truetype('/usr/share/fonts/truetype/google-fonts/Oswald-Regular.ttf', font_size)

# Determine text size using a scratch image. Initially it is in grayscale, we'll convert it into B/W later.
img = Image.new("L", (1,1))
draw = ImageDraw.Draw(img)
textsize = draw.textsize(text_toprint.strip(), spacing=4, font=ttf)
# There is a bug in PIL that causes clipping of the fonts, 
# it is described in https://stackoverflow.com/questions/1933766/fonts-clipping-with-pil
# To avoid it, we'll add a generous +25% margin on the bottom:
temp = list(textsize)
temp[1] = int(temp[1] * 1.25)
textsize = tuple(temp)

img = Image.new("L", textsize, (255))
draw = ImageDraw.Draw(img)
draw.text((0, 0), text_toprint.strip(), (0), ttf)
print("Result is: {}px × {}px".format(img.size[0], img.size[1]))
if debug == 1: img.save(workdir + '/p1.png' , dpi=(prn_dpi, prn_dpi)  )

# To get rid of the unnecessary white space we've added earlier, we scan it pixel by pixel,
# and leave only non-white rows and columns. Sadly, it is a compute-intensive task 
# for a single board PC with ARM processor
print("Determining unused blank margins (this can take a while)..")
nonwhite_positions = [(x,y) for x in range(img.size[0]) for y in range(img.size[1]) if img.getdata()[x+y*img.size[0]] != (255)] 
rect = (min([x for x,y in nonwhite_positions]), min([y for x,y in nonwhite_positions]), max([x for x,y in nonwhite_positions]), max([y for x,y in nonwhite_positions])) # scans for unused margins of canvas
print("Cropping image..")
img = img.crop(rect) # crops margins
if debug == 1: img.save(workdir + '/p2.png' , dpi=(prn_dpi, prn_dpi)  )
print("Result is: {}px × {}px".format(img.size[0], img.size[1]))

# resize to fit the paper width:
maxwidth = int(prn_dpi * inches_width)
currwidth = img.size[0]
currheight = img.size[1]
print("Max allowed width is: {}px, actual width is {}px".format(maxwidth, currwidth))
scaling_ratio = maxwidth / currwidth
print("Scaling factor needs to be {}%".format(int(scaling_ratio*100)))
if scaling_ratio < 1:
    img = img.resize((maxwidth,int(currheight * scaling_ratio)), Image.BILINEAR)
    print("Resized to: {}px × {}px".format(maxwidth,int(currheight * scaling_ratio)))
else:
    print("No downscaling was required, will leave image as-is.")
if debug == 1: img.save(workdir + '/p3.png' , dpi=(prn_dpi, prn_dpi)  )

# fixes issue with poorly printed top margin (adds spare 5px on top)
nwidth, nheight = img.size
margin = 5
new_height = nheight + margin
print("Size with margin: {}px × {}px".format(nwidth,new_height))
fix = Image.new("L", (nwidth, new_height), (255))
fix.paste(img, (0, margin))
img = fix

# converts canvas to BW (better we do it here than rely on printer's firmware)
img = img.convert('1')
img.save(workdir + '/p4.png' , dpi=(prn_dpi, prn_dpi)  )

# sends the image to printer
from escpos.printer import Usb
#p = Usb(0x2730, 0x0fff, in_ep=0x81, out_ep=0x02)
p = Usb(0x04b8, 0x0e15, 0)
p.set(align=u'center') 
print("Printing..")
p.image(workdir + '/p4.png')

# p.qr("https://yandex.ru/maps/-/CShNUNmr", size=12)

if args.crop != "no":
    print("Cropping paper: {}".format(str(args.crop)))
    p.cut(mode='FULL')
else:
    print("Cropping paper is disabled.")
print("Finished.")
