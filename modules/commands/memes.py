from asyncio import sleep

from discord import Embed

from modules.commands.base import BaseCommand
from modules.database.memes import MemesList
from get_enviroment import COMMAND_PREFIX


class Memes(BaseCommand):

    def __init__(self, channel, author, message):
        super().__init__(channel, author)
        list = message.split(' ')
        self.name = list[0]
        # Check if substring is help example: 'prefix meme help'
        self.is_help = list[0] == 'help'
        # check if is help meme ex: 'prefix meme memename help'
        if (len(list) > 1):
            self.is_meme_help = list[1] == 'help'
        else:
            self.is_meme_help = True

        joinable = '_'
        text = joinable.join(list[1:])
        self.message = text.split('|')

    async def apply(self):
        if self.is_help:
            await self.help()
        elif self.is_meme_help:
            await self.meme_help()
        else:
            await self.meme()

    async def help(self):
        list = MemesList().get_info_all()
        list_message = []
        message = "**USE: " + COMMAND_PREFIX + " meme [meme_code] help**\n"
        for item in list:
            message += "**%s**: %s\n" % (item['name'], item['key'])
            if len(message) > 1900:
                list_message.append(message)
                message = ""
        first = True
        for message in list_message:
            embed = Embed()
            if first:
                first = False
                embed.title = 'List of meme commands'
            embed.description = message
            await self.user.send(embed=embed)
            await sleep(1)

    async def meme(self):
        # check if meme exists
        if(MemesList().get_url_meme(self.name) == ""):
            await self.channel.send("Meme not found")
        else:
            embed = Embed()
            url = MemesList().get_url_meme(self.name)
            url_format = '/'.join(self.message)
            embed.set_image(url="%s/%s.png?width=500" % (url, url_format))
            await self.channel.send(embed=embed)

    async def meme_help(self):
        embed = Embed()
        meme = MemesList().get_info(self.name)
        embed.title = meme['name']
        format = ""
        for i in range(0, int(meme['lines'])):
            format += "text%d|" % i
        format = format[:-1]
        url_format = format.replace('|', '/')
        embed.description = '**Use**: ' + COMMAND_PREFIX + ' meme %s %s' % (meme['key'], format)
        embed.set_image(url='%s/%s.png?width=500' % (meme['url'], url_format))
        await self.channel.send(embed=embed)
