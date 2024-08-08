import discord
from discord.ext import commands
from discord.ui import Button, Select, View
from pytube import YouTube, Search ,cipher
import os
from dotenv import load_dotenv
import asyncio
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from music_controls import *  # Import the MusicControls class
from playlist_controls import PlaylistControls  # Import the PlaylistControls class
from cohere_client import ask_cohere  # Import the Cohere interaction function
from custom_playlist import CustomPlaylist  # Import the CustomPlaylist class
from flask import Flask, request, jsonify, render_template
from threading import Thread
import requests
import json
load_dotenv()
TOKEN = os.getenv('discord_token')

SPOTIFY_CLIENT_ID = os.getenv('spotify_client_id')
SPOTIFY_CLIENT_SECRET = os.getenv('spotify_client_secret')
SPOTIFY_REDIRECT_URI = os.getenv('spotify_redirect_uri')

spotify_auth_manager = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                    client_secret=SPOTIFY_CLIENT_SECRET,
                                    redirect_uri=SPOTIFY_REDIRECT_URI,
                                    scope="playlist-read-private")

sp = spotipy.Spotify(auth_manager=spotify_auth_manager)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Create a folder to store downloaded songs
if not os.path.exists('songs'):
    os.makedirs('songs')

# Global playlist queue and playback state
playlist_queue = []
is_playing = False
current_ctx = None

# Flask application
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.json['query']
    search = Search(query)
    results = search.results[:5]
    options = [{"title": result.title, "author": result.author, "url": result.watch_url, "thumbnail": result.thumbnail_url} for result in results]
    return jsonify(options)

@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    global is_playing, current_ctx
    song = request.json['song']
    playlist_queue.append(song)
    if current_ctx and not is_playing:
        asyncio.run_coroutine_threadsafe(play_next_song(current_ctx), bot.loop)
    return jsonify(playlist_queue)

@app.route('/remove_from_queue', methods=['POST'])
def remove_from_queue():
    song_url = request.json['url']
    global playlist_queue
    playlist_queue = [song for song in playlist_queue if song['url'] != song_url]
    return jsonify(playlist_queue)

@app.route('/get_queue', methods=['GET'])
def get_queue():
    return jsonify(playlist_queue)

def run_flask_app():
    app.run(port=8080)

# Run Flask app in a separate thread
flask_thread = Thread(target=run_flask_app)
flask_thread.start()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='join', help='The bot joins the voice channel')
async def join(ctx):
    global current_ctx
    current_ctx = ctx
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You are not in a voice channel!")

@bot.command(name='leave', help='The bot leaves the voice channel')
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")

@bot.command(name='play', help='Play a song from YouTube by URL or name')
async def play(ctx, *, query):
    global current_ctx
    current_ctx = ctx
    if query.startswith("http://") or query.startswith("https://"):
        await add_song_to_queue(ctx, query)
    else:
        search = Search(query)
        results = search.results[:5]

        if not results:
            await ctx.send("No results found.")
            return

        # 播放第一首搜索結果
        await add_song_to_queue(ctx, results[0].watch_url)

        class SongSelect(Select):
            def __init__(self):
                options = [
                    discord.SelectOption(label=result.title, description=result.author, value=result.watch_url)
                    for result in results
                ]
                super().__init__(placeholder='Choose a song...', min_values=1, max_values=1, options=options)

            async def callback(self, interaction: discord.Interaction):
                await interaction.response.send_message(f'You selected {self.values[0]}')
                await add_song_to_queue(ctx, self.values[0])

        view = View()
        view.add_item(SongSelect())
        await ctx.send("Select a song to play:", view=view)

async def add_song_to_queue(ctx, url):
    global is_playing, playlist_queue
    yt = await asyncio.to_thread(YouTube, url)
    song = {
        "title": yt.title,
        "author": yt.author,
        "url": url,
        "thumbnail": yt.thumbnail_url,
    }
    playlist_queue.append(song)
    if not is_playing:
        await play_next_song(ctx)

async def play_next_song(ctx):
    global is_playing, current_ctx
    if playlist_queue:
        song = playlist_queue.pop(0)
        is_playing = True
        current_ctx = ctx
        await play_song(ctx, song['url'])
    else:
        is_playing = False

async def play_song(ctx, url):
    global is_playing, current_song
    try:
        yt = await asyncio.to_thread(YouTube, url)
        stream = await asyncio.to_thread(yt.streams.filter(only_audio=True).first)
        output_file = await asyncio.to_thread(stream.download, 'songs')
        base, ext = os.path.splitext(output_file)
        new_file = base + '.mp3'

        if not os.path.exists(new_file):
            os.rename(output_file, new_file)
        else:
            os.remove(output_file)

        if ctx.voice_client is None:
            if ctx.author.voice:
                channel = ctx.author.voice.channel
                await channel.connect()
            else:
                await ctx.send("You are not in a voice channel!")
                return

        def after_playing(error):
            asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop)

        ctx.voice_client.stop()
        ctx.voice_client.play(discord.FFmpegPCMAudio(new_file), after=after_playing)

        current_song = {
            "title": yt.title,
            "author": yt.author,
            "thumbnail": yt.thumbnail_url
        }

        await ctx.send(f'Now playing: {yt.title}', view=MusicControls(ctx, None))

        # Update the current song on the Flask server
        with open('current_song.json', 'w') as f:
            json.dump(current_song, f)
        
    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')
        is_playing = False

@app.route('/get_current_song', methods=['GET'])
def get_current_song():
    try:
        with open('current_song.json', 'r') as f:
            current_song = json.load(f)
        return jsonify(current_song)
    except FileNotFoundError:
        return jsonify(None)

async def fetch_spotify_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return [{'name': track['track']['name'], 'artist': track['track']['artists'][0]['name']} for track in tracks]

@bot.command(name='spotlist', help='Play a Spotify playlist')
async def spotlist(ctx, url):
    try:
        playlist_id = url.split("/")[-1].split("?")[0]
        tracks = await fetch_spotify_playlist_tracks(playlist_id)
        await ctx.send(f'The Spotify playlist contains {len(tracks)} songs.')
        
        custom_playlist = CustomPlaylist()
        for track in tracks:
            custom_playlist.add_track(track['name'], track['artist'])
        
        view = PlaylistControls(ctx, custom_playlist, play_song)
        await ctx.send('Use the buttons and dropdown below to navigate the playlist.', view=view)
        await view.play_current_song()

    except Exception as e:
        await ctx.send(f'An error occurred: {str(e)}')

@bot.command(name='ai', help='Ask a question to the AI')
async def ai(ctx, *, question):
    summary = await ask_cohere(question)
    await ctx.send(f'AI says: {summary}')

bot.run(TOKEN)
