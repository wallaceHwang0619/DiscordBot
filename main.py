import discord
import os
import random
from riotwatcher import LolWatcher
from keep_alive import keep_alive

client = discord.Client()

my_api = os.environ['api_key']
watcher = LolWatcher(my_api)
my_region = 'na1'

nailImages = ['Nail.jpg', 'Hypers.jpg', 'Nationalism.png', 'Nayeel_poggers.jpg', 'Pharaoh.png', 'Trash.png', 'sadge.png', 'nail_eating.png', 'A-squab.jpeg', 'kiss.jpeg']

steveImages = ['cute.png', 'tommy.png', 'small boy.png', 'smol.jpeg']

def get_rank(username):
    player = watcher.summoner.by_name(my_region, username)
    ranked_stats = watcher.league.by_summoner(my_region, player['id'])

    soloQ = ""
    flexQ = ""
    for items in ranked_stats:
        if items['queueType'] == 'RANKED_SOLO_5x5':
            soloQ += items['tier'] + ' ' + items['rank'] + ' ' + str(items['leaguePoints']) + 'LP'

    for items in ranked_stats:
        if items['queueType'] == 'RANKED_FLEX_SR':
            flexQ += items['tier'] + ' ' + items['rank'] + ' ' + str(items['leaguePoints']) + 'LP'
    if soloQ == "" and flexQ == "":
        return 'You\'re unranked bruv.'
    if soloQ == "":
        return "Flex Rank: " + flexQ
    if flexQ == "":
        return "Solo/Duo Rank: " + soloQ
    return "Solo/Duo Rank: " + soloQ + '\n' + "Flex Rank: " + flexQ


def get_queue(username):
    player = watcher.summoner.by_name(my_region, username)

    ranked_stats = watcher.league.by_summoner(my_region, player['id'])

    soloQ = ""
    flexQ = ""

    for items in ranked_stats:
        if items['queueType'] == 'RANKED_SOLO_5x5':
            if items['hotStreak'] == True:
                soloQ += "in winners queue."
            else:
                soloQ += "not in winners queue. xd"

    for items in ranked_stats:
        if items['queueType'] == 'RANKED_FLEX_SR':
            if items['hotStreak'] == True:
                flexQ += "in winners queue."
            else:
                flexQ += "not in winners queue. xd"

    if soloQ == "" and flexQ == "":
        return "You don\'t play ranked. You're in neither winners nor losers queue. You in shitters queue."
    if soloQ == "":
        return "For flex, you\'re " + flexQ
    if flexQ == "":
        return "For solo/duo, you\'re " + soloQ
    return "For solo/duo, you\'re " + soloQ + '\n' + "For flex, you\'re " + flexQ


def get_Info(username):
    player = watcher.summoner.by_name(my_region, username)
    ranked_stats = watcher.league.by_summoner(my_region, player['id'])
    soloQ = ""
    flexQ = ""
    for items in ranked_stats:
        if items['queueType'] == 'RANKED_SOLO_5x5':
            winRate = float(items['wins'] / (items['wins'] + items['losses'])) * 100
            if winRate >= 55:
                soloQ += "***YOU'RE POG CHIMP*** (SoloQ: " + str(winRate) + "% WR)"
            elif winRate < 55 and winRate >= 50:
                soloQ += ("***You shilling*** (SoloQ: " + str(winRate) + "% WR)")
            elif winRate < 45:
                soloQ += ("***Ngl, you a shitter*** (SoloQ: " + str(winRate) + "% WR)")
            elif winRate >= 45 and winRate < 50:
                soloQ += ("***Oof*** (SoloQ: " + str(winRate) + "% WR)")
        if items['queueType'] == 'RANKED_FLEX_SR':
            winRate = float(items['wins'] / (items['wins'] + items['losses'])) * 100
            if winRate >= 55:
                flexQ += "***YOU'RE POG CHIMP*** (FlexQ: " + str(winRate) + "% WR)"
            elif winRate < 55 and winRate >= 50:
                flexQ += ("***You shilling*** (FlexQ: " + str(winRate) + "% WR)")
            elif winRate < 45:
                flexQ += ("***Ngl, you a shitter*** (FlexQ: " + str(winRate) + "% WR)")
            elif winRate >= 45 and winRate < 50:
                flexQ += ("***Oof*** (FlexQ: " + str(winRate) + "% WR)")
    if soloQ == "" and flexQ == "":
        return 'You\'re unranked bruv.'
    if flexQ == "":
        return soloQ
    if soloQ == "":
        return flexQ
    return soloQ + '\n' + flexQ


def get_OPGG(people):
  link = "https://na.op.gg/multi/query="
  if len(people) == 1:
    if people[0].find(' ') != -1:
      people[0] = people[0].replace(' ', '%20')
    return "https://na.op.gg/summoner/userName=" + people[0]
  for players in people:
    if players.find(' ') != -1:
      players = players.replace(' ', '%20')
    link+= players + '%2C%20'
  
  return link

def get_masteries(username):
  player = watcher.summoner.by_name(my_region, username)
  masteries = watcher.champion_mastery.by_summoner(my_region, player['id'])

  latest = watcher.data_dragon.versions_for_region(my_region)['n']['champion']

  champ_list = watcher.data_dragon.champions(latest, False, 'en_US')

  champ_dict = {}
  for key in champ_list['data']:
      row = champ_list['data'][key]
      champ_dict[row['key']] = row['id']

  playerMastery = "**3 Highest Mastery Champs:**\n"
  for i in range (0,3):
      playerMastery+= 'Champion: ' + champ_dict[str(masteries[i]['championId'])] + '\nMastery Level: ' + str(masteries[i]['championLevel']) + '\nMastery Points: ' + str(masteries[i]['championPoints']) + '\n\n'
  return playerMastery


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
      if channel.permissions_for(guild.me).send_messages:
        await channel.send('Suppity sup sup! To know my commands, type \'$help\'')
      break


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content

    if msg.startswith('$help'):
        await message.channel.send(
            "Here is a list of my commands:\n$help\n$myQueue ***Player Name*** \n$myRank ***Player Name*** \n$importantInfo ***Player Name***\n$opgg ***Player Name(s)*** *Separate multiple users with a \'**,**\'*\n$myMastery ***Player Name***")

    if msg.startswith('$myRank'):
        player = msg.replace('$myRank ', '')
        winRate = get_rank(player)
        await message.channel.send(winRate)

    if msg.startswith('$myQueue'):
        player = msg.replace('$myQueue ', '')
        queueType = get_queue(player)
        await message.channel.send(queueType)

    if msg.startswith('$importantInfo'):
        player = msg.replace('$importantInfo ', '')
        info = get_Info(player)
        await message.channel.send(info)

    if msg.startswith('$opgg'):
        line = msg.replace('$opgg ', '')
        accounts = line.split(',')
        links = get_OPGG(accounts)
        await message.channel.send(links)

    if msg.startswith('$myMastery'):
        player = msg.replace('$myMastery ', '')
        masteries = get_masteries(player)
        await message.channel.send(masteries)

    keyWords = msg.lower().split()

    for words in keyWords:
      if words.find('nayeel') != -1 or words.find('nail') != -1:
        await message.channel.send(file=discord.File(random.choice(nailImages)))

    for words in keyWords:
      if words.find('stephen') != -1 or words.find('steve') != -1 or words.find('yezihang') != -1:
        await message.channel.send(file=discord.File(random.choice(steveImages)))
    
    


keep_alive()
client.run(os.environ['TOKEN'])
