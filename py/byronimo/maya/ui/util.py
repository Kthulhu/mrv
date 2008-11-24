"""B{byronimo.ui.util}

Utilities and classes useful for user interfaces 

@todo: more documentation

@newfield revision: Revision
@newfield id: SVN Id
"""

__author__='$Author: byron $'
__contact__='byron@byronimo.de'
__version__=1
__license__='MIT License'
__date__="$Date: 2008-05-29 02:30:46 +0200 (Thu, 29 May 2008) $"
__revision__="$Revision: 16 $"
__id__="$Id: configuration.py 16 2008-05-29 00:30:46Z byron $"
__copyright__='(c) 2008 Sebastian Thiel'


from byronimo.util import CallbackBase, Call, WeakInstFunction
import maya.cmds as cmds 
import weakref

#{ MEL Function Wrappers
 
def makeEditOrQueryMethod( flag, isEdit=False, methodName=None ):
	"""Create a function calling inFunc with an edit or query flag set.
	@note: only works on byronimo wrapped ui elements
	@note: THIS IS MOSTLY A DUPLICATION OF PROVEN CODE FROM MAYA.UTIL !
	@param flag: name of the query or edit flag
	@param isEdit: If not False, the method returned will be an edit function
	@param methoName: the name of the method returned, defaults to inCmd name  """
	
	func = None
	if isEdit:
		def editFunc(self, val, **kwargs): 
			kwargs[ 'edit' ] = True
			kwargs[ flag ] = val
			return self.__melcmd__( self, **kwargs )
			
		func = editFunc
	# END if edit 
	else:
		def queryFunc(self, **kwargs): 
			kwargs[ 'query' ] = True
			kwargs[ flag ] = True
			return self.__melcmd__( self, **kwargs )
			
		func = queryFunc
	# END if query 
	
	if not methodName:
		methodName = flag 
	func.__name__ = methodName
			 
	return func


def queryMethod( flag, methodName = None ):
	""" Shorthand query version of makeEditOrQueryMethod """
	return makeEditOrQueryMethod( flag, isEdit=False, methodName=methodName )

def editMethod( flag, methodName = None ):
	""" Shorthand edit version of makeEditOrQueryMethod """
	return makeEditOrQueryMethod( flag, isEdit=True, methodName=methodName )

def propertyQE( flag, methodName = None ):
	""" Shorthand for simple query and edit properties """
	editFunc = editMethod( flag, methodName = methodName )
	queryFunc = queryMethod( flag, methodName = methodName )
	return property( queryFunc, editFunc )
	
#} 


class CallbackBaseUI( CallbackBase ):
	"""Allows registration of a typical UI callback
	It basically streamlines the registration for a callback such that any 
	number of listeners can be called when an event occours - this works by 
	keeping an own list of callbacks registered for a specific event, and calling them 
	whenever the maya ui callback has been triggered
	
	To make this work it is essential that you work with one and the same instance of your 
	class.
	
	To use this class , see the documentation of L{CallbackBase}, but use the UIEvent 
	instead.
	If you want to add your own events, use your own events, use the L{Event} class instead
	
	The class does NOT use weakreferences for the main callbacks to make it easier to use.
	Use the WeakFunction to properly and weakly bind an instance function
	
	When registered for an event, the sender will be provided to each callback as first 
	argument.
	
	@note: your functions that are being registered for a certain event should 
	reside on a class that is being held alive by more than the callback
	"""
	#( Configuration 
	# we are to be put as first arguemnt, allowing listeners to do something 
	# with the sender when handling the event
	sender_as_argument = True
	#} END configuration 
	
	class UIEvent( CallbackBase.Event ):
		"""Event suitable to deal with user interface callback"""
		#( Configuration 
		use_weakref = False
		#) END configuration
		
		def __init__( self, eventname, **kwargs ):
			"""Allows to set additional arguments to be given when a callback 
			is actually set"""
			super( CallbackBaseUI.UIEvent, self ).__init__( eventname )
			self._kwargs = kwargs
		
		def __set__(  self, inst, eventfunc ):
			"""Set the given event to be called when this event is being triggered"""
			eventset = self.__get__( inst )
			
			# REGISTE TO MEL IF THIS IS THE FIRST EVENT 
			# do we have to register the callback ?
			if not eventset:
				kwargs = dict()
				# generic call that will receive maya's own arguments and pass them on
				weakSendEvent = WeakInstFunction( inst.sendEvent )
				call = Call( weakSendEvent, self )
				dyncall =  lambda *args, **kwargs: call( *args, **kwargs )
				
				kwargs[ 'e' ] = 1
				kwargs[ self._name ] = dyncall
				kwargs.update( self._kwargs )		# allow user kwargs 
				inst.__melcmd__( str( inst ) , **kwargs )
			# END create event 
			
			super( CallbackBaseUI.UIEvent, self ).__set__( inst, eventfunc )
			
	# END uievent
	
	#( iDuplicatable Deactivated 
	
	def createInstance( self, *args, **kwargs ):
		"""Deactivated as we cannot copy callbacks safely if the maya ui is involved"""
		raise RuntimeError( "A CallbackBaseUI instance cannot be duplicated" )
		
	def copyFrom( self, other, *args, **kwargs ):
		raise RuntimeError( "A CallbackBaseUI instance cannot be copied" )
		
	#) end iduplicatable deactivated
	
	
class UIContainerBase( object ):
	"""A ui container is a base for all classes that can have child controls or 
	other containers. 
	This class is just supposed to keep references to it's children so that additional 
	information stored in python will not get lost
	Child-Instances are always unique, thus adding them several times will not 
	keep them several times , but just once"""
	
	
	def __init__( self, *args, **kwargs ):
		self._children = list()
		super( UIContainerBase, self ).__init__( *args, **kwargs )
	
	def __getitem__( self, key ):
		"""@return: the child with the given name, see L{getChildByName}
		@param key: if integer, will return the given list index, if string, the child 
		matching the id"""
		if isinstance( key, basestring ):
			return self.getChildByName( key )
		else:
			return self._children[ key ]
			
	def add( self, child, set_self_active = False, revert_to_previous_parent = True ):
		"""Add the given child UI item to our list of children
		@param set_self_active: if True, we explicitly make ourselves the current parent 
		for newly created UI elements
		@param revert_to_previous_parent: if True, the previous parent will be restored 
		once we are done, if Fales we stay the parent - only effective if set_self_active is True
		@return: the newly added child, allowing contructs like 
		button = layout.addChild( Button( ) )"""
		if child in self._children:
			return child 
			
		prevparent = None
		if set_self_active:
			prevparent = self.getCurrentParent()
			self.setActive( )
		# END set active handling
		
		self._children.append( child )
		
		if revert_to_previous_parent and prevparent:
			cmds.setParent( prevparent )
			
		return child
		
	def remove( self, child ):
		"""Remove the given child from our list
		@return: True if the child was found and has been removed, False otherwise"""
		try:
			self._children.remove( child )
			return True
		except ValueError:
			return False
	
	def deleteChild( self, child ):
		"""Delete the given child ui physically so it will not be shown anymore
		after removing it from our list of children"""
		if self.removeChild( child ):
			child.delete()
			
	def listChildren( self ):
		"""@return: list with our child instances
		@note: it's a copy, so you can freely act on the list
		@note: children will be returned in the order in which they have been added"""
		return self._children[:]
		
	def getChildByName( self, childname ):
		"""@return: stored child instance, specified either as short name ( without pipes ) 
		or fully qualified ( i.e. mychild or parent|subparent|mychild" )
		@raise KeyError: if a child with that name does not exist"""
		if "|" in childname:
			for child in self._children:
				if child == childname:
					return child
			# END for each chld
		# END fqn handling 
		
		childname = childname.split( '|' )[-1]		# |hello|world -> world 
		for child in self._children:
			if child.getBasename() == childname:
				return child
		# END non- fqn handling
		
		raise KeyError( "Child named %s could not be found below %s" % ( childname, self ) )
	
	def setActive( self ):
		"""Set this container active, such that newly created items will be children 
		of this layout
		@note: always use the addChild function to add the children !"""
		cmds.setParent( self )