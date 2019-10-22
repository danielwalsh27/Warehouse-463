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
            self.widthMultiplier = w / h
            self.heightMultiplier = 1
            self.displayWidth = self.displayWidth * self.widthMultiplier
        elif w > h:
            self.heightMultiplier = h / w
            self.widthMultiplier = 1
            self.displayHeight = self.displayHeight * self.heightMultiplier
        self.area = w*h
        self.boxes = []
        self.grid = [[None for x in range(w)] for y in range(h)]
        self.normalizationCoefficient = 1

    def getRemainingSpace(self):
        usedArea = 0
        for x in self.boxes:
            usedArea += x.area
        return self.area - usedArea

    def usedSpace(self):
        return self.area - self.getRemainingSpace()

    def largestRemainingBoxSpace(self):
        return
        #todo

    def getboxlist(self):
        return self.boxes
        # optimization routine, todo

    ###########################################

    def canFit(self, box):  # checks if box can fit into warehouse
        if (box.x * box.y) <= self.getRemainingSpace():
            return True
        return False

    def checkFit (self, box, atX, atY):
        # Places top left corner of box at X and Y
        # Check if there is enough empty space
        if self.width - atX < box.width or self.height - atY < box.height:  # check if box steps out of bounds
            return False

        # check if box fits in current position
        for y in range(box.height):
            for x in range(box.width):
                if self.grid[atY + y][atX + x] is not None:
                    return False
        print("fits at", atX, " ", atY)
        return True
    ############################################

    def addBox(self, box):
        if not self.canFit(box):  # no possible way to fit
            print("not enough area")
            return False

        for boxx in self.boxes:
            if box.name == boxx.name:
                print("Name already exists. Try another name.")
                setErrorText("Name already exists. Try another name.")
                return False

        for y in range(self.height):    # exhaustively search grid for empty spot
            for x in range(self.width):  # stop when first fit is found
                if self.grid[y][x] is None:  # found empty spot
                    if self.checkFit(box, x, y):    # check if it fits
                        # update x and y coordinates before appending box to list
                        box.x = x
                        box.y = y
                        self.boxes.append(box)
                        for by in range(box.height):
                            for bx in range(box.width):
                                self.grid[y + by][x + bx] = box
                        return True

                    else:
                        # rotate box if it doesn't fit and try again in the same spot
                        rotatedBox = self.rotateBox(box)
                        if self.grid[y][x] is None and self.checkFit(rotatedBox, x, y):
                            # update x and y coordinates before appending box to list
                            rotatedBox.x = x
                            rotatedBox.y = y
                            self.boxes.append(rotatedBox)
                            # fill grid cells with box for its respective dimensions
                            for by in range(rotatedBox.height):
                                for bx in range(rotatedBox.width):
                                    self.grid[y + by][x + bx] = rotatedBox
                            return True
        return False

    def rotateBox(self, rtbox):  # create new instance of box with width and height flipped
        return box(rtbox.name, 0, 0, rtbox.height, rtbox.width, 0, 0, 0)

    ######################################################

    def printWarehouse(self):
        margin = ""
        for count in range(self.width):
            margin += str(count)
        print(margin)
        for y in range(self.height):
            row = "" + str(y) + " "
            for x in range(self.width):
                if self.grid[y][x] is not None:
                    row += self.grid[y][x].name
                else:
                    row += "-"
            print(row)

    def removeBox(self, name):
        for box in self.boxes:
            if box.name == name:
                for by in range(box.height):
                    for bx in range(box.width):
                        self.grid[box.y + by][box.x + bx] = None
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
        
    def getWorldCoordinatesFromMouseCoordinates(self, x, y):
        widthCoefficient = (self.displayWidth / self.width)
        heightCoefficient = (self.displayHeight / self.height)
        normalizationCoefficient = min([widthCoefficient, heightCoefficient])
        return (x / normalizationCoefficient, y / normalizationCoefficient)
        
    def getBoxAtCoordinate(self, x, y):
        for box in self.boxes:
            if x >= box.x and x <= box.x + box.width and y >= box.y and y <= box.y + box.height:
                return box