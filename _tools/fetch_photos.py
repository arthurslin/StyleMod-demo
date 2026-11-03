"""Download the chosen Unsplash photos to images/, record photographer credits, build a review sheet."""
import io, json, os, re, html, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding='utf-8')

PICKS = """crop-tee 1789110521321-5884d515be75 person-in-orange-crop-top-h0Tiqq98-kc
rib-tee 1521572163474-6864f9cf17ab man-wearing-white-crew-neck-t-shirts-WWesmHEgXDs
rib-tank 1598554793905-075f7b355cd9 woman-in-white-sleeveless-shirt-DeUmcgcf3is
train-tank 1714269083381-7c50384205ff a-woman-standing-in-front-of-a-machine-GdbqZVaUsqs
knit-polo 1625910513394-ea511bed44ca gray-polo-shirt-on-blue-textile-Y-00g_VgQTc
tech-tee 1574180566232-aaad1b5b8450 man-wearing-white-crew-neck-shirt-and-black-denim-jeans-with-hands-in-pocket-7WE1LbSc4zM
peplum 1627135200389-fe36dc74dac9 woman-in-white-long-sleeve-dress-standing-on-brown-field-during-daytime-CEnEmLHQgxw
crew-tee 1778671394516-8270eac13c42 a-plain-white-t-shirt-hangs-on-a-wooden-hanger-8ACmRoleM24
oxford 1774104363794-446a3a7e3812 a-smiling-man-with-a-beard-glasses-and-green-shirt-PfSBj1EpK0s
fine-knit 1629580626780-7fe7fb0523e9 woman-in-white-and-black-checkered-dress-shirt-KlkfFwXXbXc
camp-shirt 1605794432120-f4bb5dc9067d man-in-black-and-white-stripe-button-up-shirt-standing-beside-white-wall-caPZQg42c54
drape-top 1674384613407-43e021208955 a-woman-sitting-on-a-chair-wearing-a-white-shirt-S93BN-GJV4Y
crinkle-shirt 1793263145472-eab42964c52c woman-in-white-shirt-during-golden-hour-p0szCewNk80
over-tee 1661110546797-d86cc72a2765 a-woman-wearing-a-black-shirt-jeeVeM86xKw
pump-cover 1760998209708-5fc89d7983c0 young-woman-holding-a-basketball-with-a-pout-BRDiOWVhfyA
boxy-sweat 1661111015459-7a2314e6501f a-person-posing-for-a-picture-CwLFMmMq9gI
chunky-knit 1631541909061-71e349d1f203 a-sweater-hanging-on-a-hook-in-a-room-mavrg7cLwbA
big-shirt 1793203727651-2bcb2a7d70d9 woman-in-white-shirt-on-phone-TujD-uf5SSg
slim-chino 1584865288642-42078afe6942 man-in-white-t-shirt-and-black-pants-standing-on-white-floor-ylHcWlrMlzs
slim-jean 1714143164072-7646ef5cb24d a-pair-of-dark-blue-jeans-on-a-white-background-wNP79A-_bRY
cig-pant 1694447814836-c93ab70f7398 a-mannequin-wearing-a-black-shirt-and-pants-WNYmTVGVDhA
tapered-jog 1473966968600-fa801b869a1a man-wearing-brown-fitted-jeans-and-sneakers-standing-on-road-at-daytime-jC7nVH_Sw8k
flare-legging 1657130284737-cafb5d96b07c a-person-walking-on-a-dirt-path-a0NqxYoy5c0
str-jean 1598554747436-c9293d6a588f woman-in-white-tank-top-and-blue-denim-jeans-sitting-on-white-chair-2s3GhhJz2uY
str-pant 1789110854331-6d3cabfef781 person-wearing-red-linen-trousers-rTG-AwMj08o
track-pant 1711175017307-bbacf7c2ca13 a-person-standing-on-a-chain-on-top-of-a-mountain-tDmx86tPlqA
midi-skirt 1618244942912-7351be026e8b woman-in-white-tank-top-and-brown-skirt-standing-on-sidewalk-during-daytime-yy2BPHT8U94
maxi-skirt 1786641982679-7bbcddad7c2a woman-in-pink-shirt-and-skirt-V0CAxqlToZc
wide-pant 1687825515654-23620796760c a-woman-in-a-white-top-and-green-pants-moEtNGG8tM4
pleat-wide 1789110853466-4a541d4183a3 woman-in-white-top-and-culottes-qxXNndu5_Hc
cargo 1691407981600-62ebb537a0f2 a-man-standing-on-a-dirt-road-with-his-back-to-the-camera-NVKDAAf8L9w
parachute 1783012687000-26e994270984 a-persons-legs-in-black-baggy-pants-and-pink-shoes-7sA1agAJDhQ
wide-jean 1789111161072-766f7c6284cc woman-in-white-t-shirt-and-trousers-lTRj2ijTPAM
wide-sweat 1789110854262-ec66f0648ec7 person-in-sweatpants-and-crop-top-q7HfJHayc18
gym-short 1600878585887-c2b9530999a1 man-in-gray-tank-top-and-black-shorts-holding-black-dumbbell--DcG2kR5cPc
chunky-snk 1652370658121-cd0060db5fa9 a-persons-legs-and-shoes-13tGujgi4Rk
low-snk 1626379616459-b2ce1d9decbc person-wearing-white-nike-sneakers-DTZV8WDM1Ho
runner 1597892657493-6847b9640bac person-running-in-gray-asics-sneakers-A4579vLezz8
loafer 1661332445185-6e2ca6754fc4 a-couple-of-black-and-silver-pens-nBAqLLgMtqM
chelsea 1608629601270-a0007becead3 brown-and-white-suede-boots-miNo_SFAcws
strap-heel 1770757685000-c80e45122986 beige-strappy-heels-resting-on-a-white-surface-EiHNRle-oRM
blazer 1730715145729-bf929994c328 a-woman-standing-in-front-of-a-white-wall-sLvl6f-78-Y
power-blazer 1766951087359-fe48ea4f2796 woman-in-oversized-blazer-against-a-spotlighted-wall-LLKu9dGnXKE
chore 1700059425529-411240553003 a-man-standing-in-front-of-a-stone-wall-aXA9ql1n1kE
track-top 1768983953826-231e8ef0b6dc woman-in-blue-track-jacket-with-red-stripes-stands-outside-AlHkVtAQHdE
trench 1633821879282-0c4e91f96232 a-woman-in-a-trench-coat-posing-for-a-picture-5vrque5NVHI
crop-puffer 1609241824968-2780ccc069e6 woman-in-black-jacket-standing-near-black-wall-EJhY8XOi0qM
crossbody 1620786514684-ff35b5aae55e black-sling-bag-on-white-surface-LW2iqpHzr8Y
tote 1732963947955-858ad7d5e540 a-bag-sitting-on-top-of-a-white-chair-next-to-a-plant-6Rh4vvSaiSg
scarf 1789845137280-8fd8eee7e691 plaid-wool-blanket-on-rack-tYVIPf0wN1s
cap 1588850561407-ed78c282e89b white-baseball-cap-on-white-surface-t8HiP3e5abg
beanie 1510598969022-c4c6c5d05769 woman-wearing-green-knit-cap-and-blue-denim-jacket-Lprffwrv9cY"""

UA = {'User-Agent': 'Mozilla/5.0 (StyleMod demo)'}
os.makedirs('images', exist_ok=True)

def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return r.read()

def work(line):
    sid, photo, slug = line.split()
    img = get(f'https://images.unsplash.com/photo-{photo}?w=520&h=650&fit=crop&crop=entropy&fm=jpg&q=70')
    Image.open(io.BytesIO(img)).verify()
    open(f'images/{sid}.jpg', 'wb').write(img)
    page = f'https://unsplash.com/photos/{slug}'
    try:
        title = html.unescape(re.search(r'<title[^>]*>(.*?)</title>', get(page).decode('utf-8', 'replace'), re.S).group(1))
        m = re.search(r'[Pp]hoto by (.+?) on Unsplash', title) or re.search(r'by (.+?) \| Unsplash', title)
        who = m.group(1).strip() if m else ''
    except Exception as e:
        who = ''
    return sid, {'page': page, 'by': who}

with ThreadPoolExecutor(5) as ex:
    res = dict(ex.map(work, PICKS.splitlines()))
json.dump(res, open('_tools/credits.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(sum(1 for v in res.values() if v['by']), 'credited of', len(res))
print([k for k, v in res.items() if not v['by']])

W, H = 150, 205
ids = list(res)
sheet = Image.new('RGB', (W * 9, H * ((len(ids) + 8) // 9)), 'white')
d = ImageDraw.Draw(sheet)
for n, sid in enumerate(ids):
    im = Image.open(f'images/{sid}.jpg'); im.thumbnail((W - 4, H - 16))
    x, y = n % 9 * W, n // 9 * H
    sheet.paste(im, (x + 2, y + 14)); d.text((x + 2, y + 1), sid, fill='red')
sheet.save('_tools/review.jpg', quality=85)
