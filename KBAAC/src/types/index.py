from typing import Dict, Any, List

class UserEconomyData:
    def __init__(self, wallet: int = 0, bank: int = 0, work_cooldown: int = 0, credit: float = 0.0, interest_rate: float = 0.0):
        self.wallet = wallet
        self.bank = bank
        self.work_cooldown = work_cooldown
        self.credit = credit
        self.interest_rate = interest_rate

class EconomyConfig:
    def __init__(self, min_work_amount: int, max_work_amount: int, casino_odds: Dict[str, float]):
        self.min_work_amount = min_work_amount
        self.max_work_amount = max_work_amount
        self.casino_odds = casino_odds

class CreditData:
    def __init__(self, principal: float, interest_rate: float, days: int):
        self.principal = principal
        self.interest_rate = interest_rate
        self.days = days

class EconomyData:
    def __init__(self):
        self.users: Dict[str, UserEconomyData] = {}
        self.config: EconomyConfig = EconomyConfig(0, 0, {})

    def add_user(self, user_id: str, user_data: UserEconomyData):
        self.users[user_id] = user_data

    def set_config(self, config: EconomyConfig):
        self.config = config

class CasinoOdds:
    def __init__(self, game: str, odds: float):
        self.game = game
        self.odds = odds

class InterestRate:
    def __init__(self, rate: float):
        self.rate = rate