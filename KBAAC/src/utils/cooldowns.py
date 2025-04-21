from datetime import datetime, timedelta
import time

class CooldownManager:
    def __init__(self):
        self.cooldowns = {}

    def set_cooldown(self, user_id, duration):
        # Встановлення кулдауну. Бо не можна працювати кожну секунду. 🕒
        self.cooldowns[user_id] = datetime.now() + timedelta(seconds=duration)

    def is_on_cooldown(self, user_id):
        # Перевірка кулдауну. Бо правила є правила. 📜
        if user_id in self.cooldowns:
            if datetime.now() < self.cooldowns[user_id]:
                return True
            else:
                del self.cooldowns[user_id]
        return False

    def get_remaining_cooldown(self, user_id):
        if user_id in self.cooldowns:
            remaining = self.cooldowns[user_id] - datetime.now()
            return max(0, remaining.total_seconds())
        return 0

# Create a global instance of CooldownManager
cooldown_manager = CooldownManager()