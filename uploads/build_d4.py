import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/D4F/'
POKE_DESC = ('{name} {num} {rar} from Pokemon TCG: {setname}. English, ungraded, Near Mint. The photos are high-resolution '
             'scans of the exact card you will receive (front and back). Ships in a penny sleeve and toploader.')
OP_DESC = ('{name} {num} {rar} ({fin}) from the One Piece Card Game set The Dominance of God (OP-18), English, Bandai. '
           'Condition: Near Mint, pack fresh. The photos are high-resolution scans of the exact card you will receive, '
           'front and back. Ships in a penny sleeve and toploader.')

poke = []
op = [
    ('iceburg-op18-061', 'Iceburg', 'OP18-061', 'Super Rare', 'Super Rare', 'Character', 'Foil', '1.79', 'Iceburg'),
    ('mr2-bon-kurei-bentham-op18-049', 'Mr.2.Bon.Kurei(Bentham)', 'OP18-049', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Bentham'),
    ('ill-make-the-call-op18-096', "I'll Make the Call", 'OP18-096', 'Rare', 'Rare', 'Event', 'Foil', '1.79', 'Celestial Dragons'),
    ('mr3-miss-goldenweek-op18-050', 'Mr.3 & Miss.Goldenweek', 'OP18-050', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Mr. 3'),
    ('sleeptids-op18-093', 'Sleeptids', 'OP18-093', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Sleeptids'),
    ('i-pray-for-your-success-op18-059', 'I Pray For Your Success.', 'OP18-059', 'Rare', 'Rare', 'Event', 'Foil', '1.79', 'Crocodile'),
    ('zoro-sogeking-op18-027', 'Zoro & Sogeking', 'OP18-027', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Roronoa Zoro'),
    ('karoo-op18-004', 'Karoo', 'OP18-004', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Karoo'),
    ('ms-all-sunday-op18-041', 'Ms. All Sunday', 'OP18-041', 'Leader', 'Leader', 'Leader', 'Non-Foil', '1.79', 'Nico Robin'),
]
rows = []
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='D4', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
            'C:Material': 'Card Stock', 'C:Age Level': '6+', 'C:Autographed': 'No', 'C:Customized': 'No', 'C:Vintage': 'No', 'C:Graded': 'No'})
for f, name, num, setx, setname, rar, stage, hp, typ, ill, yr, fin, char in poke:
    r = dict(base); r.update({HDR[0]: 'Add', 'StoreCategory': '42347961010',
        'Title': f'{name} {num} {rar} {setname} Pokemon TCG NM', 'StartPrice': '1.79',
        'PicURL': URL + f + '-front.jpg|' + URL + f + '-back.jpg',
        'Description': POKE_DESC.format(name=name, num=num, rar=rar, setname=setname),
        'ShippingProfileName': 'Under $20 - Free Shipping',
        'C:Game': 'Pokémon TCG', 'C:Card Type': 'Pokémon', 'C:Manufacturer': 'The Pokémon Company', 'C:Franchise': 'Pokémon',
        'C:Country of Origin': 'United States', 'C:Finish': fin, 'C:Card Name': name, 'C:Character': char, 'C:Card Number': num,
        'C:Set': setx, 'C:Rarity': rar, 'C:Stage': stage, 'C:HP': hp, 'C:Type': typ, 'C:Illustrator': ill, 'C:Year Manufactured': yr})
    rows.append(r)
for f, name, num, rart, rar, ctype, fin, price, char in op:
    r = dict(base); r.update({HDR[0]: 'Add', 'StoreCategory': '42347759010',
        'Title': f'{name} {num} {rart} The Dominance of God One Piece Card Game NM', 'StartPrice': price,
        'PicURL': URL + f + '-front.jpg|' + URL + f + '-back.jpg',
        'Description': OP_DESC.format(name=name, num=num, rar=rar, fin=fin.lower()),
        'ShippingProfileName': '$20+ and Slabs - $5.99 Ground Advantage' if float(price) >= 20 else 'Under $20 - Free Shipping',
        'C:Game': 'One Piece Card Game', 'C:Card Type': ctype, 'C:Manufacturer': 'Bandai', 'C:Franchise': 'One Piece',
        'C:Country of Origin': 'Japan', 'C:Finish': fin, 'C:Card Name': name, 'C:Character': char, 'C:Card Number': num,
        'C:Set': 'The Dominance of God', 'C:Rarity': rar, 'C:Year Manufactured': '2026'})
    rows.append(r)
for r in rows:
    if len(r['Title'])>80: r['Title']=r['Title'].replace('One Piece Card Game','One Piece TCG')
    assert len(r['Title']) <= 80, r['Title']
with open('uploads/d4-flatbed-add.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=HDR, extrasaction='raise'); w.writeheader()
    for r in rows: w.writerow({k: r.get(k, '') for k in HDR})
for r in rows: print(r['StartPrice'], len(r['Title']), r['Title'])
