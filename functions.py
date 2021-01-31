def register(name,password):
	name = name.replace(' ','')
	password = password.replace(' ','')

	users = open('users','a')
	users.write('\n' + name)
	users.close()

	passwords = open('passwords','a')
	passwords.write('\n' + password)
	passwords.close()

def reload_files():
	users_file = open('users','r')
	users = users_file.read()
	users = users.strip('\n')
	users_file.close()

	passwords_file = open('passwords','r')
	passwords = passwords_file.read()
	passwords = passwords.strip('\n')
	passwords_file.close()