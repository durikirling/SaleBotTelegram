import requests, bs4, json, time
from db.models import Product, User

site='https://market.yandex.ru'

productList = [
    {
        'name': 'product--koltso-sokolov-iz-zolota-s-fianitom-019243',
        'product_id': 1784515300,
        'uniqueId': 979250,
        'skuList': [
            (101871194746, 19), # 19
            (101926300922, 18.5), # 18.5
            (101926167973, 18), # 18
            (101926300923, 17.5), # 17.5
            (101926300921, 17), # 17
            (101871194747, 16.5), # 16.5
            (101870798311, 16), # 16
            (101983193933, 15.5), # 15.5
        ]
    },
    {
        'name': 'product--koltso-sokolov-diamonds-iz-zolota-s-brilliantami-1012584',
        'product_id': 1829448687,
        'uniqueId': 979250,
        'skuList': [
            101983079614, # 18
            101983079615, # 16
            102963565220, # 15.5
            101983079617, # 15
        ]
    },
]

def test(flag=True):
    # session = requests.Session()
    # session.headers = {
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    #         'Accept-Language': 'ru',
    #     }
    
    index = 0
    # discount = 40
    ex = '' # f"uniqueId={productList[index]['uniqueId']}&"
    
    url = f"{site}/{productList[index]['name']}/{productList[index]['product_id']}?{ex}sku="

    res = []
    returnedResult = []
    data_base = None

    try:
        with open('db/products_data.txt', "r", encoding='utf-8') as file_data:
            data_base = file_data.read()
            data_base = json.loads(data_base)
    except Exception as err:
        print("ERROR READ DATA FILE", err)
        data_base = None
    
    for sku in productList[index]['skuList']:
        product_url = url + str(sku[0])
        req = requests.get(product_url)
        text = req.text
        soup = bs4.BeautifulSoup(text, 'lxml')
        container = soup.select("script[type='application/ld+json']")
        for item in container:
            if item.contents[0]:
                content = item.contents[0]
                if content.find('"@type":"Product"') != -1:
                    json_data = json.loads(content)
                    if json_data.get('@type') == 'Product':
                        data = json_data.get('offers')
                        price = int(data.get('price'))
                        # price = price*(1-discount/100)
                        res.append({
                            'size': sku[1],
                            'sku': sku[0],
                            'price': price,
                            'url': product_url,
                        })
                        if data_base:
                            product_data = [x for x in data_base["data"] if x["sku"] == sku[0]]
                            if product_data:
                                product_data = product_data[0]
                                if (product_data["price"] != price):
                                    returnedResult.append({
                                        'size': sku[1],
                                        'sku': sku[0],
                                        'new_price': price,
                                        'old_price': product_data["price"],
                                        'url': product_url
                                    })
                            else:
                                returnedResult.append({
                                    'size': sku[1],
                                    'sku': sku[0],
                                    'new_price': price,
                                    'old_price': None,
                                    'url': product_url,
                                })
                        else:
                            returnedResult.append({
                                'size': sku[1],
                                'sku': sku[0],
                                'new_price': price,
                                'old_price': None,
                                'url': product_url,
                            })
            else:
                continue

    res = {
                'last_update_alt': time.strftime("%H:%M:%S - %d.%m.%Y", time.localtime()),
                'last_update': time.time(),
                'data': res
            }
    if flag:
        with open('db/products_data.txt', "w+", encoding='utf-8') as file_data:
            json.dump(res, file_data)

    returnedResult = {
        "last_update": data_base["last_update"] if data_base else None,
        "last_update_alt": data_base["last_update_alt"] if data_base else None,
        "data": returnedResult
    }    
    return returnedResult if flag else res["data"]




    # url2 = 'https://market.yandex.ru/product--koltso-sokolov-diamonds-iz-zolota-s-brilliantami-1012584/1829448687?sku=101983079614&uniqueId=979250'
    # req2 = session.get(url2)
    # print(req2)
    # print(req2.cookies)

    # url = 'https://market.yandex.ru/api/resolve/?r=src/resolvers/productPage/resolveProductCardRemote:resolveProductCardRemote&r=src/resolvers/productPage/resolveProductCardRemote:resolveProductCardRemote'
    # params = {
    #     'params':[
    #         {'skuId':'101983079614','businessId':'979250','productId':'1829448687'},
    #         {'skuId':'101983079614','businessId':'979250','productId':'1829448687'}
    #     ],
    #     'path':'/product--koltso-sokolov-diamonds-iz-zolota-s-brilliantami-1012584/1829448687?sku=101983079615&uniqueId=979250'
    # }
    # req = session.post(url=url, params=params, cookies=req2.cookies)
    # print(req)


# test()