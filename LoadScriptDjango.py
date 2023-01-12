import requests
import random


r = requests.get("http://127.0.0.1:8000")

cookies = {
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'http://127.0.0.1:8000/accounts/login/',
    'Origin': 'http://127.0.0.1:8000',
    'Connection': 'keep-alive',
}

#Disclaimer, dummy username and password. Please change
data = {
    'username': 'admin',
    'password': 'admin',
}

print("Logging in....")
r = requests.post('http://127.0.0.1:8000/accounts/login/', cookies=cookies, headers=headers, data=data)
print("Logging in....DONE")

runs = 1000

print("Randomly viewing polls " + str(runs) + " number of times")

while(runs > 0):
    random_poll = random.randint(1,10)
    r = requests.get("http://127.0.0.1:8000/polls/" + str(random_poll) + "/")
    print("Viewed random poll " + str(random_poll))
    runs = runs - 1

    print("Randomly voting on poll " + str(random_poll))

    print("Found the following choices:")

    valid_choices = []
    for item in r.text.split('\n'):
        if "id=\"choice" in item:
            values = item.split("=\"")
            valid_choice = values[len(values)-1].strip(">").strip("\"")
            valid_choices.append(valid_choice)
    print("Picking random choice of: ")
    print(valid_choices)
    print("Picked random choice: ")

    random_pick = random.randint(1,len(valid_choices)-1)
    random_pick_value = valid_choices[random_pick]
    print(random_pick_value)

    data = {
        'choice': str(random_pick_value),
    }

    cookies = {
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'http://127.0.0.1:8000/accounts/login/',
        'Origin': 'http://127.0.0.1:8000',
        'Connection': 'keep-alive',
    }
    r = requests.post('http://127.0.0.1:8000/polls/' +str(random_poll)+ '/vote/', cookies=cookies, headers=headers, data=data)