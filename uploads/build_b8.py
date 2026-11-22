import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B8F/'
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='B8', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
            'C:Material': 'Card Stock', 'C:Age Level': '6+', 'C:Autographed': 'No', 'C:Customized': 'No', 'C:Vintage': 'No', 'C:Graded': 'No'})
PKD = ('{d} from Pokemon TCG: {s}. English, ungraded, Near Mint. The photos are high-resolution scans of the exact card you will receive '
       '(front and back). Ships in a penny sleeve and toploader.')
C='Me: 30th Celebration'; CC='Me: 30th Celebration Classic Collection'
cards = [
 ('mewtwo-ex-064-128','Mewtwo ex','064/128',C,'Double Rare','Basic','230','Psychic','1.79','Mewtwo'),
 ('scraggy-140-128','Scraggy','140/128',C,'Illustration Rare','Basic','80','Darkness','1.79','Scraggy'),
 ('scizor-ex-108-115-classic','Scizor ex','108/115',CC,'Classic Collection','Stage 1','120','Metal','7.19','Scizor'),
 ('chandelure-137-128','Chandelure','137/128',C,'Illustration Rare','Stage 2','140','','1.79','Chandelure'),
 ('pikachu-ex-149-128','Pikachu ex','149/128',C,'Special Illustration Rare','Basic','190','Lightning','33.09','Pikachu'),
 ('umbreon-ex-092-128','Umbreon ex','092/128',C,'Double Rare','Stage 1','270','Darkness','1.79','Umbreon'),
 ('kommo-o-143-128','Kommo-o','143/128',C,'Illustration Rare','Stage 2','180','','1.79','Kommo-o'),
]
rows=[]
for f,name,num,setx,rar,stage,hp,typ,price,ch in cards:
    sname=setx.replace('Me: ','')
    t = f'{name} {num} Holo 30th Celebration Classic Collection Pokemon NM' if setx==CC else f'{name} {num} {rar} 30th Celebration Pokemon TCG NM'
    r=dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347963010','Title':t,'StartPrice':price,'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':PKD.format(d=f'{name} {num} {rar}',s=sname),
        'ShippingProfileName':'$20+ and Slabs - $5.99 Ground Advantage' if float(price)>=20 else 'Under $20 - Free Shipping',
        'C:Game':'Pokémon TCG','C:Card Type':'Pokémon','C:Manufacturer':'The Pokémon Company','C:Franchise':'Pokémon','C:Country of Origin':'United States',
        'C:Finish':'Holo','C:Card Name':name,'C:Character':ch,'C:Card Number':num,'C:Set':setx,'C:Rarity':rar,'C:Stage':stage,'C:HP':hp,'C:Type':typ,'C:Year Manufactured':'2026'})
    rows.append(r)
for r in rows: assert len(r['Title'])<=80, r['Title']
with open('uploads/b8-flatbed-add.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=HDR); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,'') for k in HDR})
with open('uploads/b8-flatbed-qty.csv','w',encoding='utf-8') as fh:
    fh.write('Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8),ItemID,CustomLabel,Quantity\nRevise,920154675515,A10 B11 B8,3\nRevise,920119222816,B8 B9 D9,4\n')
for r in rows: print(r['StartPrice'], len(r['Title']), r['Title'])
