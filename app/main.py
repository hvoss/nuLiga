# Copyright 2015 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging
from model import Club, Game, Hall, League, Person, Staffel, Team
from NuLigaDAO import NuLigaDAO

from flask import Flask
from flask import render_template
from flask import request


import datetime

app = Flask(__name__)
nuLigaDAO = NuLigaDAO()

@app.route('/Vereinsansetzungen/<string:refereeClub>')
def referees(refereeClub):
    nuLigaDAO.update(datetime.timedelta(minutes=60))
    mygames = [g for g in nuLigaDAO.games if g.isMyGame(refereeClub)]
    mygames.sort()

    renderRefereeClubs = request.args.get('renderRefereeClubs') is not None

    clubs, selectedClub = findClubWithMostReferees(mygames)

    if len(mygames) == 0:
        return render_template('KeineSpieleGefunden.html', searchName=refereeClub)
    elif isClubRefereeForAllGames(selectedClub, mygames):
        return render_template('Vereinsansetzungen.html', selectedClub=selectedClub, games=mygames, renderRefereeClubs=renderRefereeClubs)
    else:
        return render_template('ZuVieleVereine.html', clubs=clubs, searchName=refereeClub)

def findClubWithMostReferees(games):
    clubs = {}
    for g in games:
        if g.firstReferee.club not in clubs:
            clubs[g.firstReferee.club] = 1
            continue
        else:
            clubs[g.firstReferee.club] = clubs[g.firstReferee.club] + 1
            continue
        if g.secondReferee is not None:
            if g.secondReferee.club not in clubs:
                clubs[g.secondReferee.club] = 1
                continue
            else:
                clubs[g.secondReferee.club] = clubs[g.secondReferee.club] + 1
                continue

    clubWithMostReferees = None
    numOfMostReferees = 0
    for c, num in clubs.items():
        if num > numOfMostReferees:
            numOfMostReferees = num
            clubWithMostReferees = c

    return (clubs, clubWithMostReferees)

def isClubRefereeForAllGames(club, games):
    print(club)
    for g in games:
        count = 0;
        if g.firstReferee is not None:
            if g.firstReferee.club == club:
                count = count + 1
        if g.secondReferee is not None:
            if g.secondReferee.club == club:
                count = count + 1
        if count == 0:
            print(g.firstReferee)
            print(g.secondReferee)
            return False
    return True

@app.route('/update')
def update():
    nuLigaDAO.update(datetime.timedelta(minutes=0))
    return "update successfully"

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500




if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END app]
