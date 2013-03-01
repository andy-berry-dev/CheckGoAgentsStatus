import sys
sys.path.append('py-libs')
import requests, json, argparse

parser = argparse.ArgumentParser(description='Checks the status of Go agents.')
parser.add_argument('--hostname', help='The hostname for the Go server', required=True)
parser.add_argument('--port', help='The port for the Go server', required=False, default=80)
parser.add_argument('--username', help='The username to use for API requests', required=False, default="")
parser.add_argument('--password', help='The password to use for API requests', required=False, default="")
args = vars(parser.parse_args())



def isAgentLowOnSpace(agentSpace, minSpace):
	agentSpace = agentSpace.replace(" ","").replace("GB","")
	if "MB" in agentSpace:
		return true
	else:
		return float(agentSpace) < minSpace
		

goAgentsUrl = "http://newgo/go/api/agents" 
response = requests.get(goAgentsUrl, auth=('build', 'd3V4321'))

agentsList = response.json()
for agent in agentsList:
	agentName = agent["agent_name"]
	agentIp = agent["ip_address"]
	agentFreeSpace = agent["free_space"]
	
	if isAgentLowOnSpace(agentFreeSpace, 10):
		print "AGENT "+agentName+" low on space."
	
	
	

	