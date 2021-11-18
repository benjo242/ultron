import discord
from discord.ext import commands
import random
import json
import os
from requests import get
import aiohttp
import praw

os.chdir("C:\\Users\\kicon\\Desktop\\coding\\DiscordBot")

client = commands.Bot(command_prefix = '.')
client.sniped_messages = {}
client.remove_command('help')

@client.event
async def on_ready():
	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Holiday season movies. merry X-mas ❄️"))
	print('ultron has been uploaded')

@client.event
async def on_message_delete(message):
    print(f'sniped message {message}')
    client.sniped_messages[message.guild.id] = (
        message.content, message.author, message.channel.name, message.created_at)

@client.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)

@client.command()
async def help(ctx):
	embed=discord.Embed(title="Ultron's help menu", description="Help", color=0x861dbf)
	embed.set_author(name="Ultron")
	embed.add_field(name="8ball,ultron", value="Fun", inline=False)
	embed.add_field(name="avatar", value="check someones avatar", inline=True)
	embed.add_field(name="Who,who,Whois,whois", value="check someone", inline=True)
	embed.add_field(name="bal", value="economy", inline=False)
	embed.add_field(name="beg", value="economy", inline=True)
	embed.add_field(name="deposit", value="economy", inline=True)
	embed.add_field(name="pay", value="economy", inline=True)
	embed.add_field(name="withdraw", value="economy", inline=True)
	embed.add_field(name="rob", value="steal", inline=False)
	embed.add_field(name="ban", value="moderation The ban hammer", inline=True)
	embed.add_field(name="kick", value="moderation", inline=True)
	embed.add_field(name="unban", value="moderation", inline=True)
	embed.add_field(name="ping ", value="check ping", inline=True)
	embed.add_field(name="poll", value="create a poll :white_check_mark:  :x:", inline=True)
	embed.add_field(name="pollv2", value="number poll", inline=True)
	embed.add_field(name="meme", value="big chungus", inline=True)
	embed.add_field(name="clear", value="purge messages", inline=True)
	embed.add_field(name="rps", value="rock paper scissors choose", inline=True)
	embed.add_field(name="slots", value="betting addiction", inline=True)
	embed.add_field(name="snipe", value="someone says something sus? use snipe", inline=True)
	embed.add_field(name="help", value="this command", inline=True)
	await ctx.send(embed=embed)

@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]

    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents,
                          color=discord.Color.purple(), timestamp=time)
    embed.set_author(
        name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)

@client.command(pass_context=True)
async def chnick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')

@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@client.command(aliases=["whois", "Whois", "Who", "who"])
async def userinfo(ctx, member: discord.Member = None):
    if not member:  # if member is no mentioned
        member = ctx.message.author  # set member as the author
    roles = [role for role in member.roles]
    embed = discord.Embed(colour=discord.Colour.purple(), timestamp=ctx.message.created_at,
                          title=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested by {ctx.author}")

    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Display Name:", value=member.display_name)

    embed.add_field(name="Created Account On:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined Server On:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"))

    embed.add_field(name="Roles:", value="".join([role.mention for role in roles]))
    embed.add_field(name="Highest Role:", value=member.top_role.mention)
    print(member.top_role.mention)
    await ctx.send(embed=embed)


@client.command()
async def rps(ctx, choice):
    choices=["rock", "paper", "scissors"]
    if choice not in choices:
        await ctx.send("error: please put rock, paper or scissors")
    else:
        await ctx.send(random.choice(choices))

@client.command()
#the content will contain the question, which must be answerable with yes or no in order to make sense
async def poll(ctx, *, content:str):
  print("Creating yes/no poll...")
  #create the embed file
  embed=discord.Embed(title=f"{content}", description="React to this message with ✅ for yes, ❌ for no.",  color=0xd10a07)
  #set the author and icon
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  print("Embed created")
  #send the embed
  message = await ctx.channel.send(embed=embed)
  #add the reactions
  await message.add_reaction("✅")
  await message.add_reaction("❌")


@client.command()
#the content will contain the question, which must be answerable with yes or no in order to make sense
async def pollv2(ctx, *, content:str):
  print("Creating yes/no poll...")
  #create the embed file
  embed=discord.Embed(title=f"{content}", description="React to this message with :one: for one, :two: for two.",  color=0xd10a07)
  #set the author and icon
  embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
  print("Embed created")
  #send the embed
  message = await ctx.channel.send(embed=embed)
  #add the reactions
  await message.add_reaction("1️⃣")
  await message.add_reaction("2️⃣")

players = {}

@client.command()
async def bal(ctx):
	await open_account(ctx.author)
	user = ctx.author
	users = await get_bank_data()

	wallet_amt = users[str(user.id)]["wallet"]
	bank_amt = users[str(user.id)]["bank"]

	em = discord.Embed(title = f"{ctx.author.name}'s balance",color = discord.Color.red())
	em.add_field(name = "Wallet balance",value = wallet_amt)
	em.add_field(name = "Bank balance",value = bank_amt)
	await ctx.send(embed = em)


@client.command()
async def beg(ctx):
	await open_account(ctx.author)

	users = await get_bank_data()

	user = ctx.author

	earnings = random.randrange(20)

	await ctx.send(f"Someone gave you {earnings} spectral coins!!")




	users[str(user.id)]["wallet"] += earnings

	with open("mainbank.json","w") as f:
		json.dump(users,f)

@client.command()
async def withdraw(ctx,amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("Please enter the amount of spectral coins you wish to withdraw")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[1]:
		await ctx.send("You don't have that much spectral coins!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author,amount)
	await update_bank(ctx.author,-1*amount,"bank")

	await ctx.send(f"You withdrew {amount} the spectral coins!")

@client.command()
async def deposit(ctx,amount = None):
	await open_account(ctx.author)

	if amount == None:
		await ctx.send("Please enter the amount of spectral coins you wish to deposit")
		return

	bal = await update_bank(ctx.author)

	amount = int(amount)
	if amount>bal[0]:
		await ctx.send("You don't have that much spectral coins!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author,-1*amount)
	await update_bank(ctx.author,amount,"bank")

	await ctx.send(f"You deposited {amount} the spectral coins!")

@client.command()
async def pay(ctx,member:discord.Member,amount = None):
	await open_account(ctx.author)
	await open_account(member)

	if amount == None:
		await ctx.send("Please enter the amount of spectral coins you wish to deposit")
		return

	bal = await update_bank(ctx.author)
	if amount == "all":
		amount = bal[1]


	amount = int(amount)
	if amount>bal[1]:
		await ctx.send("You don't have that much spectral coins!")
		return
	if amount<0:
		await ctx.send("Amount must be positive!")
		return

	await update_bank(ctx.author,-1*amount,"bank")
	await update_bank(member,amount,"bank")

	await ctx.send(f"You gave {amount} the spectral coins!")

@client.command(pass_context=True)
async def slots(ctx, amount=None):

    if amount == None:
        await ctx.send("Please enter an amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)
    if amount > bal[0]:
        await ctx.send("You don't have that much money!")
        return
    if amount < 0:
        await ctx.send("Amount must be positive")
        return

    slots = ['bus', 'train', 'horse', 'tiger', 'monkey', 'cow']
    slot1 = slots[random.randint(0, 5)]
    slot2 = slots[random.randint(0, 5)]
    slot3 = slots[random.randint(0, 5)]

    slotOutput = '| :{}: | :{}: | :{}: |\n'.format(slot1, slot2, slot3)

    ok = discord.Embed(title = "Slots Machine", color = discord.Color(0xFFEC))
    ok.add_field(name = "{}\nWon".format(slotOutput), value = f'You won {2*amount} coins')


    won = discord.Embed(title = "Slots Machine", color = discord.Color(0xFFEC))
    won.add_field(name = "{}\nWon".format(slotOutput), value = f'You won {3*amount} coins')


    lost = discord.Embed(title = "Slots Machine", color = discord.Color(0xFFEC))
    lost.add_field(name = "{}\nLost".format(slotOutput), value = f'You lost {1*amount} coins')


    if slot1 == slot2 == slot3:
        await update_bank(ctx.author, 3 * amount)
        await ctx.send(embed = won)
        return

    if slot1 == slot2:
        await update_bank(ctx.author, 2 * amount)
        await ctx.send(embed = ok)
        return

    else:
        await update_bank(ctx.author, -1 * amount)
        await ctx.send(embed = lost)
        return

@client.command()
async def rob(ctx,member:discord.Member):
	await open_account(ctx.author)
	await open_account(member)

	bal = await update_bank(member)

	if bal[0]<5:
		await ctx.send("Sorry but that member is too poor to rob")
		return

	earnings = random.randrange(0, bal[0])

	await update_bank(ctx.author,earnings)
	await update_bank(member,-1*earnings)

	await ctx.send(f"You robbed and got {earnings} the spectral coins!")

async def open_account(user):

	users = await get_bank_data()

	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["wallet"] = 0
		users[str(user.id)]["bank"] = 0

	with open("mainbank.json","w") as f:
		json.dump(users,f)
	return True


async def get_bank_data():
		with open("mainbank.json","r") as f:
			users = json.load(f)

		return users


async def update_bank(user,change = 0,mode = "wallet"):
	users = await get_bank_data()

	users[str(user.id)][mode] += change

	with open("mainbank.json","w") as f:
		json.dump(users,f)

	bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
	return bal


@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {round(client.latency * 1000)}ms')\

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'kicked {member.name}#{member.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'banned {member.name}#{member.mention}')

@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if(user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.name}#{user.mention}')
			return


@client.command(aliases=['8ball', 'ultron'])
async def _8ball(ctx, *, question):
	responses = ['It is certain.',
				 'It is decidedly so.',
				 'Without a doubt.',
 				 'Yes definitely.',
 				 'You may rely on it.',
				 'As I see it, yes.',
				 'Most likely.',
 				 'Outlook good.',
 				 'Yes.',
 				 'Signs point to yes.',
 				 'Reply hazy, try again.',
 				 'Ask again later.',
 				 'Better not tell you now.',
 				 'Cannot predict now.',
 			 	 'Concentrate and ask again.',
 				 "Don't count on it.",
 				 'My reply is no.',
 			 	 'My sources say no.',
 				 'Outlook not so good.',
				 'Very doubtful.']
	await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

client.run('OTAyOTg0NzUzNzc3NjA2NzM4.YXmYFQ.HK1_EYWDPRl7i5dky8-rudz8j9w')
