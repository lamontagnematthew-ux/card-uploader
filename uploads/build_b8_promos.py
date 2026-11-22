import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B8F/'
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI', PostalCode='48079',
            ReturnProfileName='No Return Accepted (274946871012)', PaymentProfileName='eBay Managed Payments (274946873012) Copy',
            ShippingProfileName='$20+ and Slabs - $5.99 Ground Advantage', BestOfferEnabled='0', PackageLength='11', PackageWidth='6',
            PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1', CustomLabel='B8', StoreCategory='42347963010',
            **{'CD:Card Condition - (ID: 40001)':'400010','C:Language':'English','C:Card Size':'Standard','C:Material':'Card Stock','C:Age Level':'6+',
               'C:Autographed':'No','C:Customized':'No','C:Vintage':'No','C:Graded':'No','C:Game':'Pokémon TCG','C:Card Type':'Pokémon',
               'C:Manufacturer':'The Pokémon Company','C:Franchise':'Pokémon','C:Country of Origin':'United States','C:Finish':'Holo',
               'C:Set':'Me: Mega Evolution Promo','C:Rarity':'Promo','C:Year Manufactured':'2026'})
rows=[]
for f,name,num,price,stage,hp,typ,ch in [('pikachu-ex-109-promo-sealed','Pikachu ex','109','22.89','Basic','190','Lightning','Pikachu'),
                                         ('umbreon-ex-110-promo-sealed','Umbreon ex','110','60.89','Stage 1','270','Darkness','Umbreon')]:
    r=dict(base); r.update({HDR[0]:'Add','Title':f'{name} {num} Promo MEP 30th Celebration Sealed Pokemon TCG NM','StartPrice':price,
        'PicURL':URL+f+'-front.jpg|'+URL+f+'-back.jpg',
        'Description':f'{name} {num} 30th Celebration Black Star Promo (MEP {num}) from Pokemon TCG: Mega Evolution Promos. English, ungraded, still sealed in the original promo wrapper. The photos show the exact card you will receive (front and back). Ships in a toploader.',
        'C:Card Name':name,'C:Character':ch,'C:Card Number':num,'C:Stage':stage,'C:HP':hp,'C:Type':typ})
    rows.append(r)
with open('uploads/b8-promos-add.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.DictWriter(fh,fieldnames=HDR); w.writeheader()
    for r in rows: w.writerow({k:r.get(k,'') for k in HDR})
for r in rows: print(r['StartPrice'],len(r['Title']),r['Title'])
