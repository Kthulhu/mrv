"""B{byronimo.maya.scene}

Provides methodes to query and alter the currently loaded scene. It covers 
most of the functionality of the 'file' command, but has been renamed to scene
as disambiguation to a filesystem file.

@todo: more documentation
@todo: create real class properties - currently its only working with instances

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


# export filter 
__all__ = [ 'currentScene', 'Scene' ]

import maya.cmds as cmds
from byronimo.path import Path
import byronimo.maya.util as util
import byronimo.maya
import maya.OpenMaya as om
import maya.cmds as cmds



	
class _SceneCallback( util.CallbackBase ):
	""" Implements Scene Callbacks """
	
	_checkCBSet = set( ( 	om.MSceneMessage.kBeforeNewCheck,
							om.MSceneMessage.kBeforeSaveCheck ) )

	_checkFileCBSet = set( ( 	om.MSceneMessage.kBeforeImportCheck,
							  	om.MSceneMessage.kBeforeOpenCheck,
								om.MSceneMessage.kBeforeExportCheck,
								om.MSceneMessage.kBeforeReferenceCheck,
								om.MSceneMessage.kBeforeLoadReferenceCheck  ) )
	
	_cbgroupToMethod = { 	0 : om.MSceneMessage.addCheckCallback, 
							1 : om.MSceneMessage.addCheckFileCallback, 
							2 : om.MSceneMessage.addCallback }
	
	def addListener( self, listenerID, callback, sceneMessageId ):
		"""Add a listener for the given sceneMessageId - all other parameters 
		correspond to the baseclass method: L{CallbackBase.addListener}
		@param sceneMessageId: MSceneMessage message id enumeration member 
		@note: this message enforces the required signature"""
		util.CallbackBase.addListener( self, listenerID, callback, callbackID = sceneMessageId )

	def _getCallbackGroupID( self, sceneMessageId ):
		if sceneMessageId in self._checkCBSet:
			return 0
		elif sceneMessageId in self._checkFileCBSet:
			return 1
		else:
			return 2

	def _addMasterCallback( self, callbackGroup, sceneMessageId ):
		""" Setup or delete a scene callback 
		@return : the possibly created callback id """
		groupId = self._getCallbackGroupID( sceneMessageId )
		messageCreator = self._cbgroupToMethod[ groupId ]
		return messageCreator( sceneMessageId, self._call, callbackGroup )
		
		

class Scene( util.Singleton ):
	"""Singleton Class allowing access to the maya scene"""
	
	
	#{ Public Members
	Callbacks = _SceneCallback()
	#}
	
	
	#{ Edit Methods 
	@staticmethod
	def open( filePath, loadReferenceDepth="all", force=False, **kvargs ):
		""" Open a scene 
		@param filePath: The path to the file to be opened
		@param loadReferenceDepth: 'all' - load all references
		'topOnly' - only top level references, no subreferences
		'none' - load no references
		@param force - if True, the new scene will be loaded although currently 
		loaded contains unsaved changes 
		@return: a path object to the loaded scene"""
		filepath = cmds.file( filePath, loadReferenceDepth=loadReferenceDepth, force=force, **kvargs )
		return Path( filepath )
		
	@staticmethod
	def new( force = False, **kvargs ):
		""" Create a new scene 
		@param force: if True, the new scene will be created even though there 
		are unsaved modifications"""
		cmds.file( new = True, force = force, **kvargs )
		
	#} END edit methods
	
	
	#{ Query Methods
	def getName( self ):
		return Path( cmds.file( q=1, exn=1 ) )
		
	
	def isModified( self ):
		return cmds.file( q=1, amf=True )
	#} END query methods
	
	
	#{ Properties 
	p_name = property( getName )
	p_anyModified = property( isModified )
	#} END Properties 

 
	

# END SCENE




## ATTACH SINGLETON SCENE
####################
# store the current scene as instance, allowing to use properties
byronimo.maya.Scene = Scene()

