import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B9F/'
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='B9', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
            'C:Material': 'Card Stock', 'C:Age Level': '6+', 'C:Autographed': 'No', 'C:Customized': 'No', 'C:Vintage': 'No', 'C:Graded': 'No'})
PKD = ('{d} from Pokemon TCG: {s}. English, ungraded, Near Mint. The photos are high-resolution scans of the exact card you will receive '
       '(front and back). Ships in a penny sleeve and toploader.')
C='Me: 30th Celebration'; CC='Me: 30th Celebration Classic Collection'
cards = [
 ('solgaleo-gx-89-149-classic','Solgaleo GX','89/149',CC,'Classic Collection','Stage 2','250','Metal','5.29','Solgaleo','1'),
 ('pikachu-ex-054-128','Pikachu ex','054/128',C,'Double Rare','Basic','190','Lightning','1.79','Pikachu','1'),
 ('drifloon-136-128','Drifloon','136/128',C,'Illustration Rare','Basic','70','Psychic','1.89','Drifloon','1'),
 ('pikachu-032-128','Pikachu','032/128',C,'Pikachu Rare','Basic','50','Lightning','1.79','Pikachu','2'),
]
rows=[]
for f,name,num,setx,rar,stage,hp,typ,price,ch,qty in cards:
    sname=setx.replace('Me: ','')
    t = f'{name} {num} Holo 30th Celebration Classic Collection Pokemon NM' if setx==CC else (f'{name} {num} {rar} 10/30 Holo 30th Celebration Pokemon TCG NM' if rar=='Pikachu Rare' else f'{name} {num} {rar} 30th Celebration Pokemon TCG NM')
    r=dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347963010','Title':t,'StartPrice':price,'Quantity':qty,'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':PKD.format(d=f'{name} {num} {rar}'+(' (10/30 Pikachu stamp)' if rar=='Pikachu Rare' else ''),s=sname),
        'ShippingProfileName':'$20+ and Slabs - $5.99 Ground Advantage' if float(price)>=20 else 'Under $20 - Free Shipping',
        'C:Game':'Pokémon TCG','C:Card Type':'Pokémon','C:Manufacturer':'The Pokémon Company','C:Franchise':'Pokémon','C:Country of Origin':'United States',
        'C:Finish':'Holo','C:Card Name':name,'C:Character':ch,'C:Card Number':num,'C:Set':setx,'C:Rarity':rar,'C:Stage':stage,'C:HP':hp,'C:Type':typ,'C:Year Manufactured':'2026'})
    rows.append(r)
for r in rows: assert len(r['Title'])<=80, r['Title']
with open('uploads/b9-flatbed-add.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=HDR); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,'') for k in HDR})
with open('uploads/b9-flatbed-qty.csv','w',encoding='utf-8') as fh:
    fh.write('Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8),ItemID,CustomLabel,Quantity\nRevise,920123855727,B10 B11 B9,4\nRevise,920119222809,B8 B9 D4 A12,4\nRevise,920119200292,B7 B8 B9 D4 D9,4\n')
for r in rows: print(r['StartPrice'], r['Quantity'], len(r['Title']), r['Title'])
