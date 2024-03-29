import discord 
from discord.ext import commands
#from prince2.classes import Colors, Emojis
from discord.ui import Modal
#from cogs.events import commandhelp
import aiosqlite
import json
from discord.ui import *
from prince1.Tools import *
class vcModal(Modal, title="rename your voice channel"):
       name = discord.ui.TextInput(
        label="voice channel name",
        placeholder="give your channel a better name",
        required=True,
        style=discord.TextStyle.short
       )

       async def on_submit(self, interaction: discord.Interaction):
        name = self.name.value
        try: 
           await interaction.user.voice.channel.edit(name=name)   
           e = discord.Embed(color=Colors.green, description=f"{Emojis.check} {interaction.user.mention}: voice channel renamed to **{name}**")
           await interaction.response.send_message(embed=e, ephemeral=True)
        except Exception as er:
            em = discord.Embed(color=Colors.red, description=f"{Emojis.wrong} {interaction.user.mention}: an error occured {er}")
            await interaction.response.send_message(embed=em, ephemeral=True)  

class vmbuttons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="", emoji="<:lockk:1113355187378212874>", style=discord.ButtonStyle.gray, custom_id="persistent_view:lock")    
    async def lock(self, interaction: discord.Interaction, button: discord.ui.Button):
         async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
              await interaction.user.voice.channel.set_permissions(interaction.guild.default_role, connect=False)
              emb = discord.Embed(color=0x2f3126, description=f" {interaction.user.mention}: locked <#{interaction.user.voice.channel.id}>")
              await interaction.response.send_message(embed=emb, view=None, ephemeral=True)      

    @discord.ui.button(label="", emoji="<:a_unlock:1113361337851052083>", style=discord.ButtonStyle.gray, custom_id="persistent_view:unlock")
    async def unlock(self, interaction: discord.Interaction, button: discord.ui.Button):   
        async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3135, description=f" {interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3135, description=f" {interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
              await interaction.user.voice.channel.set_permissions(interaction.guild.default_role, connect=True)
              emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: unlocked <#{interaction.user.voice.channel.id}>")
              await interaction.response.send_message(embed=emb, view=None, ephemeral=True)

    @discord.ui.button(label="", emoji="<:SR_UNHIDE:1113357968449224834>", style=discord.ButtonStyle.gray, custom_id="persistent_view:reveal")
    async def reveal(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
              await interaction.user.voice.channel.set_permissions(interaction.guild.default_role, view_channel=True)
              emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: revealed <#{interaction.user.voice.channel.id}>")
              await interaction.response.send_message(embed=emb, view=None, ephemeral=True)
      
    @discord.ui.button(label="", emoji="<:unhide:1113358008337055764> ", style=discord.ButtonStyle.gray, custom_id="persistent_view:hide")
    async def hide(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
              await interaction.user.voice.channel.set_permissions(interaction.guild.default_role, view_channel=False)
              emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: hidden <#{interaction.user.voice.channel.id}>")
              await interaction.response.send_message(embed=emb, view=None, ephemeral=True)   

    @discord.ui.button(label="", emoji="<:rename:1113358579152474132>", style=discord.ButtonStyle.gray, custom_id="persistent_view:rename")
    async def rename(self, interaction: discord.Interaction, button: discord.ui.Button): 
       async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
                rename = vcModal()
                await interaction.response.send_modal(rename)
    
    @discord.ui.button(label="", emoji="<:increasevc:1113358776116985886>", style=discord.ButtonStyle.gray, custom_id="persistent_view:increase")
    async def increase(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
              limit = interaction.user.voice.channel.user_limit
              if limit == 99:
                emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: I can't increase the limit for <#{interaction.user.voice.channel.id}>")
                await interaction.response.send_message(embed=emb, view=None, ephemeral=True)
                return
              
              res = limit + 1
              await interaction.user.voice.channel.edit(user_limit=res)
              emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention} increased <#{interaction.user.voice.channel.id}> limit to **{res}** members")
              await interaction.response.send_message(embed=emb, view=None, ephemeral=True)

    @discord.ui.button(label="", emoji="<:decrease:1113358718776655893>", style=discord.ButtonStyle.gray, custom_id="persistent_view:decrease")
    async def decrease(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None:
              limit = interaction.user.voice.channel.user_limit
              if limit == 0:
                emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention} i can't decrease the limit for <#{interaction.user.voice.channel.id}>")
                await interaction.response.send_message(embed=emb, view=None, ephemeral=True)
                return
              
              res = limit - 1
              await interaction.user.voice.channel.edit(user_limit=res)
              emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: decreased <#{interaction.user.voice.channel.id}> limit to **{res}** members")
              await interaction.response.send_message(embed=emb, view=None, ephemeral=True)          
    
    @discord.ui.button(label="", emoji="<:crownop:1113359355803357236>", style=discord.ButtonStyle.gray, custom_id="persistent_view:claim")
    async def claim(self, interaction: discord.Interaction, button: discord.ui.Button):
         async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {}".format(interaction.user.voice.channel.id))
             che = await cursor.fetchone()
             if che is not None:
                memberid = che[0]   
                member = interaction.guild.get_member(memberid)
                if member in interaction.user.voice.channel.members:
                    embed = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: the owner is still in the voice channel")
                    await interaction.response.send_message(embed=embed, ephemeral=True, view=None)
                else:
                    await cursor.execute(f"UPDATE vcs SET user_id = {interaction.user.id} WHERE voice = {interaction.user.voice.channel.id}")
                    await interaction.client.db.commit()
                    embed = discord.Embed(color=0x2f3135, description=f"{interaction.user.mention}: you own {interaction.user.voice.channel.mention}")
                    await interaction.response.send_message(embed=embed, view=None, ephemeral=True)        
    
    @discord.ui.button(label="", emoji="<:Info:1113359917470973982>", style=discord.ButtonStyle.gray, custom_id="persistent_view:info")
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f" {interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {}".format(interaction.user.voice.channel.id))
             che = await cursor.fetchone()
             if che is not None:
                memberid = che[0]   
                member = interaction.guild.get_member(memberid)
                embed = discord.Embed(color=0x2f3135, title=interaction.user.voice.channel.name, description=f"owner: **{member}** (`{member.id}`)\ncreated: <t:{int(interaction.user.voice.channel.created_at.timestamp())}:R>\nbitrate: **{interaction.user.voice.channel.bitrate/1000}kbps**\nconnected: **{len(interaction.user.voice.channel.members)}**")    
                embed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                embed.set_thumbnail(url=member.display_avatar)
                await interaction.response.send_message(embed=embed, view=None, ephemeral=True)  
    
    @discord.ui.button(label="", emoji="<:delete:1113366280905424936>", style=discord.ButtonStyle.gray, custom_id="persistent_view:delete")
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
     async with interaction.client.db.cursor() as cursor: 
          await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(interaction.guild.id)) 
          check = await cursor.fetchone()
          if check is not None:     
             channeid = check[1]
             voicechannel = interaction.guild.get_channel(channeid)
             category = voicechannel.category 
             if interaction.user.voice is None:
                e = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in your voice channel")
                await interaction.response.send_message(embed=e, view=None, ephemeral=True)
                return
             elif interaction.user.voice is not None:
                if interaction.user.voice.channel.category != category:
                    emb = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: You are not in a voice channel created by the bot")
                    await interaction.response.send_message(embed=emb, view=None, ephemeral=True) 
                    return

             await cursor.execute("SELECT * FROM vcs WHERE voice = {} AND user_id = {}".format(interaction.user.voice.channel.id, interaction.user.id))
             che = await cursor.fetchone()
             if che is None:
                embe = discord.Embed(color=0x2f3135, description=f"{interaction.user.mention}: you don't own this voice channel")
                await interaction.response.send_message(embed=embe, view=None, ephemeral=True)
                return
             elif che is not None: 
              await cursor.execute("DELETE FROM vcs WHERE voice = {}".format(interaction.user.voice.channel.id))
              await interaction.client.db.commit()               
              await interaction.user.voice.channel.delete() 
              embed = discord.Embed(color=0x2f3136, description=f"{interaction.user.mention}: deleted the channel")
              await interaction.response.send_message(embed=embed, view=None, ephemeral=True)        
                
class VoiceMaster(commands.Cog): 
   def __init__(self, bot: commands.AutoShardedBot): 
        self.bot = bot 
   
   @commands.Cog.listener()
   async def on_connect(self):
       setattr(self.bot, "db", await aiosqlite.connect("main.db"))
       async with self.bot.db.cursor() as cursor: 
           await cursor.execute("CREATE TABLE IF NOT EXISTS voicemaster (guild_id INTEGER, vc INTEGER, interface INTEGER)")
           await cursor.execute("CREATE TABLE IF NOT EXISTS vcs (user_id INTEGER, voice INTEGER)") 
           await self.bot.db.commit()        

   @commands.Cog.listener() 
   async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
     async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(member.guild.id))
      check = await cursor.fetchone()
      if check is not None:
       chan = check[1]
       if (after.channel is not None and before.channel is None) or (after.channel is not None and before.channel is not None):
        if after.channel.id == int(chan) and before.channel is None:     
          channel = await member.guild.create_voice_channel(f"{member.name}'s channel", category=after.channel.category)
          await member.move_to(channel)
          await cursor.execute("INSERT INTO vcs VALUES (?,?)", (member.id, after.channel.id))
          await self.bot.db.commit()
        elif before.channel is not None and after.channel is not None:
         await cursor.execute("SELECT * FROM vcs WHERE voice = {}".format(before.channel.id))
         chek = await cursor.fetchone()
         if (chek is not None) and (before.channel is not None and after.channel.id == int(chan)):
          if before.channel.category == after.channel.category: 
           if before.channel.id == after.channel.id: return  
           await before.channel.delete()
           await cursor.execute("DELETE FROM vcs WHERE voice = {}".format(before.channel.id))
           await self.bot.db.commit() 
           await member.move_to(channel=None)
          else: 
            chane = await member.guild.create_voice_channel(f"{member.name}'s channel", category=after.channel.category)
            await member.move_to(chane)
            await cursor.execute("INSERT INTO vcs VALUES (?,?)", (member.id, chane.id))
            await self.bot.db.commit()   
         elif (chek is not None) and (before.channel is not None and after.channel.id != int(chan)):
            if before.channel.category == after.channel.category: 
             if before.channel.id == after.channel.id: return    
             await before.channel.delete()
             await cursor.execute("DELETE FROM vcs WHERE voice = {}".format(before.channel.id))
             await self.bot.db.commit() 
            elif after.channel.category != before.channel.category: 
                 if before.channel.id == int(chan): return
                 channel = before.channel  
                 members = channel.members
                 if len(members) == 0:
                  await cursor.execute("DELETE FROM vcs WHERE voice = {}".format(before.channel.id))
                  await self.bot.db.commit()
                  await channel.delete() 
                  
       elif before.channel is not None and after.channel is None: 
         async with self.bot.db.cursor() as curs: 
            await curs.execute("SELECT * FROM vcs WHERE voice = {}".format(before.channel.id))
            cheki = await curs.fetchone() 
            if cheki is not None:  
               channel = before.channel  
               members = channel.members
               if len(members) == 0:
                await curs.execute("DELETE FROM vcs WHERE voice = {}".format(before.channel.id))
                await self.bot.db.commit()
                await channel.delete()   
           
   @commands.command(aliases=["j2c"], help="setup join to create module for your server", description="config", usage="[subcommand]", brief="j2c setup - j2c setup\nj2c reset - reset j2c setup")
   @commands.cooldown(1, 5, commands.BucketType.guild)
   @ignore_check()
   @commands.has_permissions(administrator=True)

   #@blacklist()
   async def join2create(self, ctx: commands.Context, option=None):
    with open ("premium.json","r") as f:

        member = json.load(f)
    
        prm = member["guild"]
    if str(ctx.guild.id) not in prm:
        embed = discord.Embed(title="You are not a premium user! Please buy premium to use this command!",color=0x2f3136)
        embed.set_thumbnail(url=self.bot.user.avatar)
        embed.set_author(name=ctx.author,icon_url=ctx.author.display_avatar)

            

            

        embed.set_footer(text="Made By Prince",icon_url=self.bot.user.avatar)

        B = Button(label='Get Premium',emoji="<a:Diamonds:1087431201117179944>" ,style=discord.ButtonStyle.link,url='https://discord.gg/soward')

        view = View()

        view.add_item(B)

        return await ctx.send(embed=embed,view=view)
    
   
 
    if option == None:
        await ctx.send_help( ctx.command) 
        return  
    elif option == "setup":
     async with self.bot.db.cursor() as cursor: 
      await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(ctx.guild.id))
      check = await cursor.fetchone() 
      if check is not None:
            em = discord.Embed(color=0x2f3136, description=f" {ctx.author.mention}: voice master is already set")
            await ctx.reply(embed=em, mention_author=False)
            return
      elif check is None:                   
        category = await ctx.guild.create_category("Soward Prime j2c")
        overwrite = {ctx.guild.default_role: discord.PermissionOverwrite(view_channel=True, send_messages=False)}  
        em = discord.Embed(color=0x2f3136, title="Soward Prime", description="click the buttons below to control the voice channel")
        em.set_footer(text="Made By Prince",icon_url=self.bot.user.avatar.url)

        em.set_thumbnail(url=self.bot.user.avatar.url)
        em.add_field(name="Button Usage", value="<:lockk:1113355187378212874> - [`lock`](https://discord.gg/soward) the voice channel\n<:a_unlock:1113361337851052083> - [`unlock`](https://discord.gg/soward) the voice channel\n<:SR_UNHIDE:1113357968449224834> - [`unhide`](https://discord.gg/soward) the voice channel\n<:unhide:1113358008337055764> - [`hide`](https://discord.gg/soward) the voice channel\n<:rename:1113358579152474132> - [`rename`](https://discord.gg/soward) the voice channel\n<:increasevc:1113358776116985886> - [`increase`](https://discord.gg/soward) the user limit\n<:decrease:1113358718776655893> - [`decrease`](https://discord.gg/soward) the user limit\n<:crownop:1113359355803357236> - [`claim`](https://discord.gg/soward) the voice channel\n<:Info:1113359917470973982> - [`info`](https://discord.gg/soward) of the voice channel\n<:delete:1113366280905424936> - [`delete`](https://discord.gg/soward) a voice channel")    
        text = await ctx.guild.create_text_channel("soward-interface", category=category, overwrites=overwrite)
        vc = await ctx.guild.create_voice_channel("Join to create", category=category)
        await text.send(embed=em, view=vmbuttons())
        await cursor.execute("INSERT INTO voicemaster VALUES (?,?,?)", (ctx.guild.id, vc.id, text.id))
        await self.bot.db.commit()
        e = discord.Embed(color=0x2f3136, description=f" {ctx.author.mention}: configured the join to create interface")
        await ctx.reply(embed=e, mention_author=False)               
    elif option == "reset":
      async with self.bot.db.cursor() as cursor: 
         await cursor.execute("SELECT * FROM voicemaster WHERE guild_id = {}".format(ctx.guild.id))
         check = await cursor.fetchone() 
         if check is None:
            em = discord.Embed(color=0x2f3136, description=f"{ctx.author.mention}: join to create module isn't set")
            await ctx.reply(embed=em, mention_author=False)
            return
         elif check is not None:
            try:
             channelid = check[1]
             interfaceid = check[2]
             channel2 = ctx.guild.get_channel(interfaceid)
             channel = ctx.guild.get_channel(channelid)
             category = channel.category
             channels = category.channels
             for chan in channels:
                try:
                    await chan.delete()
                except:
                   continue

             await category.delete()    
             await channel2.delete()      
             await cursor.execute("DELETE FROM voicemaster WHERE guild_id = {}".format(ctx.guild.id))
             await self.bot.db.commit()
             embed = discord.Embed(color=0x2f3136, description=f" {ctx.author.mention}: join to create module has been disabled")
             await ctx.reply(embed=embed, mention_author=False) 
             return
            except:
             
             await cursor.execute("DELETE FROM voicemaster WHERE guild_id = {}".format(ctx.guild.id))
             await self.bot.db.commit()
             embed = discord.Embed(color=0x2f3136, description=f" {ctx.author.mention}: join to create module has been disabled")
             await ctx.reply(embed=embed, mention_author=False)  
  #  else:
    #    await commandhelp(self, ctx, ctx.command.name) 
    #    return         
        
async def setup(bot):
    await bot.add_cog(VoiceMaster(bot))        