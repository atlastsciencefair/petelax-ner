import requests
r = requests.post("https://api.pushover.net/1/messages.json", data={
            "token":"aajaiutjvx1fwdqy15g2nqcp6av8dt",
            "user":"usqmx1mv4pams23f4nq8igh5a7okzf",
            "message":"Got Image?"}, 
files={"attachment":open("/home/pi/Desktop/thermal_pic.jpg","rb")})
