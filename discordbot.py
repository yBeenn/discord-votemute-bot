import discord
from discord.ext import commands
import time
import os

client = commands.Bot(command_prefix = "!")

votes = {}
id = 0



@client.event
async def on_ready():
    print("Online")

@client.event
async def on_reaction_add(reaction, user):
    global id
    global votes
    channel = reaction.message.channel
    if reaction.message.id == id:
        if reaction.emoji == "✅":

            votes[id] = votes[id] +1


        elif reaction.emoji == "❌":


            votes[id] = votes[id] -1







@client.event
async def on_raw_reaction_remove(payload):
    global id
    global votes

    if payload.message_id == id:

        if payload.emoji.name == "✅":
            votes[id] = votes[id] -1


        elif payload.emoji.name == "❌":

            votes[id] = votes[id] +1





@client.command()
async def ping(ctx):
    await ctx.send(f"My ping is " + str(round(client.latency*1000, 0)))





@client.command(description="Mutes the specified user.")
#commands.has_permissions(manage_messages=True)
async def votemute(ctx, member: discord.Member, *, reason=None):
    global id
    global votes

    if id == 0:
        guild = ctx.guild

        mutedRole = discord.utils.get(guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)


        msg=await ctx.send("> Votemute: Der Benutzer" + member.mention+ " wird gevotemuted. Reagiere mit ✅ um den votemute zuzustimmen. Mit ❌ dagegen. \n Verbleibende Zeit: 30 ")

        ctx.message.delete

        id=msg.id
        votes[id] = 0
        reaction1 = "✅"
        reaction2 = "❌"

        await msg.add_reaction(emoji=reaction1)
        await msg.add_reaction(emoji=reaction2)
        await ctx.message.delete()


        for i in range(31):

            time.sleep(1)
            
            if i != 30:
                await msg.edit(content="> Votemute: Der Benutzer" + member.mention+ " wird gevotemuted. Reagiere mit ✅ um den votemute zuzustimmen. Mit ❌ dagegen. \n Verbleibende Zeit: "+str(29-i))

            else:
                await msg.delete()





        if votes[id] == 0:
            await ctx.send("> Es gab gleich viele ✅ wie ❌. \n > Der Benutzer "+ member.mention + " wird **NICHT** gemutet")
            id = 0
        elif votes[id] > 0:
            await ctx.send("> Es gab mehr ✅ als ❌. \n > Der Benutzer "+ member.mention + " wird **gemutet**")

            await member.send("> Du bist für 3 min gemuted")
            id = 0
            await mutet(member, guild)


        elif votes[id] < 0:
            await ctx.send("> Es gab weniger ✅ wie ❌. \n > Der Benutzer "+ member.mention + " wird **NICHT** gemutet")
            id = 0
            #await memüber.add_roles(mutedRole, reason=reason)
            #await ctx.send(f"Der Benutzer {member.mention} wurde für 3min gemuted")
    else:
        await ctx.message.delete()
        await ctx.author.send("> Es ist nur ein Votemute gleichzeitig möglich")



@client.command(description="Unmutes a specified user.")
#@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"{member.mention} ist unmuted")



async def mutet (member, guild):
    mutedRole = discord.utils.get(guild.roles, name="Muted")
    await member.add_roles(mutedRole, reason=None)
    channel = await guild.create_voice_channel(name="Kick")
    try:
        await member.move_to(channel)
    except:
        print("Error")
    await channel.delete()
    time.sleep(180)
    await member.remove_roles(mutedRole, reason=None)




client.run("ODEyMjY2MjMxNDQ0OTMwNTcx.YC-P4A.c61GUhZPxdHQfTECpE6qUhY50PU")
