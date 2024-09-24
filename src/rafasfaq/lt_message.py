import discord

def embed_message() -> discord.Embed:
    title = "What is Language Transfer?"
    description = """Language Transfer is an audio series that teaches the basics of Modern Greek in a natural and easy to comprehend manner, focusing mainly on grammar and teaching useful vocab to prepare you for everyday conversations.
    
    It's highly encouraged you check it out, as it will help you build a very solid foundation to communicate in Greek. The complete series can be found [on Youtube](https://www.youtube.com/watch?v=dHsgJkV9J30&list=PLeA5t3dWTWvtWkl4oOV8J9SMB7L9N9Ogt), and [on SoundCloud](https://soundcloud.com/languagetransfer/sets/complete-greek-more-audios), along with [the transcript available, here](https://static1.squarespace.com/static/5c69bfa4f4e531370e74fa44/t/5d03d32873f6f10001a364b5/1560531782855/COMPLETE+GREEK+-+Transcripts_LT.pdf).
    
    The audio series follows the teacher (Mihalis) who teaches the student useful grammatical constructions and how to form sentences in a natural way, allowing you to follow along with the student by putting yourself in their shoes. More useful resources can be found in [the resources channel](https://discord.com/channels/350234668680871946/359578025228107776), notably in the pins, to help you advance your Greek level after Language Transfer."""
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x3392FF
    )
    embed.set_footer(text=faq_footer())
    
    return embed