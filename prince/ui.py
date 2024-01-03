

import asyncio
import discord
from typing import Optional, Union, List
from discord.ext import commands
from discord import SelectOption


class SelectWithMultipleOptions(discord.ui.Select):
    def __init__(self, placeholder: str, options: List[str]):
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=len(options),
            options=[SelectOption(label=option.replace("_", " ").title(), value=option) for option in options],
        )


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = None):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(f"This is {self.ctx.author.mention}'s command, not yours.", ephemeral=True)
            return False
        return True


class Confirm(discord.ui.View):
    def __init__(self, context: commands.Context, timeout: Optional[int] = 300, user: Optional[Union[discord.Member, discord.User]] = None):
        super().__init__(timeout=timeout)
        self.value = None
        self.context = context
        self.user = user or self.context.author

    @discord.ui.button(label='Yes', style=discord.ButtonStyle.green)
    async def yes(self, b, i):
        self.value = True
        self.stop()

    @discord.ui.button(label='No', style=discord.ButtonStyle.red)
    async def no(self, b, i):
        self.value = False
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            await interaction.response.send_message("You cannot interact in other's commands.", ephemeral=True)
            return False
        return True


class Paginator(discord.ui.View):
    def __init__(self, ctx: commands.Context, embeds: List[discord.Embed]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.embeds = embeds
        self.current = 0

    async def edit(self, msg, pos):
        em = self.embeds[pos]
        em.set_footer(text=f"Page: {pos+1}/{len(self.embeds)}")
        await msg.edit(embed=em)

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def bac(self, b, i):
        if self.current == 0:
            return
        await self.edit(i.message, self.current - 1)
        self.current -= 1

    @discord.ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
    async def stap(self, b, i):
        await i.message.delete()

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def nex(self, b, i):
        if self.current + 1 == len(self.embeds):
            return
        await self.edit(i.message, self.current + 1)
        self.current += 1

    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command ._.", ephemeral=True)


class PaginatorText(discord.ui.View):
    def __init__(self, ctx: commands.Context, stuff: List[str]):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.stuff = stuff
        self.current = 0

    async def edit(self, msg, pos):
        await msg.edit(content=self.stuff[pos])

    @discord.ui.button(emoji='◀️', style=discord.ButtonStyle.blurple)
    async def bac(self, b, i):
        if self.current == 0:
            return
        await self.edit(i.message, self.current - 1)
        self.current -= 1

    @discord.ui.button(emoji='⏹️', style=discord.ButtonStyle.blurple)
    async def stap(self, b, i):
        await i.message.delete()

    @discord.ui.button(emoji='▶️', style=discord.ButtonStyle.blurple)
    async def nex(self, b, i):
        if self.current + 1 == len(self.stuff):
            return
        await self.edit(i.message, self.current + 1)
        self.current += 1

    async def interaction_check(self, interaction):
        if interaction.user == self.ctx.author:
            return True
        await interaction.response.send_message("Not your command ._.", ephemeral=True)


class CloseOrClaimTicket(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Claim', style=discord.ButtonStyle.blurple)
    async def claim(self, b: discord.ui.Button, i: discord.Interaction):
        b.disabled = True
        await i.message.edit(view=self)
        await i.channel.send(f'This ticket has been claimed by: {i.user.mention}')

    @discord.ui.button(label='Close', style=discord.ButtonStyle.red)
    async def close(self, b: discord.ui.Button, i: discord.Interaction):
        b.disabled = True
        await i.message.edit(view=self)
        await i.channel.send('Closing ticket...')
        await asyncio.sleep(2)
        await i.channel.edit(archived=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def open_ticket(self, i):
        pass

    @discord.ui.button(label="Click to open ticket.", emoji='🎟️', custom_id='epicbot-tickets')
    async def ticket(self, button: discord.Button, interaction: discord.Interaction):
        for t in interaction.guild.threads:
            if t.name == f'ticket-{interaction.user.id}' and not t.archived:
                return await interaction.response.send_message(f'You already have a ticket {t.mention}', ephemeral=True)
        channel = interaction.channel
        thread = await channel.create_thread(name=f'ticket-{interaction.user.id}')
        await thread.send(
            f"📂 {interaction.user.mention} has created a ticket.",
            allowed_mentions=discord.AllowedMentions(
                everyone=False,
                roles=False,
                users=True,
                replied_user=False
            ),
            view=CloseOrClaimTicket()
        )

class SelfRoleOptionSelecter(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = 300):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None


    @discord.ui.button(label="Reactions", style=discord.ButtonStyle.blurple)
    async def rctns(self, b: discord.Button, i: discord.Interaction):
        self.value = "reaction"
        self.stop()

    @discord.ui.button(label="Buttons", style=discord.ButtonStyle.danger)
    async def btns(self, b: discord.Button, i: discord.Interaction):
        self.value = "button"
        self.stop()

    @discord.ui.button(label="Dropdowns", style=discord.ButtonStyle.success)
    async def ddn(self, b: discord.Button, i: discord.Interaction):
        self.value = "dropdown"
        self.stop()  

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            return False
        return True

    






class SelfRoleEditor(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout: Optional[int] = 300):
        super().__init__(timeout=timeout)
        self.ctx = ctx
        self.value = None

    @discord.ui.button(label="Add", style=discord.ButtonStyle.blurple)
    async def go_ahead(self, b: discord.Button, i: discord.Interaction):
        self.value = "add"
        self.stop()

    @discord.ui.button(label="Remove", style=discord.ButtonStyle.red)
    async def cancel(self, b: discord.Button, i: discord.Interaction):
        self.value = "remove"
        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.ctx.author:
            return False
        return True


class SelfRoleButton(discord.ui.Button):
    def __init__(self, guild: discord.Guild, emoji: str, role_id: int):
        super().__init__(emoji=emoji, style=discord.ButtonStyle.blurple, custom_id=str(role_id))
        self.guild = guild
        self.emoji = emoji
        self.role = guild.get_role(int(role_id))

    async def callback(self, interaction: discord.Interaction):
        if self.role is None:
            return
        if self.role in interaction.user.roles:
            await interaction.user.remove_roles(self.role, reason="Soward Selfroles")
            await interaction.response.send_message(f"Removed the {self.role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(self.role, reason="Soward Selfroles")
            await interaction.response.send_message(f"Gave you the {self.role.mention} role.", ephemeral=True)


class ButtonSelfRoleView(discord.ui.View):
    def __init__(self, guild: discord.Guild, stuff: dict):
        super().__init__(timeout=None)
        for role_id, emoji in stuff.items():
            button = SelfRoleButton(guild, emoji, int(role_id))
            self.add_item(button)


class DropDownSelfRoleSelect(discord.ui.Select):
    def __init__(self, guild: discord.Guild, stuff: dict):
        options = []
        for role_id, emoji in stuff.items():
            role = guild.get_role(int(role_id))
            if role is not None:
                options.append(discord.SelectOption(label=role.name, emoji=emoji, value=str(role_id)))
        if len(options) == 1:
            options.append(discord.SelectOption(label="Remove role", emoji='❌', value='remove'))
        super().__init__(placeholder="Please select a role.", options=options, custom_id='selfrole-dropdown')
        self.guild = guild
        self.stuff = stuff

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == 'remove':
            role = self.guild.get_role(int(self.options[0].value))
            await interaction.user.remove_roles(role, reason="Soward Selfroles")
            await interaction.response.send_message(f"Removed the {role.mention} role.", ephemeral=True)
            return
        role = self.guild.get_role(int(self.values[0]))
        if role is None:
            return
        if role in interaction.user.roles:
            await interaction.user.remove_roles(role, reason="Soward Selfroles")
            await interaction.response.send_message(f"Removed the {role.mention} role.", ephemeral=True)
        else:
            await interaction.user.add_roles(role, reason="Soward Selfroles")
            await interaction.response.send_message(f"Gave you the {role.mention} role.", ephemeral=True)


class DropDownSelfRoleView(discord.ui.View):
    def __init__(self, guild: discord.Guild, stuff: dict):
        super().__init__(timeout=None)
        self.add_item(DropDownSelfRoleSelect(guild, stuff))