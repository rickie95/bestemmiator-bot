# A nice and kind bot.
import os
import random
import discord
from dotenv  import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
DICTONARY_FILE = 'bestemmie.txt'
swear_dict = []
client = discord.Client()

def init_swear_dict():
    with open(DICTONARY_FILE, 'r') as file:
        for row in file.readlines():
            swear_dict.append(row.rstrip())
        print("Loaded {} elements".format(len(swear_dict)))

def get_random_swear():
    index = random.randrange(0, len(swear_dict))
    return swear_dict[index]

def add_new_swear(swear):
    swear = swear.lower()
    swear_dict.append(swear)
    with open(DICTONARY_FILE, 'a') as file:
        file.write("{}\n".format(swear))
    print('Added {}'.format(swear))
    return swear

@client.event
async def on_ready():
    print(f'Bestemmiator is entered in {client.guilds[0]}')

@client.event
async def on_member_join(member):
    swear = get_random_swear()
    message = '{}! A quanto pare {member.name} è entrato.'.format(swear.capitalize())
    await member.create_dm()
    await member.dm_channel.send(message)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0] == '!':
        response = ''
        if message.content == '!moccola' or message.content == '!bestemmia':
            response = '{}'.format(get_random_swear().capitalize())
        elif message.content == '!presentati':
            response = '{}, sono Bestemmiator. Mi sembra abbastanza esplicativo {}.'.format(get_random_swear().capitalize(),get_random_swear())
            response = 'Sono stato creato perchè @MorbidezzaRick aveva del tempo da buttare mentre aspettava che Warzone si aggiornasse ({} Activision).'.format(get_random_swear())
        elif '!aggiungi' in message.content:
            response = ''
            # TODO: input sanification and exception management
            new_swear = message.content
            new_swear = new_swear.replace('!aggiungi ', '')
            response = ('{} mi piace!').format(add_new_swear(new_swear))
        elif message.content == '!aiuto' or message.content == '!help':
            response = ('{}, sembra che tu non abbia chiare le mie capacità:\n').format(get_random_swear().capitalize())
            response += '\n`!moccola` o `!bestemmia`: lancio qualche oscenità.'
            response += '\n`!presentati`: una breve ma efficace presentazione'
            response += '\n`!aggiungi [bestemmia]`: aggiungo `bestemmia` al mio personale elenco. **Non sarai citato**.'
            response += '\n\nUn update da 80Gb e tanta incazzatura hanno reso possibile tutto questo.'
            response += '\n*{} bestemmie e tanto amore per voi <3*'.format(len(swear_dict))

        await message.channel.send(response)

def main():
    init_swear_dict()
    client.run(TOKEN)

if __name__ == "__main__":
    main()
