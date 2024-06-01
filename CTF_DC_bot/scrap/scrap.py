import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',  # Do Not Track Request Header
}

response = requests.get("https://ctftime.org/event/list/?year=2024&online=-1&format=0&restrictions=-1&upcoming=true",
                        headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


# 尋找所有的表格行
rows = soup.find_all('tr')
ctf_list = []


def get_official_URL(event_link):
    global headers
    res = requests.get("https://ctftime.org" + event_link, headers=headers)
    res_soup = BeautifulSoup(res.text, "html.parser")
    paragraphs = res_soup.find_all("p")
    for p in paragraphs:
        if "Official URL" in p.get_text():
            a_tag = p.find("a")
            if a_tag:
                return a_tag["href"]
            else:
                return None


def get_info(row):

    # 先清除先前存取到的資料
    ctf_list.clear()
    # 遍歷表格行，跳過表頭
    for row in rows[1:4]:  # rows[0] 是表頭
        cells = row.find_all('td')
        if cells:
            event_name = cells[0].text.strip()  # 從第一個 <td> 中獲得文字
            event_link = cells[0].a['href'] if cells[0].a else None  # 獲得鏈接
            date = cells[1].text.strip()
            weight = cells[4].text.strip()

            official_url = get_official_URL(event_link)
            if not official_url:
                official_url = "https://ctftime.org" + event_link

            if float(weight) >= 25:
                cell_dict = {"event_name": event_name, "date": date, "weight": weight, "url": official_url}
                ctf_list.append(cell_dict)

    return ctf_list
