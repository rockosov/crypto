# coding: utf8

from sys import stdout
import config as conf

__author__ = "rockosov@gmail.com"

##
# @brief описывает блоки замены и методы работы с ними 
class Block ( object ):
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

		# значение функции блоков на множестве определения [0;15]
		self.a_output = []
		for i in range( 16 ):
			self.a_output.append( self.substitution( i ) )

		self.diff_table = []
		return

	##
	# @brief печатает блок
	def print_block( self ):
		print "Blocks", self.num, "[", self.var_num, "]:"
		for i in self.content:
			for j in i:
				stdout.write(str(j) + " ")
		print

	##
	# @brief печатает таблицу вероятностей появления дифференциала C от дифференциала A
	#
	# @return
	#	@retval ValueError - если таблица пуста
	def print_diff_table( self ):
		if self.diff_table == []:
			raise ValueError, "diff_table is empty!"
		print "diff_table of block %d:" % self.num
		for i in self.diff_table:
			for j in i:
				print "%02d" % j ,
			print
		return
	
	##
	# @brief выполняет непосредственно замену
	#
	# @param bits - вход функции замены
	#
	# @return результат
	def substitution( self, bits ):
		bits &= 15 # если поступили биты, длина которых больше 4
		if self.num == 3:
			return self.content[(bits & 1) + ((bits & 8) >> 2)][(bits & 6) >> 1]
		else:
			return self.content[bits >> 3][bits & 7]

	##
	# @brief строит таблицу вероятностей появления dС от dA
	#
	def build_diff_table( self ):
		# подготовим место
		self.diff_table.extend( range( 16 ) )
		for i in range( len( self.diff_table ) ):
			self.diff_table[ i ] = range( 16 )
			for j in range( len( self.diff_table[ i ] ) ):
				# и инициализируем как нужно
				self.diff_table[ i ][ j ] = 0
		for delta_a in range( 16 ):
			for a1 in range( 16 ):
				a2 = delta_a ^ a1
				# посчитаем c1 и c2
				c1 = self.substitution( a1 )
				c2 = self.substitution( a2 )
				# вычислим delta_c
				delta_c = c1 ^ c2
				# запомним
				self.diff_table[delta_a][delta_c] += 1
		return

	##
	# @brief ищет максимальные значения вероятности
	#
	# @return результат работы
	#	@retval out - представляет собой список вида [[x11, x21, x31], ..., [x1n, x2n, x3n]],
	#			где x1i = dA, x2i = dC, x3i = maximum
	#	@retval ValueError - если таблица пуста
	def max_in_diff_table( self ):
		result = list()
		if self.diff_table == []:
			raise ValueError, "diff_table is empty!"
		for i in self.diff_table[1:]:
			maximum = max( i )
			for j in range( len( i ) ):
				if maximum == i[ j ]:
					result.append( ( self.diff_table.index( i ), j, i[ j ] ) )
		temp = max( result, key = lambda current: current[2] )
		out = list()
		for index, value in enumerate( result ):
			if value[ 2 ] == temp[ 2 ]:
				out.append( value )
		return out

class Permutation ( object ):
	def __init__( self, initial_name ):
		if initial_name == "E":
			self.direct = conf.PERM_EXT
		elif initial_name == "P":
			self.direct = conf.PERM
		else:
			raise ValueError, "Unknown name of permutation"
		self.inverse = self.__inverse( self.direct )
		return

	def __inverse( self, direct):
		result = range( max( direct ) )
		for i in range( len( result ) ):
			result[i] = []
		for i in range( len( direct ) ):
			result[ direct[ i ] - 1 ].append(i + 1)
		return result

	def make_permutation( self, bits, mode ):
		result = 0
		direct_size = len( self.direct )
		inverse_size = len( self.inverse )
		if mode == 1:
			# используем прямую перестановку
			for i in range( direct_size ):
				result += ( ( bits >> ( inverse_size - self.direct[ i ] ) ) & 1 ) << ( direct_size - i - 1 )
		elif mode == -1:
			# используем обратную перестановку	
			for i in range( len( self.inverse ) ):
				result += ( ( bits >> ( direct_size - self.inverse[ i ][ 0 ] ) ) & 1 ) << ( inverse_size - i - 1 )
		else:
			raise ValueError, "Invalid mode of permutation"
		return result
	
