
class Point() :
    def __init__(self,px : int = 0,py :int =0):
        self._px = px
        self._py = py

    @property
    def px(self) -> int:
        return self._px

    @px.setter
    def px(self, px: int) -> None:
        self._px = px

    @property
    def py(self) -> int:
        return self._py

    @py.setter
    def py(self, py: int) -> None:
        self._py = py

    def __str__(self) -> str:
        return f"({self.px},{self.py})"

class Dessin() :
    def __init__(self,contient : list[Point] = None):
        if contient == None :
            self._contient = []
        else :
            self._contient = contient

    def __str__(self):
        return f"Scene : {[str(p) for p in self._contient]}"

    def ajout(self,p : Point) -> None:
        self._contient.append(p)

    @classmethod
    def test1(cls) -> 'Dessin':
        p1 = Point(0,0)
        p2 = Point(20,10)
        p3 = Point(50,50)
        res = Dessin()
        res.ajout(p1)
        res.ajout(p2)
        res.ajout(p3)

def testScene() :
    sc1 = Dessin()
    sc1.ajout(Point(3,4))
    print(sc1)
    print(Point(6,7))
    sc2 = Dessin()
    sc2.ajout(Point(7,8))
    print(sc1)
    print(sc2)
    sc3 = Dessin([])
    print(sc3)

if __name__ == '__main__':
    testScene()

