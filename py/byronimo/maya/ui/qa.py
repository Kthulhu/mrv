# -*- coding: utf-8 -*-
"""B{byronimo.ui.qa}

Contains a modular UI able to display quality assurance checks, run them and 
present their results. It should be easy to override and adjust it to suit additional needs
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


import base as uibase
import controls
import maya.cmds as cmds
import byronimo.util as util
import byronimo.maya.util as mutil
import util as uiutil
import layouts
from byronimo.automation.qa import QAWorkflow
import maya.OpenMaya as api
from itertools import chain
import sys

class QACheckLayout( layouts.RowLayout ):
	"""Row Layout able to display a qa check and related information
	@note: currently we make assumptions about the positions of the children in the 
	RowLayout, thus you may only append new ones"""
	isNodeTypeTreeMember = False
	
	#{ Configuration
	# paths to icons to display
	# [0] = check not run
	# [1] = check success
	# [2] = check failed
	# [3] = check threw exception
	icons = [ "offRadioBtnIcon.xpm", "onRadioBtnIcon.xpm", "fstop.xpm", "fstop.xpm" ]	# explicitly a list
	
	# height of the UI control 
	height = 25
	
	# number of columns to use - assure to fill the respective slots
	numcols = 3
	
	# as checks can take some time, it might be useful to have realtime results 
	# to std out in UI mode at least. It accompanies the feedback the workflow 
	# gives and keeps the default unittest style
	info_to_stdout = not cmds.about( batch = 1 )
	#} END configuration 
	
	def __new__( cls, *args, **kwargs ):
		"""Initialize this RowColumnLayout instance with a check instance
		@param check: the check this instance should attach itself to - it needs to be set"""
		check = kwargs.pop( "check" )
		
		numcols = cls.numcols # without fix
		if check.plug.implements_fix:
			numcols += 1
		
		assert numcols < 7	# more than 6 not supported by underlying layout
		
		kwargs[ 'numberOfColumns' ] = numcols
		kwargs[ 'adj' ] = 1
		kwargs[ 'h' ] = cls.height
		kwargs[ 'cw%i' % numcols ] = ( cls.height + 2, ) * numcols
		self = super( QACheckLayout, cls ).__new__( cls, *args, **kwargs )
		
		# create instance variables 
		self._check = check
		return self
		
	def __init__( self, *args, **kwargs ):
		"""Initialize our instance with members"""
		super( QACheckLayout, self ).__init__( *args, **kwargs )
		
		# populate 
		self._create( )
	
	def _create( self ):
		"""Create our layout elements according to the details given in check"""
		# assume we are active
		checkplug = self.getCheck().plug
		self.add( controls.Text( label = checkplug.getName(), ann = checkplug.annotation ) )
		
		ibutton = self.add( controls.IconTextButton( 	style="iconOnly", 
														h = self.height, w = self.height ) )
		sbutton = self.add( controls.Button( label = "S", w = self.height, 
												ann = "Select faild or fixed items" ) )
		
		# if we can actually fix the item, we add an additional button
		if checkplug.implements_fix:
			fbutton = self.add( controls.Button( label = "Fix", ann = "Attempt to fix failed items" ) )
			fbutton.e_released = self._runCheck 
		# END fix button setup
			
		# attach callbacks 
		ibutton.e_command = self._runCheck
		sbutton.e_released = self.selectPressed
	
	def update( self ):
		"""Update ourselves to match information in our stored check"""
		# check the cache for a result - if so, ask it for its state
		# otherwise we are not run and indicate that 
		bicon = self.listChildren()[1]
		bicon.p_image = self.icons[0]
		
		check = self.getCheck()
		if check.hasCache():
			result = check.getCache()
			self.setResult( result )
		# END if previous result exists
		
		
	def getCheck( self ):
		"""@return: check we are operating upon"""
		return self._check
	
	#{ Check Callbacks
	
	def _runCheck( self, *args, **kwargs ):
		"""Run our check
		@note: we may also be used as a ui callback and figure out ourselves
		whether we have been pressed by the fix button or by the run button
		@param force_check: if True, default True, a computation will be forced, 
		otherwise a cached result may be used
		@param **kwargs: will be passed to the workflow's runChecks method
		@return: result of our check"""
		check = self.getCheck()
		wfl = check.node.getWorkflow()
		force_check = kwargs.get( "force_check", True )
		
		mode = check.node.eMode.query
		if args and isinstance( args[0], controls.Button ):
			mode = check.node.eMode.fix
		# END fix button handling 
		
		return wfl.runChecks( [ check ], mode = mode, clear_result = force_check, **kwargs )[0][1]
	
	def selectPressed( self, *args ):
		"""Called if the selected button has been pressed
		Triggers a workflow run if not yet done"""
		# use the cache directly to prevent the whole runprocess to be kicked on 
		# although the result is already known
		check = self.getCheck()
		result = None
		if check.hasCache():
			result = check.getCache()
		else:
			result = self._runCheck( force_check = False )
		
		# select items , ignore erorrs if it is not selectable 
		sellist = api.MSelectionList()
		for item in chain( result.getFixedItems(), result.getFailedItems() ):
			try:
				sellist.add( str( item ) )
			except RuntimeError:
				pass
		# END for each item to select
		
		api.MGlobal.setActiveSelectionList( sellist )
			
	def preCheck( self ):
		"""Runs before the check starts"""
		if self.info_to_stdout:
			checkplug = self.getCheck().plug
			sys.__stdout__.write( "Running %s: %s ... " % ( checkplug.getName(), checkplug.annotation ) )
		# END extra info
		
		text = self.listChildren()[0]
		text.p_label = "Running ..."
		 
	def postCheck( self, result ):
		"""Runs after the check has finished including the given result"""
		if self.info_to_stdout:
			msg = "FAILED"
			if result.isSuccessful():
				msg = "OK"
			sys.__stdout__.write( msg + "\n" )
		# END extra info 
			
		text = self.listChildren()[0]
		text.p_label = str( self.getCheck().plug.getName() )
		
		self.setResult( result )
		
	def checkError( self ):
		"""Called if the checks fails with an error"""
		text = self.listChildren()[0]
		text.p_label = str( self.getCheck().plug.getName() ) + " ( ERROR )"
	
	def setResult( self, result ):
		"""Setup ourselves to indicate the given check result
		@return: our adjusted iconTextButton Member"""
		target_icon = self.icons[2]		# failed by default
		
		if result.isSuccessful():
			target_icon = self.icons[1]
		elif result.isNull():		# indicates failure, something bad happened
			target_icon = self.icons[3]
		
		# annotate the text with the result
		children = self.listChildren()
		text = children[0]
		text.p_annotation = str( result )
		
		bicon = children[1]
		bicon.p_image = target_icon
		
		return bicon
	#} END interface

class QALayout( layouts.FormLayout, uiutil.iItemSet ):
	"""Layout able to dynamically display QAChecks, run them and display their result"""
	isNodeTypeTreeMember = False 
	
	#{ Configuration
	# class used to create a layout displaying details about the check
	# it must be compatible to QACheckLayout as a certain API is expected
	checkuicls = QACheckLayout
	
	# if True, a button to run all checks at once will be appended
	run_all_button = True

	# class used to access default workflow events 
	qaworkflowcls = QAWorkflow
	#} END configuration 
	
	def __new__( cls, *args, **kwargs ):
		"""Set some default arguments"""
		return super( QALayout, cls ).__new__( cls, *args, **kwargs )
	
	
	def __init__( self, *args, **kwargs ):
		"""Initialize our basic interface involving a column layout to store the 
		actual check widgets"""
		super( QALayout, self ).__init__( *args, **kwargs )
		scroll_layout = self.add( layouts.ScrollLayout( cr=1 ) )
		
		if scroll_layout:
			# will contain the checks
			self.col_layout = scroll_layout.add( layouts.ColumnLayout( adj = 1 ) )
		# END scroll_layout
		self.setActive()
	#{ Interface
	
	def setChecks( self, checks ):
		"""Set the checks this layout should display
		@param checks: iterable of qa checks as retrieved by L{listChecks}
		@raise ValueErorr: if one check is from a different workflow and there is a run_all button"""
		# we might change the layout, so be active
		# IMPORTANT: if this is not the case, we might easily confuse layouts ... 
		# figure out why exactly
		self.setActive()
		
		# map check names to actual checks
		name_to_check_map = dict( ( ( str( c ), c ) for c in checks ) )
		name_to_child_map = dict()
		
		self.setItems( name_to_check_map.keys(), 	name_to_check_map = name_to_check_map, 
					  								name_to_child_map = name_to_child_map )
		
		# SET EVENTS 
		#############
		# NOTE: currently we only register ourselves for callbacks, and deregeister 
		# automatically through the weak reference system
		wfls_done = list()
		for check in checks:
			cwfl = check.node.getWorkflow()
			if cwfl in wfls_done:
				continue 
			wfls_done.append( cwfl )
			
			if self.run_all_button and len( wfls_done ) > 1:
				raise ValueError( "This UI can currently only handle checks from only one workflow at a time if run_all_button is set" )
			
			cwfl.e_preCheck = self.checkHandler
			cwfl.e_postCheck = self.checkHandler
			cwfl.e_checkError = self.checkHandler
		# END for each check
		
		# POSSIBLY ADD BUTTON TO THE END
		#################################
		# remove possibly existing button ( ignore the flag, its about the button here )
		# its stored in a column layout
		button_layout_name = "additionals_column_layout"
		layout_child = self.listChildren( predicate = lambda c: c.getBasename() == button_layout_name )
		if layout_child:
			assert len( layout_child ) == 1
			self.deleteChild( layout_child[0] )
			
		# create child layout ?
		if self.run_all_button:
			layout_child = self.add( layouts.ColumnLayout( adj = 1, name = button_layout_name ) )
			if layout_child:
				controls.Separator( style = "single", h = 10 )
				run_button = controls.Button( label = "Run All", ann = "Run all checks in one go" )
				run_button.e_pressed = self.runAllPressed
			# END button layout setup
			self.setActive()
		# END if run all button is requested
		
		# setup form layout - depending on the amount of items - we have 1 or two 
		# children, never more 
		children = self.listChildren()
		assert len( children ) < 3
		o = 2	# offset
		t,b,l,r = self.kSides 
		if len( children ) == 1:
			c = children[0]
			self.setup( af = ( ( c, b, o ), ( c, t, o ), ( c, l, o ), ( c, r, o ) ) )
		# END case one child 
		else:
			c1 = children[0]
			c2 = children[1]
			self.setup( af = ( 	( c1, l, o ), ( c1, r, o ), ( c1, t, o ), 
							 	( c2, l, o ), ( c2, r, o ), ( c2, b, o ) ), 
						ac = ( 	( c1, b, o, c2 ) ), 
						an = (	( c2, t ) ) ) 
		# END case two children 
		
	def getCheckLayouts( self ):
		"""@return: list of checkLayouts representing our checks"""
		ntcm = dict()
		self.getCurrentItemIds( name_to_child_map = ntcm )
		return ntcm.values()
	
	def getChecks( self ):
		"""@return: list of checks we are currently holding in our layout"""
		return [ l.getCheck() for l in self.getCheckLayouts() ]
		
	#} END interface
	
	#{ iItemSet Implementation 
	
	def getCurrentItemIds( self, name_to_child_map = None, **kwargs ):
		"""@return: current check ids as defined by exsiting children. 
		@note: additionally fills in the name_to_child_map"""
		outids = list()
		for child in self.col_layout.listChildren( predicate = lambda c: isinstance( c, QACheckLayout ) ):
			check = child.getCheck()
			cid = str( check )
			outids.append( cid )
			
			name_to_child_map[ cid ] = child
		# END for each of our children
		return outids
		
	def handleEvent( self, eventid, **kwargs ):
		"""Assure we have the proper layouts active"""
		if eventid == self.eSetItemCBID.preCreate:
			self.col_layout.setActive()
		if eventid == self.eSetItemCBID.postCreate:
			self.setActive()
	
	def createItem( self, checkid, name_to_child_map = None, name_to_check_map = None, **kwargs ):
		"""Create and return a layout displaying the given check instance
		@param kwargs: will be passed to checkui class's initializer, allowing subclasses to easily 
		adjust the paramter list
		@note: its using self.checkuicls to create the instance"""
		self.col_layout.setActive()
		
		check_child = self.checkuicls( check = name_to_check_map[ checkid ], **kwargs )
		name_to_child_map[ checkid ] = check_child
		newItem = self.col_layout.add( check_child )
		
		return newItem
		
	def updateItem( self, checkid, name_to_child_map = None, **kwargs ):
		"""Update the item identified by the given checkid so that it represents the 
		current state of the application"""
		name_to_child_map[ checkid ].update( )
	
	def removeItem( self, checkid, name_to_child_map = None, **kwargs ):
		"""Delete the user interface portion representing the checkid"""
		self.col_layout.deleteChild( name_to_child_map[ checkid ] )
		
	#} END iitemset implementation
	
	#{ Eventhandlers 
	def checkHandler( self, event, check, *args ):
		"""Called for the given event - it will find the UI element handling the 
		call respective function on the UI instance
		@note: find the check using predefined names as they server as unique-enough keys.
		This would possibly be faster, but might not make a difference after all"""
		# find a child handling the given check
		# skip ones we do not find 
		checkchild = None
		for child in self.getCheckLayouts():
			if child.getCheck() == check:
				checkchild = child
				break
			# END if check matches
		# END for each child in children
		
		# this could actually happen as we get calls for all checks, not only 
		# for the ones we actually have 
		if checkchild is None:
			return
			
		if event == self.qaworkflowcls.e_preCheck:
			checkchild.preCheck( )
		elif event == self.qaworkflowcls.e_postCheck:
			result = args[0]
			checkchild.postCheck( result )			
		elif event == self.qaworkflowcls.e_checkError:
			checkchild.checkError( )
			
	def runAllPressed( self, *args, **kwargs ):
		"""Called once the Run-All button is pressed
		@param **kwargs: will be passed to runChecks method of workflow
		@note: we assume all checks are from one workflow only as we 
		do not sort them by workflow
		@note: currently we only run in query mode as sort of safety measure - check and fix 
		on all might be too much and lead to unexpected results"""
		checks = self.getChecks()
		if not checks:
			print "No checks found to run"
			return 
		# END check assertion
		
		wfl = checks[0].node.getWorkflow()
		wfl.runChecks( checks, clear_result = 1, **kwargs )
		
	
	#} END Eventhandlers
	 
	
