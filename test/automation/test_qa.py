# -*- coding: utf-8 -*-
"""
Test the quality assurance framework



"""

__author__='$Author: byron $'
__contact__='byronimo <.a.t.> gmail <.> com'
__version__=1
__license__='MIT License'
__date__="$Date: 2008-05-29 02:30:46 +0200 (Thu, 29 May 2008) $"
__revision__="$Revision: 16 $"
__id__="$Id: configuration.py 16 2008-05-29 00:30:46Z byron $"
__copyright__='(c) 2008 Sebastian Thiel'


import unittest
import workflows
import mayarv.automation.qa as qa
from cStringIO import StringIO
from mayarv.automation.processes import QACheckProcess

class TestQualityAssurance( unittest.TestCase ):
	"""Test qa framework"""

	def test_simpleQAWorkflow( self ):
		"""mayarv.automation.qa: test how a simple qa workflow handles itself"""
		qawfl = workflows.qualitychecking
		checks = qawfl.listChecks( )
		
		# assure we do not get any special derived checks
		checks = [ c for c in checks if c.node.__class__ == QACheckProcess ]
		assert checks

		for mode in qa.QAProcessBase.eMode:

			results = qawfl.runChecks( checks, mode = mode )
			assert len( results ) == len( checks )
			assert len( results[0] ) == 2
			assert isinstance( results[0][1], qa.QACheckResult )

			for ( cshell, result ), oshell in zip( results, checks ):
				assert cshell == oshell

				attr = "failed_items"
				if mode == qa.QAProcessBase.eMode.fix:
					attr = "fixed_items"
					assert result.isSuccessful()
				else:
					assert not result.isSuccessful()

				# We cannot assume this works as other tests can add their own 
				# nodes with own checks that respond differently
				# assert getattr( result, attr )
			# END for each result/checkshell
		# END for each check mode

		assert qawfl.QACheckProcess.listChecks()
