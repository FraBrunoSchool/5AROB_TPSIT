import requests


def main():
    URL = "https://api.rawg.io/api/games"
    PARAMS = {'dates': '2019-01-01,2019-12-31', 'ordering': '-added'}
    r = requests.get(url=URL, params=PARAMS)
    for line in (r.json())['results']:
        print(line)


if __name__ == '__main__':
    main()