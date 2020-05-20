import datetime
import psycopg2
import psycopg2.extras

from datetime import date
from lib.config import * #@UnusedWildImport


def connectToPostgres():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % (POSTGRES_DATABASE, POSTGRES_USER, POSTGRES_PASSWORD,POSTGRES_HOST)
    print (connectionString)
    try:
        return psycopg2.connect(connectionString)
    except Exception as e:    # BP2 especially this part where you print the exception
        print(type(e))
        print(e)
        print("Can't connect to database")
        return None

# generic execute statement
# select=True if it is a select statement
#        False if it is an insert
#


def execute(input_query, conn, select=True, args=None):
	print ("in execute query")
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	
	results = None
	try: 
		sql = cur.mogrify(input_query, args)   # BP6  never use Python concatenation
		                                  # for database queries
		print("Query going to the database: ", sql)
		cur.execute(sql)
		if select:
			results = cur.fetchall()
		conn.commit()   # BP5  commit and rollback frequently
	except Exception as e:
		print("failed query", sql)
		conn.rollback()
		print(type(e))
		print(e)
	cur.close()      # BP3 Dispose of old cursors as soon as possible
	return results

def all_matches():
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "select match_id, mbn, bet_type, odd, t1name, t2name from currentbetview;"
	maclar = execute(query_string, conn, select=True)
	conn.close()
	return maclar

def get_username(email):
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "select s_name from suser where email = %s;"
	name = execute(query_string, conn, select=True, args= ( [email]  ))
	conn.close()
	return name

def login_check(email, password):
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "select exists(select from suser where email = %s and s_password = %s);"
	exists = execute(query_string, conn, select=True, args= ([email, password]))
	conn.close()
	return exists

def create_user(name, password, email, s_type='player'): # for now insert player type only
	conn = connectToPostgres()
	if conn == None:
		return None
	
	query_string = "insert into suser(s_name, s_password, email, s_type) values(%s, %s, %s, %s);"
	# TODO
	# add a query to insert into player table as well
	execute(query_string, conn, select=False, args=([name, password, email, s_type]))
	conn.close()
def register_check(email):
	conn = connectToPostgres()
	if conn == None:
		return None
	query_string = "select exists(select from suser where email = %s);"
	exists = execute(query_string, conn, select=True, args= ([email]))
	conn.close()
	return exists


def play_bet(list_bets = [{'team1':'fenerbahce', 'team2':'bursa', 'date':'2019-02-19 00:00:00', 'type':'1.5 ALT', 'odd':4.52}], user_id = '1', stake = '10', shared='0'):
	# Check if the connection is succesful
	conn = connectToPostgres()
	
	#get the bets from list_bets

	#example list_bets = [{'team1':'FB', 'team2':'BJK', 'date':'May 3 2020', 'type':'MS1', 'odd':3.1}]
	#get current time 
	currentdate = datetime.datetime.now()
	#create our betslip
	query_string = "insert into betslip values(default , %s ,%s , %s , %s, 1.0  )"
	execute(query_string, conn, select=False, args=( [user_id, stake, shared, currentdate] ))
	
	query_string = "select betslip_id from betslip  where total_odd = 1.0"
	betslip_id = execute(query_string, conn, select=True )


	betslip_length = len(list_bets)
	for i in range(betslip_length):
		team1 = list_bets[i]["team1"]
		team2 = list_bets[i]["team2"]
		date = list_bets[i]["date"]
		match_type = list_bets[i]["type"]
		# select the first team
		query_string = "select team_id from team where name = %s "
		team1_id = execute( query_string, conn, select= True, args = ( [team1] ))
		# select the second team
		query_string = "select team_id from team where name = %s "
		team2_id = execute(query_string, conn, select=True, args = ( [team2] ))
		query_string = "select bet_id from bet natural join match where home_team_id = %s and away_team_id = %s and match.match_date = %s and bet_type = %s"
		bet_id = execute(query_string, conn, select=True , args = ( [ team1_id[0]["team_id"] , team2_id[0]["team_id"] , date , match_type ]  ))
		#selectBet(bet_id[0]["bet_id"] , betslip_id[0]["betslip_id"])

	conn.close()
	#playbet(betslip_id[0]["betslip_id"])