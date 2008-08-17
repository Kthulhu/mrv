"""B{byronimotest.byronimo.maya.undo}

Test ALL features of the undo queue

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


import unittest
import byronimo.maya as bmaya 
import maya.cmds as cmds
import byronimo.maya.undo as undo
import sys

class TestUndoQueue( unittest.TestCase ):
	"""Test all aspects of the api undo queue"""
	
	class TestOperation( undo.Operation ):
		def __init__( self ):
			undo.Operation.__init__( self )
			self.numDoit = 0
			self.numUndoIt = 0
			
		def doIt( self ):
			self.numDoit += 1 
			
		def undoIt( self ):
			self.numUndoIt += 1
	
	
	def test_undoBasics( self ):
		"""byronimo.maya.undo: basic assertions"""
		bmaya.Mel.eval( "byronimoUndo -psh" )
		
		# put some undoable operation
		op = TestUndoQueue.TestOperation()
		op.doIt( )			# apply operation
		
		self.failUnless( len( sys._maya_stack ) == 1 )
		self.failUnless( sys._maya_stack_depth == 1 )
		
		
		bmaya.Mel.eval( "byronimoUndo -pop" )
		
		# STACK MUST BE EMPTY#
		# as it has been taken by the command
		self.failUnless( len( sys._maya_stack ) == 0 )
		
		# UNDO 
		cmds.undo()
		self.failUnless( op.numDoit == op.numUndoIt )
		
		# REDO
		cmds.redo()
		self.failUnless( op.numDoit - 1 == op.numUndoIt )
		
		# OP WITHOUT PUSH
		self.failUnlessRaises( ValueError, TestUndoQueue.TestOperation )
			
		
		bmaya.Mel.flushUndo()
		
	@staticmethod
	@undoable
	def _recurseUndoDeco( numOps, curDepth, maxDepth ):
		"""Recurse and create operations according to args
		@note: decorator used !"""
		if curDepth == maxDepth:
			return 0
		numops = 0
		for i in xrange( numOps ):
			op = TestUndoQueue.TestOperation()
			op.doIt( )			# apply operation
			numops += TestUndoQueue._recurseUndo( numOps, curDepth+1, maxDepth )
			numops += 1
		# END for each op
		return numops

	@staticmethod
	def _recurseUndo( numOps, curDepth, maxDepth ):
		"""Recurse and create operations according to args
		@note: decorator used !"""
		if curDepth == maxDepth:
			return 0
		undo.startUndo()
		
		numops = 0
		for i in xrange( numOps ):
			op = TestUndoQueue.TestOperation()
			op.doIt( )			# apply operation
			numops += TestUndoQueue._recurseUndo( numOps, curDepth+1, maxDepth )
			numops += 1
		# END for each op
		
		undo.endUndo()
		return numops
	
	def test_undoPerformance( self ):
		"byronimo.maya.undo: recursive undo including decorator"
		import time
		iterations = 25
		maxdepth = 3
		totalops = 0 
		
		all_elapsed = [[],[]]
		
		for undoEnabled in range( 2 ):
			
			undo = ""
			if not undoEnabled:
				undo = "Undo disabled"
				
			cmds.undoInfo( st=undoEnabled )
			
			# decorated !
			starttime = time.clock()
			numops = TestUndoQueue._recurseUndoDeco( iterations, 0, maxdepth )
			totalops += numops
			elapsed = time.clock() - starttime
			all_elapsed[undoEnabled].append( elapsed )
			
			print "DECORATED %s: %i ops in %f s ( %f / s )" % ( undo, numops, elapsed, numops / elapsed ) 
			
			
			starttime = time.clock()
			numops = TestUndoQueue._recurseUndo( iterations, 0, maxdepth )
			totalops += numops
			elapsed_deco = elapsed
			elapsed = time.clock() - starttime
			all_elapsed[undoEnabled].append( elapsed )
			
			print "MANUAL %s: %i ops in %f s ( %f / s )" % ( undo, numops, elapsed, numops / elapsed )
			starttime = time.clock()
			
			print "DECORATED is %f %% faster than manually implemented functions !" % ( 100 - ( elapsed_deco / elapsed ) * 100 )
			
			if undoEnabled:
				cmds.undo()
				cmds.undo()
				cmds.redo()
				cmds.redo()
				elapsed = time.clock() - starttime
				
				print "CALL TIME: %i operations in %f s ( %f / s )" % ( totalops, elapsed, totalops / elapsed )
			#END if undo enabled
		# END for each undo queue state 
		
		ratio = 100.0 - ( ( all_elapsed[0][0] / all_elapsed[1][0] ) * 100 )
		difference = all_elapsed[1][1] - all_elapsed[0][1]
		
		# RATIOS between enabled undo system and without
		print "RATIO UNDO QUEUE ON/OFF: %f s (on) vs %f s (off) = %f %% speedup on disabled queue ( difference [s] = %f )" % (all_elapsed[1][0], all_elapsed[0][0], ratio, difference ) 
		
		