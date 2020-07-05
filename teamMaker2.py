import itertools
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

SPREADSHEET_ID = '1c2Kvc3y1GrF9EFqAKvPoRU8NmFV_exCrAeCTrmDct2Y'
ELOS_RANGE = 'TEST!A2:ZZ12'
TEAMS_RANGE = 'TEST!A16:ZZ26'

class Sheets(object):
    def __init__(self):
        self._creds = self.get_credentials()
        service = build('sheets', 'v4', credentials=self._creds)
        self._sheets = service.spreadsheets()
        
    def get_credentials(self):
        """Sets up credentials to be able to access the google sheet.

        The first time this is called, this method will open a
        web page for the user to sign in. After signing in, a
        token.pickle file will be created to remember the sign-in, so
        that future runs of the program no longer require signing in.
        """
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def get_elos(self):
        """Reads the latest ELO values from the spreadsheet.

        ELO values are return as a {name: ELO} dictionary.
        """
        result = self._sheets.values().get(spreadsheetId=SPREADSHEET_ID,
                                           range=ELOS_RANGE).execute()
        values = result.get('values', [])
        if not values:
            raise RuntimeError('No elo data found.')

        elos = {}
        for row in values:
            name = row[0]
            elos[name] = int(row[-1])
        return elos 
        
    def get_players(self):
        """Returns the list of players to calculate teams for.

        This is determined by looking at the "Team" rows of the
        spreadsheet, and choosing all players with a "?" in the
        last column.
        """
        result = self._sheets.values().get(spreadsheetId=SPREADSHEET_ID,
                                           range=TEAMS_RANGE).execute()
        values = result.get('values', [])
        if not values:
            raise RuntimeError('No team data found.')
        
        players = []
        last_column = max(len(row) for row in values) - 1
        for row in values:
            if last_column < len(row) and row[last_column] == '?':
                players.append(row[0])
        return players


class TeamChooser(object):
    def __init__(self, elos):
        self._elos = elos

    def team_score(self, players):
        return sum(self._elos[p] for p in players)

    def print_team(self, team_index, team):
        print("  Team {} ({}):".format(team_index, self.team_score(team)))
        for p in team:
            print("    {} ({})".format(p, self._elos[p]))

    def show_best_teams(self, players, num_teams=2, results_to_show=3):
        results = set()  # (team_score_difference, team_1, team_2)
        for order in itertools.permutations(players):
            # Choose teams by deciding positions at which to split the permutation
            for inds in itertools.combinations(range(len(players)), num_teams-1):
                inds = (0,) + inds + (len(players),)
                teams = [ order[inds[i]:inds[i+1]] for i in range(num_teams) ]
                scores = [ self.team_score(team) for team in teams ]
                mean = sum(scores) / len(scores)
                unfairness = sum(abs(score-mean) for score in scores)
                # Use a set to deduplicate equivalent teams.
                # Using frozenset instead of set because frozenset, unlike set, is hashable
                results.add((unfairness, frozenset(frozenset(team) for team in teams)))
        for diff, teams in sorted(results)[:results_to_show]:
            print("----- Result with unfairness {} -----".format(diff))
            for i, team in enumerate(teams):
                self.print_team(i+1, team)

num_teams = 2
gaming_players = ['Arno', 'Will', 'Wang', 'JZ', 'Jind', 'Drew', "Mike"] 

sheets = Sheets()
elos = sheets.get_elos()
players = sheets.get_players()
print(elos)
print(players)

chooser = TeamChooser(elos)
chooser.show_best_teams(players, num_teams)


