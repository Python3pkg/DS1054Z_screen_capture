__author__ = 'RoGeorge'
#
# TODO: Port for Linux
# TODO: Add command line parameters for IP, file path and file format
# TODO: Add GUI
# TODO: Add browse and custom filename selection
# TODO: Create executable distributions
# TODO: Use git, upload to GitHub
#
import telnetlib_receive_all
import time
import Image
import StringIO
import sys
import os

# Update the next lines for your own default settings:
path_to_save = ""
save_format = "PNG"
IP_DS1104Z = "192.168.1.3"

# Port used by Rigol LXI protocol
port = 5555

# Check parameters
script_name = os.path.basename(sys.argv[0])

# Print usage
print
print "Usage:"
print "    " + script_name + " [oscilloscope_IP [save_path [PNG | BMP]]]"
print
print "Usage examples:"
print "    " + script_name
print "    " + script_name + " 192.168.1.3"
print "    " + script_name + " 192.168.1.3 my_place_for_osc_captures"
print "    " + script_name + " 192.168.1.3 my_place_for_osc_captures BMP"
print
print "This program capture the image displayed"
print "    by a Rigol DS1000Z series oscilloscope, then save it on the computer"
print "    as a PNG or BMP file with a timestamp in the file name."
print
print "    The program is using LXI protocol, so the computer"
print "    must have LAN connection with the oscilloscope."
print "    USB and/or GPIB connections are not used by this software."
print
print "    No VISA, IVI or Rigol drivers are needed."
print

# Create/check if 'path' exists


# Check network response (ping)
response = os.system("ping -n 1 " + IP_DS1104Z + " > nul")
if response != 0:
	print
	print "No response pinging " + IP_DS1104Z
	print "Check network cables and settings."
	print "You should be able to ping the oscilloscope."

# Open a modified telnet session
# The default telnetlib drops 0x00 characters,
#   so a modified library 'telnetlib_receive_all' is used instead
tn = telnetlib_receive_all.Telnet(IP_DS1104Z, port)
tn.write("*idn?")                       # ask for instrument ID
instrument_id = tn.read_until("\n", 1)

# Check if instrument is set to accept LAN commands
if instrument_id == "command error":
	print instrument_id
	print "Check the oscilloscope settings."
	print "Utility -> IO Setting -> RemoteIO -> LAN must be ON"
	sys.exit("ERROR")

# Check if instrument is indeed a Rigol DS1000Z series
id_fields = instrument_id.split(",")
if (id_fields[0] != "RIGOL TECHNOLOGIES") or \
	((id_fields[1][:3] != "DS1") and (id_fields[1][-1] != "Z")):
	print
	print "ERROR: No Rigol from series DS1000Z found at ", IP_DS1104Z
	sys.exit("ERROR")

print "Instrument ID:"
print instrument_id

# Prepare filename as C:\MODEL_SERIAL_YYYY-MM-DD_HH.MM.SS
timestamp = time.strftime("%Y-%m-%d_%H.%M.%S", time.localtime())
filename = path_to_save + id_fields[1] + "_" + id_fields[2] + "_" + timestamp

# Ask for an oscilloscope display print screen
tn.write("display:data?")
print "Receiving..."
buff = tn.read_until("\n", 10)

# Just in case the transfer did not complete in 10 seconds
while len(buff) < 1152068:
	tmp = tn.read_until("\n", 1)
	if len(tmp) == 0:
		break
	buff += tmp

# Strip TMC Blockheader and last 3 bytes
buff = buff[11:-3]

# Save as PNG
im = Image.open(StringIO.StringIO(buff))
im.save(filename + ".png", "PNG")
print "Saved file:", filename + ".png"

# Save as BMP
# scr_file = open(filename + ".bmp", "wb")
# scr_file.write(buff)
# scr_file.close()

tn.close()


# The code after this line was only for debugging purposes.
# It prints the BMP header params, which are always the same.
#
# def print_hex(prt_buff):
# 	print "(",
# 	for c in prt_buff:
# 		print hex(ord(c)),
# 	print ")"
#
#
# def print_dec(prt_buff):
# 	n = 0
# 	for c in reversed(prt_buff):
# 		n = 256 * n + ord(c)
# 	print n,
#
#
# def prt_dec_hex(prt_buff):
# 	print_dec(prt_buff)
# 	print_hex(prt_buff)
#
#
# def print_next_as(description, nr_of_bytes):
# 	print description + " " * (50 - len(description)),
# 	prt_dec_hex(buff[print_next_as.offset:print_next_as.offset+nr_of_bytes])
# 	print_next_as.offset += nr_of_bytes
# print_next_as.offset = 2
#
#
# print
# print "BMP header"
# print "----------"
# print "Header type:                                      ", buff[0:2],
# print_hex(buff[0:2])
# print_next_as("BMP size in bytes:", 4)
# print_next_as("reserved 2 bytes:", 2)
# print_next_as("reserved 2 bytes:", 2)
# print_next_as("Offset for BMP start of pixels array:", 4)
# print
# print "DIB header"
# print "----------"
# print_next_as("Number of DIB header bytes:", 4)
# print_next_as("Image width (in pixels):", 4)
# print_next_as("Image height (in pixels):", 4)
# print_next_as("Number of color planes:", 4)
# print_next_as("Number of bits per pixel:", 2)
# print_next_as("Compression type used:", 4)
# print_next_as("Size of the raw bitmap data (including padding):", 4)
# print_next_as("Horizontal print resolution (pixels/meter):", 4)
# print_next_as("Vertical print resolution (pixels/meter):", 4)
# print_next_as("Number of colors in palette:", 4)
# print_next_as("Important colors (0 means all):", 4)
# print_next_as("First pixel (BGR):", 3)
