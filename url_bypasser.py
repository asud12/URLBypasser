#!/usr/bin/env python3
import sys
import os
import string
import signal
import random
import requests
from resources.payload_headers import payload_headers,payload_header_values

def signal_handler(sig,frame):
	print("\033[1;31m\n[!] Control-C detected. Exiting...")
	sys.exit(9)

class P():
	def print_result(self, r_obj, hide_code, hide_size, custom_header=""):
		
		end_c = "\033[0m"
		if str(r_obj.status_code)[0] == "4":
			c = "\033[1;31m"
		else:
			c = "\033[1;32m"

		if str(r_obj.status_code) in hide_code:
			pass		
		elif str(len(r_obj.content)) in hide_size:
			pass
		elif custom_header == "":
			#Table header - "{:<20} {:<50} {:<20} {:<20} "
			print("{}{:<20}{} {:<20} {:<20} {:<50}".format(
				c,
				r_obj.status_code,
				end_c,
				len(r_obj.content),
				r_obj.request.method,
				r_obj.request.path_url,
			))
		else:
			header_str = "{}: {}".format(custom_header, r_obj.request.headers[custom_header])
			print("{}{:<20}{} {:<20} {:<20} {:<30} {:<60}".format(
				c,
				r_obj.status_code,
				end_c,
				len(r_obj.content),
				r_obj.request.method,
				r_obj.request.path_url,
				header_str
			))
		
	def print_debug_req_info(self, r_obj):
		sys.stdout.write("\033[1;34m--- [Debug] ---\033[0m\n")
		print('{}\r\n{}\r\n\r\n{}'.format(
        	r_obj.request.method + ' ' + r_obj.request.url,
        	'\r\n'.join('{}: {}'.format(k, v) for k, v in r_obj.request.headers.items()),
        	r_obj.request.body)
		)

class RequesterBase():

	def __init__(self, hide_code, hide_size, verbose):

		self.p = P
		self.hide_codes = hide_codes
		self.hide_sizes = hide_sizes
		self.verbose = verbose

	def make_request(self, verb, path, additional_headers={}, data={}, custom_header=""):

		url_to_request = "{}".format(path).strip()

		r = requests.request(verb, url_to_request, headers=additional_headers, data=data, allow_redirects=False)

		status = int(r.status_code)
		size   = len(r.content)

		self.p.print_result(self, r, self.hide_codes, self.hide_sizes, custom_header=custom_header)

		if self.verbose:
			if not status in self.hide_codes:
				self.p.print_debug_req_info(self, r)

def gen_rand_string():

	master = string.ascii_uppercase + string.ascii_lowercase + string.digits

	return ''.join(random.choice(master) for i in range(10))

def replace_random(base_string):

	if "[random_string]" in base_string:
		return base_string.replace("[random_string]", gen_rand_string())
	else:
		return base_string

def banner():
		print("""	      __           __       __        __   __   ___  __     
	|  | |__) |       |__) \ / |__)  /\  /__` /__` |__  |__)    
	\__/ |  \ |___    |__)  |  |    /~~\ .__/ .__/ |___ |  \    

	v1.0

	@_g0dmode
	@dcocking7

	""")

def printhelp():
	print("Usage: {} [url] [base_path] (optional)".format(sys.argv[0]))
	print("")
	print("\t{:<20} \t\t - {:<100}".format("url", "The url (e.g. https://google.com)"))
	print("\t{:<20} \t\t - {:<100}".format("base_path", "The base path you want to access (e.g. /api)"))
	print("")
	print("Optional arguments:")
	print("")
	print("\tAttack Options:")
	print("")
	print("\t\t{:<20} \t - {:<100}".format("--verbs", "Cycle through all the verbs for the specified path."))
	print("\t\t{:<20} \t - {:<100}".format("--headers", "Cycle through all of the headers (defined in resources/payload_headers.py)"))
	print("\t\t{:<20} \t - {:<100}".format("--payloads (default)", "Try all of the payloads (defined in resources/payload_checks.txt)"))
	print("")
	print("\tRequest Options:")
	print("")
	print("\t\t{:<13} {:<7} \t - {:<100}".format("--user-agent", "[string]", "Cycle through all the verbs for the specified path."))
	print("")
	print("\tFilter Options:")
	print("")
	print("\t\t{:<5} {:<10} \t - {:<100}".format("--hc", "[code]", "The response code(s) to hide (e.g. --hc 302 or --hc 404,400)"))
	print("\t\t{:<5} {:<10} \t - {:<100}".format("--hs", "[size]", "The response size to hide (e.g. --hs 4096 or --hs 4096,1024"))
	print("\t\t{:<20} \t - {:<100}".format("--verbose","Show debug information"))
	print("")
	print("Examples:")
	print("")
	print("\t{} https://www.google.com/ /api".format(sys.argv[0]))
	print("\t{} https://www.google.com/ /api --hc 302,404 --verbs".format(sys.argv[0]))
	print("\t{} https://www.google.com/ /api --hs 1024 --headers".format(sys.argv[0]))
	print("")

def do_verbs(rb, base_url, base_path, verbs, additional_headers):
	print("\033[1;32m[+]\033[0m Performing verb attacks.\n")
	print("{:<20} {:<20} {:<20} {:<30}".format(
	"Response code",
	"Response size",
	"Verb",
	"Path",
	))
	print("-"*94)
	
	for verb in verbs:
		verb = verb.strip()
		url = "{}/{}".format(base_url, base_path)
		rb.make_request(verb, url, additional_headers=additional_headers)

def do_headers(rb, base_url, base_path, ah):
	print("\033[1;32m[+]\033[0m Performing header attacks.\n")
	print("{:<20} {:<20} {:<20} {:<30} {:<60}".format(
		"Response code",
		"Response size",
		"Verb",
		"Path",
		"Custom Header"
	))
	print("-"*155)

	for header in payload_headers:
		for header_value in payload_header_values:

			# request base url for x-original-url & x-rewrite-url to work correctly
			if header == "X-Original-URL" or header == "X-rewrite-url":
				url = "{}/{}".format(base_url, "")
			else:
				url = "{}/{}".format(base_url, base_path) 
			
			additional_headers = {}	
			
			header_value = header_value.format(base_url=base_url, base_path=base_path)
			additional_headers[header] = header_value.strip()
			# Add in default headers
			for h,c in ah.items():
				additional_headers[h] = c

			rb.make_request("GET", url, additional_headers=additional_headers, custom_header=header)

def do_payloads(rb, base_url, base_path, ah):
	print("\033[1;32m[+]\033[0m Performing different path attacks.\n")
	print("{:<20} {:<20} {:<20} {:<30}".format(
		"Response code",
		"Response size",
		"Verb",
		"Path",
	))
	print("-"*94)
	for payload in payloads:
		payload = replace_random(payload).format(base_url, base_path)

		if "[file_extension]" in payload:
			for e in extensions:
				payload = payload.replace("[file_extension]", e)
				rb.make_request("GET", payload, additional_headers=ah)

		elif "[param]" in payload:
			for p in params:
				payload = payload.replace("[param]", p)
				rb.make_request("GET", payload, additional_headers=ah)
		else:
			rb.make_request("GET", payload, additional_headers=ah)

if __name__ == "__main__":

	banner()
	signal.signal(signal.SIGINT, signal_handler)

	if len(sys.argv) < 3:
		printhelp()
		exit(1)

	ah = {}
	
	fHandle = open("resources/verbs.txt", "r")
	verbs = fHandle.readlines()
	fHandle.close

	fHandle = open("resources/payload_checks.txt", "r")
	payloads = fHandle.readlines()

	fHandle = open("resources/extensions.txt", "r")
	extensions = fHandle.readlines()

	fHandle = open("resources/params.txt", "r")
	params = fHandle.readlines()

	base_url = sys.argv[1]
	base_path = sys.argv[2]

	if base_url.endswith("/"):
		base_url = base_url[:-1]

	if base_path.startswith("/"):
		base_path = base_path[1:]

	if "--hc" in sys.argv:
		hide_code = sys.argv[sys.argv.index("--hc")+1]
		if "," in hide_code:
			hide_codes = hide_code.split(",")
		else:
			hide_codes = [hide_code]
	else:
		hide_codes = [000]

	if "--hs" in sys.argv:
		hide_size = sys.argv[sys.argv.index("--hs")+1]
		if "," in hide_size:
			hide_sizes = hide_size.split(",")
		else:
			hide_sizes = [hide_size]
	else:
		hide_sizes = [000]

	if "-v" in sys.argv or "--verbose" in sys.argv:
		verbose = 1
	else:
		verbose = 0

	if "--user-agent" in sys.argv:
		ah["User-Agent"] = sys.argv[sys.argv.index("--user-agent")+1]
	else:
		ah["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36 Edg/88.0.705.81"

	rb = RequesterBase(hide_codes, hide_sizes, verbose)

	print("Settings:")
	print("")
	print("Base URL   : {}".format(base_url))
	print("Base Path  : /{}".format(base_path))
	print("User-Agent : {}".format(ah["User-Agent"]))
	print("")

	verbs_check = False
	headers_check = False
	payloads_check = False
	if "--verbs" in sys.argv:
		verbs_check = True
				
	if "--headers" in sys.argv:
		headers_check = True

	if "--payloads" in sys.argv:
		payloads_check = True
		
	if "-a" in sys.argv or "--all" in sys.argv or (payloads_check == False and headers_check == False and verbs_check == False):
		do_verbs(rb, base_url, base_path, verbs, ah)
		print("Done.\n")
		do_payloads(rb, base_url, base_path, ah)
		print("Done.\n")
		do_headers(rb, base_url, base_path, ah)
		print("Done.\n")
		exit(1)

	if verbs_check:
		do_verbs(rb, base_url, base_path, verbs, ah)
		print("Done.\n")
	if payloads_check:
		do_payloads(rb, base_url, base_path, ah)
		print("Done.\n")
	if headers_check:
		do_headers(rb, base_url, base_path, ah)
		print("Done.\n")
