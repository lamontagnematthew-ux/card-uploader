import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B7F/'
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)', ShippingProfileName='Under $20 - Free Shipping',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='B7', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
            'C:Material': 'Card Stock', 'C:Age Level': '6+', 'C:Autographed': 'No', 'C:Customized': 'No', 'C:Vintage': 'No', 'C:Graded': 'No'})
OPD = ('{d} from the One Piece Card Game set The Dominance of God (OP-18), English, Bandai. Condition: Near Mint, pack fresh. '
       'The photos are high-resolution scans of the exact card you will receive, front and back. Ships in a penny sleeve and toploader.')
PKD = ('{d} from Pokemon TCG: {s}. English, ungraded, Near Mint. The photos are high-resolution scans of the exact card you will receive '
       '(front and back). Ships in a penny sleeve and toploader.')
rows = []
def opr(f,t,p,q,name,num,rar,ct,fin,ch,lead):
    r = dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347759010','Title':t,'StartPrice':p,'Quantity':q,'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':OPD.format(d=lead),'C:Game':'One Piece Card Game','C:Card Type':ct,'C:Manufacturer':'Bandai','C:Franchise':'One Piece',
        'C:Country of Origin':'Japan','C:Finish':fin,'C:Card Name':name,'C:Character':ch,'C:Card Number':num,'C:Set':'The Dominance of God','C:Rarity':rar,'C:Year Manufactured':'2026'})
    rows.append(r)
def pkr(f,t,p,name,num,setx,rar,stage,hp,typ,ch,lead):
    r = dict(base); r.update({HDR[0]:'Add','StoreCategory':'42347963010','Title':t,'StartPrice':p,'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':PKD.format(d=lead,s=setx.replace('Me: ','')),'C:Game':'Pokémon TCG','C:Card Type':'Pokémon','C:Manufacturer':'The Pokémon Company',
        'C:Franchise':'Pokémon','C:Country of Origin':'United States','C:Finish':'Holo','C:Card Name':name,'C:Character':ch,'C:Card Number':num,
        'C:Set':setx,'C:Rarity':rar,'C:Stage':stage,'C:HP':hp,'C:Type':typ,'C:Year Manufactured':'2026'})
    rows.append(r)
opr('pell-op18-013','Pell OP18-013 Rare The Dominance of God One Piece Card Game NM','1.79','1','Pell','OP18-013','Rare','Character','Foil','Pell','Pell OP18-013 Rare (foil)')
opr('super-spot-billed-duck-troops-op18-009','Super Spot-Billed Duck Troops OP18-009 Rare Dominance of God One Piece TCG NM','1.79','2','Super Spot-Billed Duck Troops','OP18-009','Rare','Character','Foil','Super Spot-Billed Duck Troops','Super Spot-Billed Duck Troops OP18-009 Rare (foil)')
opr('don-card-say-that-you-want-to-live','DON!! Card Say That You Want to Live! Alt Art Dominance of God One Piece NM','1.79','1','DON!! Card','','DON!!','DON!!','Non-Foil','Monkey D. Luffy','DON!! Card ("Say That You Want to Live!" alternate art)')
pkr('gengar-ex-090-128','Gengar ex 090/128 Double Rare 30th Celebration Pokemon TCG NM','1.79','Gengar ex','090/128','Me: 30th Celebration','Double Rare','Stage 2','280','Darkness','Gengar','Gengar ex 090/128 Double Rare')
pkr('toxtricity-134-128','Toxtricity 134/128 Illustration Rare 30th Celebration Pokemon TCG NM','1.79','Toxtricity','134/128','Me: 30th Celebration','Illustration Rare','Stage 1','140','Lightning','Toxtricity','Toxtricity 134/128 Illustration Rare')
t='Darkrai & Cresselia LEGEND Top 99/102 Holo 30th Celebration Classic Collection NM'
if len(t)>80: t=t.replace(' Holo','')
pkr('darkrai-cresselia-legend-top-99-102',t,'13.09','Darkrai & Cresselia LEGEND','99/102','Me: 30th Celebration Classic Collection','Classic Collection','LEGEND','150','','Darkrai','Darkrai & Cresselia LEGEND (Top half) 99/102 Classic Collection')
for r in rows: assert len(r['Title']) <= 80, (len(r['Title']), r['Title'])
with open('uploads/b7-flatbed-add.csv','w',newline='',encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=HDR); w.writeheader()
    for r in rows: w.writerow({k: r.get(k,'') for k in HDR})
with open('uploads/b7-flatbed-qty.csv','w',encoding='utf-8') as fh:
    fh.write('Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8),ItemID,CustomLabel,Quantity\nRevise,920169721859,B2 B7,2\n')
for r in rows: print(r['StartPrice'], r['Quantity'], len(r['Title']), r['Title'])
