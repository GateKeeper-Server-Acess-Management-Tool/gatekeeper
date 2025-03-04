gatekeeper_config = """
# SDSLabs gatekeeper configuration START

UsePAM yes
PasswordAuthentication no
AuthorizedKeysCommand /opt/gatekeeper/bin/gatekeeper auth -u %u -t %t -p %k
AuthorizedKeysCommandUser root

# SDSLabs gatekeeper configuration END
"""


modified_options = [
	'AuthorizedKeysCommand',
	'AuthorizedKeysCommandUser',
	'PasswordAuthentication',
	'UsePAM'
]

inside_gatekeeper_config = False

def process_line(line):
	global inside_gatekeeper_config

	if inside_gatekeeper_config and line == "# SDSLabs gatekeeper configuration END\n":
		inside_gatekeeper_config = False
		return ''

	if inside_gatekeeper_config:
		return ''

	if line == "# SDSLabs gatekeeper configuration START\n":
		inside_gatekeeper_config = True
		return ''

	l = line.strip()
	i = l.find('#')
	if i != -1:
		l = l[:i]
	if len(l) == 0:
		return line
	i = l.find(' ')
	j = l.find('\t')
	if i == -1 and j != -1:
		i = j
	elif j == -1 and i != -1:
		pass
	elif j == -1 and i == -1:
		return line
	else:
		i = min(i, j)
	key = l[:i]
	value = l[i+1:].strip()
	if key in modified_options:
		# comment this line
		return '# gatekeeper: Commenting the line below out\n#' + line
	else:
		return line

def main():
	inp = open("/etc/ssh/sshd_config")
	out = open("gatekeeper_tmp_sshd_config", "w")
	lines = inp.readlines()
	for l in lines:
		output_line = process_line(l)
		out.write(output_line)

	out.write(gatekeeper_config)

	inp.close()
	out.close()


main()
