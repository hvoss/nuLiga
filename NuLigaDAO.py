
import datetime
import urllib.request
from model import Club, Game, Hall, League, Person, Staffel, Team


class NuLigaDAO:

    def __init__(self):
        self.clear()

    def clear(self):
        self.lastUpdate = None
        self.halls = {}
        self.leagues = {}
        self.teams = {}
        self.staffeln = {}
        self.clubs = {}
        self.referees = {}
        self.games = []

    def update(self, delta):
        if self.lastUpdate is None or (self.lastUpdate + delta) < datetime.datetime.now():
            self.clear()
            self.lastUpdate = datetime.datetime.now()
            self.readFile("https://bremerhv-handball.liga.nu/cgi-bin/WebObjects/nuLigaDokumentHBDE.woa/wa/nuDokument?dokument=RegionMeetingsFOP&championship=HVN+2017%2F18")
            self.readFile("https://bremerhv-handball.liga.nu/cgi-bin/WebObjects/nuLigaDokumentHBDE.woa/wa/nuDokument?dokument=RegionMeetingsFOP&championship=Bremer+HV+2017%2F18")

    def readFile(self, fileName):
        response = urllib.request.urlopen(fileName)
        data = response.read()      # a `bytes` object
        text = data.decode('iso-8859-1') # a `str`; this step can't be used if data is binary

        for row in text.strip().split("\n")[1:]:
            try:
                cells = row.split(";")
                goals = cells[10].split(":")
                halfGoals = cells[11].split(":")

                staffel = self.createStaffel(cells[7])
                homeHalfGoals = halfGoals[0]
                guestHalfGoals = halfGoals[1]
                firstRefereeClub = self.createClub(cells[13])
                secondRefereeClub = self.createClub(cells[15])

                game = Game(no=cells[5], timestamp=datetime.datetime.strptime(cells[1]+cells[2], "%d.%m.%Y%H:%M"), hall=self.createHall(cells[3], cells[4]), league=self.createLeague(cells[6]), staffel=staffel, homeTeam=self.createTeam(staffel, cells[8]), guestTeam=self.createTeam(staffel, cells[9]), homeGoals=goals[0], guestGoals=[1], homeHalfGoals=halfGoals[0], guestHalfGoals=halfGoals[1], firstReferee=self.createReferee(firstRefereeClub, cells[12]), secondReferee=self.createReferee(secondRefereeClub, cells[14]))
                self.games.append(game)
            except Exception as e:
                print(row)
                raise e


    def createHall(self, id, name):
        if id in self.halls:
            hall = self.halls[id]
        else:
            hall = Hall(id, name)
            self.halls[id] = hall
        return hall

    def createLeague(self, name):
        if name in self.leagues:
            league = self.leagues[name]
        else:
            league = League(name)
            self.leagues[name] = league
        return league

    def createClub(self, name):
        if name.strip() == "":
            return None

        if name in self.clubs:
            club = self.clubs[name]
        else:
            club = Club(name)
            self.clubs[name] = club
        return club

    def createStaffel(self, name):
        if name in self.staffeln:
            staffel = self.staffeln[name]
        else:
            staffel = Staffel(name)
            self.staffeln[name] = staffel
        return staffel

    def createTeam(self, staffel, name):
        team = Team(staffel, name)
        if team in self.teams:
            team = self.teams[team]
        else:
            self.teams[team] = team
        return team

    def createReferee(self, club, name):
        if club is None or name.strip() == "":
            return None

        referee = Person(club, name)
        if referee in self.referees:
            referee = self.referees[referee]
        else:
            self.referees[referee] = referee
        return referee
