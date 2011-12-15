# coding: utf8

__author__ = "rockosov@gmail.com"

##
# @brief получает значени бита в source из position
#
# @param source		[ in ] - откуда получаем значение
# @param position	[ in ] - позиция бита
#
# @return значение бита
def get_bit( source, position ):
	return ( source >> position ) & 1

##
# @brief устанавливает бит в destination по position в значени bit
#
# @param destination	[ in ] - назначение
# @param position	[ in ] - позиция
# @param bit		[ in ] - значени бита
#
# @return новое значение destination
def set_bit( destination, position, bit ):
	if bit == 1:
		return destination | ( bit << position )
	else:
		mask = 0
		for i in range( len( bin( destination ).lstrip( "0b" ) ) ):
			if i == position:
				continue
			mask += 1 << i
		return destination & mask 

##
# @brief получает значения битов в source по position в размере num
#
# @param source		[ in ] - откуда получаем
# @param position	[ in ] - начальная позиция
# @param num		[ in ] - количество битов
#
# @return значение битов в виде десятичного числа
def get_bits( source, position, num ):
	mask = 0
	for i in range( num ):
		mask += 1 << i
	return ( source >> position ) & mask

##
# @brief ковертирует десятичное число в двоичный вид, равняя его по размеру size
#
# @param integer	[ in ] - целевое число
# @param size		[ in ] - размер
#
# @return результирующий двоичный вид
def full_bin( integer, size ):
	str = bin( integer )
	str = str.lstrip( "0b" )
	if len( str ) < size:
		str = "0"*( size - len( str ) ) + str
	return str
