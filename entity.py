class Entity:
    """
    플레이어, 적, 아이템 등등 모든 것을 표현할 때 쓰는 객체.
    """
    def __init__(self, x, y, char, color, name, **kwargs):
        # 엔티티 속성: x,y좌표, 외관(문자), 색깔
        self.x = x
        self.y = y
        self.char = char
        self.name = name
        self.color = color

        # 컴포넌트 추가
        component_list = {'_Luminary':None, 'blocks':False}        
        for key,value in component_list.items() :
            print("kwargs")
            print (kwargs)
            if key in kwargs.keys():
                print (F"kwargs:{kwargs[key]}")
                setattr(self, key, kwargs[key])
            else:
                print (F"key{key},value:{value}")
                setattr(self, key, value)
                
        print(self.__dict__)
        #((k, v) for k, v in if k in component_list.keys())
        
        if self._Luminary:
            self._Luminary.owner = self


    def move(self, dx, dy):
        #  엔티티를 지정한 양 만큼 이동시킴
        self.x += dx
        self.y += dy

# 클래스 밖 함수   
def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity
    return None