# coding: utf8

import sys

sys.path.append( "../" )

import blocks
import config as conf
import bits_ops

__author__ = "rockosov@gmail.com"

##
# @brief описывает блоки замены и методы работы с ними 
class Block_Internal( blocks.Block ):
	##
	# @brief конструктор
	#
	# @param num - номер блока ( 1, 2, 3 )
	def __init__( self, num ):
		if num == 1:
			self.content = conf.FIRST_BLOCK
			self.var_num = conf.FIRST_BLOCK_NUM
		elif num == 2:
			self.content = conf.SECOND_BLOCK
			self.var_num = conf.SECOND_BLOCK_NUM
		elif num == 3:
			self.content = conf.THIRD_BLOCK
			self.var_num = conf.THIRD_BLOCK_NUM
		else:
			raise ValueError, "Error of input num!"

		self.num = num

		self.Y = list()
		for i in range( 16 ):
			self.Y.append( self.substitution( i ) )
		
		self.statistics = list();
		for i in range( 16 ):
			if self.num != 3:
				self.statistics.append( range( 8 ) )
				for j in range( 8 ):
					self.statistics[ i ][ j ] = 0
			else:
				self.statistics.append( range( 4 ) )
				for j in range( 4 ):
					self.statistics[ i ][ j ] = 0
		return
		
	def __get_stat( self, X, Y, alfa, beta ):
		bits_X = range( 4 )[::-1]
		if self.num != 3:
			bits_Y = range( 3 )[::-1]
		else:
			bits_Y = range( 2 )[::-1]
		result = 0
		for i in bits_X:
			result ^= bits_ops.get_bit( X, i ) & bits_ops.get_bit( alfa, i )
		for j in bits_Y:
			result ^= bits_ops.get_bit( Y, j ) & bits_ops.get_bit( beta, j )

		return result
	
	def __build_statistics_1_2( self ):
		for alfa in range( 16 ):
			for beta in range( 8 ):
				for iter in range( 16 ):
					X = iter
					Y = self.Y[ iter ]
					current_stat = self.__get_stat(X, Y, alfa, beta)
					if current_stat == 0:
						self.statistics[ alfa ][ beta ] += 1
				self.statistics[ alfa ][ beta ] /= 16.
		return
	
	def __build_statistics_3( self ):
		for alfa in range( 16 ):
			for beta in range( 4 ):
				for iter in range( 16 ):
					X = iter
					Y = self.Y[ iter ]
					current_stat = self.__get_stat(X, Y, alfa, beta)
					if current_stat == 0:
						self.statistics[ alfa ][ beta ] += 1
				self.statistics[ alfa ][ beta ] /= 16.
		return

	def build_statistics( self ):
		if self.num != 3:
			return self.__build_statistics_1_2()
		else:
			return self.__build_statistics_3()
	
	def get_good_stat( self ):
		result = list()
		for i in range( len( self.statistics ) ):
			for j in range( len( self.statistics[ i ] ) ):
				current = 1 - self.statistics[ i ][ j ] * 2
				# отклонение от 0.5
				if abs( current ) <= 1 and abs( current ) >= 0.5 :
					if i != 0 and j != 0:
						result.append( ( i, j, self.statistics[ i ][ j ] ) )
		return result

##
# @brief описывает блоки перестановки и специфичные им методы в рамках линейного анализа
class Permutation_Internal( blocks.Permutation ):
	##
	# @brief производит перестановку в контексте порядка битов
	#
	# @param bits_order	[ in ] - порядок битов, которые нужно переставить
	# @param mode		[ in ] - режим перестановки: 1 - прямая, -1 - обратная
	#
	# @return переставленный порядок входных битов
	def make_permutation_in_bit_order( self, bits_order, mode ):
		result = list()
		if mode == 1:
			# используем прямую перестановку
			for i in self.direct:
				result.append( bits_order[ i - 1 ] )
		elif mode == -1:
			# используем обратную перестановку
			for i in range( len( self.inverse ) ):
				result.append( list() )
				for j in self.inverse[ i ]:
					result[ i ].append( bits_order[ j - 1 ] )
		else:
			raise ValueError, "Invalid mode of permutation"
		return result
