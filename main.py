import discord, os, asyncio, datetime, pytz,gspread
from discord.ext import commands
from keep_alive import keep_alive
from random import choice, randint
from replit import db
from oauth2client.service_account import ServiceAccountCredentials as sac

print("Loading...")
client = commands.Bot(command_prefix="$")
client.remove_command("help")

admin=[351239431102922752,  591107669180284928] 

def update(author_id, attr, val):
	context = db[author_id]
	context[attr] = val
	db[author_id] = context


@client.event
async def on_ready():
  scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
  ]
  creds = sac.from_json_keyfile_name('Gacha Discord Key.json', scope)
  google_client = gspread.authorize(creds)
  # Open Spreadsheets Here
  sheet = google_client.open("Loot Tables").sheet1
	print("Online")


async def change_p():
	await client.wait_until_ready()
	statuses = [
	    f"{len(client.guilds)} Servers", "$help",
	    f"Latency: {round(client.latency*1000)}ms",
	    choice(client.guilds).name
	]
	while not client.is_closed():
		await client.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.watching, name=choice(statuses)))
		await asyncio.sleep(2)


@client.command()
async def help(ctx):
	embed = discord.Embed(
	    title="Help",
	    description=
	    f"Command Prefix: `$`\n**Version `{open('version').readlines()[0]}`**",
	    color=discord.Colour.teal())
	embed.set_footer(text="Made by 402 Class of 2021")
	embed.add_field(
	    name="Commands Available",
	    value=
	    "`$guessgame` - Play a Number Guessing Game\n`$stats|$create` - Shows Stats or Create Account\n`$dice <bet>` - Play dice against the bot\n`$leaderboard|$lb` - See Leaderboard\n`$blackjack|$bj` - play a game of blackjack. type hit/stand to play")
	embed.add_field(
	    name="--------------",
	    value=
	    "Intrested in Being a Developer?\nJoin Our [Discord Server](https://discord.gg/SkKVSq9z95) and contact one of our **Pink Fluffy Dinosaur Pilots**",
	    inline=False)
	await ctx.send(embed=embed)


@client.command()
async def clear_db(ctx):
	if ctx.author.id in admin:
		for i in db:
			del db[i]
		await ctx.send("**Database __Wipe Out__ Completed!!!**")
	else:
		await ctx.send('You do not have the relevant permssion')

@client.command(aliases=["lb"])
async def leaderboard(ctx):
  embed = discord.Embed(
    title = "Leaderboard",
    description = f"Players May Not Include members of this guild ({ctx.guild.name})",
    color=discord.Color.teal())
  pla_n,val_n=[],[]
  for i in db:
    pla_n.append(db[i]["name"])
    val_n.append(db[i]["tokens"])
  rep=0
  for i in range(len(val_n)):
    rep+=1
    index = val_n.index(max(val_n))
    embed.add_field(name=f"**{rep} - {pla_n[index]}**",value=f"__{val_n[index]}__",inline=False)
    val_n.pop(index)
    pla_n.pop(index)
  embed.set_footer(text=f"Powered by Replit DB")
  embed.set_author(name="402 Gacha")
  await ctx.send(embed=embed)

@client.command()
async def list_db(ctx):
  for i in ctx.author.roles:
    if i.name=="Bot Tester":
      flg=True
      break
  if flg!=True:
    await ctx.send("You dont have the role **Bot Tester**.")
  for i in db:
    await ctx.send(db[i])
  await ctx.send("**Done**")

@client.command(aliases=["stats", "create"])
async def statistics(ctx):
	author_id = str(ctx.author.id)
	while True:
		await ctx.send("*Finding Player Data...*", delete_after=2)
		try:
			tokens = db[author_id]["tokens"]
			prompt = await ctx.send("Player Data Found!!!")
			break
		except KeyError:
			prompt = await ctx.send(
			    f"**Player Data for the name ({ctx.author.name})Not Found**!!!\n__*Attempting* To Create New Dataset__"
			)

			joined_in = pytz.timezone("Asia/Singapore").localize(
			    datetime.datetime.now() +
			    datetime.timedelta(hours=8)).strftime("%c")
			db[author_id] = {"name":ctx.author.name,"joined_in": str(joined_in), "tokens": 50}
		await prompt.delete()
	display = discord.Embed(
	    title=f"Statistics for @{ctx.author.name}",
	    description=
	    f"__**402 Gacha Bot** *Statistics*__\nPlayer ID: **{ctx.author.id}**\n",
	    color=discord.Colour.green())
	display.add_field(name="*Joined In*",
	                  value=db[author_id]["joined_in"],
	                  inline=False)
	display.add_field(name="**TraceTogether Tokens**", value=tokens)
	await ctx.send(embed=display)


@client.command(aliases=["ggame"])
async def guessgame(ctx):
	display = discord.Embed(title="Guessing Game",
	                        description="*Guess* a __Number__ from *1 - 100*",
	                        color=discord.Colour.green())
	number = randint(1, 100)
	tries = 0
	author_id = str(ctx.author.id)
	try:
		tokens = db[author_id]["tokens"]
	except:
		await ctx.send("Create an Account First By Doing `$create`")
		return

	def check(m):
		if m.author == ctx.author:
			if m.content.isdigit():
				return True

	prompt = await ctx.send("Guess a **Number** from __1 - 100__.")
	while tries < 10:
		guess = await client.wait_for('message', check=check)
		await prompt.delete()
		await guess.delete()
		guess = int(guess.content)
		tries += 1
		if guess < number:
			prompt = await ctx.send(f"@{ctx.author.name}\nThe number is larger"
			                        )
		elif guess > number:
			prompt = await ctx.send(
			    f"@{ctx.author.name}\nThe number is smaller")
		else:
			prompt = await ctx.send(
			    f"@{ctx.author.name}\nYou have guessed the correct number")
			break
	if tries <= 9:
		if tries == 1:
			incre = 50
		elif tries == 2:
			incre = 40
		elif tries == 3:
			incre = 20
		elif tries == 4:
			incre = 10
		else:
			incre = 5
		update(author_id, "tokens", db[author_id]["tokens"] + 5)
	else:
		incre = 0
		await ctx.send(
		    f"**Too Bad @{ctx.author.name}!** You don't get  any points.")
	embed = discord.Embed(
	    title=
	    f"You took __**{tries} tries**__ and recieved __{incre} tokens__!!!",
	    description=f"**The Number** is `{number}`",
	    color=discord.Color.green())
	embed.set_author(name= ctx.author.name)
	await ctx.send(embed=embed)


@client.command()
async def dice(ctx, bet):
	author_id = str(ctx.author.id)
	try:
		tokens = db[author_id]["tokens"]
	except:
		await ctx.send("Create an Account First By Doing `$create`") 
	if int(bet) > tokens:
	    await ctx.send("You can't bet more than you have. ")
	    return
	bot_dice = randint(1, 6)
	player_dice = randint(1, 6)
	await ctx.send(
	    f"**402 Gacha Bot** rolled {bot_dice}.\n**{ctx.author.name}** rolled {player_dice}.")
	if player_dice > bot_dice:
		await ctx.send(f'Congrats {ctx.message.author.mention}, you won {bet} tokens!')
		update(author_id, "tokens", db[author_id]["tokens"] + int(bet))
	elif player_dice < bot_dice:
		await ctx.send(f'Lmao {ctx.message.author.mention}, you lost {bet} tokens.')
		update(author_id, "tokens", db[author_id]["tokens"] - int(bet))
	else:
		await ctx.send('Both of you rolled the same number. Bet returned.') 

@client.command()
async def addtokens(ctx, user, amt):
    if ctx.author.id in admin:
        user = user.replace("<","")
        user = user.replace(">","")
        user = user.replace("@","")
        user = user.replace("!","")
        update(user,'tokens',db[user]['tokens'] + int(amt))
        await ctx.send(f'{amt} tokens added. ')
    else:
        await ctx.send("Lmao you can't do this you peasent")
    
@client.command()
async def removetokens(ctx, user, amt):
    user = user.replace("<","")
    user = user.replace(">","")
    user = user.replace("@","")
    user = user.replace("!","")
    if ctx.author.id in admin:  
        update(user,'tokens',db[user]['tokens'] - int(amt))
        await ctx.send(f'{amt} tokens removed. ')
    else:
        await ctx.send("Lmao you can't do this you peasent")

@client.command(aliases=['bj'])
async def blackjack(ctx, bet):
    author_id=str(ctx.author.id)
    placeholder=0
    player_cards=[] 
    bot_cards=[] 
    bot_view=[]
    win=0
    win21=False
    draw=False  
    def check(m):
        if m.author == ctx.author:
            return True
        return False
    try:
        tokens = db[author_id]['tokens']
    except:
        await ctx.send("Create an Account First By Doing `$create`") 
    if int(bet) > tokens or int(bet) <0:
	    await ctx.send("Bruh what you doing???")
	    return
    for i in range(4):
        placeholder=randint(1,13) 
        if i < 2:
            if placeholder==11 or placeholder==12 or placeholder==13:
                player_cards.append(10)
            else:
                player_cards.append(placeholder)
        else:
            if placeholder==11 or placeholder==12 or placeholder==13:
                bot_cards.append(10)
            else:
                bot_cards.append(placeholder)
    bot_view.append(bot_cards[0])
    bot_view += ['???']
    await ctx.send(f'**{ctx.author.name} --- {player_cards} --- {sum(player_cards)}\ndealer --- {bot_view} --- ???**')
    if sum(player_cards)==21:
        win=1
    elif sum(bot_cards)==21:
        win=-1
    while True:
        if win>0:
            await ctx.send(f'**{ctx.author.name} --- {player_cards} --- {sum(player_cards)}\ndealer --- {bot_cards} --- {sum(bot_cards)}**')
            if win21==True:
                await ctx.send(f'Congrats {ctx.message.author.mention}, you won {str(int(bet) *2) } tokens! ')
                update(author_id, "tokens", db[author_id]["tokens"] + (int(bet)*2))
            else:
                await ctx.send(f'Congrats {ctx.message.author.mention}, you won {bet} tokens! ')
                update(author_id, "tokens", db[author_id]["tokens"]+int(bet))
            break
        elif win<0:
            await ctx.send(f'**{ctx.author.name} --- {player_cards} --- {sum(player_cards)}\ndealer --- {bot_cards} --- {sum(bot_cards)}**')
            if draw==True:
                await ctx.send('Draw')    
            else:
                await ctx.send(f'Rip {ctx.message.author.mention} you lost {bet} tokens. ')
                update(author_id, "tokens", db[author_id]["tokens"] - int(bet))
            break
        else:
            msg=await client.wait_for('message',check=check)
            cmd=(msg.content)
            if cmd=='hit':
                placeholder=randint(1, 13)
                if placeholder==11 or placeholder==12 or placeholder==13:
                    player_cards.append(10)
                else:
                    player_cards.append(placeholder)
                if sum(bot_cards)<18:
                    placeholder=randint(0, 13)
                    if placeholder==11 or placeholder==12 or placeholder==13:
                        bot_cards.append(10)
                    else:
                        bot_cards.append(placeholder)
            elif cmd=='stand':
                if sum(bot_cards)<18:
                    placeholder=randint(1, 13)
                    if placeholder==11 or placeholder==12 or placeholder==13:
                        bot_cards.append(10)
                    else:
                        bot_cards.append(placeholder)
                if sum(bot_cards)>21:
                    await ctx.send('Dealer bust')
                    win+=1
                    continue
                elif sum(player_cards)>sum(bot_cards):
                    win+=1
                    continue
                elif sum(player_cards)<sum(bot_cards):
                    win-=1
                    continue
                else:
                    win-=1
                    draw=True
                    continue
            if sum(bot_cards)>21:
                await ctx.send('Dealer bust')
                win+=1
                continue
            elif sum(player_cards)>21:
                await ctx.send('Player bust')
                win-=1
                continue
            elif sum(player_cards)==21:
                win+=1
                win21=True
                continue
            elif sum(bot_cards)==21:
                win-=1
                continue
            await ctx.send(f'**{ctx.author.name} --- {player_cards} --- {sum(player_cards)}\ndealer --- {bot_view} --- ???**')

@client.command()
async def grandentrance(ctx):
    if ctx.author.id in admin:
        await ctx.send(f"**All hail the great, mighty and powerful, {ctx.author.name}! **")
    else:
        await ctx.send("**You do not deserve a grand entrance you peasent.**" )


client.loop.create_task(change_p())
keep_alive()
client.run(os.getenv("token"))