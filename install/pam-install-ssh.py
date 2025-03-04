gatekeeper_config = """
# SDSLabs gatekeeper configuration START

session optional pam_exec.so seteuid log=/opt/gatekeeper/logs/ssh.logs /opt/gatekeeper/bin/gatekeeper ssh

# SDSLabs gatekeeper configuration END
"""

inside_gatekeeper_config_section = False

def process_line(line):
	global inside_gatekeeper_config_section

	if inside_gatekeeper_config_section and line == "# SDSLabs gatekeeper configuration END\n":
		inside_gatekeeper_config_section = False
		return ''

	if inside_gatekeeper_config_section:
		return ''

	if line == "# SDSLabs gatekeeper configuration START\n":
		inside_gatekeeper_config_section = True
		return ''

	return line

def main():
	iput = open("/etc/pam.d/sshd")
	oput = open("gatekeeper_tmp_ssh", "w")
	lines = iput.readlines()
	for l in lines:
		oputline = process_line(l)
		oput.write(oputline)

	oput.write(gatekeeper_config)

	iput.close()
	oput.close()


main()