"""B{byronimo.automation.workflows}
Keeps all workflows specific to maya  

@newfield revision: Revision
@newfield id: SVN Id
"""

__author__='$Author: byron $'
__contact__='byron@byronimo.de'
__version__=1
__license__='MIT License'
__date__="$Date: 2008-08-12 15:33:55 +0200 (Tue, 12 Aug 2008) $"
__revision__="$Revision: 50 $"
__id__="$Id: configuration.py 50 2008-08-12 13:33:55Z byron $"
__copyright__='(c) 2008 Sebastian Thiel'


from byronimo.path import Path
_this_module = __import__( "byronimo.automation.workflows", globals(), locals(), ['workflows'] )
import pydot
import processes


#{ Initialization


# assure we only do certain things once
if 'init_done' not in locals():
	init_done = False
	
# SYSTEM INITIALIZATIONs
if not init_done:
	import byronimo.automation.base as common
	common.addWorkflowsFromDotFiles( _this_module, Path( __file__ ).p_parent.glob( "*.dot" ) )

#} END initialization




