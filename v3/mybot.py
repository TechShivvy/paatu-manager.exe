from db import ServerStore
from discord.ext import commands


class CustomBot(commands.Bot):
    def __init__(
        self,
        *args,
        serversdb: ServerStore,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.serversdb = ServerStore()
