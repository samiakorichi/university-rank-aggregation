import re
import json
import requests
import time


def get_one_page(url):  # Cookie Le délai expirera, veuillez mettre à jour à nouveau.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        'Cookie': '__mta=246748859.1696065841332.1696069479939.1696069774805.13; uuid_n_v=v1; uuid=15CABCF05F7311EE9B48656ACF070BDBEE75DD5BC68B475492A27F08326C5E8B; _csrf=f6151547ff338979b7f35fa8a1d55adf4f637b549f0f122ce94bfc40937a18a3; _lxsdk_cuid=18ae566e181c8-017f502ff42a3e-26031e51-384000-18ae566e181c8; _lxsdk=15CABCF05F7311EE9B48656ACF070BDBEE75DD5BC68B475492A27F08326C5E8B; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1696065841; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1696069774; _lxsdk_s=18ae58b00b1-38-c29-d99%7C%7C19'
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {'index': item[0],
               'image': item[1],
               'title': item[2].strip(),  # strip()Utilisé pour supprimer les caractères spécifiés ou les caractères d'espacement par défaut des deux côtés d'une chaîne
               'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
               'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
               'score': item[5].strip() + item[6].strip()
               }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(2.5)
