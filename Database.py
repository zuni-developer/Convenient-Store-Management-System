import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text, gender text,contact text, dob text,doj text, pass text, utype text, address text, salary text)")
    con.commit()

    employees = [
        ("Angus MacLeod","angus.mac@example.com","Male","07700123401","1985-03-12","2020-01-05","pass123","Admin","12 Princes St, Edinburgh, EH2 2AA","35000"),
        ("Fiona Campbell","fiona.campbell@example.com","Female","07700234502","1990-07-21","2021-06-15","pass123","Staff","45 George St, Edinburgh, EH2 2JG","30000"),
        ("Ewan Robertson","ewan.robertson@example.com","Male","07700345603","1988-11-05","2019-09-20","pass123","Staff","78 Queen St, Edinburgh, EH2 4NR","32000"),
        ("Isla MacDonald","isla.macdonald@example.com","Female","07700456704","1992-02-18","2022-03-12","pass123","Staff","23 Royal Mile, Edinburgh, EH1 1SG","31000"),
        ("Callum Fraser","callum.fraser@example.com","Male","07700567805","1987-12-30","2018-07-01","pass123","Admin","56 Lothian Rd, Edinburgh, EH3 9BG","36000"),
        ("Alasdair Stewart","alasdair.stewart@example.com","Male","07700678906","1986-05-14","2017-05-10","pass123","Staff","5 Broughton St, Edinburgh, EH1 3JU","34000"),
        ("Morag Sinclair","morag.sinclair@example.com","Female","07700789007","1991-08-22","2020-11-18","pass123","Staff","17 Hanover St, Edinburgh, EH2 2DL","30000"),
        ("Finlay MacKay","finlay.mackay@example.com","Male","07700890108","1989-04-03","2019-01-23","pass123","Staff","32 Dalry Rd, Edinburgh, EH11 2AA","32000"),
        ("Ailsa MacLeod","ailsa.macleod@example.com","Female","07700901209","1993-09-17","2021-07-07","pass123","Staff","9 St Andrew Square, Edinburgh, EH2 2AF","31000"),
        ("Gregor MacKenzie","gregor.mackenzie@example.com","Male","07701012310","1984-11-29","2016-06-30","pass123","Admin","44 Rose St, Edinburgh, EH2 3JB","36000"),
        ("Catriona Boyd","catriona.boyd@example.com","Female","07701123411","1992-01-14","2018-10-05","pass123","Staff","12 Victoria St, Edinburgh, EH1 2EX","30000"),
        ("Hamish Cameron","hamish.cameron@example.com","Male","07701234512","1987-03-09","2017-02-20","pass123","Staff","21 Grassmarket, Edinburgh, EH1 2JU","32000"),
        ("Eilidh MacLean","eilidh.maclean@example.com","Female","07701345613","1991-07-11","2019-12-01","pass123","Staff","30 Leith Walk, Edinburgh, EH6 5BR","31000"),
        ("Ruairi Graham","ruairi.graham@example.com","Male","07701456714","1988-09-26","2020-08-15","pass123","Staff","5 North Bridge, Edinburgh, EH1 1SB","34000"),
        ("Skye MacDonald","skye.macdonald@example.com","Female","07701567815","1990-12-30","2018-04-10","pass123","Staff","8 Canongate, Edinburgh, EH8 8BN","30000"),
        ("Lachlan Ross","lachlan.ross@example.com","Male","07701678916","1985-06-05","2015-09-05","pass123","Admin","12 Bruntsfield Pl, Edinburgh, EH10 4EY","36000"),
        ("Morven Sinclair","morven.sinclair@example.com","Female","07701789017","1993-03-14","2021-05-15","pass123","Staff","6 Stockbridge, Edinburgh, EH3 6NB","31000"),
        ("Calum MacLeod","calum.macleod@example.com","Male","07701890118","1986-10-18","2016-11-25","pass123","Staff","18 Morningside Rd, Edinburgh, EH10 4DD","34000"),
        ("Iona Stewart","iona.stewart@example.com","Female","07701901219","1992-05-22","2019-03-12","pass123","Staff","22 Marchmont Rd, Edinburgh, EH9 1AA","30000"),
        ("Torin MacKenzie","torin.mackenzie@example.com","Male","07702012320","1989-08-29","2017-07-07","pass123","Staff","11 Easter Rd, Edinburgh, EH6 8JG","32000"),
        ("Eira Cameron","eira.cameron@example.com","Female","07702123421","1991-11-05","2020-01-15","pass123","Staff","3 Colinton Rd, Edinburgh, EH14 1DJ","31000"),
        ("Alistair MacLeod","alistair.macleod@example.com","Male","07702234522","1987-02-10","2018-08-20","pass123","Admin","5 Abbeyhill, Edinburgh, EH8 8DP","36000"),
        ("Freya Boyd","freya.boyd@example.com","Female","07702345623","1990-06-18","2019-04-01","pass123","Staff","8 Newington Rd, Edinburgh, EH9 1QR","30000"),
        ("Struan Fraser","struan.fraser@example.com","Male","07702456724","1985-09-23","2016-03-15","pass123","Staff","14 Broughton St, Edinburgh, EH3 3JD","34000"),
        ("Maisie MacDonald","maisie.macdonald@example.com","Female","07702567825","1993-12-11","2021-01-20","pass123","Staff","19 Fountainbridge, Edinburgh, EH3 9QA","31000"),
        ("Duncan MacKay","duncan.mackay@example.com","Male","07702678926","1988-04-30","2017-05-15","pass123","Staff","7 Stockbridge, Edinburgh, EH3 6NB","32000"),
        ("Caitlin Robertson","caitlin.robertson@example.com","Female","07702789027","1991-08-16","2020-06-05","pass123","Staff","12 Canongate, Edinburgh, EH8 8BN","31000"),
        ("Gregor Stewart","gregor.stewart@example.com","Male","07702890128","1986-01-25","2015-12-10","pass123","Admin","9 Bruntsfield Pl, Edinburgh, EH10 4EY","36000"),
        ("Niamh MacDonald","niamh.macdonald@example.com","Female","07702901229","1992-10-05","2019-07-22","pass123","Staff","10 Leith Walk, Edinburgh, EH6 5BR","30000")
    ]
    cur.executemany("INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES (?,?,?,?,?,?,?,?,?,?)", employees)
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    con.commit()

    categories = [
        ("Snacks",), ("Beverages",), ("Instant Food",), ("Confectionery",), 
        ("Dairy",), ("Frozen Food",), ("Bakery",), ("Health & Personal Care",), 
        ("Household",), ("Stationery",)
    ]
    cur.executemany("INSERT INTO category(name) VALUES (?)", categories)
    con.commit()

    cur.execute("""CREATE TABLE IF NOT EXISTS Supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,contact TEXT,description TEXT)""")
    con.commit()

    suppliers = [
        ("K-Market Co.", "07710000101", "Korean snacks & instant food"),
        ("Seoul Beverages", "07710000202", "Korean drinks supplier"),
        ("Han Bakery", "07710000303", "Korean bakery supplier"),
        ("Korean Dairy Ltd.", "07710000404", "Korean dairy supplier"),
        ("Frozen Seoul", "07710000505", "Frozen food supplier"),
        ("Sweet Seoul", "07710000606", "Confectionery supplier"),
        ("Health Korea", "07710000707", "Health & personal care"),
        ("Household Co.", "07710000808", "Household items supplier"),
        ("Stationery Plus", "07710000909", "Stationery supplier"),
        ("Korean Express", "07710001010", "General Korean goods"),
        ("Seoul Snacks", "07710001111", "Additional Korean snack supplier"),
        ("Bibim Foods", "07710001212", "Korean instant foods"),
        ("Chingu Beverages", "07710001313", "Korean drinks"),
        ("Mochi Bakery", "07710001414", "Specialty bakery"),
        ("K-Frozen Ltd.", "07710001515", "Frozen Korean foods"),
        ("Candy Korea", "07710001616", "Confectionery and sweets"),
        ("Wellness Korea", "07710001717", "Health and hygiene"),
        ("House Essentials", "07710001818", "Household items"),
        ("Paper & Pen Co.", "07710001919", "Stationery supplier"),
        ("Seoul General", "07710002020", "General Korean products")
    ]
    cur.executemany("INSERT INTO Supplier(name,contact,description) VALUES (?,?,?)", suppliers)
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Supplier text,Category text, name text,price text, qty text,status text)")
    con.commit()

    products = [
        # Snacks
        ("K-Market Co.", "Snacks", "Choco Banana Chips", "2.80", "100", "Active"),
        ("Seoul Snacks", "Snacks", "Spicy Seaweed Snack", "3.00", "100", "Active"),
        ("K-Market Co.", "Snacks", "Honey Butter Chips", "2.50", "80", "Active"),
        # Beverages
        ("Seoul Beverages", "Beverages", "Banana Milk", "1.80", "120", "Active"),
        ("Chingu Beverages", "Beverages", "Aloe Vera Drink", "2.00", "100", "Active"),
        ("Seoul Beverages", "Beverages", "Citron Tea", "1.90", "100", "Active"),
        # Instant Food
        ("Bibim Foods", "Instant Food", "Bibimbap Instant Pack", "5.50", "50", "Active"),
        ("Bibim Foods", "Instant Food", "Tteokbokki Instant", "4.50", "50", "Active"),
        ("K-Market Co.", "Instant Food", "Instant Udon", "4.70", "40", "Active"),
        # Confectionery
        ("Candy Korea", "Confectionery", "Choco Pie", "2.80", "100", "Active"),
        ("Sweet Seoul", "Confectionery", "Peach Gummies", "2.50", "100", "Active"),
        ("Candy Korea", "Confectionery", "Strawberry Mochi", "3.00", "80", "Active"),
        # Dairy
        ("Korean Dairy Ltd.", "Dairy", "Yogurt Drink", "2.00", "90", "Active"),
        ("Korean Dairy Ltd.", "Dairy", "Cheese Snack", "2.50", "80", "Active"),
        ("Korean Dairy Ltd.", "Dairy", "Milk 1L", "1.80", "100", "Active"),
        # Frozen Food
        ("Frozen Seoul", "Frozen Food", "Frozen Mandu", "6.50", "40", "Active"),
        ("K-Frozen Ltd.", "Frozen Food", "Frozen Dumplings", "6.20", "40", "Active"),
        ("Frozen Seoul", "Frozen Food", "Frozen Kimchi Pancake", "5.50", "40", "Active"),
        # Bakery
        ("Han Bakery", "Bakery", "Red Bean Bread", "2.50", "60", "Active"),
        ("Mochi Bakery", "Bakery", "Melon Pan", "2.80", "50", "Active"),
        ("Han Bakery", "Bakery", "Butter Croissant", "2.20", "60", "Active"),
        # Health & Personal Care
        ("Wellness Korea", "Health & Personal Care", "Ginseng Soap", "3.50", "70", "Active"),
        ("Health Korea", "Health & Personal Care", "Vitamin C Gummies", "4.00", "80", "Active"),
        ("Wellness Korea", "Health & Personal Care", "Face Mask Pack", "2.50", "100", "Active"),
        # Household
        ("Household Co.", "Household", "Detergent 1kg", "4.50", "60", "Active"),
        ("House Essentials", "Household", "Cleaning Spray", "3.50", "70", "Active"),
        ("Household Co.", "Household", "Reusable Shopping Bag", "2.50", "100", "Active"),
        # Stationery
        ("Stationery Plus", "Stationery", "Korean Pen Set", "2.80", "100", "Active"),
        ("Paper & Pen Co.", "Stationery", "Notebook", "2.50", "80", "Active"),
        ("Stationery Plus", "Stationery", "Sticky Notes Pack", "1.80", "100", "Active"),
        # Add more to reach 50
        ("Seoul General", "Snacks", "Seaweed Crisps", "2.50", "90", "Active"),
        ("Seoul General", "Beverages", "Green Tea Latte", "2.50", "90", "Active"),
        ("Seoul General", "Instant Food", "Instant Fried Rice", "4.90", "50", "Active"),
        ("Sweet Seoul", "Confectionery", "Peanut Candy", "2.70", "60", "Active"),
        ("Mochi Bakery", "Bakery", "Chestnut Cake", "3.00", "50", "Active"),
        ("Korean Dairy Ltd.", "Dairy", "Strawberry Milk", "1.80", "100", "Active"),
        ("K-Frozen Ltd.", "Frozen Food", "Frozen Tteok", "5.80", "40", "Active"),
        ("Health Korea", "Health & Personal Care", "Herbal Shampoo", "4.50", "50", "Active"),
        ("House Essentials", "Household", "Kitchen Towels", "2.50", "70", "Active"),
        ("Paper & Pen Co.", "Stationery", "Eraser Pack", "1.50", "100", "Active")
    ]


    cur.executemany("INSERT INTO product(Supplier,Category,name,price,qty,status) VALUES (?,?,?,?,?,?)", products)
    con.commit()

create_db()