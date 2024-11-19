import requests, bs4, json

s1 = 'https://market.yandex.ru/product--koltso-sokolov-iz-zolota-s-fianitom-019243/1784515300'
s2 = 'https://market.yandex.ru/product--zolotoe-koltso-diamant-online-280750-s-fianitom/1862489806'
s3 = 'https://market.yandex.ru/product--novaia-stantsiia-mini-umnaia-kolonka-s-alisoi/1423994419'
s4 = 'https://market.yandex.ru/product--redmi-note-13-pro-4g/52493593'

def parse_product(url=s1):
    product = {}
    req = requests.get(url)
    text = req.text
    soup = bs4.BeautifulSoup(text, 'lxml')
    container = soup.select('noframes[data-apiary="patch"]')
    for item in container:
        content = item.contents[0]
        if content.find('productCardJumpTableValues') != -1:
            json_data = json.loads(content)
            collections = json_data.get('collections')
            # for key in collections:
            #     print('+'*30)
            #     print(key)
            #     print(collections[key])
            params = collections.get('pageParams').get('current').get('params')
            product['name'] = params.get('slug')
            product['product_id'] = params.get('productId')
            productCardJumpTableValues = collections.get('productCardJumpTableValues')
            product['skuList'] = []
            a = None
            for key in productCardJumpTableValues:
                prod_title = productCardJumpTableValues[key].get('title')
                prod_data = productCardJumpTableValues[key].get('transition').get('params')
                product['skuList'].append((prod_data.get('skuId'), prod_title))
                if a is None: a = prod_data.get('additionalParams')[0].get('value')
            break

    product['uniqueId'] = a
    print(product)
    print(len(product['skuList']))

    # print(type(json_data))
    # for key in json_data:
    #     print('+'*30)
    #     print(key)
    #     print(json_data[key])


# parse_product()