import discord
from discord.ui import Button, View

class MusicControls(View):
    def __init__(self, ctx, playlist_controls):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.playlist_controls = playlist_controls

    @discord.ui.button(label='Pause', style=discord.ButtonStyle.primary)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client.is_playing():
            interaction.guild.voice_client.pause()
            await interaction.response.send_message("Music paused.", ephemeral=True)

    @discord.ui.button(label='Resume', style=discord.ButtonStyle.success)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.resume()
            await interaction.response.send_message("Music resumed.", ephemeral=True)

    @discord.ui.button(label='Stop', style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild.voice_client.is_playing() or interaction.guild.voice_client.is_paused():
            interaction.guild.voice_client.stop()
            await interaction.response.send_message("Music stopped.", ephemeral=True)
        self.playlist_controls.stop()
