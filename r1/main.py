import pygame as pg 
from warehouse import warehouse
from box import box

pg.init()
pg.display.set_caption('Warehouse Project - CPSC 463')
screen = pg.display.set_mode((1280, 720))
COLOR_INACTIVE = pg.Color(100, 100, 100)
COLOR_ACTIVE = pg.Color(250, 0, 0)
COLOR_BUTTON_BG = pg.Color(0, 0, 0)
FONT = pg.font.Font(None, 25)
HEADER_FONT = pg.font.Font(None, 32)


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
        width = max(200, self.txt_surface.get_width()+10)
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
    def __init__(self, id, x, y, w, h, text=''):
        self.id = id
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_BUTTON_BG
        self.text = text

    def update(self):
        # Resize the box if the text is too long.
        self.txt_surface = FONT.render(self.text, True, self.color)
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
        pg.draw.rect(screen, pg.Color(self.box.colorR, self.box.colorG, self.box.colorB, self.box.colorA), pg.Rect(self.box.x, self.box.y, self.box.width, self.box.height), 0)


def onWarehouseDimensionButtonClicked():
    newWareHouse = warehouse(int(getInputValue("warehouseWidth")), int(getInputValue("warehouseHeight")), 720, 720)
    warehouses.append(newWareHouse)


def onAddBoxButtonClicked():
    if len(warehouses) > 0:
        activeWarehouse = warehouses[selectedWarehouseIndex]
        newBox = box(getInputValue("createObjectName"), 0, 0, int(getInputValue("createObjectWidth")), int(getInputValue("createObjectHeight")), 0, 0, 0)
        ###########################^^^^ the default parameters here for x and y of the added box are 0 and 0; CHANGE IT!!
        activeWarehouse.addBox(newBox)
        setErrorText("")
    else:
        setErrorText("Error: Create a warehouse before adding a box")


def onRemoveBoxClicked():
    if len(warehouses) > 0:
        activeWarehouse = warehouses[selectedWarehouseIndex]
        activeWarehouse.removeBox(getInputValue("removeObjectName"))
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

# Setup Warehouse UI
warehouseHeader = StaticText("warehouseHeader", 900, 40, 100, 32, "Warehouse Dimensons", True)
warehouseWidthText = StaticText("warehouseWidthST", 900, 80, 100, 32, "Warehouse Width")
warehouseWidth = InputBox("warehouseWidth", 1070, 80, 140, 32)
warehouseHeightText = StaticText("warehouseHeightST", 900, 120, 100, 32, "Warehouse Height")
warehouseHeight = InputBox("warehouseHeight", 1070, 120, 140, 32)
warehouseButton = Button("warehouseCreateButton", 900, 160, 160, 32, onWarehouseDimensionButtonClicked, "Create Warehouse")

# Setup Object Creation UI
createObjectHeader = StaticText("createObjectHeader", 900, 240, 100, 32, "Create Object", True)
createObjectNameText = StaticText("createObjectNameST", 900, 280, 100, 32, "Item Name")
createObjectName = InputBox("createObjectName", 1070, 280, 140, 32)
createObjectWidthText = StaticText("createObjectWidthST", 900, 320, 100, 32, "Item Width")
createObjectWidth = InputBox("createObjectWidth", 1070, 320, 140, 32)
createObjectHeightText = StaticText("wareHouseHeightST", 900, 360, 100, 32, "Item Height")
createObjectHeight = InputBox("createObjectHeight", 1070, 360, 140, 32)
createObjectButton = Button("createObjectButton", 900, 400, 160, 32, onAddBoxButtonClicked, "Create Object")

# Setup Object Removal UI
removeObjectHeader = StaticText("createObjectHeader", 900, 480, 100, 32, "Remove Object", True)
removeObjectNameText = StaticText("removeObjectNameST", 900, 520, 100, 32, "Item Name")
removeObjectName = InputBox("removeObjectName", 1070, 520, 140, 32)
removeObjectButton = Button("removeObjectButton", 900, 560, 160, 32, onRemoveBoxClicked, "Remove Object")

# Stats UI
maxAreaST = StaticText("maxAreaST", 900, 620, 100, 32, "Max Area: 0")
spaceUsedST = StaticText("spaceUsedST", 900, 650, 100, 32, "Space Used: 0")
spaceRemainingST = StaticText("spaceRemainingST", 900, 680, 100, 32, "Space Remaining: 0")

# Error Text UI
errorText = DynamicText("errorText", 350, 680, 100, 32, "")

inputs = [warehouseHeight, warehouseWidth, warehouseButton, warehouseHeader, warehouseWidthText, warehouseHeightText, createObjectHeader,
createObjectWidthText, createObjectWidth, createObjectHeightText, createObjectHeight, createObjectButton, createObjectNameText,
createObjectName, removeObjectHeader, removeObjectNameText, removeObjectName, removeObjectButton, maxAreaST, spaceUsedST, spaceRemainingST,
errorText]

selectedWarehouseIndex = 0
warehouses = []
# needsRedraw = True #Later: Use this to optimize redraw loop if we need


def main():
    clock = pg.time.Clock()
    done = False

    # TEST --------------------------------------------------
    store = warehouse(5, 7, 720, 720)
    store.printWarehouse()
    box1 = box("1", 0, 0, 3, 3, 0, 0, 0)
    store.addBox(box1)
    store.printWarehouse()
    box2 = box("2", 0, 0, 4, 4, 0, 0, 0)
    store.addBox(box2)
    store.printWarehouse()
    box3 = box("3", 0, 0, 2, 2, 0, 0, 0)
    store.addBox(box3)
    store.printWarehouse()
    box4 = box("4", 0, 0, 1, 2, 0, 0, 0)
    store.addBox(box4)
    store.printWarehouse()
    box5 = box("5", 0, 0, 4, 1, 0, 0, 0)
    store.addBox(box5)
    store.printWarehouse()

    # TEST ----------------------------------------------------
    while not done:
        screen.fill((255, 255, 255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for boxx in inputs:
                if hasattr(boxx, 'handle_event'):
                    boxx.handle_event(event)

        for boxx in inputs:
            boxx.update()

        for boxx in inputs:
            boxx.draw(screen)
            
        if len(warehouses) > 0:
            pg.draw.rect(screen, pg.Color(140,140,140), pg.Rect(0, 0, 720, 720), 0)  # draw the warehouse
            activeWarehouse = warehouses[selectedWarehouseIndex]  # RETURN THIS TO 720, 720 ^^^^^^^^ IF NO SIZE LIMIT
            normalizedBoxes = activeWarehouse.getNormalizedBoxes()
            for boxx in normalizedBoxes:
                renderedBox = RenderedBox(box)
                renderedBox.draw(screen)

        pg.display.flip()
        clock.tick(50) #20fps


if __name__ == '__main__':
    main()
    pg.quit()