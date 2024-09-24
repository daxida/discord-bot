import discord
from utils import faq_footer

def embed_message() -> discord.Embed:
    title = "RafasBot FAQ list"
    description = """Available commands are:
    `rafasbot, explain language transfer`
    """
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x3392FF
    )
    embed.set_footer(text=faq_footer())
    
    return embed