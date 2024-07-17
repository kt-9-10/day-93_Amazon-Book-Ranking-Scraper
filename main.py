import requests
from bs4 import BeautifulSoup
import pandas as pd


URL = "https://www.amazon.co.jp/gp/bestsellers/books/ref=zg_bs_pg_1_books?ie=UTF8&pg=1"

# スクレイピングデータの取得
response = requests.get(URL)
soup = BeautifulSoup(response.text, "html.parser")

# 書籍データの取得
book_list = soup.select("._cDEzb_iveVideoWrapper_JJ34T")

# 書籍のデータを格納するリスト
books_data = []

for book in book_list:
    # ランク
    rank = book.find('span').text.replace("#", "")

    # 書籍名
    title = book.select_one('span > div').get_text()

    # 著者
    author = None
    if book.select_one('div:nth-child(2) > a > div'):
        author = book.select_one('div:nth-child(2) > a > div').get_text()
    elif book.select_one('div:nth-child(2) > span > div'):
        author = book.select_one('div:nth-child(2) > span > div').get_text()

    # レビュースコア
    review_score = book.select_one('i > span').get_text().replace("5つ星のうち", "") if book.select_one('i > span') else None

    # レビュアー数
    reviewer_num = None
    if book.select_one('div:nth-child(3) > div > a > span'):
        reviewer_num = book.select_one('div:nth-child(3) > div > a > span').get_text()
    elif book.select_one('.a-icon-row  span:nth-child(2)'):
        reviewer_num = book.select_one('.a-icon-row  span:nth-child(2)').get_text()

    # 媒体形式
    book_type = None
    if book.select_one('div:nth-child(4) > span'):
        book_type = book.select_one('div:nth-child(4) > span').get_text()
    elif book.select_one('div:nth-child(3) > span'):
        book_type = book.select_one('div:nth-child(3) > span').get_text()

    # 価格
    price = book.select_one('.p13n-sc-price').get_text().replace("￥", "") if book.select_one('.p13n-sc-price') else None

    # 書籍のデータを辞書にまとめる
    book_data = {
        'Rank': rank,
        'Title': title,
        'Author': author,
        'Review Score': review_score,
        'Reviewer Numbers': reviewer_num,
        'Book Type': book_type,
        'Price': price
    }

    books_data.append(book_data)

# DataFrameに変換
df = pd.DataFrame(books_data)

# CSVファイルとして保存
df.to_csv('books_data.csv', index=False, encoding='utf-8')

print("CSVファイルが作成されました。")
