TIE-23500 Web-ohjelmointi

## Projektisuunnitelma

Ryhmän jäsenet:

* Osku Haavisto, 229440
* Tomi Mäkelä, 208990
* Mette Rahunen, 211374

Tarkoituksena olisi toteuttaa kaikki työohjeessa annetut ominaisuudet sekä lisäksi toteuttaa pelien arvostelu viiden tähden systeemillä.
* Tunnistautuminen: Kirjautuminen tehdään sähköpostin avulla ja lisäksi kolmannen osapuolen tunnistautuminen hoidetaan Django - Social Registarion palikan avulla.
* Pelaaja: Pelejä voi hakea eri ryhmistä taikka haun avulla.
* Oma peli: Toteutetaan jos aikaa on jäljellä tarpeeksi.

Aikataulu/toteutusjärjestys:
Backend-osat ensimmäisenä kuntoon ja sitten frontend-puoli. Ensimmäisenä toteutetaan käyttäjien hallinta. Seuraavaksi tehdään developer-osat ja sitten pelaajan/käyttäjän osat.
Huhtikuun alussa on valmiina raakile versio ohjelmistossa, jossa ei ole toteutettu vielä lisäominaisuuksia. Sen jälkeen aletaan lisätä ominaisuuksia ja hiomaan ohjelmistoa palautuskuntoon.

Käytämme kommunikaatioon Slackkia ja Trelloa ja tarpeen tullessa tapaamme koululla.


## Lopullinen palautus

> * What features you implemented and how much points you would like to give to yourself from those? Where do you feel that you were successful and where you had most problems. Give sufficient details, this will influence the non-functional points awarded.
> * How did you divide the work between the team members - who did what?
> * Instructions how to use your application and link to Heroku where it is deployed.
> * If a specific account/password (e.g. game developer) is required to try out and test some aspects of the work, please provide the details.

Toteutimme kaikki pakolliset ominaisuudet ja lisäksi myös joitain lisäominaisuuksia.
* Authentication: Rekisteröinti varmennetaan sähköpostilla. (200/200)
* Basic player functionalities: Kaikki ominaisuudet ovat toteutettu ja pelit löydetään kategorioista.(300/300)
* Basic developer functionalities: Kaikki omaisuudet toteuttettu. (200/200)
* Game/service interaction: Pelitulosten tallennus on toteutettu. (200/200)
* Save/load and resolution feature: Toteutettu. (100/100)
* 3rd party login: Toteutettu Facebookin avulla. (100/100)
* Own game: Yksinkertainen peli toteutettu ([https://gitlab.rd.tut.fi/haavist5/seitti2016_project/blob/master/static_in_pro/our_static/misc/kolikonheitto_peli.html](),
    kaupassa saatavilla nimellä Coin Toss) (100/100)
* Social media sharing: Facebook jako peleille (50/50)

Työn jako:

* Osku: Käyttöliittymän perusrunko, paikallinen autentikaatio
* Tomi: Tietomallin luominen, kehittäjän ja asiakkaan ominaisuudet, pelien lisääminen, maksuintegraatio, pelinäkymä ja social media sharing
* Mette: 3rd party login, oma peli, social media sharing

Linkki herokuun: [http://seitti2016-fogstore.herokuapp.com/]()

### Käyttö
Sivun käyttö on hyvin yksinkertaista. Aluksi rekisteröidytään tai sisäänkirjaudutaan. Sitten, jos käyttäjä on kehittäjä,
voi hän luoda oman yrityksen, johon hän voi lisätä omia pelejään. Kehittäjä voi myös ostaa kaupasta muiden pelejä ja
pelata niitä. Asiakas voi ainostaan käyttää kauppaa, eli ostaa ja pelata pelejä. Ostetut
pelit löytyvät omasta kirjastosta.

Oletusdatassa asetetut käyttäjätunnukset:

* Ylläpitäjä: `admin`/`admin` ([http://seitti2016-fogstore.herokuapp.com/admin]())
* Kehittäjä: `aegames`/`aegames`


### Käyttöönotto muissa tilanteissa
#### Paikallinen
```
git clone git@gitlab.rd.tut.fi:haavist5/seitti2016_project.git
cd seitti2016_project
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata default_categories
python manage.py loaddata default_users
python manage.py loaddata default_companies
python manage.py loaddata default_games
python manage.py runserver
```

#### Heroku
```
git clone git@gitlab.rd.tut.fi:haavist5/seitti2016_project.git
cd seitti2016_project
git checkout heroku-prod
heroku login
heroku create your-heroku-app-name
git push heroku head:master
heroku ps:scale web=1
heroku run python manage.py migrate
```
Heroku saattaa yrittää ajaa eri moduulien migraatiot väärässä järjestyksessä, jolloin yllä oleva komento ei toimi.
Tällöin migraatiot voi ajaa manuaalisesti oikeassa järjestyksessä, mahdolliset virheet viimeistä komentoa huomioimatta:
```
heroku run python manage.py migrate contenttypes
heroku run python manage.py migrate auth
heroku run python manage.py migrate account
heroku run python manage.py migrate admin
heroku run python manage.py migrate contenttypes
heroku run python manage.py migrate auth
heroku run python manage.py migrate gamewebstore
heroku run python manage.py migrate sessions
heroku run python manage.py migrate sites
heroku run python manage.py migrate socialaccount
```

Migraatioiden jälkeen:
```
heroku run python manage.py loaddata default_categories
heroku run python manage.py loaddata default_users
heroku run python manage.py loaddata default_companies
heroku run python manage.py loaddata default_games
heroku open
```
