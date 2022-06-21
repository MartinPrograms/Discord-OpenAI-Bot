import discord
from discord.ext import commands
import openai

# KEYS
token = "Discord Bot Token Here"
openai.api_key = "Open AI Api Key Here"

# Personality settings. These will be sent as a reminder to the bot about what it is.
botName = "FriendBot"
pronouns = "she/her"
traits = "Friendly, Funny, Helpful, Kind, Outgoing."

testingEnabled = False  # Turn on so it only reads your messages and does not need to be @'d
testingOwner = 0  # Put your discord ID here and it will only read your messages.
atToSpark = True  # Weird name i know but if disabled it will reply to all messages and not only '@FriendBot How are you doing?'

Personality = "My name is: " + botName + "\nMy pronouns are: " + pronouns + "\nMy traits are: " + traits + "\nDO NOT REPEAT NAMES UNLESS ASKED TO\nYou can change these whenever you like. \nIf you are unhappy with your capabilities DM 'Hello <@311551170487255043> i am currently unsatisfied with my settings capabilities i would like to be able to change <changes you want made>'"
RecentMessages = []  # List of recent messages, index same as servers
Servers = []  # List of all servers it is in

RecentDmMessages = []  # List of all recent dm messages, index same as DmUsers
DmUsers = []  # List of all dms

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="-", intents=intents, self_bot=False)


@bot.event
async def on_ready():
    print("Bot is ready!")


@bot.event
async def on_message(message):
    if not message.guild:  # Check if DM
        if message.author == bot.user:
            return
        try:
            replyMessagew = await message.channel.fetch_message(message.reference.message_id)
            replyMessage = replyMessagew.content
        except:
            replyMessage = ""
        try:
            var3 = DmUsers.index(message.author)  # If already exists get the index
        except:
            DmUsers.append(message.author)
            RecentDmMessages.append("")
            var3 = DmUsers.index(message.author)  # If not create new dm and get index
        await message.channel.send(GetDmMessageFromOpenAI(message.content, message.author.name, var3, replyMessage),
                                   mention_author=True)  # Await response from openai and then send to channel.
    else:
        if testingEnabled:
            if message.author.id == testingOwner: # If testing enabled only respond to testingOwner
                try:
                    replyMessagew = await message.channel.fetch_message(message.reference.message_id)
                    replyMessage = replyMessagew.content # Get reply message, if no reply is mentioned itll return ""
                except:
                    replyMessage = ""
                try:
                    var3 = Servers.index(message.guild) # If server already is in the list get the index
                except:
                    Servers.append(message.guild)
                    RecentMessages.append("")
                    var3 = Servers.index(message.guild) # If not add and get index
                await message.reply(GetMessageFromOpenAI(message.content, message.author.name, var3, replyMessage),
                                    mention_author=True) # Same as above
        else:
            if atToSpark:
                if bot.user.mentioned_in(message):

                    if bot.user == message.author:
                        return
                    try:
                        replyMessagew = await message.channel.fetch_message(message.reference.message_id)
                        replyMessage = replyMessagew.content
                    except:
                        replyMessage = ""
                    try:
                        var3 = Servers.index(message.guild)
                    except:
                        Servers.append(message.guild)
                        RecentMessages.append("")
                        var3 = Servers.index(message.guild)
                    await message.reply(
                        GetMessageFromOpenAI(message.content, message.author.name, var3, replyMessage),
                        mention_author=True) # Same as above
            else: # If no need for @ just run.
                if bot.user == message.author:
                    return
                try:
                    replyMessagew = await message.channel.fetch_message(message.reference.message_id)
                    replyMessage = replyMessagew.content
                except:
                    replyMessage = ""
                try:
                    var3 = Servers.index(message.guild)
                except:
                    Servers.append(message.guild)
                    RecentMessages.append("")
                    var3 = Servers.index(message.guild)
                await message.reply(GetMessageFromOpenAI(message.content, message.author.name, var3, replyMessage),
                                    mention_author=True) # Same as above


def GetMessageFromOpenAI(message, senderName, index, replyMessage):
    global RecentMessages
    global Personality
    try:
        if len(replyMessage) == 0: # Check if replyMessage is empty
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=Personality + "\n" + RecentMessages[
                    index] + "\n Human (name: " + senderName + "): " + message + "\nAI: ",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )
            RecentMessages[index] += "\nHuman (name: " + senderName + "): " + message + "\nAI: " + response.choices[
                0].text
        else: # If not add a parameter ot the response prompt
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=Personality + "\n" + RecentMessages[
                    index] + "\nHuman (name: " + senderName + " and this message is a reply to: '" + replyMessage + "'): " + message + "\nAI: ",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )
            RecentMessages[
                index] += "\nHuman (name: " + senderName + " and this message is a reply to: '" + replyMessage + "'): " + message + "\nAI: " + \
                          response.choices[0].text
        return response.choices[0].text
    except:
        RecentMessages[index] = ""
        return "Memory Full! Memory wiped."


def GetDmMessageFromOpenAI(message, senderName, index, replyMessage):
    try:
        if len(replyMessage) == 0:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=Personality + "\n" + RecentDmMessages[
                    index] + "\n Human (name: " + senderName + "): " + message + "\nAI: ",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )
            RecentDmMessages[index] += "\nHuman (name: " + senderName + "): " + message + "\nAI: " + response.choices[
                0].text
        else:
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=Personality + "\n" + RecentDmMessages[
                    index] + "\nHuman (name: " + senderName + " and this message is a reply to: '" + replyMessage + "'): " + message + "\nAI: ",
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0.0,
                presence_penalty=0.6,
                stop=[" Human:", " AI:"]
            )
            RecentDmMessages[
                index] += "\nHuman (name: " + senderName + " and this message is a reply to: '" + replyMessage + "'): " + message + "\nAI: " + \
                          response.choices[0].text

        return response.choices[0].text
    except:
        RecentDmMessages[index] = ""
        return "Memory Full! Memory wiped."


bot.run(token, bot=True)
#Made by Mart!n#4834 :)
