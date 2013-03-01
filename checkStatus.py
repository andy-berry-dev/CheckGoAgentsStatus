import sys
sys.path.append('py-libs')
import requests, json

def isAgentLowOnSpace(agentSpace, minSpace):
	agentSpace = agentSpace.replace(" ","").replace("GB","")
	if "MB" in agentSpace:
		return true
	else:
		return float(agentSpace) < minSpace
		

goAgentsUrl = "http://localhost:8000/go/api/agents" 
response = requests.get(goAgentsUrl, auth=('build', 'd3V4321'))

agentsList = response.json()
for agent in agentsList:
	agentName = agent["agent_name"]
	agentIp = agent["ip_address"]
	agentFreeSpace = agent["free_space"]
	
	if isAgentLowOnSpace(agentFreeSpace, 10):
		print "AGENT "+agentName+" low on space."
	
	
	

	