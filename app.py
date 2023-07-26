from flask import Flask,render_template, template_rendered, flash, request, url_for, redirect,jsonify
import threading
app = Flask(__name__)
from scrapper import Scrapper
import random
import os,time,csv,json
import webbrowser
def get_index_data():
    all_fifth_wheen_products = []
    if os.path.exists("static/fifth-wheel.csv"):
        with open("static/fifth-wheel.csv", 'r', encoding='latin-1') as csv_f:
            all_fifth_wheen_products = list(csv.DictReader(csv_f, delimiter=','))
    all_travel_trailer_products = []
    if os.path.exists("static/travel-trailer.csv"):
        with open("static/travel-trailer.csv", 'r', encoding='latin-1') as csv_f:
            all_travel_trailer_products = list(csv.DictReader(csv_f, delimiter=','))
    return all_fifth_wheen_products, all_travel_trailer_products
@app.route('/')
@app.route('/dashboard')
def inedex():
    fifthWheel, travelTrailer = get_index_data()
    return render_template('products.html',fifthWheel=len(fifthWheel),travelTrailer=len(travelTrailer))
@app.route('/products', methods = ["POST","GET"])
def products_page():
    global bot
    if request.method == "POST":
        product = request.form['product-name']
        if product == "fifth-wheel":
            bot = Scrapper(product=product)
            t = threading.Thread(target=bot.browse,args=("https://www.sanantoniorvs.com/product/fifth-wheel"+"?pagesize=5000",))
            t.start()
            return render_template('products.html', product="Fifth Wheel",msg="ANALYZING STARTED...")
        elif product == "travel-trailer":
            bot = Scrapper(product=product)
            t = threading.Thread(target=bot.browse,args=("https://www.sanantoniorvs.com/product/travel-trailer"+"?pagesize=5000",))
            t.start()
            return render_template('products.html',product="Travel Trailer", msg="ANALYZING STARTED...")
    return render_template('products.html')
up_flag = ''
@app.route('/updates')
def updates():
    data,total,new,removed,flag,product = get_results()
    if product == "fifth-wheel":
        product="Fifth Wheel"
    elif product == "travel-trailer":
        product="Travel Trailer"
        
    if flag == True:
        return jsonify(data=data,product=product,total=total,done=len(data),new=len(new),removed=len(removed),status="Running")
    else:
        return jsonify(data=data,product=product,total=total,done=len(data),new=len(new),removed=len(removed),status="Finished")
def get_results():
    data = bot.allProducts
    total = bot.total
    new = bot.newProducts
    removed = bot.removedProducts
    flag = bot.flag
    product = bot.product
    return data,total,new,removed,flag,product
@app.route('/notifications')
def notifications_page():
    return render_template('notifications.html')
@app.route('/notify')
def notify():
    data = get_notify_results()
    return jsonify(data=data)
def get_notify_results():
    new = bot.newProducts
    removed = bot.removedProducts
    data = new + removed
    return data
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(use_reloader=False)
    
    
