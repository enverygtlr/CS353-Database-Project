
# Home page!
def play_bet(list_bets, user_id, stake, shared='private'):
    '''
        example list_bets = [{'team1':'FB', 'team2':'BJK', 'date':'May 3 2020', 'type':'MS1', 'odd':3.1}]
    '''
    def create_betslip(user_id, stake, shared, total_odd=1, bet_date='now'):
        return 'betslip_id'

    def insert_bet_to_betslip(team1, team2, match_date, betslip_id):
        ''' create a new bet & insert it to a new '''

    total_odd = len(list_bets)
    betslip_id = create_betslip(user_id, stake, shared, total_odd, 'now') # check balance and stake

    for bet in list_bets:
        insert_bet_to_betslip(bet.team1, bet.team2, bet.date, betslip_id)

    return 'success' if True else 'failure'

def get_user_balance(user_id):
    return {'balance':234}

def get_bet_table(sport_branch, league, min_date): 
    ''' We have given the dummy data! '''
    table_content = [{'team1':'FB', 'team2':'BJK', 'date':'May 3 2020', 'odds':[3.1, 1.15, 1.45, 2.60, 3.0]}]
    table_titles = ['MS1', 'MSX', '25ALT', '25UST', 'KGVAR']
    return table_content, table_titles

# User plofile
def get_all_followers(user_id):
    return [{'user_id':1, 'username':'ahmet'}]

def get_all_followee(user_id):
    return [{'user_id':2, 'username':'mehmet'}]

def get_all_betslips(user_id):
    return 'list bets'

def update_shared_status(betslip_id):
    pass

def get_user_betslips(user_id, include_private=False):
    # herhangi bi userin shared content
    return [
        {
            'betslip_id':0,
            'stake':1,
            'total_odd':3,
            'betslip_date':'May 3 2020',
            'bets':[
                {
                    'team1':'FB', 
                    'team2':'BJK', 
                    'bet_type':'25ALT', 
                    'match_date':4, 
                    'mnbn':4, 
                    'odd':3.1
                }
            ]
        }
    ]

# Admin settings
def delete_user(user_id):
    pass

def update_odds(team1, team2, match_date, type, new_odd):
    # new_odd = if none then cancels the odd
    pass

# Editor
def editor_suggest(user_id, suggestion_content, trust_point, bet):
    '''
{'team1':'FB', 'team2':'BJK', 'date':'May 3 2020', 'type':'MS1', 'odd':3.1}
    '''
    pass

def get_editor_suggestions_by_user_id(user_id):
    # bizim userin takip ettigi editorlerin suggestionlari!
    return [
        {
            'team1':'FB', 
            'team2':'BJK', 
            'bet_type':'25ALT', 
            'match_date':4, 
            'mnbn':4, 
            'odd':3.1
        }
    ]

def get_editor_suggestions_by_editor_id(editor_id):
    # bizim editorun suggestionlari!
    return [
        {
            'team1':'FB', 
            'team2':'BJK', 
            'bet_type':'25ALT', 
            'match_date':4, 
            'mnbn':4, 
            'odd':3.1
        }
    ]


# Search
def search_by_username(username):
    return [
        {
            'username':'enverygtlr', 
            'user_id':212,
            'followers':5000000, 
            'following':0}
    ]

def follow_user(user_id, requested_user_id):
    return True or False

