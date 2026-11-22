import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B5F/'
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='B5', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
            'C:Material': 'Card Stock', 'C:Age Level': '6+', 'C:Autographed': 'No', 'C:Customized': 'No', 'C:Vintage': 'No', 'C:Graded': 'No'})
ship = lambda p: '$20+ and Slabs - $5.99 Ground Advantage' if float(p) >= 20 else 'Under $20 - Free Shipping'
# file, name, number, eBay set, title, rarity, stage, hp, type, illus, price, character, store cat
poke = [
 ('alolan-exeggutor-129-128','Alolan Exeggutor','129/128','Me: 30th Celebration','Alolan Exeggutor 129/128 Illustration Rare 30th Celebration Pokemon TCG NM','Illustration Rare','Stage 1','150','Grass','','1.79','Exeggutor'),
 ('pikachu-ex-150-128','Pikachu ex','150/128','Me: 30th Celebration','Pikachu ex 150/128 Special Illustration Rare 30th Celebration Pokemon TCG NM','Special Illustration Rare','Basic','190','Lightning','','37.89','Pikachu'),
 ('lugia-149-147-classic','Lugia','149/147','Me: 30th Celebration Classic Collection','Lugia 149/147 Holo 30th Celebration Classic Collection Pokemon NM','Classic Collection','Basic','80','','','112.29','Lugia'),
 ('pikachu-zekrom-gx-33-181-classic','Pikachu & Zekrom GX','33/181','Me: 30th Celebration Classic Collection','Pikachu & Zekrom GX 33/181 Holo 30th Celebration Classic Collection Pokemon NM','Classic Collection','Basic','240','Lightning','','19.39','Pikachu'),
 ('greninja-break-41-122-classic','Greninja BREAK','41/122','Me: 30th Celebration Classic Collection','Greninja BREAK 41/122 Holo 30th Celebration Classic Collection Pokemon NM','Classic Collection','BREAK','170','Water','5ban Graphics','6.49','Greninja'),
]
op = [
 ('monkey-d-luffy-op18-118','Monkey.D.Luffy','OP18-118','Secret Rare','Character','12.39','Monkey D. Luffy'),
 ('franky-op18-034','Franky','OP18-034','Super Rare','Character','1.79','Franky'),
 ('mr1-miss-doublefinger-op18-048','Mr.1 & Miss Doublefinger','OP18-048','Super Rare','Character','1.79','Mr. 1'),
]
rows = []
for f,name,num,setx,title,rar,stage,hp,typ,ill,price,char in poke:
    setname = setx.replace('Me: ','')
    r = dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347963010','Title':title,'StartPrice':price,
        'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':f'{name} {num} {rar} from Pokemon TCG: {setname}. English, ungraded, Near Mint. The photos are high-resolution scans of the exact card you will receive (front and back). Ships in a penny sleeve and toploader.',
        'ShippingProfileName':ship(price),'C:Game':'Pokémon TCG','C:Card Type':'Pokémon','C:Manufacturer':'The Pokémon Company',
        'C:Franchise':'Pokémon','C:Country of Origin':'United States','C:Finish':'Holo','C:Card Name':name,'C:Character':char,
        'C:Card Number':num,'C:Set':setx,'C:Rarity':rar,'C:Stage':stage,'C:HP':hp,'C:Type':typ,'C:Illustrator':ill,'C:Year Manufactured':'2026'})
    rows.append(r)
for f,name,num,rar,ctype,price,char in op:
    t = f'{name} {num} {rar} The Dominance of God One Piece Card Game NM'
    if len(t) > 80: t = t.replace('One Piece Card Game','One Piece TCG')
    if len(t) > 80: t = t.replace('Super Rare','SR')
    r = dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347759010','Title':t,'StartPrice':price,
        'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':f'{name} {num} {rar} (foil) from the One Piece Card Game set The Dominance of God (OP-18), English, Bandai. Condition: Near Mint, pack fresh. The photos are high-resolution scans of the exact card you will receive, front and back. Ships in a penny sleeve and toploader.',
        'ShippingProfileName':ship(price),'C:Game':'One Piece Card Game','C:Card Type':ctype,'C:Manufacturer':'Bandai','C:Franchise':'One Piece',
        'C:Country of Origin':'Japan','C:Finish':'Foil','C:Card Name':name,'C:Character':char,'C:Card Number':num,
        'C:Set':'The Dominance of God','C:Rarity':rar,'C:Year Manufactured':'2026'})
    rows.append(r)
for r in rows: assert len(r['Title']) <= 80, r['Title']
with open('uploads/b5-flatbed-add.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=HDR); w.writeheader()
    for r in rows: w.writerow({k: r.get(k,'') for k in HDR})
with open('uploads/b5-flatbed-qty.csv','w',encoding='utf-8') as fh:
    fh.write('Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8),ItemID,CustomLabel,Quantity\nRevise,920169721860,B2 B5,2\n')
for r in rows: print(r['StartPrice'], len(r['Title']), r['ShippingProfileName'][:6], r['Title'])
