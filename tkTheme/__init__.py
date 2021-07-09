import tkinter as tk

#class Theme, which holds values for the colors and that the program should use for all widgets.  Default values approximate Tkinter defaults.
class Theme:

    #default values
    default_title = "default theme"
    default_bg = "#F0F0F0" #94% gray
    default_fg = "black"
    default_selectbg = "#0078D7" #default blue highlight
    default_selectfg = "white"
    default_contrast_bg = "white"
    default_contrast_fg = "black"
    default_contrast_selectbg = "#0078D7" #default blue highlight
    default_contrast_selectfg = "white"

    #list of all acceptable color representations from the X11 protocol, which are the color names accepted by tkinter
    x11colors = ['snow', 'ghost white', 'GhostWhite', 'white smoke', 'WhiteSmoke', 'gainsboro', 'floral white', 'FloralWhite', 'old lace', 'OldLace', 'linen', 'antique white', 'AntiqueWhite', 'papaya whip', 'PapayaWhip', 'blanched almond', 'BlanchedAlmond', 'bisque', 'peach puff', 'PeachPuff', 'navajo white', 'NavajoWhite', 'moccasin', 'cornsilk', 'ivory', 'lemon chiffon', 'LemonChiffon', 'seashell', 'honeydew', 'mint cream', 'MintCream', 'azure', 'alice blue', 'AliceBlue', 'lavender', 'lavender blush', 'LavenderBlush', 'misty rose', 'MistyRose', 'white', 'black', 'dark slate gray', 'DarkSlateGray', 'dark slate grey', 'DarkSlateGrey', 'dim gray', 'DimGray', 'dim grey', 'DimGrey', 'slate gray', 'SlateGray', 'slate grey', 'SlateGrey', 'light slate gray', 'LightSlateGray', 'light slate grey', 'LightSlateGrey', 'gray', 'grey', 'light grey', 'LightGrey', 'light gray', 'LightGray', 'midnight blue', 'MidnightBlue', 'navy', 'navy blue', 'NavyBlue', 'cornflower blue', 'CornflowerBlue', 'dark slate blue', 'DarkSlateBlue', 'slate blue', 'SlateBlue', 'medium slate blue', 'MediumSlateBlue', 'light slate blue', 'LightSlateBlue', 'medium blue', 'MediumBlue', 'royal blue', 'RoyalBlue', 'blue', 'dodger blue', 'DodgerBlue', 'deep sky blue', 'DeepSkyBlue', 'sky blue', 'SkyBlue', 'light sky blue', 'LightSkyBlue', 'steel blue', 'SteelBlue', 'light steel blue', 'LightSteelBlue', 'light blue', 'LightBlue', 'powder blue', 'PowderBlue', 'pale turquoise', 'PaleTurquoise', 'dark turquoise', 'DarkTurquoise', 'medium turquoise', 'MediumTurquoise', 'turquoise', 'cyan', 'light cyan', 'LightCyan', 'cadet blue', 'CadetBlue', 'medium aquamarine', 'MediumAquamarine', 'aquamarine', 'dark green', 'DarkGreen', 'dark olive green', 'DarkOliveGreen', 'dark sea green', 'DarkSeaGreen', 'sea green', 'SeaGreen', 'medium sea green', 'MediumSeaGreen', 'light sea green', 'LightSeaGreen', 'pale green', 'PaleGreen', 'spring green', 'SpringGreen', 'lawn green', 'LawnGreen', 'green', 'chartreuse', 'medium spring green', 'MediumSpringGreen', 'green yellow', 'GreenYellow', 'lime green', 'LimeGreen', 'yellow green', 'YellowGreen', 'forest green', 'ForestGreen', 'olive drab', 'OliveDrab', 'dark khaki', 'DarkKhaki', 'khaki', 'pale goldenrod', 'PaleGoldenrod', 'light goldenrod yellow', 'LightGoldenrodYellow', 'light yellow', 'LightYellow', 'yellow', 'gold', 'light goldenrod', 'LightGoldenrod', 'goldenrod', 'dark goldenrod', 'DarkGoldenrod', 'rosy brown', 'RosyBrown', 'indian red', 'IndianRed', 'saddle brown', 'SaddleBrown', 'sienna', 'peru', 'burlywood', 'beige', 'wheat', 'sandy brown', 'SandyBrown', 'tan', 'chocolate', 'firebrick', 'brown', 'dark salmon', 'DarkSalmon', 'salmon', 'light salmon', 'LightSalmon', 'orange', 'dark orange', 'DarkOrange', 'coral', 'light coral', 'LightCoral', 'tomato', 'orange red', 'OrangeRed', 'red', 'hot pink', 'HotPink', 'deep pink', 'DeepPink', 'pink', 'light pink', 'LightPink', 'pale violet red', 'PaleVioletRed', 'maroon', 'medium violet red', 'MediumVioletRed', 'violet red', 'VioletRed', 'magenta', 'violet', 'plum', 'orchid', 'medium orchid', 'MediumOrchid', 'dark orchid', 'DarkOrchid', 'dark violet', 'DarkViolet', 'blue violet', 'BlueViolet', 'purple', 'medium purple', 'MediumPurple', 'thistle', 'snow1', 'snow2', 'snow3', 'snow4', 'seashell1', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'bisque1', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff1', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'NavajoWhite1', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'LemonChiffon1', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk1', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'ivory1', 'ivory2', 'ivory3', 'ivory4', 'honeydew1', 'honeydew2', 'honeydew3', 'honeydew4', 'LavenderBlush1', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose1', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'azure1', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue1', 'blue2', 'blue3', 'blue4', 'DodgerBlue1', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue1', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3', 'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCyan1', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan1', 'cyan2', 'cyan3', 'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4', 'aquamarine1', 'aquamarine2', 'aquamarine3', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'SeaGreen4', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'SpringGreen1', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'green1', 'green2', 'green3', 'green4', 'chartreuse1', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'OliveDrab1', 'OliveDrab2', 'OliveDrab3', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightYellow1', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow1', 'yellow2', 'yellow3', 'yellow4', 'gold1', 'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1', 'tan2', 'tan3', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'chocolate4', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'LightSalmon1', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange1', 'orange2', 'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'coral1', 'coral2', 'coral3', 'coral4', 'tomato1', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed1', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'red1', 'red2', 'red3', 'red4', 'DeepPink1', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'magenta1', 'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1', 'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'gray0', 'grey0', 'gray1', 'grey1', 'gray2', 'grey2', 'gray3', 'grey3', 'gray4', 'grey4', 'gray5', 'grey5', 'gray6', 'grey6', 'gray7', 'grey7', 'gray8', 'grey8', 'gray9', 'grey9', 'gray10', 'grey10', 'gray11', 'grey11', 'gray12', 'grey12', 'gray13', 'grey13', 'gray14', 'grey14', 'gray15', 'grey15', 'gray16', 'grey16', 'gray17', 'grey17', 'gray18', 'grey18', 'gray19', 'grey19', 'gray20', 'grey20', 'gray21', 'grey21', 'gray22', 'grey22', 'gray23', 'grey23', 'gray24', 'grey24', 'gray25', 'grey25', 'gray26', 'grey26', 'gray27', 'grey27', 'gray28', 'grey28', 'gray29', 'grey29', 'gray30', 'grey30', 'gray31', 'grey31', 'gray32', 'grey32', 'gray33', 'grey33', 'gray34', 'grey34', 'gray35', 'grey35', 'gray36', 'grey36', 'gray37', 'grey37', 'gray38', 'grey38', 'gray39', 'grey39', 'gray40', 'grey40', 'gray41', 'grey41', 'gray42', 'grey42', 'gray43', 'grey43', 'gray44', 'grey44', 'gray45', 'grey45', 'gray46', 'grey46', 'gray47', 'grey47', 'gray48', 'grey48', 'gray49', 'grey49', 'gray50', 'grey50', 'gray51', 'grey51', 'gray52', 'grey52', 'gray53', 'grey53', 'gray54', 'grey54', 'gray55', 'grey55', 'gray56', 'grey56', 'gray57', 'grey57', 'gray58', 'grey58', 'gray59', 'grey59', 'gray60', 'grey60', 'gray61', 'grey61', 'gray62', 'grey62', 'gray63', 'grey63', 'gray64', 'grey64', 'gray65', 'grey65', 'gray66', 'grey66', 'gray67', 'grey67', 'gray68', 'grey68', 'gray69', 'grey69', 'gray70', 'grey70', 'gray71', 'grey71', 'gray72', 'grey72', 'gray73', 'grey73', 'gray74', 'grey74', 'gray75', 'grey75', 'gray76', 'grey76', 'gray77', 'grey77', 'gray78', 'grey78', 'gray79', 'grey79', 'gray80', 'grey80', 'gray81', 'grey81', 'gray82', 'grey82', 'gray83', 'grey83', 'gray84', 'grey84', 'gray85', 'grey85', 'gray86', 'grey86', 'gray87', 'grey87', 'gray88', 'grey88', 'gray89', 'grey89', 'gray90', 'grey90', 'gray91', 'grey91', 'gray92', 'grey92', 'gray93', 'grey93', 'gray94', 'grey94', 'gray95', 'grey95', 'gray96', 'grey96', 'gray97', 'grey97', 'gray98', 'grey98', 'gray99', 'grey99', 'gray100', 'grey100', 'dark grey', 'DarkGrey', 'dark gray', 'DarkGray', 'dark blue', 'DarkBlue', 'dark cyan', 'DarkCyan', 'dark magenta', 'DarkMagenta', 'dark red', 'DarkRed', 'light green', 'LightGreen']

    #static function that returns True if the given string represents a color, false otherwise
    def isColor(color):
        if isinstance(color, str):
            #parse if color is a valid rgb hex code
            if len(color) in [4, 7, 10]:
                if color[0] == '#' and all(cc in '0123456789abcdefABCDEF' for cc in color[1:]):
                    return True
            #parse if color is a valid X11 named color
            if color in Theme.x11colors:
                return True
        return False

    def __init__(self, title=None, bg=None, fg=None, selectbg=None, selectfg=None, contrast_bg=None, contrast_fg=None, contrast_selectbg=None, contrast_selectfg=None):
        #inititalize theme title
        if isinstance(title, str):
            self.title = title
        else:
            self.title = Theme.default_title

        #inititalize values
        if Theme.isColor(bg): #background color to be used for most elements
            self.bg=bg
        else: 
            self.bg = Theme.default_bg 

        if Theme.isColor(fg): #foreground color to be used for most elements
            self.fg=fg
        else: 
            self.fg = Theme.default_fg

        if Theme.isColor(selectbg): #background color used when highlighting text
            self.selectbg=selectbg
        else: 
            self.selectbg = Theme.default_selectbg

        if Theme.isColor(selectfg): #foreground color used when highlighting text
            self.selectfg=selectfg
        else: 
            self.selectfg = Theme.default_selectfg

        if Theme.isColor(contrast_bg): #background color to be used for elements that need to stand out from surrounding widgets
            self.contrast_bg=contrast_bg
        else: 
            self.contrast_bg = Theme.default_contrast_bg

        if Theme.isColor(contrast_fg): #foreground color to be used for elements that need to stand out from surrounding widgets
            self.contrast_fg=contrast_fg
        else: 
            self.contrast_fg = Theme.default_contrast_fg

        if Theme.isColor(contrast_selectbg): #background color used when highlighting text on elements that need to stand out from surrounding widgets
            self.contrast_selectbg=contrast_selectbg
        else: 
            self.contrast_selectbg = Theme.default_contrast_selectbg

        if Theme.isColor(contrast_selectfg): #foreground color used when highlighting text on elements that need to stand out from surrounding widgets
            self.contrast_selectfg=contrast_selectfg
        else: 
            self.contrast_selectfg = Theme.default_contrast_selectfg

    #Theme.set(), method for setting the theme's title and color attributes
    def set(self, title=None, bg=None, fg=None, selectbg=None, selectfg=None, contrast_bg=None, contrast_fg=None, contrast_selectbg=None, contrast_selectfg=None):
        if isinstance(title, str):
            self.title = title

        #inititalize values
        if Theme.isColor(bg): #background color to be used for most elements
            self.bg=bg

        if Theme.isColor(fg): #foreground color to be used for most elements
            self.fg=fg

        if Theme.isColor(selectbg): #background color used when highlighting text
            self.selectbg=selectbg

        if Theme.isColor(selectfg): #foreground color used when highlighting text
            self.selectfg=selectfg

        if Theme.isColor(contrast_bg): #background color to be used for elements that need to stand out from surrounding widgets
            self.contrast_bg=contrast_bg

        if Theme.isColor(contrast_fg): #foreground color to be used for elements that need to stand out from surrounding widgets
            self.contrast_fg=contrast_fg

        if Theme.isColor(contrast_selectbg): #background color used when highlighting text on elements that need to stand out from surrounding widgets
            self.contrast_selectbg=contrast_selectbg

        if Theme.isColor(contrast_selectfg): #foreground color used when highlighting text on elements that need to stand out from surrounding widgets
            self.contrast_selectfg=contrast_selectfg

    #Theme.apply(), passing this method a supported widget will automatically reconfigure its colors according to the theme
    def apply(self, widget):
        if isinstance(widget, list):  #if passed a list of widgets, recursively handle all widgets
            for oo in widget:
                self.apply(oo)

        if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
            widget.config(bg=self.bg)

        elif isinstance(widget, tk.Frame):
            widget.config(bg=self.bg)

        elif isinstance(widget, tk.LabelFrame):
            widget.config(bg=self.bg, fg=self.fg)

        elif isinstance(widget, tk.Label):
            widget.config(bg=self.bg, fg=self.fg)

        elif isinstance(widget, tk.Button) or isinstance(widget, tk.Menubutton):
            widget.config(bg=self.bg, fg=self.fg, activebackground=self.bg, activeforeground=self.fg)

        elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
            widget.config(bg=self.contrast_bg, fg=self.contrast_fg, selectbackground=self.contrast_selectbg, selectforeground=self.contrast_selectfg)
       
        elif isinstance(widget, tk.Checkbutton) or isinstance(widget, Radiobutton):
            widget.config(bg=self.bg, fg='black', activebackground=self.bg, activeforeground=self.bg)
        
        elif isinstance (widget, tk.Menu):
            widget.config(bg=self.contrast_bg, fg=self.contrast_fg, activebackground=self.contrast_selectbg, activeforeground=self.contrast_selectfg, disabledforeground=None)
        
        return widget

    #Theme objects are callable as an alias of Theme.apply()
    __call__ = apply

#class ThemeAndFont, a container class for Theme which also includes attributes for the font family and size
class ThemeAndFont:
    #default font values
    default_family = "Segoe UI" #Windows Default
    default_size = 9

    def __init__(self, theme = None, family = None, size = None):
        #initialize theme
        if isinstance(theme, Theme):
            self.theme = theme
        else:
            self.theme = Theme()

        #initialize font family
        if isinstance(family, str):
            self.family = family
        else:
            self.family = ThemeAndFont.default_family

        #initialize font size
        if isinstance(size, str):
            if all(cc in '-0123456789' for cc in size):
                self.size = int(size)
        elif isinstance(size, int):
            self.size = size
        else:
            self.size = ThemeAndFont.default_size

    #ThemeAndFont.set(), method for setting a new theme, font family, and/or font size
    def set(self, theme = None, family = None, size = None):
        #set theme
        if isinstance(theme, Theme):
            self.theme = theme

        #set font family
        if isinstance(family, str):
            self.family = family

        #set font size
        if isinstance(size, str):
            if all(cc in '-0123456789' for cc in size):
                self.size = int(size)
        elif isinstance(size, int):
            self.size = size  

    #ThemeAndFont.apply(), passing this method a supported widget will automatically reconfigure its color theme and font
    def apply(self, widget):
        if isinstance(widget, list):  #if passed a list of widgets, recursively handle all widgets
            for oo in widget:
                self.apply(oo)

        if isinstance(widget, tk.Tk) or isinstance(widget, tk.Toplevel):
            widget.config(bg=self.theme.bg)

        elif isinstance(widget, tk.Frame):
            widget.config(bg=self.theme.bg)

        elif isinstance(widget, tk.LabelFrame):
            widget.config(bg=self.theme.bg, fg=self.theme.fg, font=(self.family, self.size+2))

        elif isinstance(widget, tk.Label):
            widget.config(bg=self.theme.bg, fg=self.theme.fg, font=(self.family, self.size))

        elif isinstance(widget, tk.Button) or isinstance(widget, tk.Menubutton):
            widget.config(bg=self.theme.bg, fg=self.theme.fg, activebackground=self.theme.bg, activeforeground=self.theme.fg, font=(self.family, self.size))

        elif isinstance(widget, tk.Entry) or isinstance(widget, tk.Text):
            widget.config(bg=self.theme.contrast_bg, fg=self.theme.contrast_fg, selectbackground=self.theme.contrast_selectbg, selectforeground=self.theme.contrast_selectfg, font=(self.family, self.size))
        
        elif isinstance(widget, tk.Checkbutton) or isinstance(widget, tk.Radiobutton):
            widget.config(bg=self.theme.bg, fg='black', activebackground=self.theme.bg, activeforeground=self.theme.bg, font=(self.family, self.size))

        elif isinstance (widget, tk.Menu):
            widget.config(bg=self.theme.contrast_bg, fg=self.theme.contrast_fg, activebackground=self.theme.contrast_selectbg, activeforeground=self.theme.contrast_selectfg, disabledforeground=None, font=(self.family, self.size))
        
        return widget

    #ThemeAndFont objects are callable as an alias of ThemeAndFont.apply()
    __call__ = apply 

#Testing stuff
if __name__ == "__main__":
    print(all(Theme.isColor(oo) for oo in Theme.x11colors))
    Th = Theme(bg='red', fg = 'purple4', contrast_bg = 'PaleVioletRed2', contrast_fg = 'LimeGreen', contrast_selectbg='MediumSpringGreen', contrast_selectfg='purple')
    T = ThemeAndFont(theme=Th, family = 'Comic Sans MS', size = 19)
    root = T(tk.Tk())
    T(tk.Label(root, text="Hello")).pack()
    T(tk.Button(root, text="Hi")).pack()
    T(tk.Text(root)).pack()
    T(tk.Checkbutton(root)).pack()

    root.mainloop()