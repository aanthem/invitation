from flask import Flask

app = Flask(__name__)

# Define your routes and bot logic here

if __name__ == "__main__":
    # Use the PORT environment variable provided by Heroku, default to 5000 if not available
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)




from dotenv import load_dotenv
load_dotenv()
import os
token = os.getenv("DISCORD_TOKEN")
import discord
from discord.ext import commands
import datetime
import pytz
intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix=',', intents=intents)




@bot.event
async def on_ready():
    print("""
  \x1b[35m
    ██████╗  ██████╗     ██╗██╗███╗   ██╗██╗   ██╗██╗████████╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
   ██╔════╝ ██╔════╝    ██╔╝██║████╗  ██║██║   ██║██║╚══██╔══╝██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
   ██║  ███╗██║  ███╗  ██╔╝ ██║██╔██╗ ██║██║   ██║██║   ██║   ███████║   ██║   ██║██║   ██║██╔██╗ ██║
   ██║   ██║██║   ██║ ██╔╝  ██║██║╚██╗██║╚██╗ ██╔╝██║   ██║   ██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
██╗╚██████╔╝╚██████╔╝██╔╝   ██║██║ ╚████║ ╚████╔╝ ██║   ██║   ██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
╚═╝ ╚═════╝  ╚═════╝ ╚═╝    ╚═╝╚═╝  ╚═══╝  ╚═══╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝                                                                                                            
  \x1b[0m""")








# ██████   ██████  ██      ███████ ███████     ███████ ███    ███ ██████  ███████ ██████  
# ██   ██ ██    ██ ██      ██      ██          ██      ████  ████ ██   ██ ██      ██   ██ 
# ██████  ██    ██ ██      █████   ███████     █████   ██ ████ ██ ██████  █████   ██   ██ 
# ██   ██ ██    ██ ██      ██           ██     ██      ██  ██  ██ ██   ██ ██      ██   ██ 
# ██   ██  ██████  ███████ ███████ ███████     ███████ ██      ██ ██████  ███████ ██████  
    



@bot.event
async def on_member_update(before, after):
    if before.roles != after.roles:
        channel_id = 1190827872261251142  # Replace this with your Channel ID that you want the Role Update embed sent to.
        channel = bot.get_channel(channel_id)
        
        server_timezone = pytz.timezone('Australia/Sydney')
        
        if channel:
            async for log in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_role_update):
                if log.target.id == after.id:
                    roles_updated_time = log.created_at.astimezone(server_timezone)
                    responsible_moderator = log.user
                    break
            else:
                roles_updated_time = datetime.datetime.now(server_timezone)
                responsible_moderator = "Unknown Moderator"

            role_colors = [role.color.value for role in after.roles]
            if role_colors:
                embed_color = discord.Colour(max(role_colors))
            else:
                embed_color = discord.Colour.blue()

            embed = discord.Embed(
                title=f"Updated Roles:",
                description=f"**✍️ {after.mention} has been updated.**",
                color=embed_color
            )

            embed.set_thumbnail(url=after.avatar.url if after.avatar else after.default_avatar.url)

            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)

            if added_roles:
                embed.add_field(name="✅Role Gained:", value="\n".join([f" {role.name}" for role in added_roles]), inline=True)

            if removed_roles:
                embed.color = 0x851d1d
                embed.add_field(name="❌Role Removed:", value="\n".join([f" {role.name}" for role in removed_roles]), inline=True)

            embed.add_field(name="📌 Responsible Moderator:", value=responsible_moderator.mention, inline=True)

            current_time = datetime.datetime.now(server_timezone)
            difference = (current_time - roles_updated_time).total_seconds()
            if difference < 86400:  # Less than 24 hours
                footer_text = f"Today at {roles_updated_time.strftime('%I:%M %p')}"
            elif difference < 172800:  # Less than 48 hours
                footer_text = f"Yesterday at {roles_updated_time.strftime('%I:%M %p')}"
            else:
                footer_text = roles_updated_time.strftime("%d/%m/%Y at %I:%M %p")

            embed.set_footer(text=f".gg/invitation • {footer_text}")

            await channel.send(embed=embed)





#      ██  ██████  ██ ███    ██     ███████ ███    ███ ██████  ███████ ██████  
#      ██ ██    ██ ██ ████   ██     ██      ████  ████ ██   ██ ██      ██   ██ 
#      ██ ██    ██ ██ ██ ██  ██     █████   ██ ████ ██ ██████  █████   ██   ██ 
# ██   ██ ██    ██ ██ ██  ██ ██     ██      ██  ██  ██ ██   ██ ██      ██   ██ 
#  █████   ██████  ██ ██   ████     ███████ ██      ██ ██████  ███████ ██████  

@bot.event
async def on_member_join(member):
    welcome_channel_id = 1187184644181995531
    await send_welcome_embed(member, welcome_channel_id)

    try:
        role_id = 1129762410182492180  # Replace this with your Channel ID that you want the Join embed sent to.
        role = member.guild.get_role(role_id)

        if role:
            await member.add_roles(role)
            print(f"{member.display_name} has joined the server and been given the {role.name} role.")
        else:
            print(f"Role with ID {role_id} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

async def send_welcome_embed(member, welcome_channel_id):
    server_timezone = pytz.timezone('Australia/Sydney')
    joined_at_timezone = member.joined_at.astimezone(server_timezone)

    join_time = joined_at_timezone.strftime("%d/%m/%Y %I:%M %p")
    account_creation_time = member.created_at.strftime("%d/%m/%Y")
    username = member.name
    user_avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

    embed = discord.Embed(description=f"Welcome {member.mention} to /invitation!", color=0x9f72ee)
    embed.add_field(name="🛬Joined the server at:", value=join_time, inline=False)
    embed.add_field(name="⏳Account age:", value=account_creation_time, inline=False)
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    current_time = datetime.datetime.now(joined_at_timezone.tzinfo)

    difference = (current_time - joined_at_timezone).total_seconds()
    if difference < 86400:  # Less than 24 hours
        footer_text = f"Today at {joined_at_timezone.strftime('%I:%M %p')}"
    elif difference < 172800:  # Less than 48 hours
        footer_text = f"Yesterday at {joined_at_timezone.strftime('%I:%M %p')}"
    else:
        footer_text = joined_at_timezone.strftime("%d/%m/%Y at %I:%M %p")

    embed.set_footer(text=f".gg/invitation • {footer_text}")

    # Sends the embed
    channel = bot.get_channel(welcome_channel_id)
    await channel.send(embed=embed)




#  ██████   ██████   ██████  ██████  ██████  ██    ██ ███████     ███████ ███    ███ ██████  ███████ ██████  
# ██       ██    ██ ██    ██ ██   ██ ██   ██  ██  ██  ██          ██      ████  ████ ██   ██ ██      ██   ██ 
# ██   ███ ██    ██ ██    ██ ██   ██ ██████    ████   █████       █████   ██ ████ ██ ██████  █████   ██   ██ 
# ██    ██ ██    ██ ██    ██ ██   ██ ██   ██    ██    ██          ██      ██  ██  ██ ██   ██ ██      ██   ██ 
#  ██████   ██████   ██████  ██████  ██████     ██    ███████     ███████ ██      ██ ██████  ███████ ██████  

@bot.event
async def on_member_remove(member):
    if not await check_kick(member):
        farewell_channel_id = 1190092734975979631  # Replace this with your Channel ID that you want the Goodbye embed sent to.

        if await check_ban(member):
            farewell_channel_id = 1190850692626260089  # Replace this with your Channel ID that you want the Banned User embed sent to.

        await send_farewell_embed(member, farewell_channel_id)

# Kick doesn't work

@bot.event
async def on_member_kick(member):
    farewell_channel_id = 1190150284383629353  # Channel for kicked users
    await send_farewell_embed(member, farewell_channel_id)



async def check_ban(member):
    try:
        await member.guild.fetch_ban(member)
        return True
    except discord.NotFound:
        return False

async def check_kick(member):
    try:
        async for entry in member.guild.audit_logs(action=discord.AuditLogAction.kick, limit=1):
            if entry.target == member:
                reason = entry.reason if entry.reason is not None else ""
                return reason
        return None
    except discord.Forbidden:
        return None



async def get_responsible_moderator(guild, member, action):
    async for entry in guild.audit_logs(action=action, limit=1):
        if entry.target == member:
            if action == discord.AuditLogAction.ban:
                return entry.user, entry.reason
            elif action == discord.AuditLogAction.kick:
                return entry.user, None
    return None, None


async def send_farewell_embed(member, farewell_channel_id, kick_reason=None):
    server_timezone = pytz.timezone('Australia/Sydney')
    left_at_timezone = datetime.datetime.now(server_timezone)

    leave_time = left_at_timezone.strftime("%d/%m/%Y %I:%M %p")
    account_creation_time = member.created_at.strftime("%d/%m/%Y")
    username = member.name
    user_avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
    blank = ""


    if kick_reason is not None:
        action = discord.AuditLogAction.kick
        responsible_moderator, reason = await get_responsible_moderator(member.guild, member, action)
        reason = None

        embed = discord.Embed(color=0xffA500)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        if responsible_moderator:
            embed.description = f"{member.mention} has been kicked."
            embed.add_field(name="📝Reason:", value=reason, inline=True)
            embed.add_field(name="✅Responsible Moderator:", value=responsible_moderator.mention, inline=True)
            embed.add_field(name="", value=blank, inline=False)
            embed.add_field(name="👢Kicked at:", value=leave_time, inline=True)
            embed.add_field(name="⏳Account age:", value=account_creation_time, inline=True)
        else:
            embed.description = f"{member.mention} has been kicked by an unknown moderator."
            embed.add_field(name="🔨Kicked at:", value=leave_time, inline=True)
            embed.add_field(name="⏳Account age:", value=account_creation_time, inline=True)

    elif await check_ban(member):
        action = discord.AuditLogAction.ban
        responsible_moderator, reason = await get_responsible_moderator(member.guild, member, action)
        reason = None

        embed = discord.Embed(color=0xff0000)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)

        if responsible_moderator:
            embed.description = f"{member.mention} has been banned."
            embed.add_field(name="📝Reason:", value=reason, inline=True)
            embed.add_field(name="✅Responsible Moderator:", value=responsible_moderator.mention, inline=True)
            embed.add_field(name="", value=blank, inline=False)
            embed.add_field(name="🔨Banned at:", value=leave_time, inline=True)
            embed.add_field(name="⏳Account age:", value=account_creation_time, inline=True)
        else:
            embed.description = f"{member.mention} has been banned by an unknown moderator."
            embed.add_field(name="🔨Banned at:", value=leave_time, inline=True)
            embed.add_field(name="⏳Account age:", value=account_creation_time, inline=True)

    else:
        embed = discord.Embed(color=0x781010)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.description = f"Goodbye, {member.mention}!"
        embed.add_field(name="🛫Left the server at:", value=leave_time, inline=False)

    current_time = datetime.datetime.now(left_at_timezone.tzinfo)
    difference = current_time - left_at_timezone
    if difference.days == 0:
        footer_text = f"Today at {current_time.strftime('%I:%M %p')}"
    elif difference.days == 1:
        footer_text = "Yesterday"
    else:
        footer_text = current_time.strftime("%d/%m/%Y %I:%M %p")

    embed.set_footer(text=f".gg/invitation • {footer_text}")

    channel = bot.get_channel(farewell_channel_id)
    await channel.send(embed=embed)




bot.run(token)
