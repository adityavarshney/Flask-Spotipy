import random, string
from flask import Flask, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

''' 
Sets up the Spotipy client API authentication
Server-to-server auth made possible by the SpotifyClientCredentials object
Get your client_id and client_secret by:
1. signing up for Spotify developer
2. creating a test application (title, description)
3. copy your Client ID and Client Secret
4. Keep your client secret and client ID to yourself. You can reset them at any time.
'''
auth_manager = SpotifyClientCredentials(client_id=str(input("Please enter your client ID: ")), client_secret=str(input("Please enter your client secret: ")))
sp = spotipy.Spotify(client_credentials_manager=auth_manager)

''' 
Retrieve a user's playlists based on their Spotify user ID 
The user ID is available if you open Spotify, click on your profile, and share via URL 
Your user ID is the number in the URL:
https://open.spotify.com/user/<YOUR_ID>?....

Code implementation (from Client Credentials Flow): https://spotipy.readthedocs.io/en/2.17.1/

More spotipy examples here: https://replit.com/@Dan_Bailey/spotipy
'''
def get_playlists(spotify_user_id='spotify'): 
  playlists = sp.user_playlists(str(spotify_user_id), limit=1)
  output = ''
  while playlists:
      for i, playlist in enumerate(playlists['items']):
          output += playlist['name'] + '\n'
      if playlists['next']:
          playlists = sp.next(playlists)
      else:
          playlists = None
  return output

''' Creates our flask app! '''
app = Flask(
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

''' Main page of our website '''
@app.route('/')
def base_page():
  return render_template(
		'base.html',  # Template file path, starting from the templates folder.
    playlists=get_playlists('12181419277') # pass in what you'd like the element to display
	)

''' Second page of our website '''
ok_chars = string.ascii_letters + string.digits
@app.route('/2')
def page_2():
	rand_ammnt = random.randint(10, 100) # generate a string of random characters
	random_str = ''.join(random.choice(ok_chars) for a in range(rand_ammnt))
	return render_template('site_2.html', random_str=random_str)

''' Runs our flask application! '''
if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
		host='0.0.0.0',  # Establishes the host, required for repl to detect the site
		port=random.randint(2000, 9000)  # Randomly select the port the machine hosts on.
	)