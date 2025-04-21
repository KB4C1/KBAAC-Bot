import disnake
from disnake.ext import commands
import random
import json
import logging
from src.utils.data_handler import load_economy_data, save_economy_data
from src.commands.permissions import PermissionChecks

# Завантаження конфігурації
with open("data/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Команда для встановлення шансів казино
@commands.slash_command(name="set_casino_odds", description="Встановити шанси для ігор казино")
@PermissionChecks.has_admin_role()
async def set_casino_odds(inter: disnake.ApplicationCommandInteraction, game: str, odds: float):
    if odds < 0 or odds > 1:
        await inter.response.send_message("Шанси мають бути між 0 і 1. Не хитруйте! 😏", ephemeral=True)
        return

    # Збереження шансів у конфіг
    config['casino_odds'][game] = odds
    with open("data/config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

    await inter.response.send_message(f"Шанси для {game} встановлено на {odds}. 🎰", ephemeral=True)
    logging.info(f"Шанси для {game} встановлено на {odds} користувачем {inter.author}.")

# Команда для гри в рулетку
@commands.slash_command(name="roulette", description="Грати в рулетку")
async def roulette(inter: disnake.ApplicationCommandInteraction, bet: int):
    data = load_economy_data()
    user_id = str(inter.author.id)

    wallet = data.get(user_id, {}).get("wallet", 0)
    if bet <= 0 or bet > wallet:
        await inter.response.send_message("Недостатньо коштів для ставки! 💸", ephemeral=True)
        return

    # Логіка рулетки
    result = random.randint(0, 36)
    odds = config['casino_odds'].get('roulette', 0.5)  # Шанси за замовчуванням
    win = random.random() < odds  # Визначення виграшу

    if win:
        winnings = bet * 2
        data[user_id]["wallet"] += winnings
        message = f"Ви виграли! Результат: {result}. Ви отримали {winnings} монет! 🎉"
    else:
        data[user_id]["wallet"] -= bet
        message = f"Ви програли. Результат: {result}. Ви втратили {bet} монет. 😢"

    save_economy_data(data)
    await inter.response.send_message(message)