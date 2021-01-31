import sqlite3
from flask import flash, redirect, url_for, session, render_template

#INIT
conn = sqlite3.connect('users.db', check_same_thread=False)

c = conn.cursor()

foundUser = False

#FUNCTIONS
def commit():
	conn.commit()

def closeConn():
	conn.close()

def resetTable():
	c.execute("DROP TABLE users")
	c.execute("""CREATE TABLE users(
			user text, 
			password text,
			perm int
		)""")
	c.execute("INSERT INTO users VALUES ('admin','admin',1)")
	commit()

def createNewUser(user_,password_,perm_):
	c.execute("INSERT INTO users VALUES (?,?,?)",(user_,password_,perm_))
	commit()

def updateRecords():
	c.execute("""UPDATE users SET user = 'admin'
			WHERE password = 'admin'
		""")
	conn.commit()

def deleteRecords():
	c.execute("""DELETE from users WHERE user = (?)""")
	commit()

def all3users():
	c.execute("""SELECT * FROM users""")
	users = c.fetchall()
	return users

def checkUser(user,password):
	c.execute("""SELECT user FROM users
				WHERE user = ?
		""",(user,))
	if len(c.fetchall()) == 0:
		flash("NOT FOUND")
		return False
	else:
		c.execute("""SELECT password FROM users
				WHERE password = ?
		""",(password,))
		if len(c.fetchall()) == 0:
			flash("NOT FOUND")
			return False
		else:
			c.execute("""SELECT perm FROM users WHERE password = ?
		""",(password,))
			permLevel = c.fetchone()
			permLevel = permLevel[0]
			if permLevel == 1:
				session['admin'] = user
				return 1
			if permLevel == 2:
				session['user'] = [user,permLevel]
				return 2
			else:
				flash("NOT ALL")
				return False
			

def main():
	c.execute("SELECT * FROM users")

	items = c.fetchall()

	print(items)

commit()