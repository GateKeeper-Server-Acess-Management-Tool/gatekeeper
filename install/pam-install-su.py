gatekeeper_config = """
#  Gatekeeper configuration START

session optional pam_exec.so seteuid log=/opt/gatekeeper/logs/su.logs /opt/gatekeeper/bin/gatekeeper su

#  Gatekeeper configuration END
"""

inside_gatekeeper_config_section = False

def process_line(line):
	global inside_gatekeeper_config_section

	if inside_gatekeeper_config_section and line == "#  Gatekeeper configuration END\n":
		inside_gatekeeper_config_section = False
		return ''

	if inside_gatekeeper_config_section:
		return ''

	if line == "#  Gatekeeper configuration START\n":
		inside_gatekeeper_config_section = True
		return ''

	return line

def main():
	iput = open("/etc/pam.d/su")
	oput = open("gatekeeper_tmp_su", "w")
	lines = iput.readlines()
	for l in lines:
		oputline = process_line(l)
		oput.write(oputline)

	oput.write(gatekeeper_config)

	iput.close()
	oput.close()


main()