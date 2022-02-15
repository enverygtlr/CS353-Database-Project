import psycopg2
import psycopg2.extras


def connectToPostgres():
    connectionString = 'dbname=%s user=%s password=%s host=%s' % ('bet', 'postgres', 'postgres','localhost')
    try:
        return psycopg2.connect(connectionString)
    except Exception as e:    # BP2 especially this part where you print the exception
        print(type(e))
        print(e)
        print("Can't connect to database")
        return None

def execute(input_query, conn, select=True, args=None):
	cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
	
	results = None
	try: 
		sql = cur.mogrify(input_query, args)   # BP6  never use Python concatenation
		                                  # for database queries
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

def editor_suggests(editor_id = '1' , bet_id = "4" , comment = "cok iyi bet" , trust = '20'):
    conn = connectToPostgres()
    #get the match id
    selectEditorQuery = f''' 
        select user_id, bet_id
        from editor_suggests
        where user_id = {editor_id} and bet_id = {bet_id};
    '''
    similiarsuggests = execute(selectEditorQuery, conn, select=True)
    if len(similiarsuggests) == 0:
        execute("insert into editor_suggests values(%s , %s , %s , %s ) ",conn , select = False, args=([bet_id , editor_id , trust, comment] ))
    else:
        print("you already suggested one bet from the match")


editor_suggests(10,65, 'oynayin ulen', 10)