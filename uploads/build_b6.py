import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B6F/'
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)', ShippingProfileName='Under $20 - Free Shipping',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='B6', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
            'C:Material': 'Card Stock', 'C:Age Level': '6+', 'C:Autographed': 'No', 'C:Customized': 'No', 'C:Vintage': 'No', 'C:Graded': 'No'})
OPD = ('{d} from the One Piece Card Game set The Dominance of God (OP-18), English, Bandai. Condition: Near Mint, pack fresh. '
       'The photos are high-resolution scans of the exact card you will receive, front and back. Ships in a penny sleeve and toploader.')
# file, title, price, card name, number, rarity, card type, finish, character, desc lead
op = [
 ('don-card-dp13-saint-gunko','DON!! Card Saint Gunko Double Pack Set Vol. 13 Dominance of God One Piece NM','5.29','DON!! Card','','DON!!','DON!!','Non-Foil','Saint Gunko','DON!! Card (Saint Gunko) from the Double Pack Set Vol. 13 (DP-13)'),
 ('sleeptids-op18-093-vision','Sleeptids OP18-093 Rare These Things Are a Vision Dominance of God One Piece NM','1.79','Sleeptids','OP18-093','Rare','Character','Foil','Sleeptids','Sleeptids OP18-093 Rare ("These Things Are a Vision of the World..." version, foil)'),
 ('sleeptids-op18-093-terrifies','Sleeptids OP18-093 Rare Terrifies Children Most Dominance of God One Piece NM','1.79','Sleeptids','OP18-093','Rare','Character','Foil','Sleeptids','Sleeptids OP18-093 Rare ("...That Terrifies the Children Most!!!" version, foil)'),
 ('can-you-please-sail-op18-074','Can You Please Sail on the Ship I Made?! OP18-074 Rare One Piece TCG NM','1.79','Can You Please Sail on the Ship I Made?!','OP18-074','Rare','Event','Foil','Franky','Can You Please Sail on the Ship I Made?! OP18-074 Rare (foil)'),
 ('franky-leader-op18-021','Franky OP18-021 Leader The Dominance of God One Piece Card Game NM','1.79','Franky','OP18-021','Leader','Leader','Non-Foil','Franky','Franky OP18-021 Leader (non-foil)'),
]
rows = []
for f,t,p,name,num,rar,ct,fin,ch,lead in op:
    r = dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347759010','Title':t,'StartPrice':p,'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':OPD.format(d=lead),'C:Game':'One Piece Card Game','C:Card Type':ct,'C:Manufacturer':'Bandai','C:Franchise':'One Piece',
        'C:Country of Origin':'Japan','C:Finish':fin,'C:Card Name':name,'C:Character':ch,'C:Card Number':num,'C:Set':'The Dominance of God','C:Rarity':rar,'C:Year Manufactured':'2026'})
    rows.append(r)
f='pikachu-037-128'
r = dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347963010','Title':'Pikachu 037/128 Pikachu Rare 30th Celebration Pokemon TCG NM','StartPrice':'1.79',
    'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
    'Description':'Pikachu 037/128 Pikachu Rare (15/30 Pikachu stamp) from Pokemon TCG: 30th Celebration. English, ungraded, Near Mint. The photos are high-resolution scans of the exact card you will receive (front and back). Ships in a penny sleeve and toploader.',
    'C:Game':'Pokémon TCG','C:Card Type':'Pokémon','C:Manufacturer':'The Pokémon Company','C:Franchise':'Pokémon','C:Country of Origin':'United States',
    'C:Finish':'Holo','C:Card Name':'Pikachu','C:Character':'Pikachu','C:Card Number':'037/128','C:Set':'Me: 30th Celebration','C:Rarity':'Pikachu Rare',
    'C:Stage':'Basic','C:HP':'70','C:Type':'Lightning','C:Year Manufactured':'2026'})
rows.append(r)
for r in rows: assert len(r['Title']) <= 80, (len(r['Title']), r['Title'])
with open('uploads/b6-flatbed-add.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=HDR); w.writeheader()
    for r in rows: w.writerow({k: r.get(k,'') for k in HDR})
with open('uploads/b6-flatbed-qty.csv','w',encoding='utf-8') as fh:
    fh.write('Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8),ItemID,CustomLabel,Quantity\n'
             'Revise,920169721851,B2 B6,2\nRevise,920169754138,B4 B6,2\nRevise,920169754136,B4 B6,2\n')
for r in rows: print(r['StartPrice'], len(r['Title']), r['Title'])
