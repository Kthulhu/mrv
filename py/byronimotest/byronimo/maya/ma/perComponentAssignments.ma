//Maya ASCII 8.5 scene
//Name: perComponentAssignments.ma
//Last modified: Thu, Oct 09, 2008 02:54:53 PM
//Codeset: UTF-8
requires maya "8.5";
currentUnit -l centimeter -a degree -t pal;
fileInfo "application" "maya";
fileInfo "product" "Maya Unlimited 8.5";
fileInfo "version" "8.5 Service Pack 1 x64";
fileInfo "cutIdentifier" "200706070006-700509";
fileInfo "osv" "Linux 2.6.24-19-generic #1 SMP Wed Aug 20 17:53:40 UTC 2008 x86_64";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 37.860448929275499 26.385896938762354 40.07708061050073 ;
	setAttr ".r" -type "double3" -25.538352729604419 35.400000000001022 1.9509546221649844e-15 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 60.50319553531655;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "p1trans";
	setAttr ".t" -type "double3" -0.42759237442932019 0.50688416621549237 0.15746914111094412 ;
	setAttr ".s" -type "double3" 15.971570095055217 15.971570095055217 15.971570095055217 ;
createNode mesh -n "p1" -p "p1trans";
	setAttr -k off ".v";
	setAttr -s 2 ".iog";
	setAttr -s 8 ".iog[0].og";
	setAttr -s 8 ".iog[1].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr -s 2 ".ciog";
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 5 ".pt";
	setAttr ".pt[6]" -type "float3" -1.4901161e-08 0 0 ;
createNode transform -n "p1transinst";
	setAttr ".t" -type "double3" 19.727065659193293 0.50688416621549237 0.15746914111094412 ;
	setAttr ".s" -type "double3" 15.971570095055217 15.971570095055217 15.971570095055217 ;
parent -s -nc -r -add "|p1trans|p1" "p1transinst";
createNode lightLinker -n "lightLinker1";
	setAttr -s 6 ".lnk";
	setAttr -s 6 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode polyPlane -n "polyPlane1";
	setAttr ".sw" 2;
	setAttr ".sh" 2;
	setAttr ".cuv" 2;
createNode surfaceShader -n "surfaceShader1";
createNode shadingEngine -n "surfaceShader1SG";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 2 ".gn";
createNode materialInfo -n "materialInfo1";
createNode groupId -n "groupId1";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[3]";
	setAttr ".irc" -type "componentList" 1 "f[0:2]";
createNode groupId -n "groupId2";
	setAttr ".ihi" 0;
createNode groupId -n "groupId3";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts2";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[1]";
createNode surfaceShader -n "surfaceShader2";
	setAttr ".oc" -type "float3" 0.3019608 0.3019608 0.3019608 ;
createNode shadingEngine -n "surfaceShader2SG";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 2 ".gn";
createNode materialInfo -n "materialInfo2";
createNode groupId -n "groupId4";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts3";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0]";
createNode surfaceShader -n "surfaceShader3";
	setAttr ".oc" -type "float3" 0.69803923 0.69803923 0.69803923 ;
createNode shadingEngine -n "surfaceShader3SG";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 2 ".gn";
createNode materialInfo -n "materialInfo3";
createNode groupId -n "groupId5";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts4";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[2]";
createNode surfaceShader -n "surfaceShader4";
	setAttr ".oc" -type "float3" 1 1 1 ;
createNode shadingEngine -n "surfaceShader4SG";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo4";
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1.041667 -max 25 -ast 1.041667 -aet 50 ";
	setAttr ".st" 6;
createNode groupId -n "groupId6";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts5";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[3]";
createNode groupId -n "groupId7";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts6";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[1]";
createNode groupId -n "groupId8";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts7";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[0]";
createNode groupId -n "groupId9";
	setAttr ".ihi" 0;
createNode groupParts -n "groupParts8";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "f[2]";
createNode groupId -n "groupId10";
	setAttr ".ihi" 0;
select -ne :time1;
	setAttr ".o" 1;
select -ne :renderPartition;
	setAttr -s 6 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :lightList1;
select -ne :initialShadingGroup;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 3 ".gn";
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
connectAttr "groupId1.id" "|p1trans|p1.iog.og[0].gid";
connectAttr "surfaceShader4SG.mwc" "|p1trans|p1.iog.og[0].gco";
connectAttr "groupId3.id" "|p1trans|p1.iog.og[1].gid";
connectAttr "surfaceShader1SG.mwc" "|p1trans|p1.iog.og[1].gco";
connectAttr "groupId4.id" "|p1trans|p1.iog.og[2].gid";
connectAttr "surfaceShader2SG.mwc" "|p1trans|p1.iog.og[2].gco";
connectAttr "groupId5.id" "|p1trans|p1.iog.og[3].gid";
connectAttr "surfaceShader3SG.mwc" "|p1trans|p1.iog.og[3].gco";
connectAttr "groupId6.id" "|p1transinst|p1.iog.og[0].gid";
connectAttr "surfaceShader4SG.mwc" "|p1transinst|p1.iog.og[0].gco";
connectAttr "groupId7.id" "|p1transinst|p1.iog.og[1].gid";
connectAttr "surfaceShader1SG.mwc" "|p1transinst|p1.iog.og[1].gco";
connectAttr "groupId8.id" "|p1transinst|p1.iog.og[2].gid";
connectAttr "surfaceShader2SG.mwc" "|p1transinst|p1.iog.og[2].gco";
connectAttr "groupId9.id" "|p1transinst|p1.iog.og[3].gid";
connectAttr "surfaceShader3SG.mwc" "|p1transinst|p1.iog.og[3].gco";
connectAttr "groupParts8.og" "|p1trans|p1.i";
connectAttr "groupId2.id" "|p1trans|p1.ciog.cog[0].cgid";
connectAttr "groupId10.id" "|p1transinst|p1.ciog.cog[0].cgid";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[0].llnk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.lnk[0].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[1].llnk";
connectAttr ":initialParticleSE.msg" "lightLinker1.lnk[1].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[2].llnk";
connectAttr "surfaceShader1SG.msg" "lightLinker1.lnk[2].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[3].llnk";
connectAttr "surfaceShader2SG.msg" "lightLinker1.lnk[3].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[4].llnk";
connectAttr "surfaceShader3SG.msg" "lightLinker1.lnk[4].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[5].llnk";
connectAttr "surfaceShader4SG.msg" "lightLinker1.lnk[5].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[0].sllk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.slnk[0].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[1].sllk";
connectAttr ":initialParticleSE.msg" "lightLinker1.slnk[1].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[2].sllk";
connectAttr "surfaceShader1SG.msg" "lightLinker1.slnk[2].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[3].sllk";
connectAttr "surfaceShader2SG.msg" "lightLinker1.slnk[3].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[4].sllk";
connectAttr "surfaceShader3SG.msg" "lightLinker1.slnk[4].solk";
connectAttr ":defaultLightSet.msg" "lightLinker1.slnk[5].sllk";
connectAttr "surfaceShader4SG.msg" "lightLinker1.slnk[5].solk";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "surfaceShader1.oc" "surfaceShader1SG.ss";
connectAttr "groupId3.msg" "surfaceShader1SG.gn" -na;
connectAttr "groupId7.msg" "surfaceShader1SG.gn" -na;
connectAttr "|p1trans|p1.iog.og[1]" "surfaceShader1SG.dsm" -na;
connectAttr "|p1transinst|p1.iog.og[1]" "surfaceShader1SG.dsm" -na;
connectAttr "surfaceShader1SG.msg" "materialInfo1.sg";
connectAttr "surfaceShader1.msg" "materialInfo1.m";
connectAttr "surfaceShader1.msg" "materialInfo1.t" -na;
connectAttr "polyPlane1.out" "groupParts1.ig";
connectAttr "groupId1.id" "groupParts1.gi";
connectAttr "groupParts1.og" "groupParts2.ig";
connectAttr "groupId3.id" "groupParts2.gi";
connectAttr "surfaceShader2.oc" "surfaceShader2SG.ss";
connectAttr "groupId4.msg" "surfaceShader2SG.gn" -na;
connectAttr "groupId8.msg" "surfaceShader2SG.gn" -na;
connectAttr "|p1trans|p1.iog.og[2]" "surfaceShader2SG.dsm" -na;
connectAttr "|p1transinst|p1.iog.og[2]" "surfaceShader2SG.dsm" -na;
connectAttr "surfaceShader2SG.msg" "materialInfo2.sg";
connectAttr "surfaceShader2.msg" "materialInfo2.m";
connectAttr "surfaceShader2.msg" "materialInfo2.t" -na;
connectAttr "groupParts2.og" "groupParts3.ig";
connectAttr "groupId4.id" "groupParts3.gi";
connectAttr "surfaceShader3.oc" "surfaceShader3SG.ss";
connectAttr "groupId5.msg" "surfaceShader3SG.gn" -na;
connectAttr "groupId9.msg" "surfaceShader3SG.gn" -na;
connectAttr "|p1trans|p1.iog.og[3]" "surfaceShader3SG.dsm" -na;
connectAttr "|p1transinst|p1.iog.og[3]" "surfaceShader3SG.dsm" -na;
connectAttr "surfaceShader3SG.msg" "materialInfo3.sg";
connectAttr "surfaceShader3.msg" "materialInfo3.m";
connectAttr "surfaceShader3.msg" "materialInfo3.t" -na;
connectAttr "groupParts3.og" "groupParts4.ig";
connectAttr "groupId5.id" "groupParts4.gi";
connectAttr "surfaceShader4.oc" "surfaceShader4SG.ss";
connectAttr "|p1trans|p1.iog.og[0]" "surfaceShader4SG.dsm" -na;
connectAttr "|p1transinst|p1.iog.og[0]" "surfaceShader4SG.dsm" -na;
connectAttr "groupId6.msg" "surfaceShader4SG.gn" -na;
connectAttr "surfaceShader4SG.msg" "materialInfo4.sg";
connectAttr "surfaceShader4.msg" "materialInfo4.m";
connectAttr "surfaceShader4.msg" "materialInfo4.t" -na;
connectAttr "groupParts4.og" "groupParts5.ig";
connectAttr "groupId6.id" "groupParts5.gi";
connectAttr "groupParts5.og" "groupParts6.ig";
connectAttr "groupId7.id" "groupParts6.gi";
connectAttr "groupParts6.og" "groupParts7.ig";
connectAttr "groupId8.id" "groupParts7.gi";
connectAttr "groupParts7.og" "groupParts8.ig";
connectAttr "groupId9.id" "groupParts8.gi";
connectAttr "surfaceShader1SG.pa" ":renderPartition.st" -na;
connectAttr "surfaceShader2SG.pa" ":renderPartition.st" -na;
connectAttr "surfaceShader3SG.pa" ":renderPartition.st" -na;
connectAttr "surfaceShader4SG.pa" ":renderPartition.st" -na;
connectAttr "surfaceShader1.msg" ":defaultShaderList1.s" -na;
connectAttr "surfaceShader2.msg" ":defaultShaderList1.s" -na;
connectAttr "surfaceShader3.msg" ":defaultShaderList1.s" -na;
connectAttr "surfaceShader4.msg" ":defaultShaderList1.s" -na;
connectAttr "lightLinker1.msg" ":lightList1.ln" -na;
connectAttr "|p1trans|p1.ciog.cog[0]" ":initialShadingGroup.dsm" -na;
connectAttr "|p1transinst|p1.ciog.cog[0]" ":initialShadingGroup.dsm" -na;
connectAttr "groupId1.msg" ":initialShadingGroup.gn" -na;
connectAttr "groupId2.msg" ":initialShadingGroup.gn" -na;
connectAttr "groupId10.msg" ":initialShadingGroup.gn" -na;
// End of perComponentAssignments.ma
