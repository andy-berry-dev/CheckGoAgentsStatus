import sys
sys.path.append('py-libs')
import requests, json, argparse

parser = argparse.ArgumentParser(description='Checks the status of Go agents.')
parser.add_argument('--hostname', help='The hostname for the Go server', required=True)
parser.add_argument('--port', help='The port for the Go server', required=False, default=80)
parser.add_argument('--username', help='The username to use for API requests', required=False, default="")
parser.add_argument('--password', help='The password to use for API requests', required=False, default="")
parser.add_argument('--minSpace', help='The minimum space for Go agents before they are disabled', required=False, default=1)
args = vars(parser.parse_args())

goHostname = args["hostname"]
goPort = args["port"]
goUser = args["username"]
goPass = args["password"]
minAgentSpace = args["minSpace"]

exitCode = 0

def isAgentLowOnSpace(agentSpace, minSpace):
	agentSpace = agentSpace.replace(" ","").replace("GB","")
	if "MB" in agentSpace:
		return true
	else:
		return float(agentSpace) < minSpace
		

goAgentsUrl = "http://" + goHostname + ":" + str(goPort) + "/go/api/agents" 
if (goUser != "" and goPass != ""):
	response = requests.get(goAgentsUrl, auth=(goUser, goPass))
else:
	response = requests.get(goAgentsUrl)

response.raise_for_status()

agentsList = response.json()
for agent in agentsList:
	agentName = agent["agent_name"]
	agentIp = agent["ip_address"]
	agentFreeSpace = agent["free_space"]
	
	if isAgentLowOnSpace(agentFreeSpace, minAgentSpace):
		print "Agent "+agentName+" low on space"
	
	
	

	