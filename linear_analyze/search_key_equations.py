# coding=utf-8

__author__ = "rockosov@gmail.com"

import sys
sys.path.append( "../" )

import config as cfg
import bits_ops as bops

##
# @brief получает пары открытый текст - шифр-текст из файла save.txt
#
# @param filename	[ in ] - имя файла
#
# @return список таких пар
def get_texts( filename ):
	try:
		save = open( filename, "r" )
	except:
		print "Can't open file " + filename
		return []
	result = list()
	for line in save:
		res = line.split( " --- " )
		temp = list()
		for value in res:
			if value != '\r\n' and value != '':
				temp.append( int( value, 2 ) )
		result.append( temp )
	out = list()
	for i in range( len( result ) ):
		if result[ i ] == []:
			continue
		temp = list()
		for j in range( len( result[ i ] ) )[::2]:
			current = ( result[ i ][ j ] << cfg.HALF_BLOCK_SIZE ) | result[ i ][ j + 1 ]
			temp.append( current )
		out.append( temp )
	save.close()
	return out

##
# @brief ищет количество таких текстов, что Xi + Yi = 0
#
# @param texts		[ in ] - список пар X-Y
# @param analogs	[ in ] - аналоги
# @param NTexts		[ in ] - общее количество текстов
#
# @return скорректированные аналоги 
def search_num_right_texts( texts, analogs, NTexts ):
	analogs_with_num = list()
	for analog in analogs:
		current_num = 0
		for text in texts:
			result = 0
			for i in analog[ 0 ]:
				result ^= bops.get_bit( text[ 0 ], cfg.BLOCK_SIZE - i ) ^ bops.get_bit( text[ 1 ], cfg.BLOCK_SIZE - i )
			if result == 0:
				current_num += 1
		if abs( ( NTexts / 2 ) - current_num ) >= 50:
			analogs_with_num.append( [ current_num, analog ] )
				
	return analogs_with_num

##
# @brief ищет уравнения, содержащие K
#
# @param analogs	[ in ] - скорректированные аналоги
# @param NTexts		[ in ] - количество текстов всего
#
# @return 
def search_equations( analogs, NTexts ):
	equations = list()
	for current in analogs:
		num, analog = current
		right_part = 0
		if num < NTexts / 2:
			if analog[ 3 ][ 2 ] > 0.5:
				right_part = 1
			else:
				right_part = 0
		else:
			if analog[ 3 ][ 2 ] > 0.5:
				right_part = 0
			else:
				right_part = 1
		temp = list()
		temp.append( sorted( analog[ 2 ] ) )
		temp.append( right_part )
		equations.append( temp )
	return equations
			

##
# @brief поиск уравнений с K 
#
# @param analogs	[ in ] - аналоги всех блоков
#
# @return список уравнений
def search( analogs ):
	fb_analogs, sb_analogs, tb_analogs = analogs
	equations = list()
	texts = get_texts( cfg.FILENAME_COR_TEXTS )
	NTexts = len( texts )

	print NTexts

	print "\nANALOGS WITH NUM OF TEXTS:"
	print "\nFirst block:"
	fb_analogs = search_num_right_texts( texts, fb_analogs, NTexts )
	print fb_analogs
	print "\nSecond block:"
	sb_analogs = search_num_right_texts( texts, sb_analogs, NTexts )
	print sb_analogs
	print "\nThird block:"
	tb_analogs = search_num_right_texts( texts, tb_analogs, NTexts )
	print tb_analogs

	equations = search_equations( fb_analogs, NTexts )
	equations += search_equations( sb_analogs, NTexts )
	equations += search_equations( tb_analogs, NTexts )

	return equations

def main():
	print "This module hasn't main call!"
	return

if __name__ == "__main__":
	sys.exit( main() )
