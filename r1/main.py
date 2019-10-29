import pygame as pg 
from warehouse import warehouse
from box import box
import math

pg.init()
pg.display.set_caption('Warehouse Project - CPSC 463')
screen = pg.display.set_mode((1280, 720))
COLOR_INACTIVE = pg.Color(100, 100, 100)
COLOR_ACTIVE = pg.Color(255, 0, 0)
COLOR_BUTTON_BG = pg.Color(0, 0, 0)
FONT = pg.font.Font(None, 25)
HEADER_FONT = pg.font.Font(None, 32)
COLOR_CYCLE = [(255,255,255),(255,50,50),(50,255,50),(50,50,255),(255,255,50),(50,255,255),(255,50,255)]

class Graphic:
    def __init__(self, id, asset, x, y, width, height):
        self.id = id
        self.img = pg.image.load(asset)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    def update(self):
        self.x = self.x
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y, self.width, self.height))

class InputBox:
    def __init__(self, id, x, y, w, h, text=''):
        self.id = id
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class Button:
    def __init__(self, id, x, y, w, h, onClickCallback, text=''):
        self.id = id
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_BUTTON_BG
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.onClickCallback = onClickCallback

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.color = COLOR_ACTIVE
                    if self.onClickCallback:
                        self.onClickCallback()
                elif event.type == pg.MOUSEBUTTONUP:
                    self.color = COLOR_BUTTON_BG

    def update(self):
        # Resize the box if the text is too long.
        width = max(100, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


class StaticText:
    def __init__(self, id, x, y, w, h, text='', isHeader=False):
        self.id = id
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_BUTTON_BG
        self.text = text
        if isHeader:
            self.txt_surface = HEADER_FONT.render(text, True, self.color)
        else:
            self.txt_surface = FONT.render(text, True, self.color)            

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))


class DynamicText:
    def __init__(self, id, x, y, w, h, text='', count=''):
        self.id = id
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_BUTTON_BG
        self.text = text
        self.count = count

    def update(self):
        # Resize the box if the text is too long.
        ############################################# update self.text
        self.txt_surface = FONT.render(self.text + str(self.count), True, self.color)
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))


class RenderedBox:
    def __init__(self, box):
        self.box = box
        self.name = box.name

    def draw(self, screen):
        # Blit the rect.
        pg.draw.rect(screen, pg.Color(140, 140, 140, self.box.colorA), pg.Rect(self.box.x, self.box.y, self.box.width, self.box.height), 0)
        pg.draw.rect(screen, pg.Color(self.box.colorR, self.box.colorG, self.box.colorB, self.box.colorA), pg.Rect(self.box.x + 5, self.box.y + 5, self.box.width - 10, self.box.height - 10), 0)
        self.txt_surface = FONT.render(self.name, True, pg.Color(0,0,0))
        screen.blit(self.txt_surface, ((self.box.x+self.box.width/2)-(self.txt_surface.get_width()/2), (self.box.y+self.box.height/2)-5))

class InteractiveCanvas:
    def __init__(self):
        self.name = "InteractiveCanvas"
        self.isMoving = False
        self.boxActive = None
        self.startX = 0
        self.startY = 0
        
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if len(warehouses) > 0 and not self.isMoving:
                mouseCoordinates = pg.mouse.get_pos()
                activeWarehouse = warehouses[selectedWarehouseIndex]
                worldCoordinates = activeWarehouse.getWorldCoordinatesFromMouseCoordinates(mouseCoordinates[0], mouseCoordinates[1])
                boxAtWorldCoordinates = activeWarehouse.getBoxAtCoordinate(worldCoordinates[0], worldCoordinates[1])
                if boxAtWorldCoordinates:
                    self.boxActive = boxAtWorldCoordinates
                    self.startX = boxAtWorldCoordinates.x
                    self.startY = boxAtWorldCoordinates.y
                    self.isMoving = True
                    # highlight active box
                    # self.boxActive.selected = True
                    # pg.draw.rect(screen, pg.Color(250, 0, 0, self.boxActive.colorA), pg.Rect(self.boxActive.x, self.boxActive.y, self.boxActive.width, self.boxActive.height), 0)
                    #
                    for by in range(boxAtWorldCoordinates.height):
                            for bx in range(boxAtWorldCoordinates.width):
                                activeWarehouse.grid[boxAtWorldCoordinates.y + by][boxAtWorldCoordinates.x + bx] = None
        if event.type == pg.MOUSEBUTTONUP:
            if self.isMoving:
                self.isMoving = False
                # un-highlight active box
                # self.boxActive.selected = False
                # pg.draw.rect(screen, pg.Color(self.boxActive.colorR, self.boxActive.colorG, self.boxActive.colorB, self.boxActive.colorA), pg.Rect(self.boxActive.x, self.boxActive.y, self.boxActive.width, self.boxActive.height), 0)
                #
                mouseCoordinates = pg.mouse.get_pos()
                activeWarehouse = warehouses[selectedWarehouseIndex]
                newCoordinates = activeWarehouse.getWorldCoordinatesFromMouseCoordinates(mouseCoordinates[0], mouseCoordinates[1])
                if activeWarehouse.checkFit(self.boxActive, int(newCoordinates[0]), int(newCoordinates[1])):
                    self.boxActive.x = int(newCoordinates[0])
                    self.boxActive.y = int(newCoordinates[1])
                    setErrorText("")
                else:
                    setErrorText("Error collision with another box")
                    self.boxActive.x = self.startX
                    self.boxActive.y = self.startY
                for by in range(self.boxActive.height):
                            for bx in range(self.boxActive.width):
                                activeWarehouse.grid[self.startY + by][self.startX + bx] = None
                for by in range(self.boxActive.height):
                            for bx in range(self.boxActive.width):
                                activeWarehouse.grid[self.boxActive.y + by][self.boxActive.x + bx] = self.boxActive
        if event.type == pg.MOUSEMOTION:
            if self.isMoving:
                mouseCoordinates = pg.mouse.get_pos()
                activeWarehouse = warehouses[selectedWarehouseIndex]
                newCoordinates = activeWarehouse.getWorldCoordinatesFromMouseCoordinates(mouseCoordinates[0], mouseCoordinates[1])
                self.boxActive.x = newCoordinates[0]
                self.boxActive.y = newCoordinates[1]
        

def onWarehouseDimensionButtonClicked():
    newWareHouse = warehouse(int(getInputValue("warehouseWidth")), int(getInputValue("warehouseHeight")), 720, 720)
    warehouses.append(newWareHouse)
    # update UI stats
    UITxtUpdate(newWareHouse)


def onAddBoxButtonClicked():
    if len(warehouses) > 0:
        activeWarehouse = warehouses[selectedWarehouseIndex]
        color = COLOR_CYCLE[len(activeWarehouse.getboxlist()) % len(COLOR_CYCLE)]
        newBox = box(getInputValue("createObjectName"), 0, 0, int(getInputValue("createObjectWidth")), int(getInputValue("createObjectHeight")), color[0], color[1], color[2])
        for boxx in activeWarehouse.getboxlist():
            if newBox.name == boxx.name:
                print("Name already exists. Try another name.")
                setErrorText("Name already exists.")
                return False
        activeWarehouse.addBox(newBox)
        # update UI stats
        UITxtUpdate(activeWarehouse)
        setErrorText("")
    else:
        setErrorText("Error: Create a warehouse before adding a box")


def onRemoveBoxClicked():
    if len(warehouses) > 0:
        activeWarehouse = warehouses[selectedWarehouseIndex]
        activeWarehouse.removeBox(getInputValue("removeObjectName"))
        # update UI stats
        UITxtUpdate(activeWarehouse)
        setErrorText("")
    else:
        setErrorText("Error: Create a warehouse before removing a box")

def onPrintListClicked():
    if len(warehouses) > 0:
        activeWarehouse = warehouses[selectedWarehouseIndex]
        activeWarehouse.printBoxList()
        ###
        setErrorText("")
    else:
        setErrorText("Error: Create a warehouse before removing a box")


def getInputValue(inputId):
    return getInput(inputId).text


def getInput(inputId):
    for input in inputs:
        if input.id == inputId:
            return input


def setErrorText(errorText):
    getInput("errorText").text = errorText

def UITxtUpdate(warehouse):
    maxAreaDT.count = str(warehouse.area)
    spaceUsedDT.count = str(warehouse.usedSpace())
    spaceRemainingDT.count = str(warehouse.getRemainingSpace())

# Setup Warehouse UI
warehouseHeader = StaticText("warehouseHeader", 950, 40, 100, 32, "Warehouse Dimensons", True)
warehouseWidthText = StaticText("warehouseWidthST", 900, 80, 100, 32, "Warehouse Width")
warehouseWidth = InputBox("warehouseWidth", 1070, 80, 140, 32)
warehouseHeightText = StaticText("warehouseHeightST", 900, 120, 100, 32, "Warehouse Height")
warehouseHeight = InputBox("warehouseHeight", 1070, 120, 140, 32)
warehouseButton = Button("warehouseCreateButton", 900, 160, 160, 32, onWarehouseDimensionButtonClicked, "Create Warehouse")
warehouseIcon = Graphic("Warehouse", "Warehouse.png", 900, 30, 24, 24) 

# Setup Object Creation UI
createObjectHeader = StaticText("createObjectHeader", 950, 240, 100, 32, "Create Object", True)
createObjectNameText = StaticText("createObjectNameST", 900, 280, 100, 32, "Item Name")
createObjectName = InputBox("createObjectName", 1070, 280, 140, 32)
createObjectWidthText = StaticText("createObjectWidthST", 900, 320, 100, 32, "Item Width")
createObjectWidth = InputBox("createObjectWidth", 1070, 320, 140, 32)
createObjectHeightText = StaticText("wareHouseHeightST", 900, 360, 100, 32, "Item Height")
createObjectHeight = InputBox("createObjectHeight", 1070, 360, 140, 32)
createObjectButton = Button("createObjectButton", 900, 400, 160, 32, onAddBoxButtonClicked, "Create Object")
createIcon = Graphic("Box", "Box.png", 900, 230, 24, 24) 

# Setup Object Removal UI
removeObjectHeader = StaticText("createObjectHeader", 950, 480, 100, 32, "Remove Object", True)
removeObjectNameText = StaticText("removeObjectNameST", 900, 520, 100, 32, "Item Name")
removeObjectName = InputBox("removeObjectName", 1070, 520, 140, 32)
removeObjectButton = Button("removeObjectButton", 900, 560, 160, 32, onRemoveBoxClicked, "Remove Object")
removeIcon = Graphic("Remove", "Remove.png", 900, 470, 24, 24) 

# Stats UI
maxAreaDT = DynamicText("maxAreaDT", 900, 620, 100, 32, "Max Area: ", '')
spaceUsedDT = DynamicText("spaceUsedDT", 900, 650, 100, 32, "Space Used: ", '')
spaceRemainingDT = DynamicText("spaceRemainingDT", 900, 680, 100, 32, "Space Remaining: ", '')

# Setup object list print button
printList = Button("printListButton", 1150, 680, 160, 32, onPrintListClicked, "Print Box List")

# Error Text UI
errorText = DynamicText("errorText", 600, 680, 100, 32, "", '')

#Interactive Canvas for moving boxes
interactiveCanvas = InteractiveCanvas()

inputs = [warehouseHeight, warehouseWidth, warehouseButton, warehouseHeader, warehouseWidthText, warehouseHeightText, createObjectHeader,
createObjectWidthText, createObjectWidth, createObjectHeightText, createObjectHeight, createObjectButton, createObjectNameText,
createObjectName, removeObjectHeader, removeObjectNameText, removeObjectName, removeObjectButton, maxAreaDT, spaceUsedDT, spaceRemainingDT,
errorText, printList, warehouseIcon, removeIcon, createIcon, interactiveCanvas]

selectedWarehouseIndex = 0
warehouses = []
# needsRedraw = True #Later: Use this to optimize redraw loop if we need


def main():
    clock = pg.time.Clock()
    done = False
    
    while not done:
        screen.fill((255, 255, 255))
        
        if len(warehouses) > 0:
            activeWarehouse = warehouses[selectedWarehouseIndex]
            pg.draw.rect(screen, pg.Color(140, 140, 140), pg.Rect(0, 0, activeWarehouse.displayWidth, activeWarehouse.displayHeight), 0)  # draw the warehouse
            normalizedBoxes = activeWarehouse.getNormalizedBoxes()
            for boxx in normalizedBoxes:
                renderedBox = RenderedBox(boxx)
                renderedBox.draw(screen)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for boxx in inputs:
                if hasattr(boxx, 'handle_event'):
                    boxx.handle_event(event)
        # UITxtUpdate(warehouses[selectedWarehouseIndex])
        for boxx in inputs:
            if hasattr(boxx, 'update'):
                boxx.update()

        for boxx in inputs:
            if hasattr(boxx, 'draw'):
                boxx.draw(screen)

        pg.display.flip()
        clock.tick(50) #20fps


if __name__ == '__main__':
    main()
    pg.quit()