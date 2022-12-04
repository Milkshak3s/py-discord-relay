import discord
import selfcord
import os


def load_ids(filename):
    ids = []
    for line in open(filename, "r"):
        sanitized_line = line.strip(' ').split("#")[0]
        if len(sanitized_line) > 0:
            ids.append(sanitized_line)
    return ids


DISCORD_USER_TOKEN = os.environ.get("DISCORD_USER_TOKEN")
DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
GUILD_IDS_FILENAME = os.environ.get("GUILD_IDS_FILENAME")
CHANNEL_IDS_FILENAME = os.environ.get("CHANNEL_IDS_FILENAME")
LISTEN_GUILD_IDS = load_ids(GUILD_IDS_FILENAME)
LISTEN_CHANNEL_IDS = load_ids(CHANNEL_IDS_FILENAME)
SEND_CHANNEL_ID = int(os.environ.get("SEND_CHANNEL_ID"))
BOT_ID = int(os.environ.get("BOT_ID"))


def main():
    dc = selfcord.Client()

    @dc.event
    async def on_ready():
        print(f"Listening User: {dc.user}")

    @dc.event
    async def on_message(message):
        guild_id = message.guild.id
        if guild_id not in LISTEN_GUILD_IDS:
            return

        channel_id = message.channel.id
        if channel_id not in LISTEN_CHANNEL_IDS:
            return

        author_id = message.author.id
        if author_id == BOT_ID:
            return

        msg_to_send = f"[{str(message.guild.name).upper()}] {message.author.name}:\t{message.content}"
        print(msg_to_send)

        intents = discord.Intents.default()
        rc = discord.Client(intents=intents)

        @rc.event
        async def on_ready():
            print(f"Logged In: {dc.user}")
            channel = rc.get_channel(SEND_CHANNEL_ID)
            await channel.send(msg_to_send)
            await rc.close()
        
        await rc.login(DISCORD_BOT_TOKEN)
        await rc.connect(reconnect=False)
        await rc.close()
    
    dc.run(DISCORD_USER_TOKEN)


if __name__ == '__main__':
    main()
