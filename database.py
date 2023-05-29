import mysql.connector
from mysql.connector import errorcode

print("Conecting...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='root'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Invalid credentials, check the user and password')
      else:
            print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# criando tabelas
TABLES = {}
TABLES['Games'] = ('''
      CREATE TABLE `games` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) NOT NULL,
      `category` varchar(40) NOT NULL,
      `plataform` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
      CREATE TABLE `users` (
      `name` varchar(20) NOT NULL,
      `nickname` varchar(10) NOT NULL,
      `password` varchar(30) NOT NULL,
      PRIMARY KEY (`nickname`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
      tabela_sql = TABLES[tabela_nome]
      try:
            print('Creating Table {}:'.format(tabela_nome), end=' ')
            cursor.execute(tabela_sql)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Alredy Exists')
            else:
                  print(err.msg)
      else:
            print('OK')

# insert Users
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
users = [
      ("admin", "o admin", "admin"),
      ("user", "usuario", "user")
]
cursor.executemany(user_sql, users)

cursor.execute('select * from jogoteca.users')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# insert Games
games_sql = 'INSERT INTO games (name, category, plataform) VALUES (%s, %s, %s)'
games = [
      ('Tetris', 'Puzzle', 'Atari'),
      ('God of War', 'Hack n Slash', 'PS2'),
      ('Mortal Kombat', 'Fight', 'PS2'),
      ('Valorant', 'FPS', 'PC'),
      ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
      ('Super Mario', 'Plataform', 'Super Nintendo')
]

cursor.executemany(games_sql, games)

cursor.execute('select * from jogoteca.games')
print(' -------------  Games:  -------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commit the changes
conn.commit()

cursor.close()
conn.close()