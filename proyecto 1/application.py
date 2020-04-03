import os
from flask import Flask, render_template, request, session, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import timedelta

app = Flask(__name__)

app.secret_key = "chuy"
app.permanent_session_lifetime=timedelta(minutes=60)
engine = create_engine("postgres://oxiustss:7_u2OkQ8wyeI2I3q0ziR7nyWfjQJIWlL@balarama.db.elephantsql.com:5432/oxiustss")
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == 'POST':
        usuario = request.form.get("username")
        nombre = request.form.get("name")
        correo = request.form.get("email")
        contrasena = request.form.get("pass")
        contrasenar = request.form.get("repeatpass")
        if(usuario and contrasena and correo and nombre and contrasenar):
            if(contrasenar == contrasena):
                try:
                    db.execute("INSERT INTO usuarios (usuario, nombre, correo,contrasena) VALUES (:usuario, :nombre, :correo, :contrasena)", {"usuario": usuario.strip(), "nombre": nombre.strip(),"correo": correo.strip(), "contrasena": contrasena.strip()})               
                    db.commit()
                    return redirect('/')
                except:
                    db.close()
                    return render_template("index.html")
            else:
                return render_template("index.html")
        else:           
            return render_template("index.html")
    else:
        return render_template("index.html")
@app.route("/loguear", methods=["GET","POST"])
def loguear():
    if request.method == 'POST':
        usuario = request.form.get("username")
        contrasena = request.form.get("pass")
        if(usuario and contrasena):
            usuariodb = db.execute("SELECT usuario,contrasena,id FROM usuarios WHERE usuario = :usuario",{"usuario": usuario}).fetchall()
            if(not usuariodb):
                return render_template("loguear.html",)
            elif(usuario == usuariodb[0][0] and contrasena == usuariodb[0][1]):
                session.permanent = True
                session['usuario'] = usuario
                session['id'] = usuariodb[0][2]
                return redirect('/buscarlibros')     
            else:
                return render_template("loguear.html")
        else:
            return render_template("loguear.html")
    else:
        return render_template("loguear.html")


@app.route("/buscarlibros", methods=["GET","POST"])
def buscarlibros():
    if request.method == 'POST':
        busqueda = request.form.get('buscarlibro')
        libros = db.execute("SELECT * FROM libros WHERE isbn like :busqueda OR year like :busqueda OR title like :busqueda OR author like :busqueda",{"busqueda": "%"+busqueda.strip()+"%"}).fetchall()
        return render_template("buscarlibros.html",libros=libros)
    else:
        return render_template("buscarlibros.html")
@app.route("/libro/<libro_isbn>", methods=["GET","POST"])
def libro(libro_isbn):
    librof = db.execute("SELECT * FROM libros WHERE isbn = :libro_isbn", {"libro_isbn": libro_isbn}).fetchall()
    isbn =  librof[0][0]
    title = librof[0][1]
    author =  librof[0][2]
    year = librof[0][3]
    resenas = db.execute("SELECT rev.resena, usr.nombre, rev.calif FROM resenas rev INNER JOIN usuarios usr on usr.id = rev.id WHERE rev.isbn = :isbn;", {"isbn": librof[0][0]}).fetchall()
    if request.method == 'POST':
        resena = request.form.get('resena')
        try:
            calif = request.form['star']
        except:
            calif = 0
        if(resena):
            db.execute("INSERT INTO resenas (resena, calif, id, isbn) VALUES (:resena, :calif, :usuario, :isbn)", {"resena": resena, "calif": calif,"usuario": session['id'],"isbn": librof[0][0]})
            db.commit()
            resenas = db.execute("SELECT rev.resena, usr.nombre, rev.calif FROM resenas rev INNER JOIN usuarios usr on usr.id = rev.id WHERE rev.isbn = :isbn;", {"isbn": librof[0][0]}).fetchall()
            return render_template("libro.html",resenas=resenas,librof=librof)
        else:
            resenas = db.execute("SELECT rev.resena, usr.nombre, rev.calif FROM resenas rev INNER JOIN usuarios usr on usr.id = rev.id WHERE rev.isbn = :isbn;", {"isbn": librof[0][0]}).fetchall()
            return render_template("libro.html",resenas=resenas,librof=librof)
    else:
        return render_template("libro.html",librof=librof,resenas=resenas)
@app.route("/logout", methods=["GET","POST"])
def logout():
    session.pop('usuario')
    return redirect('/')   
    
    
    
    
    
    
    
    
    