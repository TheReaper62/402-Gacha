import discord, os, asyncio, datetime, pytz, gspread, time,json
from discord.ext import commands
from keep_alive import keep_alive
from random import choice, randint
from replit import db
from oauth2client.service_account import ServiceAccountCredentials as sac
from authorize import sudo

admin = [351239431102922752, 591107669180284928]

def get_prefix(client,message):
	with open("prefix.json") as f:
		prefixes = json.load(f)
	return prefixes[str(message.guild.id)]

def update(author_id, attr, val):
	context = db[author_id]
	context[attr] = val
	db[author_id] = context
def is_admin(ctx):
  if ctx.author.id in admin:
    return True
  else:
    return False
    

DEBUGGING = False
print("Loading...")
client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")

@client.event
async def on_ready():
	scope = [
	    'https://spreadsheets.google.com/feeds',
	    'https://www.googleapis.com/auth/drive'
	]
	sudo("key.json")
	creds = sac.from_json_keyfile_name("key.json", scope)
	google_client = gspread.authorize(creds)
	os.remove("key.json")
	# Open Spreadsheets Here
	place = ""
	while True:
		try:
			sheet = google_client.open("Loot Tables").sheet1
			print(sheet.acell("A1").value)
			break
		except Exception as e:
			if e == place:
				continue
			else:
				place = e
				print(f"Error: {e}")
			print("Failed to Connect to Trying Again")
	print("Online")

@client.event
async def on_message(message):
	if message.author == client.user:
		return
	content = message.content
	if DEBUGGING == True:
		with open(".console-logs","a+") as f:
			time_now = pytz.timezone("Asia/Singapore").localize(datetime.datetime.now() + datetime.timedelta(hours=8)).strftime("%d/%m/%y %H:%M")
			f.write(repr([message.author.name,message.guild.name,"#"+message.channel.name,content,time_now])+"\n")
	if "@GachaCord" in content.lower() or "<@!802842704081715230>" in content.lower():
		ctxprefix = get_prefix(message,message)
		embed = discord.Embed(
				title="Help",
				description=
				f"Command Prefix: `{ctxprefix}`\n**Version `{open('version').readlines()[0]}`**",
				color=discord.Colour.teal())
		embed.set_footer(text="Made by 402 Class of 2021")
		embed.add_field(
				name="Commands Available",
				value=
				f"`{ctxprefix}help` - Shows __**This** Message__\
				\n`{ctxprefix}guessgame` - Play a Number Guessing Game\
				\n`{ctxprefix}stats|{ctxprefix}create` - Shows Stats or Create Account\
				\n`{ctxprefix}dice <bet>` - Play dice against the bot\
				\n`{ctxprefix}leaderboard|{ctxprefix}lb` - See Leaderboard\
				\n`{ctxprefix}blackjack|{ctxprefix}bj <bet>` - Play a game of blackjack. type hit/stand to play\
				\n`{ctxprefix}support` - Support The bot by sharing with us your ideas\
				\n`{ctxprefix}suggest <'itemname'> <rarity> <description>` - Directly Suggest to the developers here\
				\n`{ctxprefix}prefix <new_prefix>` - Change your server's prefix (Requires **manage_guild** permissions)"
		)
		embed.add_field(
				name="--------------",
				value=
				"Intrested in Being a Developer?\nJoin Our [Discord Server](https://discord.gg/SkKVSq9z95) and contact one of our **Pink Fluffy Dinosaur Pilots**",
				inline=False)
		await message.channel.send(content="**Hi!**",tts=True,mention_author=True,embed=embed)
	else:
		await client.process_commands(message)

@client.event
async def on_guild_join(guild):
	with open("prefix.json") as f:
		prefixes = json.load(f)
	prefixes[str(guild.id)] = "$"
	with open("prefix.json","w") as f:
		json.dump(prefixes,f,indent=4)

@client.event
async def on_guild_remove(guild):
	with open("prefix.json") as f:
		prefixes = json.load(f)
	prefixes.pop(guild.id)
	with open("prefix.json","w") as f:
		json.dump(prefixes,f,indent=4)

async def change_p():
	await client.wait_until_ready()
	statuses = [
	    f"{len(client.guilds)} Servers", "Ping Me @GachaCord for help",
	    f"Latency: {round(client.latency*1000)}ms",
	    choice(client.guilds).name
	]
	while not client.is_closed():
		await client.change_presence(activity=discord.Activity(
		    type=discord.ActivityType.watching, name=choice(statuses)))
		await asyncio.sleep(2)


@client.command()
async def help(ctx):
	ctxprefix = get_prefix(ctx,ctx.message)
	embed = discord.Embed(
	    title="Help",
	    description=
	    f"Command Prefix: `{ctxprefix}`\n**Version `{open('version').readlines()[0]}`**",
	    color=discord.Colour.teal())
	embed.set_footer(text="Made by 402 Class of 2021")
	embed.add_field(
	    name="Commands Available",
	    value=
	    f"`{ctxprefix}help` - Shows __**This** Message__\
			\n`{ctxprefix}guessgame` - Play a Number Guessing Game\
			\n`{ctxprefix}stats|{ctxprefix}create` - Shows Stats or Create Account\
			\n`{ctxprefix}dice <bet>` - Play dice against the bot\
			\n`{ctxprefix}leaderboard|{ctxprefix}lb` - See Leaderboard\
			\n`{ctxprefix}blackjack|{ctxprefix}bj <bet>` - Play a game of blackjack. type hit/stand to play\
			\n`{ctxprefix}support` - Support The bot by sharing with us your ideas\
			\n`{ctxprefix}suggest <'itemname'> <rarity> <description>` - Directly Suggest to the developers here\
			\n`{ctxprefix}prefix <new_prefix>` - Change your server's prefix (Requires **manage_guild** permissions)"
	)
	embed.add_field(
	    name="--------------",
	    value=
	    "Intrested in Being a Developer?\nJoin Our [Discord Server](https://discord.gg/SkKVSq9z95) and contact one of our **Pink Fluffy Dinosaur Pilots**",
	    inline=False)
	await ctx.send(embed=embed)

@client.command()
async def support(ctx):
	embed = discord.Embed(
		title = "Support **@GachaCord**",
		description = "We are currently developing the Game's Loot Tables that would be the main feature the bot revolves around.\n\
		By Sharing with us __YOUR__ idea's, not only will the Loot Tables be ready even quicker, but your **own idea** will be in the game\n\
		-------------",
		colour = discord.Colour.purple()
	)
	embed.add_field(name="`itemname`",value="Give the item a name (less than 20 chars)")
	embed.add_field(inline = False,name="`rarity`",value="There are 5 Rarities:`Inferior`|`Unusual`|`Exceptional`|`Grand`|`Unreal`|`Fabricated`")
	embed.add_field(name="`description`",value="Give a short description over what you want the item to do or any features")
	await ctx.send(embed=embed)

@client.command()
async def suggest(ctx,itemname="",rarity="",*,description=""):
	while True:
		if itemname!="" and len(itemname)<20:
			break
		else:
			p = await ctx.send("Enter in `Item Name`\nRequirements: Item name has to be less than 20 Characters")
			itemname = await client.wait_for('message',check=lambda m:m.author == ctx.author)
			itemname = itemname.content
			await p.delete()
	while True:
		rarity = str(rarity).lower()
		if rarity in ['inferior', 'unusual', 'exceptional', 'grand', 'unreal', 'fabricated']:
			break
		else:
			p = await ctx.send(":warning:**Invalid or Missing** Rarity\nHere is the list: `Inferior`|`Unusual`|`Exceptional`|`Grand`|`Unreal`|`Fabricated`")
			rarity = await client.wait_for("message",check=lambda m:m.author==ctx.author)
			rarity = rarity.content
			await p.delete()
	while True:
		if len(description)==0:
			p = await ctx.send(":warning:**Invalid or Missing** Description\nShould be at least 10 Words long")
			description = await client.wait_for("message",check=lambda m:m.author==ctx.author)
			description = description.content
			await p.delete()
		elif len(description.split())>10:
			break
	
	chan = client.get_channel(817575042236940318)
	embed = discord.Embed(
		title = "Loot Table Suggestion",
		description = f"Suggested by {ctx.author.name} in {ctx.guild.name},#{ctx.channel.name}",
		colour = discord.Colour.green()
	)
	embed.add_field(name = "Suggested Item Name",value = itemname.title(),inline=False)
	embed.add_field(name = "Suggested Rarity",value = rarity.title())
	embed.add_field(name = "Description",value = description)
	await chan.send(embed=embed)
	await ctx.send("Suggestion Successfully Made!!!",embed=embed)

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
	    title="Leaderboard",
	    description=
	    f"Players May Not Include members of this guild ({ctx.guild.name})",
	    color=discord.Color.teal())
	pla_n, val_n = [], []
	for i in db:
		pla_n.append(db[i]["name"])
		val_n.append(db[i]["tokens"])
	rep = 0
	for i in range(len(val_n)):
		rep += 1
		index = val_n.index(max(val_n))
		embed.add_field(name=f"**{rep} - {pla_n[index]}**",
		                value=f"__{val_n[index]}__",
		                inline=False)
		val_n.pop(index)
		pla_n.pop(index)
	embed.set_footer(text=f"Powered by Replit DB")
	embed.set_author(name="GachaCord")
	await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx,new_prefix):
	if len(new_prefix)>5:
		await ctx.send(":warning:Prefix has to be __*less than or equal to* ** Characters**__!!!")
		return
	with open("prefix.json") as f:
		prefixes = json.load(f)
	prefixes[str(ctx.guild.id)] = new_prefix
	with open("prefix.json","w") as f:
		json.dump(prefixes,f,indent=2)
	await ctx.send(f":white_check_mark:Successfully changed Sever Prefix for Server <{ctx.guild.id}> to `{new_prefix}`")

@client.command()
async def list_db(ctx):
	flg = False
	for i in ctx.author.roles:
		if i.name == "Bot Tester" or ctx.author.name == "Fishball_Noodles":
			flg = True
			break
	if flg != True:
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
			db[author_id] = {
			    "name": ctx.author.name,
			    "joined_in": str(joined_in),
			    "tokens": 50
			}
		await prompt.delete()
	display = discord.Embed(
	    title=f"Statistics for @{ctx.author.name}",
	    description=
	    f"__**Gacha Cord Bot** *Statistics*__\nPlayer ID: **{ctx.author.id}**\n",
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
		await ctx.send(f"Create an Account First By Doing `{get_prefix(ctx,ctx.message)}create`")
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
	embed.set_author(name=ctx.author.name)
	await ctx.send(embed=embed)


@client.command()
async def dice(ctx, bet):
  author_id = str(ctx.author.id)
  tokens = db[author_id]["tokens"]
  if int(bet) > tokens:
	  await ctx.send("You can't bet more than you have. ")
	  return
  bot_dice = randint(1, 6)
  player_dice = randint(1, 6)
  await ctx.send(
	    f"**GachaCord Bot** rolled {bot_dice}.\n**{ctx.author.name}** rolled {player_dice}."
	)
  if player_dice > bot_dice:
	  await ctx.send(
		    f'Congrats {ctx.message.author.mention}, you won {bet} tokens!')
	  update(author_id, "tokens", db[author_id]["tokens"] + int(bet))
  elif player_dice < bot_dice:
  	await ctx.send(
  	    f'Lmao {ctx.message.author.mention}, you lost {bet} tokens.')
  	update(author_id, "tokens", db[author_id]["tokens"] - int(bet))
  else:
  	await ctx.send('Both of you rolled the same number. Bet returned.')


@client.command()
async def addtokens(ctx, user, amt):
	user=user.replace("<","")
	user=user.replace(">","")
	user=user.replace("@","")
	user=user.replace("!","")
	if ctx.author.id in admin:
		update(user, 'tokens', db[user]['tokens'] + int(amt))
		await ctx.send(f'{amt} tokens added. ')
	else:
		await ctx.send("Lmao you can't do this you peasent")


@client.command()
async def removetokens(ctx, user, amt):
	user = user.replace("<", "")
	user = user.replace(">", "")
	user = user.replace("@", "")
	user = user.replace("!", "")
	if ctx.author.id in admin:
		update(user, 'tokens', db[user]['tokens'] - int(amt))
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
            cmd=(msg.content.lower())
            placeholder=randint(1,13)
            if cmd == 'hit':
                if placeholder>=11 and placeholder<=13:
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


@client.command(aliases=['rl'])
async def roulette(ctx,bet_amount=""):
  import roulettesettings
  try:
    bet_amount = int(bet_amount)
  except:
    await ctx.send(embed=discord.Embed(title=":warning:Invalid Bet Amount",description="Bet amount should be more than 0 and less than your current amount of tokens",colour=discord.Colour.red()))
    return
  
  await ctx.send('**Place your Bet type or Guess a Number(x20 Reward)**')
  bet_type = await client.wait_for('message',check=lambda x:x.author==ctx.author)
  content = bet_type.content.lower()
  allowed_methods=["black","red","low","high","even","odd"]
  if content.isdigit() or content in allowed_methods:
    pass
  else:
    await ctx.send(embed=discord.Embed(
      title=":warning:**Invalid Bet Type!!!**",
      description="Choose From this list of Allowed Methods"))
    number = randint(0,36)
  props = roulettesettings.get_properties(number)
  props.pop('dozen_grp')

  if props["colour"]=="black":
    display = discord.Embed(colour=discord.Colour.dark_theme())
  elif props["colour"]=="red":
    display = discord.Embed(colour=discord.Colour.red())
  display.add_field(name=f"The number is {number}",value=f'Colour: **{props["colour"].title()}**\nHeight: **{props["height"].title()}**\nEvenerity: **{props["evenerity"].title()}**')
  await ctx.send(embed=display)
  if content.isdigit():
    if int(content)==number:
      multiplier = 20
      win = True
    else:
      for v in props:
        if props[v] == bet_type.content.lower():
          win = True
          break
        else:
          win = False
  author_id = ctx.author.id
  if win==True:
    await ctx.send(f"**You Won!!!**\n__{int(bet_amount)*multiplier}__ added to your account!")
    update(author_id, "tokens", db[author_id]["tokens"] + int(bet_amount)*multiplier)
  else:
    await ctx.send(f"**You Lost!!!**\n__{bet_amount}__ subtracted from your account!")
    update(author_id, "tokens", db[author_id]["tokens"] - int(bet_amount))

@client.command()
async def push(ctx,**kwargs):
  pass

@client.command(name = "isadmin")
async def grandentrance(ctx):
	if ctx.author.id in admin:
		await ctx.send(
		    f"**All hail the great, mighty and powerful, {ctx.author.name}! **"
		)
	else:
		await ctx.send("**You do not deserve a grand entrance you peasent.**")

client.loop.create_task(change_p())
keep_alive()
client.run(os.getenv("token"))
