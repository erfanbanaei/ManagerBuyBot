from pyrogram import *
from pyrogram.types import *
from pyromod import listen
import sqlite3
from datetime import date, datetime
# ====================================================================
api_id = 0000000
api_hash = "*******************************"
bot_token = "***********:*************-*******************"
app = Client("ManagerBuy", api_id=api_id,
             api_hash=api_hash, bot_token=bot_token)
# ====================================================================
con = sqlite3.connect("data/data.db")
# ====================================================================
Keyboard = ReplyKeyboardMarkup(
    [
        ["📥 Add 📥", "👁 Show 👁"],
        ["📝 Edit 📝", "🧹 Delete 🧹"],
        ["❓ Help ❓", "👨‍💻 Developer 👨‍💻"]
    ], resize_keyboard=True
)
# ====================================================================


@app.on_message(filters.command("start"))
async def Start(client, message):
    cur = con.cursor()
    cur.execute(
        f"CREATE TABLE IF NOT EXISTS user_{message.from_user.id}(Id INTEGER PRIMARY KEY AUTOINCREMENT,Price INTEGER, Product_Name TEXT, Date TEXT, Time TEXT)")
    con.commit()
    await message.reply_text(f"""🔥Hello <b>{message.from_user.mention}</b> ,
This helps the bot to list the products you buy and manage your purchases""",
                             reply_markup=Keyboard, parse_mode=enums.ParseMode.HTML)
# ====================================================================


@app.on_message(filters.regex("^📥 Add 📥$"))
async def Add_Purchase(client, message):
    Price = await message.chat.ask("[?] Enter your purchase price : ")
    Product_Name = await message.chat.ask("[?] Enter your purchase name : ")
    t = datetime.now().time()
    time = f"{t.hour}:{t.minute}"
    date2 = date.today()
    full = (Price.text, Product_Name.text, date2, time)
    cur = con.cursor()
    cur.execute(
        f"INSERT INTO user_{message.from_user.id}(Price, Product_Name, Date, Time) VALUES(?,?,?,?)", full)
    con.commit()
    await message.reply_text("Added product")
# ====================================================================


@app.on_message(filters.regex("^👁 Show 👁$"))
async def Show_Purchase(client, message):
    show_product = ""
    sum_price = 0
    cur = con.cursor()
    cur.execute(f'SELECT * FROM user_{message.from_user.id}')
    rows = cur.fetchall()
    for row in rows:
        show_product += f"Id : {str(row[0])}\nProduct Name : {str(row[2])}\nPrice : {str(row[1])}\nData : {str(row[3])}\nTime : {str(row[4])}\n===============================\n"
        sum_price += int(str(row[1]))
    await message.reply_text(show_product+f"\nTotal price of purchases : {sum_price}")
# ====================================================================


@app.on_message(filters.regex("^📝 Edit 📝$"))
async def Edit_Purchase(client, message):
    id_product = await message.chat.ask("[?] Enter your product ID : ")
    new_name = await message.chat.ask("[?] Enter the new name of the desired product : ")
    new_price = await message.chat.ask("[?] Enter the new price of the product you want : ")
    full = (new_price.text, new_name.text, int(id_product.text))
    cur = con.cursor()
    cur.execute(
        f"UPDATE user_{message.from_user.id} SET Price = ?, Product_Name = ? WHERE Id = ?", full)
    con.commit()
    await message.reply_text("Edited product")
# ====================================================================


@app.on_message(filters.regex("^🧹 Delete 🧹$"))
async def Delete_Purchase(client, message):
    data_id = await message.chat.ask("[?] Enter the ID of the product you want (9999 => Remove all products) : ")
    cur = con.cursor()
    full = (int(data_id.text))
    if full == 9999:
        cur.execute(f"DELETE FROM user_{message.from_user.id}")
        con.commit()
        await message.reply_text("Removed all")
    else:
        cur.execute(
            f"DELETE FROM user_{message.from_user.id} WHERE Id = {full}")
        con.commit()
        await message.reply_text("Deleted Product")
# ====================================================================


@app.on_message(filters.regex("^❓ Help ❓$"))
async def Help_Purchase(client, message):
    await message.reply_text("""
Add => Add to Database(Price , Product Name)
Show => Show all products
Edit => Product edit
Delete => Remove the product from the list
""")
# ====================================================================


@app.on_message(filters.regex("^👨‍💻 Developer 👨‍💻$"))
async def Developer(client, message):
    await message.reply_text("Communication with programming", reply_markup=InlineKeyboardMarkup(
        [
            [  # First row
                InlineKeyboardButton(  # Generates a callback query when pressed
                    "Telegram",
                    url="https://t.me/MrTakDev"
                ),
                InlineKeyboardButton(  # Opens a web URL
                    "Twitter",
                    url="https://twitter.com/erfan_banaei"
                ),
            ],
            [  # Second row
                InlineKeyboardButton(  # Opens the inline interface
                    "Youtube",
                    url="https://www.youtube.com/@hero_code"
                ),
                InlineKeyboardButton(  # Opens the inline interface in the current chat
                    "Source",
                    url="https://github.com/erfanbanaei/ManagerBuyBot"
                )
            ]
        ]
    )
    )
# ====================================================================
app.run()
