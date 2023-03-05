import requests
from bs4 import BeautifulSoup
import pandas as pd

reviewList = []

headers = {
    'User-Agent': 'My User Agent 1.0',
    'From': 'youremail@domain.example'  # This is another valid field
}

links = [
    'https://www.amazon.com/Electric-Skateboard-Longboard-Hub-Motor-Adjustment/product-reviews/B08R8P471F/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='
    ]
'''
    'https://www.amazon.com/Magneto-Kicktail-Cruiser-Longboard-Skateboard/product-reviews/B07T3BS4MX/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/MEKETEC-Skateboards-Complete-Skateboard-Beginners/product-reviews/B074XTJ75S/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/KPC-Pro-Skateboard-Complete-Heartagram/product-reviews/B004UOL6JG/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='
    'https://www.amazon.com/Atom-Longboards-All-Terrain-Longboard-Woody/product-reviews/B01IP5VQBI/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='
    'https://www.amazon.com/Skitch-Complete-Skateboards-Beginners-Skateboard/product-reviews/B01FYVC2BY/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/WOOKRAYS-Electric-Skateboard-Skateboard-Adjustment/product-reviews/B08BNS3GKB/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Xtreme-Professional-Complete-Longboard-Skateboard/product-reviews/B019ZFWQDO/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Teamgee-Electric-Skateboard-Adjustment-Longboard/product-reviews/B08LZHWX95/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/teamgee-Electric-Skateboard-Longboard-Wireless/product-reviews/B07GGTR2X6/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/BLITZART-Skateboard-Longboard-Skateboard-Electronic/product-reviews/B078HM367M/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Swagtron-Swagskate-Skateboard-Kick-Assist-Move-More/product-reviews/B07TGFBJGK/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=','https://www.amazon.com/Razor-E100-Glow-Electric-Scooter/product-reviews/B00KCK55IU/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Razor-Miniature-Euro-Style-Electric-Scooter/product-reviews/B000I44P90/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Scooters-Non-Electric-Foldable-Adjustable-Anti-Slip/product-reviews/B0934Q87SZ/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Hurtle-3-Wheeled-Scooter-Lean-Steer/product-reviews/B07VY9Q95Q/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/Ninebot-Electric-Long-range-Foldable-Portable/product-reviews/B07WYXXL4V/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=',
    'https://www.amazon.com/6KU-Scooter-Adjustable-Flashing-Children/product-reviews/B07BFXLF3G/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber='
]
'''

def get_soup(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            text = item.find('span', {'data-hook': 'review-body'}).text.strip()
            text = text.replace("The media could not be loaded.", " ")
            text = text.strip()

            review = {
                'text': text
            }
            reviewList.append(review)
    except:
        pass


def get_link(link):
    for i in range(1, 999):
        string = f'{link}{i}'
        soup = get_soup(string)
        get_reviews(soup)
        print(len(reviewList))
        if soup.find('li', {'class': 'a-disabled a-last'}):
            break


for page in links:
    get_link(page)

df = pd.DataFrame(reviewList)
df.to_csv('AmazonReviews.csv', index=False)
print('Fin.')
