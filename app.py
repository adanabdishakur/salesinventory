from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from configs.base_config import *
import pygal
app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_object(Staging)

@app.before_first_request
def create_tables():
    db.create_all()


class Item(db.Model):
    __tablename__ = 'inventories'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    stock = db.Column(db.Integer, unique=False, nullable=False)
    buying_price = db.Column(db.Integer, unique=False, nullable=False)
    selling_price = db.Column(db.Integer, unique=False, nullable=False)

class Sale(db.Model):
    __tablename__ = 'Sales'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
   
    created_at=db.Column(db.DateTime, unique=False, nullable=False, default=datetime.utcnow)

    inv_id = db.Column(db.Integer, db.ForeignKey('inventories.id'),
        nullable=False)
    inventories= db.relationship('Item',
        backref=db.backref('sales', lazy=True))




@app.route('/', methods = ['GET','POST'])
def add_details():
    if request.method == 'POST':
       name = request.form['name']
       stock = request.form['stock']
       buying_price = request.form['buying_price']
       selling_price = request.form['selling_price']
     
       
       print(name ,buying_price ,selling_price)
       inventories = Item(name = name,stock = stock, buying_price = buying_price, selling_price = selling_price)
       print('Record successfully added')
       db.session.add(inventories)
       db.session.commit()
       return redirect(url_for('add_details'))
    else:
        goods = Item.query.all()
        return render_template('items.html',goods = goods)

@app.route('/sale', methods = ['POST'])
def makesales():
    if request.method == 'POST':
        quantity = request.form['quantity']    
        inv_id= request.form['inv_id']     
        print(quantity,inv_id)
     
        item_to_edit = Item.query.filter_by(id = item_id).first()
        item_to_edit.item_quantity = int(item_to_edit.item_quantity) - int(quantity)

        if int(item_to_edit.item_quantity) - int(quantity) <= 0:
            print("Quantity entered is more than the stock available")
            return redirect(url_for('add_details'))
       
        db.session.add(item_to_edit)
        db.session.commit()
       
        sale=Sale(quantity=quantity,inv_id=inv_id)
        db.session.add(sale)
        db.session.commit()
        return redirect(url_for('add_details'))

@app.route('/viewsales/<int:x>', methods = ['GET'])
def viewsales(x):
    if request.method == 'GET':
        item_sale = Sale.query.filter_by(inv_id = x).all()
        s_item = Item.query.filter_by(id = x).all()
        print(item_sale)
        return render_template('viewsales.html', posts = item_sale)


@app.route('/sale/<int:inv_id>', methods = ['GET','POST'])
def make_sales(inv_id):
    if request.method == 'POST':
       quantity = request.form['quantity']
       inv_id = request.form['inv_id']
       
       n = Item.query.filter_by(id = inv_id).first()
       n.stock = int(n.stock) - int(quantity)
       if int(n.stock) < 0:
           flash(u"Quantity entered is more than stock", 'error')
           return redirect(url_for('add_details'))
       elif int(quantity) <= 0:
           flash(u"Invalid quantity entered. Enter amount greater than 0", 'error')
           return redirect(url_for('add_details'))
       elif Item.stock == 0:
           flash(u"There is no stock available for this item.", 'error')
           return redirect(url_for('add_details'))
       print(quantity ,inv_id)
       db.session.add(n)
       db.session.commit()    
       sale = Sale(quantity = quantity, inv_id = inv_id)
       db.session.add(sale)
       db.session.commit()
       return redirect(url_for('add_details'))        
    else:
        return render_template('items.html')


@app.route('/all_sales', methods = ['GET'])
def all_sales():
    if request.method == 'GET':
        sale_all = Sale.query.all()
        print(sale_all)
        return render_template('all_sales.html', invent = sale_all)


@app.route('/charting')
def charting():
    sale_data = Sale.query.with_entities(Sale.quantity).all()
    sale_date = Sale.query.with_entities(Sale.created_at).all()
    sales = Sale.query.all()

    chart_data = {}
   
    # Adding values in a dictionary according to their keys if the keys are the same 
    for s in sales:
        dt = s.created_at.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        if str(dt) in chart_data.keys():
            chart_data[str(dt)] = chart_data[str(dt)] + s.quantity
        else:
            chart_data[str(dt)] = s.quantity
    print(chart_data)

    line_chart = pygal.Bar()
    line_chart.title = 'Sales Made in 2021'
    for k,v in chart_data.items():
        line_chart.add(k, v)
    chart = line_chart.render()
    return render_template('chatting.html', chart = chart)        

     

if __name__=="__main__":
    app.run(debug=True)


