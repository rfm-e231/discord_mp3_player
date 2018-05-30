import discord
import sys
token=''#Input a token of your bot.

class ThisBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.player = None
        self.voice = None
    
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def join_voice(self,message):
        voice_ch = message.author.voice_channel
        if voice_ch is None:
            await self.send_message(message.channel, 'ERROR?')
            print("ERROR: Not in voice chat")
        else:
            if self.voice is None:
                self.voice = await self.join_voice_channel(voice_ch)
            elif self.voice.channel != voice_ch:
                await self.leave_voice()
                self.voice = await self.join_voice_channel(voice_ch)
                if self.player != None:
                    self.player.stop()
            print("Connecting voice")
            return self.voice is not None
    async def leave_voice(self):
        print(self.voice)
        await self.voice.disconnect()
        print("Disconnecting voice")
    async def on_message(self,message):
        if message.content.startswith('!play'):
            if self.player!=None:
                await self.send_message(message.channel,"play the song")
                print("play mp3")
                self.player.start()
        elif message.content.startswith('!stop'):
            self.player.pause()
        elif message.content.startswith('!replay') or message.content.startswith('!restart'):
            self.player.resume()
        elif message.content.startswith('!reset'):
            self.player.stop()
            self.player=None
            await self.send_message(message.channel,"music deleated")
        elif message.content.startswith('!end'):
            await self.send_message(message.channel,"bye")
            await self.leave_voice()
            sys.exit()
        elif message.content.startswith('!set'):
            if await self.join_voice(message):
                self.player = self.voice.create_ffmpeg_player("music.mp3")
                await self.send_message(message.channel, "music setted")

bot=ThisBot()
bot.run(token)