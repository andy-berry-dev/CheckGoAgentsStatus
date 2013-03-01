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
		return float(agentSpace) < float(minSpace)
		
def print_err(*args):
    sys.stderr.write(' '.join(map(str,args)) + '\n')

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
	agentUuid = agent["uuid"]
	
	if isAgentLowOnSpace(agentFreeSpace, minAgentSpace):
		exitCode = 1
		print "Agent " + agentName + " has " + agentFreeSpace + " free space which is too low - disabling it."
		disableAgentUrl = "http://" + goHostname + ":" + str(goPort) + "/go/api/agents/" + agentUuid + "/disable"
	
		if (goUser != "" and goPass != ""):
			response = requests.post(disableAgentUrl, auth=(goUser, goPass))
		else:
			response = requests.post(disableAgentUrl)
			
		if (response.status_code != requests.codes.ok):
			exitCode = 1
			print_err("Error while trying to disable " + agentName, "using URL " + disableAgentUrl, response.text)

exit(exitCode)
