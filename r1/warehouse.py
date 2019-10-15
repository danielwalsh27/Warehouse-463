from box import box

class warehouse:
    def __init__(self, w, h, maxDisplayWidth, maxDisplayHeight):
        self.width = w
        self.height = h
        self.displayWidth = maxDisplayWidth
        self.displayHeight = maxDisplayHeight
        self.heightMultiplier = 1
        self.widthMultiplier = 1
        if h > w:
            self.widthMultiplier = w/h
            self.heightMultiplier = 1
            self.displayWidth = self.displayWidth * self.widthMultiplier
        elif w > h:
            self.heightMultiplier = h/w
            self.widthMultiplier = 1
            self.displayHeight = self.displayHeight * self.heightMultiplier    
        self.area = w*h
        self.boxes = []
    
    def getRemainingSpace(self):
        return
        #todo
    def largestRemainingBoxSpace(self):
        return
        #todo
    def reorganize(self):
        return
        #optimization routine, todo
        
    def addBox(self, box):
        self.boxes.append(box)
        
    def removeBox(self, name):
        for box in self.boxes:
            if box.name == name:
                self.boxes.remove(box)
                
    def getNormalizedBoxes(self):
        widthCoefficient = (self.displayWidth / self.width)
        heightCoefficient = (self.displayHeight / self.height)
        normalizationCoefficient = min([widthCoefficient, heightCoefficient])
        renderBoxes = []
        for currentBox in self.boxes:
            normalizedBox = box(currentBox.name, currentBox.x*normalizationCoefficient, currentBox.y*normalizationCoefficient,
                                currentBox.width*normalizationCoefficient, currentBox.height*normalizationCoefficient,
                                currentBox.colorR, currentBox.colorG, currentBox.colorB, currentBox.colorA)
            renderBoxes.append(normalizedBox)
        return renderBoxes