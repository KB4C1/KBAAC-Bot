# Клас для перевірки прав доступу. Бо без цього всі будуть "адмінами" 😅
class PermissionChecks:
    @staticmethod
    def is_guild_owner():
        # Перевіряємо, чи автор команди — власник сервера. Бо хто, як не він? 👑
        def predicate(ctx_or_inter):
            return ctx_or_inter.author.id == ctx_or_inter.guild.owner_id
        return commands.check(predicate)

    @staticmethod
    def has_admin_role():
        # Перевіряємо, чи є у користувача роль адміна. Бо без ролі — ніяк! 🛡️
        async def predicate(ctx_or_inter):
            guild_id = ctx_or_inter.guild.id
            user_roles = ctx_or_inter.author.roles

            role_id = admin_roles.get(guild_id)
            if role_id is None:
                return False  # Якщо роль не налаштована, то й доступу немає 🤷‍♂️
            return any(r.id == role_id for r in user_roles)
        return commands.check(predicate)

    @staticmethod
    def can_set_money_ranges():
        # Перевіряємо, чи може користувач змінювати діапазон заробітку. Бо гроші — це серйозно! 💸
        async def predicate(ctx_or_inter):
            return await PermissionChecks.has_admin_role()(ctx_or_inter) or ctx_or_inter.author.id in config.get("money_admins", [])
        return commands.check(predicate)

    @staticmethod
    def can_set_casino_odds():
        # Перевіряємо, чи може користувач змінювати шанси в казино. Бо інакше всі будуть вигравати! 🎰
        async def predicate(ctx_or_inter):
            return await PermissionChecks.has_admin_role()(ctx_or_inter) or ctx_or_inter.author.id in config.get("casino_admins", [])
        return commands.check(predicate)