from discord.ui import View, Button, Select, Modal, TextInput
from discord import Interaction, ButtonStyle, TextStyle, SelectOption
from config import SHOP_ITEMS, CAR_RENTAL  # Добавляем импорт

class ShopView(View):
    def __init__(self):
        super().__init__(timeout=None)
        for item_name in SHOP_ITEMS:
            self.add_item(Button(
                style=ButtonStyle.secondary,
                label=item_name,
                custom_id=f"shop_{item_name}"
            ))

class AutoparkView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Select(
            placeholder="Выберите транспорт",
            options=[
                SelectOption(
                    label=car.capitalize(),
                    description=f"{data['price']} очков/час"
                ) for car, data in CAR_RENTAL.items()
            ],
            custom_id="autopark_select"
        ))