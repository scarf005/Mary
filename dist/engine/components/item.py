class Item:
    def __init__(self, quantity=1, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.quantity = quantity
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs