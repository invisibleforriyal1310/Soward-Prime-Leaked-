import discord
import os
import datetime
#from core import Soward 
from discord.ext import commands
from prince1.Tools import *
from prince.bot import Bot
from discord.ext.commands import Cog
class antibot(Cog):
    def __init__(self, client):
      self.client = client
      print("Cog Loaded: AntiBot")

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
      try:
        data = getConfig(member.guild.id)
        anti = getanti(member.guild.id)
        punishment = data["punishment"]
        wled = data["whitelisted"]
        guild = member.guild
        owner = guild.owner
        reason = "Soward | Adding Bots Not Whitelisted"
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.bot_add):
            if entry.user.id == guild.owner_id:
              return None
            elif str(entry.user.id) in wled or anti == "off":
              return None
            elif user.top_role.position >= guild.get_member(self.client.user.id).top_role.position: return
            else:
              if punishment == "ban":
               if member.bot:
                await member.ban(reason=f"{reason}")
                await guild.ban(entry.user, reason=f"{reason}")
              elif punishment == "kick":
               if member.bot:
                 await member.kick(reason=reason)
                 await guild.kick(entry.user, reason=reason)
              elif punishment == "none":
               if member.bot:
                 mem = guild.get_member(entry.user.id)
                 await mem.edit(roles=[role for role in mem.roles if not role.permissions.administrator], reason=reason)
              else:
                return

      except Exception as error:
        if isinstance(error, discord.Forbidden):
              return
async def setup(client):
    await client.add_cog(antibot(client))