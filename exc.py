# -*- coding: utf-8 -*-
"""
Contains all exceptions used by the mayarv package in general



"""

__author__='$Author$'
__contact__='byronimo <.a.t.> gmail <.> com'
__version__=1
__license__='MIT License'
__date__="$Date$"
__revision__="$Revision$"
__id__="$Id$"
__copyright__='(c) 2008 Sebastian Thiel'


class MayaRVError( Exception ):
	""" Base Class for all exceptions that the byronimo framework throws"""
	pass

#{Decorator Exceptions
class MethodTypeError( TypeError, MayaRVError ):
	""" Indicates that a method either produced or returned a type that was not anticipated """
	pass

class InterfaceError( TypeError, MayaRVError ):
	""" Indicates that an instances interface does not fully match the requrested interface """
	pass
#}

#{ Decorator Internal Exceptions
class DecoratorError( MayaRVError ):
	""" Thrown if decorators are used in an incorrect way
	@note: this can only happen if decorators take arguments that do not resolve as
	requested
	@todo: store actual function that caused the error """
	pass

class InterfaceSetupError( MayaRVError ):
	""" Thrown if L{interface} attributes are used incorrectly
		- only and ignore are both given, although they are mutually exclusive """
	pass

class TypecheckDecoratorError( DecoratorError ):
	""" Thrown if a typecheck_param decorator encounters an incorrect argument
	specification for the given method """
	pass

class ProtectedMethodError( DecoratorError ):
	""" Thrown if a 'protected' decorator detects a non-subclass calling a protected method"""
	pass

#}