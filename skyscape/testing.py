
import skyscape #import the module
c = skyscape.Connection('apiusername', 'org', 'password', 'https://api.vcd.portal.skyscapecloud.com/api', '5.6') #initialise the connection
c.login() #login
c.connected() #check session status
c.logout() #logout

vse = c.get_edgegateway() #gets all edge gateways, filter options available
vse = c.get_edgegateway(printoutput=True) #gets all edge gateways, filter options available, this prints the output to the screen, this option is avaialble on all
vm = c.get_vm() #gets all vm's, filter options available

vse[0].list_firewall_rules() #print all the firewall rules to the screen
vse.firewall[0].Description #get a firewall rule description

vm[0].list_links() #prints all of the available methods out to the screen
vm[0].links[0].invoke() #invokes a command, you can pass data within the parenthesis here if it's a POST or PUT command.