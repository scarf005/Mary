"""
나도 이게 뭐가 뭔지 모르겠다. 열흘은 더 조사해야함. 아무튼 지금은 미완성이고 쓰지 말 것
"""


import tcod
from yaml_data.yaml_loader import open_yaml
from renderer.render_functions import RenderOrder

# 엔티티
from entity import Entity

from components.ai import BasicMonster
from components.fighter import Fighter

# 미리 생성된 몬스터들
monster_list = open_yaml('pgen_monsters.yaml')

def load_and_create_monster(monster_name, x=None,y=None):
    Minfo = monster_list.get(monster_name)

    def loadk(key):
        return Minfo.get(key)

    # 기본 정보 불러오기
    name = loadk('name')
    char = loadk('char')

    # 색상: 문자열 또는 리스트
    mon_color = loadk('color')
    if type(mon_color) == str:
        color = getattr(tcod, mon_color)
    else: #리스트 형식일때
        color = tcod.Color(i for i in mon_color)

    # 싸움꾼 부품
    mon_fighter = loadk("F_comp")
    attributes = ['hp','sanity','defense','power',]
    def create_fighter(*args):
        for i in args:
            print(i)

    create_fighter(mon_fighter)
    #fighter = tuple((key,value) for key,value in mon_fighter)
    #print(fighter)
    #fighter = (i for i in mon_fighter)
    #print(fighter)

    # 인공지능 부품
    ai = loadk('AI_comp')
    if not ai: ai = BasicMonster()

    #return Entity(x,y, name, char, color, blocks=True, render_order=RenderOrder.ACTOR, _Fighter=fighter, _Ai=ai )

if __name__ == "__main__":
    #print(monster_list.get('crawling_intestine'))
    load_and_create_monster('crawling_intestine')

"""
f_comp = Fighter(hp=10, defense=0, power=3)
monster = self.create_monster(mx,my, '~', tcod.flame, 'crawling intestine',
                                            f_comp, ai_comp)

def create_monster(self, x, y, char, color, name, fighter, ai):
        return Entity(x,y, char, color, name, blocks=True,
                      render_order=RenderOrder.ACTOR, _Fighter=fighter, _Ai=ai)
"""