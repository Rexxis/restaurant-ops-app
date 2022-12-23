# 
# Cashier Web App - Harvard CS50 Final Project
# 
# Made by David Harendza - December 2022
# 
# 

from datetime import datetime
from flask import Flask, render_template, redirect, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session

from helpers import apology, login_required


# Configure application
app = Flask(__name__)

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///restaurant.db"

db = SQLAlchemy(app)

# Create database model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    hash = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return f"User: {self.username}"

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    foodname = db.Column(db.String, unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return f"food: {self.foodname}"

class Operations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String, nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))
    status = db.Column(db.String, default="queue", nullable=False)
    custom_display = db.Column(db.String, default=None)
    order_time = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self) -> str:
        return f"Operations: {self.id}"

# Create database
with app.app_context():
    db.create_all()

# Ensure templates auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET","POST"])
@login_required
def index():
    """Index page"""

    return render_template("index.html")


@app.route("/cashier", methods=["GET", "POST"])
def cashier():
    """Cashier page, to add orders"""

    if request.method == "POST":

        # Update customer name using global session
        if session["customer_name"] == None:
            session["customer_name"] = request.form.get("customer_name")
            
        return render_template("cashier.html", name=session["customer_name"])
    else:

        if session["customer_name"] == None:
            return apology("Enter customer name from homepage")

        # Get data from database
        display_data = db.session.query(Operations, Operations.id, Operations.food_id, Operations.custom_display, Food.foodname, Food.price).join(Food).filter(Operations.customer == session["customer_name"], Operations.status == 'queue', Operations.user_id == session["user_id"]).all()

        total = 0

        for data in display_data:
            total += data.price

        total = f'{total:.2f}'

        # Render the page
        return render_template("cashier.html", name=session["customer_name"], display_data = display_data, total=total)


@app.route("/addorder", methods=["POST"])
def addorder():
    """Add order to cart"""

    # Get order data
    new_order = Food.query.filter_by(id = request.form.get("food_id")).all()

    # Add new data to operations
    new_operation = Operations(customer = session["customer_name"], food_id = new_order[0].id, user_id = session["user_id"])
    db.session.add(new_operation)
    db.session.commit()
    
    return redirect("/cashier")


@app.route("/prune")
def prune():
    """Delete all items in cart"""

    # Delete all data with customer name and status queue
    db.session.query(Operations).filter(Operations.customer == session["customer_name"], Operations.status == 'queue', Operations.user_id == session["user_id"]).delete()
    db.session.commit()

    # Redirect user to cashier page
    return redirect("/cashier")


@app.route("/edit", methods=["POST"])
def edit():
    """Edit item in cart (custom)"""

    # Initiate variables
    ops_id = request.form.get("id")
    cheese_option = request.form.get("cheese-custom")
    pickle_option = request.form.get("pickle-custom")
    ketchup_option = request.form.get("ketchup-custom")
    salt_option = request.form.get("salt-custom")
    custom_option = request.form.get("text-custom")

    # Displaying values
    custom_display = ""
    user_choice = {"Cheese": cheese_option, "Pickle": pickle_option, "Ketchup" : ketchup_option, "Salt": salt_option}
    
    options = {2: "+", 50: "No "}

    for choice, value in user_choice.items():
        if int(value) != 1:
            custom_display += "[" + options[int(value)] + choice + "]"
    
    if len(custom_option) > 1:
        custom_display += "[" + custom_option + "]"

    # Update data
    updated_ops = Operations.query.filter_by(id = ops_id).first()
    updated_ops.custom_display = custom_display

    # Insert data
    db.session.commit()

    # Update cart
    if cheese_option == '2':
        # Get order data
        new_order = Food.query.filter_by(id = 101).all()

        # Add new data to operations
        new_operation = Operations(customer = session["customer_name"], food_id = new_order[0].id, user_id = session["user_id"])
        db.session.add(new_operation)
        db.session.commit()
    
    if pickle_option == '2':
        # Get order data
        new_order = Food.query.filter_by(id = 102).all()

        # Add new data to operations
        new_operation = Operations(customer = session["customer_name"], food_id = new_order[0].id, user_id = session["user_id"])
        db.session.add(new_operation)
        db.session.commit()
    
    if pickle_option == '3':
        # Get order data
        new_order = Food.query.filter_by(id = 103).all()

        # Add new data to operations
        new_operation = Operations(customer = session["customer_name"], food_id = new_order[0].id, user_id = session["user_id"])
        db.session.add(new_operation)
        db.session.commit()
    
    return redirect("/cashier")


@app.route("/push_kitchen")
def push_kitchen():
    # Query all data with customer name
    data = Operations.query.filter(Operations.customer == session["customer_name"], Operations.status == 'queue', Operations.user_id == session["user_id"]).all()

    # Update status to kitchen
    for row in data:
        row.status = 'KITCHEN'
    
    # Commit database changes
    db.session.commit()
    
    # Flash message
    flash("Successfully pushed to kitchen","warning")
    
    # Clear customer name
    session["customer_name"] = None

    return redirect("/")



@app.route("/edit/<int:item_id>")
def editdraft(item_id):
    return render_template("edit.html", item_id = item_id)
    

@app.route("/delete/<int:id>")
def delete(id):
    """Delete item from cart"""

    # Get the item to delete
    item_to_delete = Operations.query.get_or_404(id)

    try:
        # Delete database entry
        db.session.delete(item_to_delete)
        db.session.commit()
        
        return redirect("/cashier")

    except:
        flash("Failed")
        return redirect("/cashier")


@app.route("/cancel")
def cancel():
    """Cancel order, routes user back to homepage"""

    # Clear cart
    prune()

    # Clear customer name from session
    session["customer_name"] = None
    
    return redirect("/")


@app.route("/kitchen")
def kitchen():
    """Monitor page for kitchen crew"""
    display_data = db.session.query(Operations, Operations.id, Operations.food_id, Operations.customer, Operations.custom_display, Operations.status, Food.foodname).join(Food).filter(Operations.status == 'KITCHEN', Operations.user_id == session["user_id"]).all()

    return render_template("kitchen.html", display_data = display_data)


@app.route("/deletekitchen/<int:id>")
def deletekitchen(id):
    """Delete item from cart"""

    # Get the item to delete
    item_to_delete = Operations.query.get_or_404(id)

    try:
        # Delete database entry
        db.session.delete(item_to_delete)
        db.session.commit()
        
        flash("Cancel order success","warning")
        return redirect("/kitchen")

    except:
        flash("Failed")
        return redirect("/kitchen")


@app.route("/serve/<int:id>")
def serve(id):
    """Change item status to ready"""

    #Get item
    item_to_serve = Operations.query.get(id)
    item_to_serve.status = "READY"

    db.session.commit()

    flash("1 item served","success")

    return redirect("/kitchen")


@app.route("/servecust/<name>")
def servecust(name):
    """Change all item status with customer name"""

    #Get item
    group_to_serve = Operations.query.filter_by(customer = name).all()

    for group in group_to_serve:
        group.status = "READY"

    db.session.commit()

    total_item = len(group_to_serve)

    flash(f"{name} - {total_item} item served","success")

    return redirect("/kitchen")


@app.route("/monitor", methods=["GET", "POST"])
def monitor():
    """Display order with status ready"""

    if request.method == "POST":
        # Get item id
        item_id = request.form.get("id")

        # Get completed item
        completed_item = Operations.query.get(item_id)
        completed_item.status = "COMPLETED"

        db.session.commit()

        flash(f"({completed_item.customer}) 1 order completed","success")

        return redirect("/monitor")

    else:
        display_data = db.session.query(Operations, Operations.id, Operations.food_id, Operations.customer, Operations.custom_display, Operations.status, Food.foodname).join(Food).filter(Operations.status == 'READY', Operations.user_id == session["user_id"]).all()

        return render_template("monitor.html", display_data = display_data)


@app.route("/complete/<name>")
def complete(name):
    # Get completed item with name
    completed_group = Operations.query.filter(Operations.customer == name, Operations.status == "READY", Operations.user_id == session["user_id"]).all()

    # Update item status
    for item in completed_group:
        item.status = "COMPLETED"
    
    total = len(completed_group)

    db.session.commit()

    flash(f"Completed {total} items for {item.customer}","warning")

    return redirect("/monitor")


@app.route("/update", methods=["GET", "POST"])
def update():
    """Update food prices"""
    if request.method == "POST":
        # Check username
        user = Users.query.filter(Users.id == session["user_id"]).first()

        # If user not admin render apology
        if user.username != "admin":
            flash(f"{user}", "info")
            return apology("You need to be logged in as admin")

        # Get item id
        item_id = request.form.get("id")
        new_price = float(request.form.get("newprice"))

        # Call item
        updated_item = Food.query.get(item_id)

        if updated_item.price == new_price:
            flash("New price is the same with current price!","warning")
            return redirect("/update")

        updated_item.price = new_price

        db.session.commit()

        flash(f"{updated_item.foodname} price updated to {new_price}","success")

        return redirect("/update")

    else:
        # Get all food item
        display_data = Food.query.all()

        return render_template("update.html", display_data = display_data)


@app.route("/history")
def history():
    display_data = db.session.query(Operations, Operations.id, Operations.customer, Operations.custom_display, Operations.order_time, Food.foodname, Food.price).join(Food).filter(Operations.user_id == session["user_id"]).all()

    return render_template("history.html", display_data = display_data)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user id
    session.clear()

    # Clear any operations with queue status
    db.session.query(Operations).filter(Operations.status == 'queue').delete()
    db.session.commit()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username") or not request.form.get("username").isalnum():
            return apology("Username cannot be blank or use special character")
        
        # Ensure password was submitted
        if not request.form.get("password") or not request.form.get("password").isalnum():
            return apology("Password cannot be blank or use special character")
        
        # Query database for username
        recorded_users = Users.query.filter_by(username = request.form.get("username")).all()

        # Ensure username exist and password is correct
        if len(recorded_users) != 1 or not check_password_hash(recorded_users[0].hash, request.form.get("password")):
            return apology("username or password does not match")

        # Remember which user has logged in & initiate sessions
        session["user_id"] = recorded_users[0].id
        session["customer_name"] = None

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user id
    session.clear()

    # redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Initialize variables
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Ensure username was submitted
        if not username or not username.isalnum():
            return apology("must provide username (no special character)")

        # Ensure password was submitted
        if not password or not password.isalnum():
            return apology("must provide password (no special character)")

        # Ensure password match confirmation
        if not password == confirmation:
            return apology("password confirmation does not match")

        # Check if username already exist
        check_username = Users.query.filter_by(username = username).all()
        if len(check_username) != 0:
            return apology("username already taken")

        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert new user to database
        new = Users(username = username, hash = hashed_password)
        db.session.add(new)
        db.session.commit()

        flash("Register success!", "success")
        return redirect("/login")

    else:
        return render_template("register.html")


# Run flask app
if __name__ == "__main__":
    app.run(debug=True)