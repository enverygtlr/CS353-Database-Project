from flask import redirect, request


def redirect_last(default='/'):
    if request.referrer is None:
        return redirect(default)
    return redirect(request.referrer)


def convert_smatch(match):
    total = []

    for bet in match['bets']:
        converted = {
            'match_id':match['match_id'],
            'branch_name':match['branch_name'],
            'league_name':match['league_name'],
            'match_date':str(match['match_date']),
            'home_score':match['home_score'],
            'away_score':match['away_score'],
            't1name':match['t1name'],
            't2name':match['t2name'],
            'mbn':bet['mbn'],
            'bet_type':bet['bet_type'],
            'cancelled':True if bet['cancelled'] != 0 else False,
            'odd':float(bet['odd']),
            'odd_timestamp':str(bet['odd_timestamp']),
        }
        total.append(converted)
    
    return total

def validate_addition(selected, row, col, matches):
    pass