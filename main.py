import discord,os,asyncio,datetime,pytz
from discord.ext import commands
from keep_alive import keep_alive
from random import choice,randint
from replit import db

print("Loading...")
client = commands.Bot(command_prefix = "$")
client.remove_command("help")

def update(author_id,attr,val):
  context = db[author_id]
  context[attr] = val
  db[author_id] = context

@client.event
async def on_ready():
  print("Online")

async def change_p():
  await client.wait_until_ready()
  statuses = [f"{len(client.guilds)} Servers","$help",f"Latency: {round(client.latency*1000)}ms",choice(client.guilds).name]
  while not client.is_closed():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=choice(statuses)))
    await asyncio.sleep(2)

@client.command()
async def help(ctx):
  embed = discord.Embed(
    title = "Help",
    description = f"Command Prefix: `$`\n**Version `{open('version').readlines()[0]}`**",
    color = discord.Colour.teal()
  )
  embed.set_footer(text = "Made by 402 Class of 2021")
  embed.add_field(name = "Commands Available",value = "`$guessgame - Play a Number Guessing Game`")
  embed.add_field(name = "--------------",value="Intrested in Being a Developer?\nJoin Our [Discord Server](https://discord.gg/SkKVSq9z95) and contact one of our **Pink Fluffy Dinosaur Pilots**",inline=False)
  await ctx.send(embed=embed)

@client.command()
async def clear_db(ctx):
  if ctx.author.id == 591107669180284928:
    for i in db:
      del db[i]
    await ctx.send("**Database __Wipe Out__ Completed!!!**")
  else:
    await ctx.send('You do not have the relevant permssion')

@client.command()
@commands.has_role("Bot Tester")
async def list_db(ctx):
  for i in db:
    await ctx.send(db[i])
  await ctx.send("**Done**")
@list_db.error
async def perms(ctx,err):
  if isinstance(err, commands.error.MissingPermissions):
    await ctx.send('You do not have the relevant permssion')

@client.command(aliases = ["stats","create"])
async def statistics(ctx):
  author_id = str(ctx.author.id)
  while True:
    await ctx.send("*Finding Player Data...*",delete_after=2)
    try:
      tokens = db[author_id]["tokens"]
      prompt = await ctx.send("Player Data Found!!!")
      break
    except KeyError:
      prompt = await ctx.send(f"**Player Data for the name ({ctx.author.name})Not Found**!!!\n__*Attempting* To Create New Dataset__")
      
      joined_in = pytz.timezone("Asia/Singapore").localize(datetime.datetime.now()+datetime.timedelta(hours = 8)).strftime("%c")
      db[author_id] = {"joined_in":str(joined_in),"tokens":0}
    await prompt.delete()
  display = discord.Embed(
    title = f"Statistics for @{ctx.author.name}",
    description = f"__**402 Gacha Bot** *Statistics*__\nPlayer ID: **{ctx.author.id}**\n",
    color = discord.Colour.green()
  )
  display.add_field(name = "*Joined In*",value = db[author_id]["joined_in"],inline=False)
  display.add_field(name = "**TraceTogether Tokens**",value = tokens)
  await ctx.send(embed=display)

@client.command()
async def guessgame(ctx):
  display = discord.Embed(
    title = "Guessing Game",
    description = "*Guess* a __Number__ from *1 - 100*",
    color = discord.Colour.green()
  )
  number = randint(1,100)
  tries = 0
  author_id = str(ctx.author.id)
  try:
    tokens = db[author_id]["tokens"]
  except:
    await ctx.send("Create an Account First By Doing `$create`")
    return

  def check(m):
    if m.author == ctx.author:
      return True
      
  while tries<10:
    await ctx.send("Guess the random number between 1-100!")
    guess = await client.wait_for('message',check=check)
    guess = int(guess.content)
    tries+=1
    if guess < number:
      await ctx.send("The number is larger")
    elif guess > number:
      await ctx.send("The number is smaller")
    else:
      await ctx.send("You have guessed the correct number")
      break
  if tries <= 9:
    if tries==1:
      incre = 25
    elif tries==2:
      incre = 20
    elif tries==3:
      incre = 15
    elif tries==4:
      incre = 10
    else:
      incre = 5
    update(author_id,"tokens",db[author_id]["tokens"]+5)
  else:
    await ctx.send(f"**Too Bad @{ctx.author.name}!** You don't any points.")
  embed = discord.Embed(
    title = f"You took **{tries} tries** and recieved __{incre}__ tokens!!!",
    description = "**The Number** is `{number}`",
    color = discord.color.green()
  )
  await ctx.send(embed = embed)
    

client.loop.create_task(change_p())
keep_alive()
client.run(os.getenv("token"))