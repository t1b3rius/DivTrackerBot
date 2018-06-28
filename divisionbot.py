import discord
from discord.ext import commands
import requests
from bs4 import BeautifulSoup
import re

bot = commands.Bot(command_prefix='$', description='Bot for check player info')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(pass_contex=True)
async def help(ctx):
    author=ctx.message.author
    em = discord.Embed(colour=discord.Colour.orange()
    )
    em.set_author(name='DivisionTrackBot')
    em.add_field(name='.help', value='Hello i am DivisionTrackBot, originally made for M8 clan Discord server\n**Comands**:\n**$short** for getting short info about player.\
    \n**$more** for get more info.\n**$all** for complete info\nExample: $short M8.DRAFT_PUNK.')
    await ctx.send(author, embed=em)


@bot.command()
async def short(ctx, nickname):
    em = discord.Embed(description=str(DivisionBot(nickname)), colour=0xDEADBF)
    em.set_author(name='DivisionTrackBot')
    await ctx.send('Checking...🤔')
    if nickname == 'Ghost--__--':
        await ctx.send('Sorry, Ghost Loh')
    else:
        await ctx.send(embed=em)


@bot.command()
async def more(ctx, nickname):
    em = discord.Embed(description=str(DivisionBotFull(nickname)), colour=0xDEADBF)
    em.set_author(name='DivisionTrackBot')
    await ctx.send('Checking...🤔')
    if nickname == 'Ghost--__--':
        await ctx.send('Sorry, Ghost Loh')
    else:
        await ctx.send(embed=em)

@bot.command()
async def all(ctx, nickname):
    em = discord.Embed(description='**Nickname**: {}'.format(nickname), colour=0xDEADBF)
    em1 = discord.Embed(description=str(DivisionBot(nickname)), colour=0xDEADBF)
    em2 = discord.Embed(description=str(DivisionBotFull(nickname)), colour=0xDEADBF)
    em.set_author(name='DivisionTrackBot')
    await ctx.send('Checking...🤔')
    if nickname == 'Ghost--__--':
        await ctx.send('Sorry, Ghost Loh')
    else:
        await ctx.send(embed=em)
        await ctx.send(embed=em1)
        await ctx.send(embed=em2)


class DivisionBot():
    def __init__(self, nickname):
        self.url = 'http://divisiontracker.com/profile/uplay/' + nickname
        self.r = requests.get(self.url).text
        self.soup = BeautifulSoup(self.r, 'lxml')

    def days(self):
        days = self.soup.body.find_all('div', attrs={'class': 'stats-stat'})
        for day in days:
            if day.find(text=re.compile('Playtime')):
                theday = day
                break
        not_form_days = theday.find('div', attrs={'class': 'value'}).text
        return ''.join(not_form_days.splitlines())

    def rogues_killed(self):
        rogues = self.soup.body.find_all('div', attrs={'class': 'stats-stat'})
        for rogue in rogues:
            if rogue.find(text=re.compile('Rogue Players Killed')):
                therogue = rogue
                break
        return therogue.find('div', attrs={'class': 'value'}).text

    def __repr__(self):
        try:
            return ('**Playtime**: {}\n**Rogue Players Killed**: {}'.format(self.days(), self.rogues_killed()))
        except UnboundLocalError:
            return ('No information')


class DivisionBotFull():
    def __init__(self, nickname):
        self.url = 'http://divisiontracker.com/profile/uplay/' + nickname
        self.r = requests.get(self.url).text
        self.soup = BeautifulSoup(self.r, 'lxml')

    def challenge(self):
        challenges = self.soup.body.find_all('div', attrs={'class': 'stats-stat'})
        for challenge in challenges:
            if challenge.find(text=re.compile('Challenge')):
                thechallenge = challenge
                break
        return thechallenge.find('div', attrs={'class': 'value'}).text

    def hard(self):
        hards = self.soup.body.find_all('div', attrs={'class': 'stats-stat'})
        for hard in hards:
            if hard.find(text=re.compile('Hard')):
                thehard = hard
                break
        return thehard.find('div', attrs={'class': 'value'}).text

    def dz_level(self):
        dz_levels = self.soup.body.find_all('div', attrs={'class': 'stats-stat'})
        for level in dz_levels:
            if level.find(text=re.compile('Darkzone Level')):
                thelevel = level
                break
        return thelevel.find('div', attrs={'class': 'value'}).text

    def kills(self):
        kills = self.soup.body.find_all('div', attrs={'class': 'stats-stat'})
        for kill in kills:
            if kill.find(text=re.compile('Kills')):
                thekill = kill
                break
        return thekill.find('div', attrs={'class': 'value'}).text

    def __repr__(self):
        try:
            return('**Darkzone Level**: {}\n**Kills**: {}\n**Hard Missions**: {}\n**Challenge Missions**: {}'.format(self.dz_level(), self.kills(), self.hard(), self.challenge()))
        except UnboundLocalError:
            return ('No information')


bot.run('placeyoubottokenhere')
