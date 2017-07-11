#! /usr/bin/env python
import pygame
from pygame.locals import *
from sys import exit
import copy
import socket
import fcntl
import struct


def load_pieces():
	pieces = {
		'pw': pygame.image.load('img/Chess_plt60.png').convert_alpha(),
		'pb': pygame.image.load('img/Chess_pdt60.png').convert_alpha(),
		'qw': pygame.image.load('img/Chess_qlt60.png').convert_alpha(),
		'qb': pygame.image.load('img/Chess_qdt60.png').convert_alpha(),
		'rw': pygame.image.load('img/Chess_rlt60.png').convert_alpha(),
		'rb': pygame.image.load('img/Chess_rdt60.png').convert_alpha(),
		'bw': pygame.image.load('img/Chess_blt60.png').convert_alpha(),
		'bb': pygame.image.load('img/Chess_bdt60.png').convert_alpha(),
		'kw': pygame.image.load('img/Chess_klt60.png').convert_alpha(),
		'kb': pygame.image.load('img/Chess_kdt60.png').convert_alpha(),
		'nw': pygame.image.load('img/Chess_nlt60.png').convert_alpha(),
		'nb': pygame.image.load('img/Chess_ndt60.png').convert_alpha(),
	}

	return pieces

def getPosicao(mouseP):
	(x, y) = mouseP
	if (x < 63 or x > 63 * 9 or y < 63 or y > 63 * 9):
		return (-1, -1)
	x = x / 63 - 1
	y = y / 63 - 1
	return (x, y)

def desenhar_peca(peca, pos):
	(i, j) = pos
	x = 63 * j + 61
	y = 63 * i + 61
	if (pos == selec):
		aux = copy.copy(pieces[peca])
		if (tabuleiro[i][j][1] == 'b'): color_replace(aux, (0, 0, 0), (255, 0, 0))
		else: color_replace(aux, (255, 255, 255), (0, 0, 255))
		screen.blit(aux, (x, y))
	else:
		screen.blit(pieces[peca], (x, y))

def iniciar_tabuleiro():
	for i in xrange(8):
		tabuleiro[1][i] = 'pb'
		tabuleiro[6][i] = 'pw'

	tabuleiro[0][0] = 'rb'
	tabuleiro[0][7] = 'rb'
	tabuleiro[7][0] = 'rw'
	tabuleiro[7][7] = 'rw'

	tabuleiro[0][1] = 'nb'
	tabuleiro[0][6] = 'nb'
	tabuleiro[7][1] = 'nw'
	tabuleiro[7][6] = 'nw'

	tabuleiro[0][2] = 'bb'
	tabuleiro[0][5] = 'bb'
	tabuleiro[7][2] = 'bw'
	tabuleiro[7][5] = 'bw'

	tabuleiro[0][3] = 'qb'
	tabuleiro[7][3] = 'qw'

	tabuleiro[0][4] = 'kb'
	tabuleiro[7][4] = 'kw'

def mover_peca(inicio, fim):
	(i0, j0) = inicio
	(i, j) = fim
	if i0 == i and j0 == j:
		return False
	peca = tabuleiro[i0][j0]

	if peca[0] == 'r':
		if i0 == i:
			move = -(j0 - j)/abs(j0 - j)
			for casa in xrange(j0 + move, j, move):
				if tabuleiro[i][casa] != '':
					return False
		elif j0 == j:
			move = -(i0 - i)/abs(i0 - i)
			for casa in xrange(i0 + move, i, move):
				if tabuleiro[casa][j] != '':
					return False
		else:
			return False

	elif peca[0] == 'b':
		if i - j == i0 - j0 or i + j == i0 + j0:
			dx = -(i0 - i)/abs(i0 - i)
			dy = -(j0 - j)/abs(j0 - j)
			x = i0 + dx
			y = j0 + dy
			while x != i and y != j:
				if tabuleiro[x][y] != '':
					return False
				x += dx
				y += dy
		else:
			return False

	elif peca[0] == 'n':
		dx = [-2, -2, -1, -1, 1, 1, 2, 2]
		dy = [-1, 1, -2, 2, -2, 2, -1, 1]
		flag = False
		for k in xrange(8):
			if i == i0 + dx[k] and j == j0 + dy[k]:
				flag = True
		if not flag:
			return False

	elif peca[0] == "q":
		if i0 == i:
			move = -(j0 - j)/abs(j0 - j)
			for casa in xrange(j0 + move, j, move):
				if tabuleiro[i][casa] != '':
					return False
		elif j0 == j:
			move = -(i0 - i)/abs(i0 - i)
			for casa in xrange(i0 + move, i, move):
				if tabuleiro[casa][j] != '':
					return False
		elif i - j == i0 - j0 or i + j == i0 + j0:
			dx = -(i0 - i)/abs(i0 - i)
			dy = -(j0 - j)/abs(j0 - j)
			x = i0 + dx
			y = j0 + dy
			while x != i and y != j:
				if tabuleiro[x][y] != '':
					return False
				x += dx
				y += dy
		else:
			return False

	elif peca[0] == "p":
		dx = 0
		if peca[1] == 'w':
			dx = -1
		else:
			dx = 1

		if i == i0 + dx and j == j0 and tabuleiro[i][j] == '':
			pass
		elif i == i0 + dx and (j == j0 - 1 or j == j0 + 1) and tabuleiro[i][j] != '' and tabuleiro[i][j][1] != tabuleiro[i0][j0][1]:
			pass
		elif tabuleiro[i0][j0][1] == 'w' and i == i0 + 2 * dx and i0 == 6 and tabuleiro[i][j] == '':
			pass
		elif tabuleiro[i0][j0][1] == 'b' and i == i0 + 2 * dx and i0 == 1 and tabuleiro[i][j] == '':
			pass
		else:
			return False

	elif peca[0] == 'k':
		global kw, kb, rbl, rbr, rwl, rwr 
		dx = [-1, -1, -1, 0, 0, 1, 1, 1]
		dy = [-1, 0, 1, -1, 1, -1, 0, 1]
		flag = False
		for k in xrange(8):
			if i == i0 + dx[k] and j == j0 + dy[k]:
				flag = True
		if not flag:
			if j0 - j == 2 and j0 == 4:
				if peca[1] == 'w':
					if tabuleiro[7][1] != '' or tabuleiro[7][2] != '' or tabuleiro[7][3] != '':
						return False
					if rwl or kw:
						return False
					tabuleiro[7][0] = ''
					tabuleiro[7][3] = 'rw'
				else:
					if tabuleiro[0][1] != '' or tabuleiro[0][2] != '' or tabuleiro[0][3] != '':
						return False
					if rbl or kb:
						return False
					tabuleiro[0][0] = ''
					tabuleiro[0][3] = 'rb'
			elif j0 - j == - 2 and j0 == 4:
				if peca[1] == 'w':
					if tabuleiro[7][5] != '' or tabuleiro[7][6] != '':
						return False
					if rwr or kw:
						return False
					tabuleiro[7][7] = ''
					tabuleiro[7][5] = 'rw'
				else:
					if tabuleiro[0][5] != '' or tabuleiro[0][6] != '':
						return False
					if rbr or kb:
						return False
					tabuleiro[0][7] = ''
					tabuleiro[0][5] = 'rb'					
			else:
				return False



	if tabuleiro[i][j] == '' or tabuleiro[i][j][1] != tabuleiro[i0][j0][1]:
		if tabuleiro[i0][j0][0] == 'r':
			if i0 == 0:
				if j0 == 0:
					rbl = True
				elif j0 == 7:
					rbr = True
			else:
				if j0 == 0:
					rwl = True
				elif j0 == 7:
					rwr = True
		elif tabuleiro[i0][j0][0] == 'k':
			if tabuleiro[i0][j0][1] == 'b':
				kb = True
			else:
				kw = True
		tabuleiro[i][j] = tabuleiro[i0][j0]
		tabuleiro[i0][j0] = ''
		if tabuleiro[i][j][0] == 'p':
			if tabuleiro[i][j][1] == 'b' and i == 7:
				tabuleiro[i][j] = 'qb'
			elif i == 0:
				tabuleiro[i][j] = 'qw'
		return True
	return False

def color_replace(surface, find_color, replace_color):
	for x in range(surface.get_size()[0]):
		for y in range(surface.get_size()[1]):
			if surface.get_at([x, y]) == find_color:
				surface.set_at([x, y], replace_color)
	return surface

def desenhar():
	screen.blit(background, (0, 0))
	for i in xrange(8):
		for j in xrange(8):
			if tabuleiro[i][j] != '':
				desenhar_peca(tabuleiro[i][j], (i, j))

	pygame.display.update()
	time_passed = clock.tick(30)

def get_ip_address(ifname):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])


'''
00 01 02 03 04 05 06 07
10 11 12 13 14 15 16 17
20 21 22 23 24 25 26 27
30 31 32 33 34 35 36 37
40 41 42 43 44 45 46 47
50 51 52 53 54 55 56 57
60 61 62 63 64 65 66 67
70 71 72 73 74 75 76 77
'''

tabuleiro = [
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', ''],
	['', '', '', '', '', '', '', '']
]

kb = False
kw = False
rbr = False
rbl = False
rwr = False
rwl = False

op = 2
while op != 0 and op != 1:
	print "Cliente: 0"
	print "Servidor: 1"
	op = input()

if op == 1:
	HOST = ''      # Endereco IP do Servidor
	print "Digite um valor para a porta:"
	PORT = input()            # Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	orig = (HOST, PORT)
	try:
		tcp.bind(orig)
	except Exception as e:
		print "Conexao falhou, por favor, tente novamente."
		exit()
	tcp.listen(1)
	con, cliente = tcp.accept()

else:
	print "Digite o ip do servidor:"
	HOST = raw_input()      # Endereco IP do Servidor
	print "Digite a porta utilizada:"
	PORT = input()            # Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	dest = (HOST, PORT)
	try:
		tcp.connect(dest)
	except Exception as e:
		print "Servidor nao encontrado, tente novamente"
		exit()

pygame.init()

screen = pygame.display.set_mode((626, 626), 0, 32)

background_filename = 'img/background.jpg'
background = pygame.image.load(	background_filename).convert()

#pecas

pieces = load_pieces()

if op == 1:
	pygame.display.set_caption('Ultimate Chess XXI Serv')
else:
	pygame.display.set_caption('Ultimate Chess XXI Client')		

iniciar_tabuleiro()

press = False
selec = (-1, -1)

clock = pygame.time.Clock()

desenhar()

turno = 1
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	if turno == op:
		if not press and pygame.mouse.get_pressed()[0]:
			press = True
		if press and not pygame.mouse.get_pressed()[0]:
			(x, y) = pygame.mouse.get_pos();
			(j, i) = getPosicao((x, y))
			if selec[0] == -1 and selec[1] == -1:
				if tabuleiro[i][j] != '':
					selec = (i, j)
			else:
				if tabuleiro[selec[0]][selec[1]] != '':
					cor = tabuleiro[selec[0]][selec[1]][1]
					if (cor == 'w' and op == 1) or (cor == 'b'and op == 0):
						if mover_peca(selec, (i, j)):
							msg = str(selec) + " " + str((i, j))

							if op == 0:
								tcp.send(msg)
							else:
								con.send(msg)

							desenhar()

							if turno == 1:
								turno = 0
							else:
								turno = 1
				selec = (-1, -1)
			press = False

	if op == 1 and turno == 0:
		msg = con.recv(1024)
		if not msg:
			break
		mover_peca((int(msg[1]), int(msg[4])), (int(msg[8]), int(msg[11])))
		if turno == 1:
			turno = 0
		else:
			turno = 1

	if op == 0 and turno == 1:
		msg = tcp.recv(1024)
		mover_peca((int(msg[1]), int(msg[4])), (int(msg[8]), int(msg[11])))
		if turno == 1:
			turno = 0
		else:
			turno = 1

	desenhar()

if op == 1:
	con.close()

else:
	tcp.close()
