import discord
from discord.ui import Button, Select, View
from pytube import YouTube, Search

class PlaylistControls(View):
    def __init__(self, ctx, playlist, play_song_func, start_index=0):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.playlist = playlist
        self.play_song_func = play_song_func
        self.index = start_index
        self.play_next_song = True
        self.max_options = 25  # Maximum number of options per select menu
        self.page = 0  # Current page index

        self.update_select_options()

    def update_select_options(self):
        # Clear existing items
        self.clear_items()

        # Calculate start and end index for the current page
        start = self.page * self.max_options
        end = start + self.max_options
        options = [
            discord.SelectOption(label=f'Song {i+1}: {track["name"]} - {track["artist"]}', value=str(i))
            for i, track in enumerate(self.playlist.tracks[start:end], start=start)
        ]

        self.select = Select(placeholder='Select a song from the playlist', options=options)
        self.select.callback = self.select_callback
        self.add_item(self.select)

        # Add pagination buttons if needed
        if len(self.playlist.tracks) > self.max_options:
            if self.page > 0:
                self.add_item(self.create_page_button('Previous', 'previous_page'))
            if end < len(self.playlist.tracks):
                self.add_item(self.create_page_button('Next', 'next_page'))

    def create_page_button(self, label, custom_id):
        return Button(label=label, custom_id=custom_id, style=discord.ButtonStyle.primary)

    async def select_callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        self.index = int(self.select.values[0])
        self.play_next_song = False  # Prevent automatic play next during manual selection
        await self.play_current_song()
        await interaction.followup.send(f'Playing: {self.playlist.get_track(self.index)["name"]}', ephemeral=True)
        self.play_next_song = True  # Re-enable automatic play next after manual selection

    async def play_current_song(self):
        track = self.playlist.get_track(self.index)
        search_query = f'{track["name"]} {track["artist"]}'
        print(f'Searching for: {search_query}')
        
        search = Search(search_query)
        result = search.results
        if result:
            url = result[0].watch_url
            await self.play_song_func(self.ctx, url, self)
        else:
            await self.ctx.send(f'No results found for the song: {track["name"]} by {track["artist"]}')
        
        # Resend the playlist controls to the user
        await self.ctx.send('', view=self)

    @discord.ui.button(label='Previous', style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = max(0, self.index - 1)
        self.play_next_song = False  # Prevent automatic play next during manual selection
        await self.play_current_song()
        await interaction.response.send_message(f'Skipped to previous song: {self.playlist.get_track(self.index)["name"]}', ephemeral=True)
        self.play_next_song = True  # Re-enable automatic play next after manual selection

    @discord.ui.button(label='Next', style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.index = min(self.playlist.get_total_tracks() - 1, self.index + 1)
        self.play_next_song = False  # Prevent automatic play next during manual selection
        await self.play_current_song()
        await interaction.response.send_message(f'Skipped to next song: {self.playlist.get_track(self.index)["name"]}', ephemeral=True)
        self.play_next_song = True  # Re-enable automatic play next after manual selection

    async def next_page(self, interaction: discord.Interaction):
        self.page += 1
        self.update_select_options()
        await interaction.response.edit_message(view=self)

    async def previous_page(self, interaction: discord.Interaction):
        self.page -= 1
        self.update_select_options()
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label='Shuffle', style=discord.ButtonStyle.secondary)
    async def shuffle_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        from random import shuffle
        shuffle(self.playlist.tracks)
        self.index = 0  # Reset index after shuffle
        self.page = 0  # Reset page after shuffle
        self.update_select_options()
        await interaction.response.send_message("Playlist shuffled.", ephemeral=True)
        await self.play_current_song()  # Play the first song after shuffle

    @discord.ui.button(label='Loop', style=discord.ButtonStyle.success)
    async def loop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.play_next_song = not self.play_next_song  # Toggle loop
        state = "enabled" if self.play_next_song else "disabled"
        await interaction.response.send_message(f"Looping {state}.", ephemeral=True)

    def stop(self):
        self.play_next_song = False
