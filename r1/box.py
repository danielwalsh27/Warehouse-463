class box:
    def __init__(self, name, x, y, w, h, colorR=0, colorG=0, colorB=0, colorA=127):
        self.name = name
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.colorR = colorR
        self.colorG = colorG
        self.colorB = colorB
        self.colorA = colorA
        self.area = w*h
        # self.selected = False
        
    def canFit(box):
        return
        # can another box fit in this box
    
    def flip(self):
        temp = self.width
        self.width = self.height
        self.height = temp
        
    def largerDimension(self):
        return max([self.width, self.height])
        
    def smallerDimension(self):
        return min([self.width, self.height])