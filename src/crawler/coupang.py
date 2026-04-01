import requests
import json
import os
from bs4 import BeautifulSoup
from datetime import datetime
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

def get_product_price(product_url: str, product_name: str) -> dict:
    """
    쿠팡 상품 URL에서 가격을 크롤링하는 함수
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(product_url, headers=headers)
        print(response.status_code)  # 200이면 접속 성공
        print(response.text[:500])   # HTML 앞부분 확인
        soup = BeautifulSoup(response.text, 'html.parser')

        # 가격 파싱
        price_element = soup.select_one('span.total-price > strong')
        
        if price_element:
            price = int(price_element.text.strip().replace(',', ''))
        else:
            price = None

        return {
            'product_name': product_name,
            'price': price,
            'url': product_url,
            'collected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        print(f"크롤링 실패 : {e}")
        return None


# 수집할 생필품 목록
PRODUCTS = [
    {
        'name': '신라면 멀티팩',
        'url': 'https://www.coupang.com/vp/products/7958974?itemId=1035120754&vendorItemId=3000987832&q=%EC%8B%A0%EB%9D%BC%EB%A9%B4&searchId=0f80ff5c4925011&sourceType=search&itemsCount=36&searchRank=3&rank=3&traceId=mnfs7eiw'
    },
    {
        'name': '3겹 화장지',
        'url': 'https://www.coupang.com/vp/products/307020051?itemId=19395560867&vendorItemId=5375349551&q=%ED%99%94%EC%9E%A5%EC%A7%80&searchId=6396ea2c4724504&sourceType=search&itemsCount=36&searchRank=7&rank=7&traceId=mnfs8a31'
    },
]


if __name__ == '__main__':
    results = []
    for product in PRODUCTS:
        result = get_product_price(product['url'], product['name'])
        if result:
            results.append(result)
            print(f"✅ {result['product_name']} : {result['price']}원")
        else:
            print(f"❌ {product['name']} 크롤링 실패")

    print(json.dumps(results, ensure_ascii=False, indent=2))