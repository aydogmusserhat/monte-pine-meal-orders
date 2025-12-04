from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DB_NAME = "otel_menu.db"


def init_db():
    """Genel yemek sipariş tablosu (sabah / öğle / akşam)"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS meal_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_type TEXT,              -- breakfast / lunch / dinner
            room_number TEXT,
            guest_name TEXT,
            guests_count INTEGER,
            service_date TEXT,
            preferred_time TEXT,
            main_option TEXT,
            extra_option TEXT,
            notes TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()


# ---------- YARDIMCI FONKSİYON ----------

def save_order(meal_type, form):
    room_number = form.get("room_number", "").strip()
    guest_name = form.get("guest_name", "").strip()
    guests_count = form.get("guests_count", "").strip()
    service_date = form.get("service_date", "").strip()
    preferred_time = form.get("preferred_time", "").strip()
    main_option = form.get("main_option", "").strip()
    extra_option = form.get("extra_option", "").strip()
    notes = form.get("notes", "").strip()

    # basit validasyon
    if not room_number or not guests_count or not service_date or not preferred_time or not main_option:
        return False, "Please fill required fields (room, guests, date, time, main option)."

    try:
        guests_count_int = int(guests_count)
    except ValueError:
        guests_count_int = 1

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO meal_orders
        (meal_type, room_number, guest_name, guests_count,
         service_date, preferred_time, main_option, extra_option,
         notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        meal_type, room_number, guest_name, guests_count_int,
        service_date, preferred_time, main_option, extra_option,
        notes, created_at
    ))
    conn.commit()
    conn.close()
    return True, None


# ---------- ROUTE: ROOT -> BREAKFAST ----------

@app.route("/")
def index():
    # ana adres kahvaltıya yönlendiriyor
    return redirect(url_for("breakfast_form"))


# ---------- BREAKFAST ----------

@app.route("/breakfast", methods=["GET"])
def breakfast_form():
    main_options = [
        {
            "id": 1,
            "title": "Sunny-side-up egg on rustic bread",
            "desc": "Perfectly cooked egg served over aromatic arugula and rustic homemade bread."
        },
        {
            "id": 2,
            "title": "Croissant with beetroot cream & scrambled eggs",
            "desc": "Homemade black bread topped with whipped beetroot cream cheese, soft scrambled eggs, fresh arugula and onions."
        },
        {
            "id": 3,
            "title": "Toast with smoked salmon & poached egg",
            "desc": "Smoked salmon, avocado cream and a poached egg on homemade toast."
        },
        {
            "id": 4,
            "title": "Vegan avocado toast",
            "desc": "Sourdough toast with avocado cream, roasted tomatoes and fresh arugula."
        },
        {
            "id": 5,
            "title": "House speciality",
            "desc": "Homemade pie (cheese or potatoes) or traditional priganice with accompaniments of your choice."
        },
        {
            "id": 6,
            "title": "Breakfast with beef rump steak",
            "desc": "Lightly cured beef rump steak served with creamy kaymak, boiled eggs, sea salt and homemade bread."
        },
        {
            "id": 7,
            "title": "Yogurt parfait",
            "desc": "Layers of fresh seasonal fruit, granola and chia seeds."
        },
        {
            "id": 8,
            "title": "Cereal with nuts & fruit",
            "desc": "Cereal with almond milk, seasonal fruit, walnuts and coconut."
        }
    ]

    extra_options = [
        {
            "id": 9,
            "title": "Homemade waffles with fruit sauce",
            "desc": "Served with vanilla cream and wild berry coulis."
        },
        {
            "id": 10,
            "title": "Crêpes with vanilla cream & forest fruit",
            "desc": "Delicate crêpes filled with vanilla pastry cream and topped with wild berry coulis."
        },
        {
            "id": 11,
            "title": "No sweet option",
            "desc": "Select this if you prefer not to have waffles or crêpes."
        }
    ]

    time_slots = ["08:00", "09:00", "10:00"]

    return render_template(
        "breakfast_form.html",
        main_options=main_options,
        extra_options=extra_options,
        time_slots=time_slots
    )


@app.route("/submit/breakfast", methods=["POST"])
def submit_breakfast():
    ok, msg = save_order("breakfast", request.form)
    if not ok:
        return msg, 400
    return redirect(url_for("breakfast_form") + "?ok=1")


# ---------- LUNCH ----------

@app.route("/lunch", methods=["GET"])
def lunch_form():
    main_options = [
        {
            "id": 1,
            "title": "Grilled chicken fillet",
            "desc": "Served with roasted vegetables, herb potatoes and light chicken jus."
        },
        {
            "id": 2,
            "title": "Beef medallions",
            "desc": "Pan-seared beef medallions with mashed potatoes and peppercorn sauce."
        },
        {
            "id": 3,
            "title": "Sea bass fillet",
            "desc": "Grilled sea bass with lemon butter, sautéed greens and rice pilaf."
        },
        {
            "id": 4,
            "title": "Pasta primavera (vegetarian)",
            "desc": "Fresh pasta with seasonal vegetables, cherry tomatoes and parmesan."
        },
        {
            "id": 5,
            "title": "Risotto with wild mushrooms",
            "desc": "Creamy arborio rice with wild mushrooms and truffle oil."
        },
        {
            "id": 6,
            "title": "Montenegro burger",
            "desc": "Homemade beef burger, local cheese, fries and salad."
        },
        {
            "id": 7,
            "title": "Caesar salad with chicken",
            "desc": "Romaine lettuce, grilled chicken, croutons and parmesan."
        },
        {
            "id": 8,
            "title": "Grilled vegetable plate (vegan)",
            "desc": "Selection of seasonal grilled vegetables served with hummus."
        }
    ]

    extra_options = [
        {
            "id": 9,
            "title": "Soup of the day",
            "desc": "Freshly prepared soup according to the chef's choice."
        },
        {
            "id": 10,
            "title": "Side salad",
            "desc": "Mixed greens with light vinaigrette."
        },
        {
            "id": 11,
            "title": "No starter / side",
            "desc": "Select this if you do not wish to have soup or salad."
        }
    ]

    time_slots = ["12:00", "13:00", "14:00"]

    return render_template(
        "lunch_form.html",
        main_options=main_options,
        extra_options=extra_options,
        time_slots=time_slots
    )


@app.route("/submit/lunch", methods=["POST"])
def submit_lunch():
    ok, msg = save_order("lunch", request.form)
    if not ok:
        return msg, 400
    return redirect(url_for("lunch_form") + "?ok=1")


# ---------- DINNER ----------

@app.route("/dinner", methods=["GET"])
def dinner_form():
    main_options = [
        {
            "id": 1,
            "title": "Slow-cooked beef cheeks",
            "desc": "Braised in red wine, served with creamy polenta and roasted root vegetables."
        },
        {
            "id": 2,
            "title": "Herb-crusted lamb rack",
            "desc": "Served with potato gratin, grilled asparagus and rosemary jus."
        },
        {
            "id": 3,
            "title": "Salmon fillet with lemon dill",
            "desc": "Pan-seared salmon with lemon dill sauce and seasonal vegetables."
        },
        {
            "id": 4,
            "title": "Homemade gnocchi with pesto",
            "desc": "Potato gnocchi, basil pesto, cherry tomatoes and parmesan."
        },
        {
            "id": 5,
            "title": "Chicken in forest mushroom sauce",
            "desc": "Grilled chicken breast topped with creamy forest mushroom sauce."
        },
        {
            "id": 6,
            "title": "Grilled vegetables & halloumi",
            "desc": "Charcoal-grilled vegetables with halloumi cheese (vegetarian)."
        },
        {
            "id": 7,
            "title": "Seafood pasta",
            "desc": "Tagliatelle pasta with mixed seafood in white wine sauce."
        },
        {
            "id": 8,
            "title": "Vegan lentil stew",
            "desc": "Slow-cooked lentils with vegetables and spices."
        }
    ]

    extra_options = [
        {
            "id": 9,
            "title": "Chocolate lava cake",
            "desc": "Warm chocolate cake with liquid centre, served with vanilla ice cream."
        },
        {
            "id": 10,
            "title": "Cheesecake with forest fruit",
            "desc": "Baked cheesecake topped with forest fruit coulis."
        },
        {
            "id": 11,
            "title": "Seasonal fruit plate",
            "desc": "Selection of fresh seasonal fruits."
        },
        {
            "id": 12,
            "title": "No dessert",
            "desc": "Select this if you prefer to skip dessert."
        }
    ]

    time_slots = ["19:00", "20:00", "21:00"]

    return render_template(
        "dinner_form.html",
        main_options=main_options,
        extra_options=extra_options,
        time_slots=time_slots
    )


@app.route("/submit/dinner", methods=["POST"])
def submit_dinner():
    ok, msg = save_order("dinner", request.form)
    if not ok:
        return msg, 400
    return redirect(url_for("dinner_form") + "?ok=1")


# ---------- ADMIN PANEL ----------

@app.route("/admin")
def admin_panel():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT id, meal_type, room_number, guest_name, guests_count,
               service_date, preferred_time, main_option, extra_option,
               notes, created_at
        FROM meal_orders
        ORDER BY service_date ASC, preferred_time ASC, meal_type ASC, room_number ASC
    """)
    orders = c.fetchall()
    conn.close()

    return render_template("admin.html", orders=orders)


if __name__ == "__main__":
    if not os.path.exists(DB_NAME):
        init_db()
    else:
        init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
