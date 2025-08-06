from enum import Enum


class PROPERTY_TYPES(Enum):
        apartment = 'Студия'
        loft = 'Лофт'
        bungalow = 'Бунгало'
        room = 'Комната'
        house = 'Дом'
        commercial = 'Комерческая'


        @classmethod
        def choices(cls):
            return[(attr.name, attr.value) for attr in cls]