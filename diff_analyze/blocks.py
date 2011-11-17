# coding: utf8

from sys import stdout
import config as conf

__author__ = "rockosov@gmail.com"

class Block ( object ):
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
	def print_block( self ):
		print "Blocks", self.num, "[", self.var_num, "]:"
		for i in self.content:
			for j in range(len(i)):
				stdout.write(str(i[j]) + " ")
			print
	
	def substitution( self, bits ):
		bits &= 15 # если поступили биты, длина которых больше 4
		if self.num == 3:
			return self.content[(bits & 1) + ((bits & 8) >> 2)][(bits & 6) >> 1]
		else:
			return self.content[bits >> 3][bits & 7]
