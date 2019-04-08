class Nigiri:
    def __init__(self, nigiri_topping):
        self.type = 'Nigiri'
        self.subtype = nigiri_topping
        self.value = self.card_value(nigiri_topping)

    def card_value(self, nigiri_topping):
        __value_dict = {'Egg': 1, 'Salmon': 2, 'Squid': 3}
        return __value_dict[nigiri_topping]

    def valid_topping(self, nigiri_topping):
        if nigiri_topping in ('Egg', 'Salmon', 'Squid'):
            pass
        else:
            raise ValueError


class Roll:
    def __init__(self, type, maki_count):
        self.type = type
        self.maki_count = maki_count
        self.validate_roll(type)

    def validate_roll(self, maki_type):
        if maki_type in ('Maki', 'Temaki', 'Uramaki'):
            pass
        else:
            raise ValueError


class Appetiser:
    def __init__(self, type):
        self.type = type
        self.validate_appetiser(type)

    def validate_appetiser(self, type):
        if type in ('Dumplings', 'Edamame', 'Eel', 'Miso Soup', 'Sashimi', 'Tempura', 'Tofu', 'Onigiri'):
            pass
        else:
            raise ValueError


class Onigiri(Appetiser):
    def __init__(self, shape):
        super().__init__('Onigiri')
        self.shape = shape

    def valid_shape(self, shape):
        if shape in ('Circle', 'Triangle', 'Square', 'Rectangle'):
            pass
        else:
            raise ValueError

class Specials:
    pass
