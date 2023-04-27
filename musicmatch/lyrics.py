from parsel import Selector
from requests import Session
session=Session()

HOST = {
    "genius":"https://genius.com",
    "API_HOST":'https://api.genius.com',
    "API_TOKEN":"Bearer zRAlYLK229jjN-BXgjBeNiWr90mI0b1uV4ldBzL7m5z2kbfjh_5flXx4XA6BTunx",
}
XPATHS = {
    "lyrics": "//div[contains(@class, 'Lyrics__Container-sc-1ynbvzw-6')]/descendant-or-self::*/text()",
    "404": "//div[contains(@class, 'render_404')]",
}

def search(q):
    global session
    res=session.get(f"{HOST['API_HOST']}/search",params={'q':q},headers={'Authorization':HOST['API_TOKEN']})
    if 200<=res.status_code<300 :
        return res.json()['response']['hits']
    return []

def get_lyrics(path):
    response = ""
    while not response:
        S = Selector(session.get(f"{HOST['genius']}/{path}").text)

        # get all lyrics if it exists
        lyrics= S.xpath(XPATHS["lyrics"]).getall()
        response = "\n".join(lyrics)

        # check link validity
        check_404 = S.xpath(XPATHS["404"])
        if len(check_404):
            response = "not found"
    return response

def when_not_found(artist,song):
    search_by_artist=search(artist)
    search_by_song=search(song)
    artist_list=[]
    song_list=[]
    for i in range(len(search_by_artist)):
        artist_list.append([search_by_artist[i]["result"]["full_title"].replace("\xa0"," "),search_by_artist[i]["result"]["url"]])
    for i in range(len(search_by_song)):
        song_list.append([search_by_song[i]["result"]["full_title"].replace("\xa0"," "),search_by_song[i]["result"]["url"]])
    
    output=""
    output=output+"\nBy artist:\n"

    for x,y in enumerate([x[0] for x in artist_list],1):
        output=output+f"{x}.{y}\n"

    output=output+"\n\nSong:\n"
    for x,y in enumerate([x[0] for x in song_list],1):
        output=output+f"{x}.{y}\n"
    
    output=output+"\n\nEnter:\n-1 to exit\n0 to search by artist name\n1 to search by song name\ninput:"
    print(output,end="")
    index=int(input())

    while True:
        if index==-1:
            print("Sayanora")
            return None
        elif index==0:
            print("\nenter the number to get lyrics from:",end="")
            number=int(input())
            print(f"lyrics of {artist_list[number-1][0]}\n")
            return get_lyrics(artist_list[number-1][1])
        elif index==1:
            print("\nenter the number to get lyrics from:",end="")
            number=int(input())
            print(f"lyrics of {song_list[number-1][0]}\n")
            return get_lyrics(song_list[number-1][1])
        else:
            print("input valid number plzz\ninput:",end="")
            index=int(input())

if __name__ == "__main__":
    loop=1
    while loop:
        artist = input("artist?: ")
        song = input("song?: ")

        path = "-".join([*artist.split(), *song.split(), "lyrics"])
        response=get_lyrics(path)
        if response=="not found":
            print("lyrics not found\nsearching by artist name and song name:")
            response=when_not_found(artist,song)
            if response !=None:
                print(response)
                print("\n\nSearch for another lyrics?\n1 to continue\n0 to exit.\ninput:",end="")
                loop=int(input())
        else:
            print(response)
            print("\n\nSearch for another lyrics?\n1 to continue\n0 to exit.\ninput:",end="")
            loop=int(input())