import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tkinter import *
import secrets

root=Tk()

root.title("Spotify Controller")
root.geometry('420x420')

#Scopes can be found at https://developer.spotify.com/documentation/general/guides/authorization/scopes/
scope = "user-read-currently-playing"


#Find your client_id and client_secret at your spotify project dashboard
id=secrets.client_id
secret=secrets.client_secret

#Create your own uri
uri=secrets.redirect_uri

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(id,secret,uri,None,scope,None,None,None,False,True))

#last-played song
try:
    lastPlayed=sp.currently_playing()['item']['name']
except:
    lastPlayed="None"
try:
    song=sp.currently_playing()['item']['name']
except:
    song="No Song Currently Playing"
#For tkinter screen creation
formed=False

#Converts RGB values to Hex
def hexify(r,g,b):
    return f'#{r:02x}{g:02x}{b:02x}'

#Goes back to previous song
def previousSong():
    scope = "streaming"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(id,secret,uri,None,scope,None,None,None,False,True))
    sp.previous_track()

#Skips to next song
def nextSong():
    scope = "streaming"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(id,secret,uri,None,scope,None,None,None,False,True))
    sp.next_track()

#Adjusts volume
def changeVolume(volumeLevel):
    scope = "streaming"
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(id,secret,uri,None,scope,None,None,None,False,True))
    sp.volume(volumeLevel)

#root.configure(background='black')


r=0
g=0
b=0

rCheck=False
gCheck=False
bCheck=False

try:
    while True:
        root.configure(background=hexify(r,g,b))
        if r!=255 and rCheck==False and bCheck==False:
                r+=3
        else:
            if bCheck==False:
                if g!=255 and gCheck==False:
                        g+=3
                else:
                    if rCheck==False:
                        rCheck=True
                    if gCheck==False:
                        gCheck=True
                    if r!=0:
                        r-=3
                    elif r==0:
                        if b!=255 and bCheck==False:
                                b+=3
                        else:
                            if g!=0:
                                g-=3
                            else:
                                bCheck=True
                                if rCheck==True:
                                    rCheck=False
            else:
                if r!=255:
                    r+=3
                else:
                    if b!=0:
                        b-=3
                    else:
                        bCheck=False
                        gCheck=False
            
        if formed==False:
            songLabel=Label(root,text=song)
            songLabel.config(background=hexify(27,215,96),fg=hexify(21,23,21))
            songLabel.place(relx=.5,rely=.1,anchor="center")

            artists=""
            
            for i in range(len(sp.currently_playing()['item']['artists'])):
                artists+=sp.currently_playing()['item']['artists'][i]['name']
                if i!=len((sp.currently_playing()['item']['artists']))-1:
                    artists+=", "

            artistLabel=Label(root,text=artists)
            artistLabel.config(background=hexify(27,215,96),fg=hexify(21,23,21))
            artistLabel.place(relx=.5,rely=.15,anchor="center")

            previousButton=Button(root,text="Previous Song",activebackground='#a3c850',command=lambda:previousSong())
            previousButton.config(highlightbackground=hexify(27,215,96),fg=hexify(21,23,21))
            previousButton.place(relx=.5,rely=.35,anchor="center")

            nextButton=Button(root,text="Next Song",command=lambda:nextSong())
            nextButton.config(highlightbackground=hexify(27,215,96),fg=hexify(21,23,21))
            nextButton.place(relx=.5,rely=.45,anchor="center")

            volumeScale=Scale(root,from_=0,to=100,orient=HORIZONTAL,highlightbackground=hexify(27,215,96))
            volumeScale.place(relx=.5,rely=.55,anchor="center")

            volumeAdjust=Button(root,text="Adjust Volume",command=lambda:changeVolume(volumeScale.get()),highlightbackground=hexify(27,215,96))
            volumeAdjust.place(relx=.5,rely=.65,anchor="center")

            root.update()
            
            formed=True
        
        try:
            song=sp.currently_playing()['item']['name']
            if song!=lastPlayed:
                songLabel.destroy()
                songLabel=Label(root,text=song)
                songLabel.config(background=hexify(27,215,96),fg=hexify(21,23,21))
                songLabel.place(relx=.5,rely=.1,anchor="center")

                lastPlayed=song

                artistLabel.destroy()
                artists=""
                for i in range(len(sp.currently_playing()['item']['artists'])):
                    artists+=sp.currently_playing()['item']['artists'][i]['name']
                    if i!=len((sp.currently_playing()['item']['artists']))-1:
                        artists+=", "

                artistLabel=Label(root,text=artists)
                artistLabel.config(background=hexify(27,215,96),fg=hexify(21,23,21))
                artistLabel.place(relx=.5,rely=.15,anchor="center")

                volumeScale=Scale(root,from_=0,to=100,orient=HORIZONTAL,highlightbackground=hexify(27,215,96))
                volumeScale.place(relx=.5,rely=.55,anchor="center")

                volumeAdjust=Button(root,text="Adjust Volume",command=lambda:changeVolume(volumeScale.get()),highlightbackground=hexify(27,215,96))
                volumeAdjust.place(relx=.5,rely=.65,anchor="center")

                root.update()
        except:
            continue
        
        root.update()
except:
    print("No song playing")