from flask import Flask, render_template, request
import requests

app = Flask(__name__)

url_cap = 'https://rickandmortyapi.com/api/episode'
resp_cap = requests.get(url=url_cap)
data_cap = resp_cap.json()
data_cap = data_cap["results"]

url_cap2 = 'https://rickandmortyapi.com/api/episode/?page=2'
resp_cap2 = requests.get(url=url_cap2)
data_cap2 = resp_cap2.json()
data_cap2 = data_cap2["results"]

data_cap += data_cap2


@app.route('/')
def base():
    return render_template("capitulos.html", len=len(data_cap), capitulos=data_cap)

@app.route('/capitulo/<name>')
def capitulo(name):
    characters = []
    bool = False

    for i in data_cap:
        if name == i["episode"]:
            bool = True
            capitulo = i
            for k in i["characters"]:
                resp_char = requests.get(k)
                data_char = resp_char.json()
                characters.append(data_char)
    if bool == False:
        return "No existe"
    else:
        return render_template("capitulos_name.html", capitulos=capitulo, characters=characters)

@app.route('/personaje/<id>')
def personaje(id):
    episodios = []
    url_char_name = 'https://rickandmortyapi.com/api/character/' + id
    resp_char_name = requests.get(url=url_char_name)
    data_char_name = resp_char_name.json()
    for i in data_char_name["episode"]:
        resp_cap_ = requests.get(url=i)
        data_cap_ = resp_cap_.json()
        episodios.append(data_cap_)
    return render_template("personaje_id.html", capitulos=episodios, characters=data_char_name)

@app.route('/lugar/<id>')
def lugar(id):
    residentes = []
    url_loc = 'https://rickandmortyapi.com/api/location/' + id
    resp_loc = requests.get(url=url_loc)
    data_loc = resp_loc.json()
    for i in data_loc["residents"]:
        resp_res = requests.get(url=i)
        data_res = resp_res.json()
        residentes.append(data_res)
    return render_template("lugar_id.html", res=residentes, loc=data_loc)


@app.route('/search')
def search():
    query = request.args['search']

    capitulos = []
    personajes = []
    lugares = []

    url_name = 'https://rickandmortyapi.com/api/location/?name=' + query
    resp_name = requests.get(url=url_name)
    data_name = resp_name.json()

    if "error" not in data_name:
        for i in range(1, data_name["info"]["pages"] + 1):
            url_name = 'https://rickandmortyapi.com/api/location/?page=' + str(i) + '&name=' + query
            resp_name = requests.get(url=url_name)
            data_name = resp_name.json()
            lugares += data_name["results"]

    url_name = 'https://rickandmortyapi.com/api/character/?name=' + query
    resp_name = requests.get(url=url_name)
    data_name = resp_name.json()

    if "error" not in data_name:
        for i in range(1, data_name["info"]["pages"] + 1):
            url_name = 'https://rickandmortyapi.com/api/character/?page=' + str(i) + '&name=' + query
            resp_name = requests.get(url=url_name)
            data_name = resp_name.json()
            personajes += data_name["results"]

    url_name = 'https://rickandmortyapi.com/api/episode/?name=' + query
    resp_name = requests.get(url=url_name)
    data_name = resp_name.json()

    if "error" not in data_name:
        for i in range(1, data_name["info"]["pages"] + 1):
            url_name = 'https://rickandmortyapi.com/api/episode/?page=' + str(i) + '&name=' + query
            resp_name = requests.get(url=url_name)
            data_name = resp_name.json()
            capitulos += data_name["results"]

    return render_template("buscador.html", capitulos=capitulos, personajes=personajes, lugares=lugares)

if __name__ == "__main__":
    app.run()
