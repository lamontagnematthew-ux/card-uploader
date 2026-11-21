import csv
HDR = open('uploads/b11-add.csv', encoding='utf-8').readline().strip().split(',')
URL = 'https://raw.githubusercontent.com/lamontagnematthew-ux/card-uploader/main/photos/B2F/'
POKE_DESC = ('{name} {num} {rar} from Pokemon TCG: {setname}. English, ungraded, Near Mint. The photos are high-resolution '
             'scans of the exact card you will receive (front and back). Ships in a penny sleeve and toploader.')
OP_DESC = ('{name} {num} {rar} ({fin}) from the One Piece Card Game set The Dominance of God (OP-18), English, Bandai. '
           'Condition: Near Mint, pack fresh. The photos are high-resolution scans of the exact card you will receive, '
           'front and back. Ships in a penny sleeve and toploader.')

# file, name, number, set(eBay), setname(title), rarity, stage, hp, type, illus, year, finish
poke = [
    ('beedrill-ex-003-086', 'Beedrill ex', '003/086', 'Me04: Chaos Rising', 'Chaos Rising', 'Double Rare', 'Stage 2', '310', 'Grass', 'toriyufu', '2026', 'Holo', 'Beedrill'),
    ('mega-floette-ex-035-086', 'Mega Floette ex', '035/086', 'Me04: Chaos Rising', 'Chaos Rising', 'Double Rare', 'Basic', '250', 'Psychic', 'aky CG Works', '2026', 'Holo', 'Floette'),
    ('ambipom-107-094', 'Ambipom', '107/094', 'Me02: Phantasmal Flames', 'Phantasmal Flames', 'Illustration Rare', 'Stage 1', '110', 'Colorless', 'Shigenori Negishi', '2025', 'Holo', 'Ambipom'),
    ('doublade-098-088', 'Doublade', '098/088', 'Me03: Perfect Order', 'Perfect Order', 'Illustration Rare', 'Stage 1', '100', 'Metal', 'Anesaki Dynamic', '2026', 'Holo', 'Doublade'),
    ('mega-gengar-ex-056-094', 'Mega Gengar ex', '056/094', 'Me02: Phantasmal Flames', 'Phantasmal Flames', 'Double Rare', 'Stage 2', '350', 'Darkness', '5ban Graphics', '2025', 'Holo', 'Gengar'),
    ('empoleon-ex-114-094', 'Empoleon ex', '114/094', 'Me02: Phantasmal Flames', 'Phantasmal Flames', 'Ultra Rare', 'Stage 2', '320', 'Metal', '5ban Graphics', '2025', 'Holo', 'Empoleon'),
]
# file, name, number, rarity(title), rarity(spec), card type, finish, price, character
op = [
    ('tony-tony-chopper-op18-029', 'Tony Tony.Chopper', 'OP18-029', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Tony Tony Chopper'),
    ('kaku-op18-099', 'Kaku', 'OP18-099', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Kaku'),
    ('saint-sommers-op18-088', 'Saint Sommers', 'OP18-088', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Saint Sommers'),
    ('karoo-op18-001', 'Karoo', 'OP18-001', 'Leader', 'Leader', 'Leader', 'Non-Foil', '1.79', 'Karoo'),
    ('spandam-op18-105', 'Spandam', 'OP18-105', 'Rare', 'Rare', 'Character', 'Foil', '1.79', 'Spandam'),
    ('monkey-d-luffy-op18-022', 'Monkey.D.Luffy', 'OP18-022', 'Leader', 'Leader', 'Leader', 'Non-Foil', '1.79', 'Monkey D. Luffy'),
    ('gum-gum-giant-axe-op18-039', 'Gum-Gum Giant Axe', 'OP18-039', 'Rare', 'Rare', 'Event', 'Foil', '1.79', 'Monkey D. Luffy'),
    ('saint-shamrock-op18-119', 'Saint Shamrock', 'OP18-119', 'Secret Rare', 'Secret Rare', 'Character', 'Foil', '32.89', 'Saint Shamrock'),
]
rows = []
base = dict(Category='183454', ConditionID='4000', Format='FixedPrice', Duration='GTC', Location='Saint Clair, MI',
            PostalCode='48079', ReturnProfileName='No Return Accepted (274946871012)',
            PaymentProfileName='eBay Managed Payments (274946873012) Copy', BestOfferEnabled='0',
            PackageLength='11', PackageWidth='6', PackageDepth='1', WeightMajor='0', WeightMinor='1', Quantity='1',
            CustomLabel='B2', **{'CD:Card Condition - (ID: 40001)': '400010', 'C:Language': 'English', 'C:Card Size': 'Standard',
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
# DON!! card from the DP-13 double pack
f = 'don-card-dp13-luffy'
r = dict(base); r.update({HDR[0]: 'Add', 'StoreCategory': '42347759010',
    'Title': 'DON!! Card Monkey.D.Luffy Double Pack Set Vol. 13 Dominance of God One Piece NM', 'StartPrice': '2.99',
    'PicURL': URL + f + '-front.jpg|' + URL + f + '-back.jpg',
    'Description': ('DON!! Card (Monkey.D.Luffy) from the One Piece Card Game Double Pack Set Vol. 13 (DP-13), '
                    'The Dominance of God, English, Bandai. Condition: Near Mint, pack fresh. The photos are high-resolution '
                    'scans of the exact card you will receive, front and back. Ships in a penny sleeve and toploader.'),
    'ShippingProfileName': 'Under $20 - Free Shipping',
    'C:Game': 'One Piece Card Game', 'C:Card Type': 'DON!!', 'C:Manufacturer': 'Bandai', 'C:Franchise': 'One Piece',
    'C:Country of Origin': 'Japan', 'C:Finish': 'Non-Foil', 'C:Card Name': 'DON!! Card', 'C:Character': 'Monkey D. Luffy',
    'C:Set': 'The Dominance of God', 'C:Rarity': 'DON!!', 'C:Year Manufactured': '2026'})
rows.append(r)
for r in rows:
    assert len(r['Title']) <= 80, r['Title']
with open('uploads/b2-flatbed-add.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=HDR, extrasaction='raise'); w.writeheader()
    for r in rows: w.writerow({k: r.get(k, '') for k in HDR})
with open('uploads/b2-flatbed-qty.csv', 'w', newline='', encoding='utf-8') as fh:
    fh.write('Action(SiteID=US|Country=US|Currency=USD|Version=1193|CC=UTF-8),ItemID,CustomLabel,Quantity\n')
    fh.write('Revise,398405490483,B2,5\nRevise,398412026576,B2,3\n')
for r in rows: print(r['StartPrice'], len(r['Title']), r['Title'])
