import bs4
from ez_aio.aio import get
from ez_aio import header0, proxy0
from json import dumps, loads
import re
import pandas


re_src = re.compile(r'src="(.+?)"')
re_name = re.compile(r'">(.+)</a>')
re_trust = re.compile(r'<span>(.+?)</span>')
re_recipe = re.compile(r'alt="(.+?)".*?<span>(.+?)</span>')


def table(cont):
    results = []
    soup = bs4.BeautifulSoup(cont, 'lxml')
    ti = soup.find('h2', {'class': 'wp-block-post-title'})
    if ti:
        clazz = ti.get_text()
    else:
        clazz = '未知类别'
    ta = soup.find('table', {'class': 'genshin_table'})
    if ta:
        thead = ta.find('thead')
        tds = thead.find_all('td')
        td_lst = [td.get_text() for td in tds]
        sc = ta.find('tbody').find('script')
        t = sc.text.strip().split('(', 1)[1].split(');', 1)[0]
        items = loads(t)
        for item in items:
            result = {'类别': clazz}
            for i, _k in enumerate(td_lst):
                if _k == 'Icon':
                    founds = re.findall(re_src, item[i])
                    if founds:
                        result['Icon'] = founds[0]
                    else:
                        result['Icon'] = '未知'
                elif _k == 'Name':
                    founds = re.findall(re_name, item[i])
                    if founds:
                        result['Name'] = founds[0]
                    else:
                        result['Name'] = '未知'
                elif _k == 'Rarity':
                    founds = re.findall(re_src, item[i])
                    result['Rarity'] = len(founds)
                elif _k == 'Adeptal Energy':
                    result['Adeptal Energy'] = item[i].split('&nbsp')[0]
                elif _k == 'Trust':
                    founds = re.findall(re_trust, item[i])
                    result['Trust'] = ','.join(founds)
                elif _k == 'Load':
                    if ' (' in item[i]:
                        n0, n1 = item[i].split(' (', 1)
                        n1 = n1.split(')')[0]
                        result['Load_0'] = n0
                        result['Load_1'] = n1
                    else:
                        result['Load_0'] = item[i]
                        result['Load_1'] = item[i]
                elif _k == 'AE/L Ratio':
                    if ' (' in item[i]:
                        n0, n1 = item[i].split(' (', 1)
                        n1 = n1.split(')')[0]
                        result['AE/L Ratio_0'] = n0
                        result['AE/L Ratio_1'] = n1
                    else:
                        result['AE/L Ratio_0'] = item[i]
                        result['AE/L Ratio_1'] = item[i]
                elif _k == 'Placement':
                    result['Placement'] = item[i]
                elif _k == 'Recipe':
                    founds = re.findall(re_recipe, item[i])
                    spans = re.findall(re_trust, item[i])
                    if spans:
                        hours = '+' + spans[-1]
                    else:
                        hours = ''
                    result['Recipe'] = '+'.join([found[1] + found[0] for found in founds]) + hours
                elif _k == 'Capturable with Net?':
                    result['Capturable with Net?'] = item[i]
                elif _k == 'Ver':
                    result['Ver'] = item[i]
            results.append(result)
    return results


def batch():
    nums = [
        1001, 1002, 1003, 1004, 1005, 1006,
        3001, 3002, 3003, 3005, 3006, 3007,
        4001, 4002, 4004,
        11003, 11001, 11002,
        5003, 5005, 5006,
        6002, 6003,
        13001, 13002, 13003, 6005, 6006, 13004, 13005,
        10001, 10002, 10003, 10004, 10005, 10006,
        7001, 7003, 7005, 7008, 7011,
        8001, 8002, 8003, 8004,
        9001, 9002,
        12001,
        7006, 7007, 7002, 7004, 7009
            ]
    # nums = [1001]
    a0 = [f'https://genshin.honeyhunterworld.com/fam_home_family_{num}/?lang=CHS' for num in nums]
    a = get([x for x in a0], func=table, headers=header0, proxy=proxy0)
    # print(json.dumps(a, indent=4, ensure_ascii=False))
    a_ = []
    for an in a:
        a_.extend(an)
    with open('results.txt', 'w', encoding='utf-8') as f:
        print(dumps(a_, indent=4, ensure_ascii=False), file=f)


def re_test():
    a = r'"<a href=\"/h_360101/?lang=CHS\"><div class=\"itempic_cont rar_bg_3\"><img loading=\"lazy\" alt=\"玉面檐枋墙\" src=\"/img/h_360101_35.webp\"></div></a>"'
    found = re.findall(re_src, a)
    print(found)
    print(len(found))


def main():
    batch()
    # re_test()
    pandas.read_json('results.txt').to_excel('results.xlsx', index=False)


if __name__ == '__main__':
    main()
