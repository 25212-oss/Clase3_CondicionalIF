 
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secreto123"

# usuario de prueba
USUARIO = "erikelpro"
PASSWORD = "67"

# lista de personas
personas = []

# LOGIN
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("usuario")
        pwd = request.form.get("password")

        if user == USUARIO and pwd == PASSWORD:
            session["usuario"] = user
            return redirect(url_for("buscador"))
        else:
            return render_template("login.html", error="Datos incorrectos")

    return render_template("login.html")


# BUSCADOR
@app.route("/buscador", methods=["GET", "POST"])
def buscador():
    if "usuario" not in session:
        return redirect(url_for("login"))

    global personas

    if request.method == "POST":
        nombre = request.form.get("nombre")
        edad = request.form.get("edad")

        if nombre and edad:
            personas.append({
                "nombre": nombre,
                "edad": edad
            })

    busqueda = request.args.get("buscar")

    if busqueda:
        resultados = [
            p for p in personas
            if busqueda.lower() in p["nombre"].lower()
        ]
    else:
        resultados = personas

    return render_template("buscador.html", personas=resultados)


# LOGOUT
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)