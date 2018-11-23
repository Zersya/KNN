class ModelData: 

    def __init__(self, Index, X1, X2, X3, X4, X5, Y):
        self.Index = Index
        self.X1 = X1
        self.X2 = X2
        self.X3 = X3
        self.X4 = X4
        self.X5 = X5
        self.Y  = Y

    def setDistance(self, dist):
        self.distance = dist

    def setY(self, Y):
        self.Y = Y