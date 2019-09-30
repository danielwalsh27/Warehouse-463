from box import box

class warehouse:
    def __init__(self, w, h, displayWidth, displayHeight):
        self.width = w
        self.height = h
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
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
        normalizationCoefficient = min([(self.displayWidth / self.width), (self.displayHeight / self.height)])
        renderBoxes = []
        for currentBox in self.boxes:
            normalizedBox = box(currentBox.name, currentBox.x*normalizationCoefficient, currentBox.y*normalizationCoefficient,
                                currentBox.width*normalizationCoefficient, currentBox.height*normalizationCoefficient,
                                currentBox.colorR, currentBox.colorG, currentBox.colorB, currentBox.colorA)
            renderBoxes.append(normalizedBox)
        return renderBoxes