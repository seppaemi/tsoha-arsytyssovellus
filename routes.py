from app import app
from flask import render_template, request, redirect
import users, regions, messages
from db import db

@app.route("/")
def index():
    list = regions.get_list_region()
    user_name = users.get_user_name()
    if user_name == False:
        return render_template("index.html", count=len(list), regions=list)
    if users.is_admin():
        is_admin = True
        return render_template("index.html", count=len(list), regions=list, is_admin=is_admin, user_name=user_name)
    else: 
        is_admin = False
        return render_template("index.html", count=len(list), regions=list, user_name=user_name)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) == 0 or len(password) == 0:
            return render_template("login.html", error1="Virheellinen Käyttäjätunnus tai salasana")
        elif users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", error1="Virheellinen käyttäjätunnus tai salasana")
    
@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if len(username) == 0 and len(password1) == 0:
            return render_template("register.html", error2="Anna käyttäjätunnus", error3="Anna salasana")
        if len(username) == 0:
            return render_template("register.html", error2="Anna käyttäjätunnus")
        if len(password1) == 0:
            return render_template("register.html", error3="Anna salasana")
        if password1 != password2:
            return render_template("register.html", error1="Salasanojen tulee olla samat")
        
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("register.html", error4=f"Käyttäjänimi {username} on varattu.")

@app.route("/edit_message/<string:message_id>")
def edit_message(message_id):
    user_name = users.get_user_name()
    message_creator = messages.get_message_creator_name(message_id)
    if user_name == message_creator:
        message_content = messages.get_message(message_id)
        return render_template("edit_message.html", message_content=message_content, message_id=message_id, user_name=user_name)
    elif user_name == False:
        return redirect("/")
    else:
       return redirect("/")
  
@app.route("/send_message_edit", methods=["GET","POST"])
def send_message_edit():
    check_csrf = users.check_csrf()
    edited_message  = request.form["content"]
    message_id = request.form["message_id"]
    if len(edited_message) <= 0:
        return render_template("edit_message.html", error1="Viesti ei voi olla tyhjä")
    if len(edited_message) > 5000:
        return render_template("edit_message.html", error2="Viesti on liian pitkä")
    messages.edit_message(message_id,edited_message)
    region_content = regions.get_region_content(message_id)
    region_creation_time = regions.get_region_sent(region_content,message_id)
    return redirect("/messages/"+ str(region_content) + "/" + str(region_creation_time))

@app.route("/delete_message/<string:message_id>")
def delete_message(message_id):
    user_name = users.get_user_name()
    message_creator_name = messages.get_message_creator_name(message_id)
    if user_name != message_creator_name:
       return redirect("/")
    message_content = messages.get_message(message_id)
    region_content = regions.get_region_content(message_id)
    region_creation_time = regions.get_region_sent(region_content,message_id)
    return render_template("delete_message.html", message_content=message_content, message_id=message_id,region_content=region_content,region_creation_time=region_creation_time)

@app.route("/deletion_confirmation/<string:message_id>", methods=["GET", "POST"])
def deletion_confirmation(message_id):
    check_csrf = users.check_csrf()
    region_content = regions.get_region_content(message_id)
    region_creation_time = regions.get_region_sent(region_content,message_id)
    messages.delete_message(message_id)
    return render_template("deletion_confirmation.html", region_content=region_content,region_creation_time=region_creation_time)


@app.route("/messages/<string:content>/<string:time>", methods=["GET"])
def get_list_message(content,time):
    user_name = users.get_user_name()
    admin = users.is_admin()
    region_content = content
    region_creation_time = time
    list = messages.get_list_message(region_content, region_creation_time)
    list_info = messages.get_list_info()
    return render_template("messages.html", count=len(list), messages=list, infos = list_info, images=list_images, region_content=region_content, time=time, user_name=user_name, is_admin=admin)

@app.route("/admin")
def admin():
    user_name = users.get_user_name()
    if user_name == False:
        return redirect("/")
    if users.is_admin():
        is_admin = True
        return render_template("admin.html", user_name=user_name)
    else: 
        is_admin = False
        return redirect("/")

@app.route("/new_region")
def new_region():
    user_name = users.get_user_name()
    admin = users.is_admin()
    return render_template("new_region.html", user_name=user_name, is_admin=admin)

@app.route("/send_region", methods=["POST"])
def send_region():
    check_csrf = users.check_csrf()
    title = request.form["title"]
    if len(title) <= 0:
        return render_template("error.html", message="Aloituksen nimi ei voi olla tyhjä")
    if len(title) > 100:
        return render_template("error.html", error="Aloituksen nimi on liian pitkä")
    elif regions.send_region(title):
        return redirect("/")
    else:
        return render_template("error.html", message="Lähetys ei onnistunut")

@app.route("/new_message/<string:region_content>/<string:time>")
def new_message(region_content,time):
    user_name = users.get_user_name()
    admin = users.is_admin()
    return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, is_admin=admin)


@app.route("/send_message/<string:region_content>/<string:time>", methods=["POST"])
def send_message(region_content,time):
    check_csrf = users.check_csrf()
    user_name = users.get_user_name()
    message_content = request.form["content"]
    info_date = request.form["date"]
    info_time = request.form["time"]
    location = request.form["name"]
    if len(message_content) == 0 and len(info_date) == 0 and len(info_time)==0 and len(location) == 0:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error1="Viesti ei voi olla tyhjä", error3="Lisää vielä päivämäärä, kiitos!", error4="Lisää vielä kellonaika, kiitos!", error5="Lisää vielä sijainti, kiitos!")
    if len(message_content) <= 0:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error1="Viesti ei voi olla tyhjä")
    if len(message_content) > 5000:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error2="Viesti on liian pitkä")
    if len(info_date) <= 0:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error3="Lisää vielä päivämäärä, kiitos!")
    if len(info_time) <= 0:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error4="Lisää vielä kellonaika, kiitos!")
    if len(location) <= 0:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error5="Lisää vielä sijainti, kiitos!")
    if messages.send_message(message_content, region_content,time, info_date=info_date,info_time=info_time,location=location) != False:
        return redirect("/messages/" + str(region_content) + "/" + str(time))
    else:
        return render_template("new_message.html", region_content=region_content, time=time, user_name=user_name, error6="Viestin lähetys ei onnistunut")

@app.route("/query")
def query():
    user_name = users.get_user_name()
    is_admin = users.is_admin()
    return render_template("query.html", is_admin=is_admin, user_name=user_name)

@app.route("/result")
def result():
    user_name = users.get_user_name()
    query = request.args["query"]
    search_results = messages.search(query)
    infos = messages.get_list_info()
    is_admin = users.is_admin()
    if len(search_results) == 0:
        return render_template("query.html", is_admin=is_admin, error=f"Hakusanalla '{query}' ei tuloksia.")
    return render_template("result.html", search_results=search_results, user_name=user_name, is_admin=is_admin, infos=infos)