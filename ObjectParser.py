class ObjectParser:
    def Parser(self, fileName):
        file = open(fileName, "r")
        lines = file.readlines()
        listCarriers = []
        for x in range(0, len(lines)):
            beforeSpacer = True
            category = ""

            #Headers Detection
            if lines[x][0] == "-" and lines[x][1] == "-":
                lines[x] = lines[x][0:]
                string = ""
                placeholder = []
                if "@%@" in lines[x]:
                    strings = lines[x].split("@%@")
                    string = strings[0]
                    string = str(string[2:])
                    text = ""
                    for z in range(0, len(strings[1])):
                        text += strings[1][z]

                    placeholder = text.split(",")
                    del placeholder[len(placeholder)-1]
                else:
                    string = str(lines[x][2:])

                listCarriers.append(Carrier(True, False, 0,  string, placeholder))
                continue




            for y in range(0,len(lines[x])):

                if lines[x][y] == '@':
                    if lines[x][y+1]== '%' and lines[x][y+2] =='@':
                        beforeSpacer = False

                if beforeSpacer:
                    category += lines[x][y]
                else:
                    text = ""
                    for z in range(y+3, len(lines[x])):
                        text += lines[x][z]

                    filenames = text.split(",")
                    del filenames[len(filenames)-1]
                    print(text)

                    listCarriers.append(Carrier(False, False, 0, category, filenames))
                    break
        #del listCarriers[len(listCarriers)-1]
        return listCarriers

    def encodedParser(self, string):
        listReturn = []

        indice = 0
        beforeSpacer = True
        for y in range(0, len(string)):

            if string[y] == '@':
                if string[y+1]== '%' and string[y+2] =='@':
                    beforeSpacer = False

            if beforeSpacer == False:
                print ("this is y : " + str(y) )
                text = string[indice: y]
                listReturn.append(text)
                print(text)
                indice = y+3
                beforeSpacer = True

    #del listCarriers[len(listCarriers)-1]
        return listReturn

    def ColorAndFontParser(self, template):
        file = open(template, "r")
        lines = file.readlines()
        ColorFontList = []

        bold = False
        italic = False
        shadow = False
        underline = False
        fontName = ""
        fontsize = 11
        fontColor = "0,0,0"
        print (template)
        for line in lines:
            print (line)

            if str(line).strip() in {"0","1","2","3","4"}:
                print ("inside")
                ColorFontList.append(ColorFont(bold,italic,shadow, underline,fontName,fontsize,fontColor))
                print (" the joe " + str(ColorFontList))

            else:
                if "bold" in line:
                    if "True" in line:

                        bold = True
                    else:

                        bold = False
                if "italic" in line:
                    if "True" in line:
                        italic = True
                    else:
                        italic = False
                if "shadow" in line:
                    if "True" in line:
                        shadow = True
                    else:
                        shadow = False
                if "underLine" in line:
                    if "True" in line:
                        underline = True
                    else:
                        underline = False
                if "fontName" in line:
                    fontName = line[10:]
                if "fontSize" in line:
                    fontsize = line[10:]
                if "fontColor" in line:
                    fontColor = line[11:]


        file.close()

        return ColorFontList



class Carrier:
    Header = False
    Done = False
    Alt = 0
    Category = ""
    FileNames = []
    def __init__(self, header, done, alt, category, fileNames: []):

        self.Header = header
        self.Done = done
        self.Alt = alt
        self.Category = category
        self.FileNames = fileNames

class ColorFont:
    Bold = False
    Italic = False
    Shadow = False
    UnderLine = False
    FontName = "Calibri"
    FontSize = 11
    FontColor = 255,255,255
    def __init__(self, bold, italic, shadow, underLine, fontName, fontSize, fontColor):

        self.Bold = bold
        self.Italic = italic
        self.Shadow = shadow
        self.UnderLine = underLine
        self.FontName = fontName
        self.FontSize = fontSize
        self.FontColor = fontColor

