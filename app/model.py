class Game:
    def __init__(self, no, timestamp, hall, league, staffel, homeTeam, guestTeam, homeGoals, guestGoals, homeHalfGoals, guestHalfGoals, firstReferee, secondReferee):
        self.no = no
        self.timestamp = timestamp
        self.hall = hall
        self.league = league
        self.staffel = staffel
        self.homeTeam = homeTeam
        self.guestTeam = guestTeam
        self.homeGoals = homeGoals
        self.guestGoals = guestGoals
        self.homeHalfGoals = homeHalfGoals
        self.guestHalfGoals = guestHalfGoals
        self.firstReferee = firstReferee
        self.secondReferee = secondReferee

    def __repr__(self):
        return "%s, " % (self.no)

    def __lt__(self, other):
         return self.timestamp < other.timestamp

    def isMyGame(self, clubname):
        if self.firstReferee is not None:
            if self.firstReferee.club.name.find(clubname) > -1:
                return True

        if self.secondReferee is not None:
            if self.secondReferee.club.name.find(clubname) > -1:
                return True

    def toCSV(self):
        return "%s;%s;%s;%s;%s;%s;%s;%s" % (self.timestamp.strftime("%d.%m.%Y"), self.timestamp.strftime("%H:%M"),self.no,self.staffel.name,self.homeTeam.name,self.guestTeam.name,self.firstReferee.name,self.secondReferee.name)

class Hall:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class League:
    def __init__(self, name):
        self.name = name


class Staffel:
    def __init__(self, name):
        self.name = name

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        return (self.name) == (other.name)

class Club:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

class Person:
    def __init__(self, club, name):
        self.club = club
        self.name = name

    def __repr__(self):
        return "%s (%s)" % (self.name, self.club)

    def __hash__(self):
        return hash((self.club, self.name))

    def __eq__(self, other):
        return other is not None and ((self.club, self.name) == (other.club, other.name))

class Team:
    def __init__(self, staffel, name):
        self.staffel = staffel
        self.name = name

    def __hash__(self):
        return hash((self.staffel, self.name))

    def __eq__(self, other):
        return (self.staffel, self.name) == (other.staffel, other.name)
