import tcod
from game_messages import Message

class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message(F'You pick up {item.name}.', tcod.light_green)
            })

            item_names = []
            for i in self.items:
                item_names.append(i.name)

            if item.name in item_names:
                for j, name_in_list in enumerate(item_names):
                    if item.name == name_in_list:

                        self.items[j]._Item.quantity += 1
            else:
                self.items.append(item)

        return results

    def use(self, item_entity, **kwargs):
        results = []

        item_component = item_entity._Item

        if item_component.use_function is None:
            results.append({'message': Message(F'The {item_entity.name} cannot be used', tcod.light_crimson)})
        else:
            # 타게팅 중
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            # 타게팅 하지 않는 아이템
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}
                item_use_results = item_component.use_function(self.owner, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        if not item_component.quantity == 1: item_component.quantity -= 1
                        else: self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message(F'You drop {item.name}',
                                                                 tcod.yellow)})

        return results