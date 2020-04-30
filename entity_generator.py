import yaml
import numpy as np
import random

"""
종류

지능:
감각: 시각, 청각, 후각
기형 여부:

"""
"""
Vision = {0:'blind', 1:'poor', 2:'normal', 3:'sharp', 4:'extreme'}
Hearing = {0:'deaf', 1:'poor', 2:'normal', 3:'sharp', 4:'extreme'}
Smelling = {0:'Noseless', 1:'normal', 2:'sharp'}

Intelligence = {0:'dimwit', 1:'poor', 2:'normal', 3:'bright', 4:'genious'}
Traits = {0:'fang', 1:'venom teeth',2:'razor sharp fang', 3:'breath flame', 4:'breath death'}

def get_trait(point, points, lists):
    num = random.randint(0, )
    point -= points
    return lists.get(point)

def generate_entity(points, theme=None,):
    entity_point = points
    num = random.randint(0,4)
    point -= num
    trait = Traits.get(num)
    print (trait)


    point -= 10
    print(point)
    point += 10
    print(point)
    pass

if __name__ == '__main__':
    generate_entity(10)

"""