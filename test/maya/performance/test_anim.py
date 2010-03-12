# -*- coding: utf-8 -*-
"""Performance Testing"""
from mayarv.test.maya import *

import mayarv.maya.nodes as nodes
import time
import sys

class TestAnimPerformance( unittest.TestCase ):
	
	@with_scene('21kcurves.mb')
	def test_iter_animation(self):
		
		# get all nodes, get all animation from them
		for as_node in range(2):
			# find animation
			st = time.time()
			sel_list = nodes.toSelectionList(nodes.it.iterDgNodes(asNode=False))
			anim_nodes = nodes.AnimCurve.getAnimation(sel_list, as_node)
			num_nodes = len(anim_nodes)
			elapsed = time.time() - st
			print >>sys.stderr, "Found %i animation nodes ( as_node=%i ) in %f s ( %f anim nodes / s )" % (num_nodes, as_node, elapsed, num_nodes/elapsed)
			
			# check plug access
			if as_node:
				st = time.time()
				for anode in anim_nodes:
					anode.output
				# END for each node
				elapsed = time.time() - st
				print >>sys.stderr, "Accessed output plug on %i nodes using node.output in %f s ( %f plugs nodes / s )" % (num_nodes, elapsed, num_nodes/elapsed)
				
				st = time.time()
				for anode in anim_nodes:
					anode.findPlug('output')
				# END for each node
				elapsed_findplug = time.time() - st
				print >>sys.stderr, "Accessed output plug on %i nodes using node.findPlug('output') in %f s ( %f plugs nodes / s )" % (num_nodes, elapsed_findplug, num_nodes/elapsed_findplug)
				print >>sys.stderr, "node.findPlug is %f times as fast as node.plug" % (elapsed/elapsed_findplug)
			else:
				st = time.time()
				mfndep = nodes.api.MFnDependencyNode()
				for apianode in anim_nodes:
					mfndep.setObject(apianode)
					mfndep.findPlug('output')
				# END for each node
				elapsed = time.time() - st
				print >>sys.stderr, "Accessed output plug on %i api nodes using mfndep.findPlug in %f s ( %f plug nodes / s )" % (num_nodes, elapsed, num_nodes/elapsed)
			# END attr access testing
			
			# make selection list
			st = time.time()
			anim_sel_list = nodes.toSelectionList(anim_nodes)
			elapsed = time.time() - st
			print >>sys.stderr, "Convenient Selection List Creation: %f s" % elapsed
			
			# make selection list manually 
			st = time.time()
			anim_sel_list = nodes.api.MSelectionList()
			if as_node:
				for an in anim_nodes:
					anim_sel_list.add(an.getApiObject())
				# END for each animation node
			else:
				for apian in anim_nodes:
					anim_sel_list.add(apian)
				# END for each animation node
			# END handle as_node
			elapsed = time.time() - st
			print >>sys.stderr, "Optimized Selection List Creation: %f s" % elapsed
			
			st = time.time()
			nodes.api.MGlobal.setActiveSelectionList(anim_sel_list)
			elapsed = time.time() - st
			print >>sys.stderr, "Setting Selection List as Maya-Selection: %f s" % elapsed
		# END for each as_node value
		
		
		# compare to plain mel 
		melcmd = """select( ls("-typ", "animCurve", (listConnections ("-s", 1, "-d", 0, "-scn", 1, "-t", "animCurve", ls()))) )"""
		st = time.time()
		nodes.api.MGlobal.executeCommand(melcmd, False, False)
		elapsed = time.time() - st
		print >>sys.stderr, "MEL: Get animation of all nodes and select the animcurves: %f s" % elapsed
		