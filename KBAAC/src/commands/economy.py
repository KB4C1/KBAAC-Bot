import os
import json
import random
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from utils.data_handler import load_economy_data, save_economy_data
from utils.cooldowns import Cooldown

# Кулдаун для команди work
work_cooldown = Cooldown(300)  # 5 хвилин

@commands.slash_command(name="work", description="Заробити гроші")
@work_cooldown.check()
async def work(inter: ApplicationCommandInteraction):
    data = load_economy_data()
    user_id = str(inter.author.id)

    # Визначення діапазону заробітку
    min_earning = 50  # Мінімальний заробіток
    max_earning = 150  # Максимальний заробіток

    # Генерація випадкової суми
    earning = random.randint(min_earning, max_earning)

    # Оновлення даних користувача
    data[user_id] = data.get(user_id, {"wallet": 0, "bank": 0})
    data[user_id]["wallet"] += earning
    save_economy_data(data)

    await inter.response.send_message(f"Ви заробили {earning} монет! 🎉")

@commands.slash_command(name="set_money_range", description="Встановити діапазон заробітку для команди work")
async def set_money_range(inter: ApplicationCommandInteraction, min_amount: int, max_amount: int):
    if min_amount < 0 or max_amount <= min_amount:
        await inter.response.send_message("Неправильний діапазон заробітку!", ephemeral=True)
        return

    # Збереження нового діапазону
    config_path = os.path.join("data", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["MoneyRange"]["min"] = min_amount
    config["MoneyRange"]["max"] = max_amount

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    await inter.response.send_message(f"Діапазон заробітку встановлено: {min_amount} - {max_amount} монет.")

@commands.slash_command(name="set_casino_odds", description="Встановити шанси для казино")
@PermissionChecks.is_guild_owner()
async def set_casino_odds(inter: ApplicationCommandInteraction, odds: float):
    if odds < 0 or odds > 1:
        await inter.response.send_message("Неправильні шанси! Вони повинні бути між 0 і 1.", ephemeral=True)
        return

    # Save the new casino odds to the config
    config_path = os.path.join("data", "config.json")
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    config["casino_odds"] = odds

    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    await inter.response.send_message(f"Шанси для казино встановлено на {odds * 100}%.")

# Additional functions for credit system can be added here as needed.