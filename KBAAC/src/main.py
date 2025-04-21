import os
import json
import logging
import random
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from utils.data_handler import load_economy_data, save_economy_data
from utils.cooldowns import CooldownManager

# Налаштування логування
LOG_FILE = "data/logs/bot.log"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

# Завантаження конфігурації
CONFIG_PATH = os.path.join("data", "config.json")
ECONOMY_PATH = os.path.join("data", "economy.json")

if not os.path.exists(CONFIG_PATH):
    logging.error("Файл конфігурації не знайдено! Хто видалив config.json? Зізнавайтесь!")
    raise FileNotFoundError("Файл конфігурації config.json не знайдено!")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

# Глобальні змінні
admin_roles: dict[int, int] = {}
work_cooldowns = CooldownManager()

# Завантаження економічних даних
if not os.path.exists(ECONOMY_PATH):
    with open(ECONOMY_PATH, "w", encoding="utf-8") as f:
        json.dump({}, f)
        logging.info("Файл economy.json створено. Сподіваюсь, тепер ніхто його не видалить...")

# Ініціалізація бота
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=config["Prefix"], intents=intents)

# Подія: бот готовий
@bot.event
async def on_ready():
    logging.info(f"Бот {bot.user} готовий до роботи! 🎉")
    logging.info(f"ID бота: {bot.user.id}")
    logging.info(f"Префікс: {config['Prefix']}")
    print("⚡ Бот запущено! Час підкорювати Discord-сервери!")

# Команди
@bot.slash_command(name="work", description="Заробити гроші (або ні)")
async def work(inter: ApplicationCommandInteraction):
    user_id = str(inter.author.id)
    
    if work_cooldowns.is_on_cooldown(user_id):
        await inter.response.send_message(
            "Ви вже працювали! Відпочиньте трохи, а то ще вигорите. 🛌", 
            ephemeral=True
        )
        return

    earnings = random.randint(config["MoneyRange"]["min"], config["MoneyRange"]["max"])
    data = load_economy_data()
    data[user_id] = data.get(user_id, {"wallet": 0, "bank": 0})
    data[user_id]["wallet"] += earnings
    save_economy_data(data)

    work_cooldowns.set_cooldown(user_id)
    await inter.response.send_message(
        f"Ви заробили {earnings} монет! 💰 Не забудьте витратити їх на щось корисне... або ні."
    )

# Запуск бота
if __name__ == "__main__":
    try:
        bot.run(config["Token"])
    except Exception as e:
        logging.critical(f"Не вдалося запустити бота: {e}")
        print("💥 Щось пішло не так... Можливо, токен неправильний? Перевірте config.json.")