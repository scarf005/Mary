from random import randint

def roll_dice(dice):
    """
    튜플 (굴리는 주사위 수, 주사위 면 수, 추가 숫자(선택적))
    """
    if len(dice) == 3:
        number_of_dice, dice_sides, addendum = dice
    else:
        number_of_dice, dice_sides = dice
        addendum = 0

    result = 0
    for i in range(number_of_dice):
        result += randint(1,dice_sides)
    result += addendum
    return result

if __name__ == '__main__':
    a = (1,2,3)
    print(roll_dice((2,2,2)))