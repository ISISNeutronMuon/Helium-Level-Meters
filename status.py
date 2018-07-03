#!/usr/bin/python
print "Content-Type: text/plain"
print "refresh: 900"
print

# The items above provide html header information for rendering of the page to a web browser.

import cx_Oracle

# Use these lengths for print alignment.
coord_len = 20 # Database is set to 50
coloc_len = 20 # Database is set to 50
dev_len = 30  # Database is set to 50
meas_len = 11 # Database is set to 4, word is 11 long
date_len = 20 # To provide space for the date string without making it feel cramped

# Items that are relatively constant, the column list, and a delimiter list.
header_line = ["Coordinator","Coordinator Location","Device","Measurement","Date/Time"]
delimiting_line = [""]*5

# The print statement is of necessity long winded for this, as such it has been placed into a
# function of it's own, note that the default fill is a space.
# This uses the string manipulation mini-language, to allow for at least some level of presentation.
def to_screen(print_line,fill = " "):
	print "{0:{filler}<{width}}".format(print_line[0], filler = fill, width = coord_len)," ","{0:{filler}<{width}}".format(print_line[1], filler = fill, width = coloc_len)," ","{0:{filler}<{width}}".format(print_line[2], filler = fill, width = dev_len)," ","{0:{filler}<{width}}".format(print_line[3], filler = fill, width = meas_len)," ","{0:{filler}<{width}}".format(print_line[4], filler = fill, width = date_len)

# Print the column headings and a delimiter.
to_screen(header_line)
to_screen(delimiting_line,"-")
	
# Connect to the database, note that REPORT can only see this view, and has nothing but SELECT abilities.
connection = cx_Oracle.connect("REPORT", "$REPORT", "NDAHEMON")
# Create a cursor to collate and read the data.
cursor = connection.cursor()
# Use the cursor to get all the data from the view.
cursor.execute("""SELECT * FROM REPORT_VIEW""")

# Loop through the cursor entries, convert the datetime to a string for display and print the data.
for entry in cursor:
	entry = list(entry)
	entry[4] = entry[4].strftime("%H:%M:%S %d-%m-%y")
	to_screen(entry)

# Close out the items created.
cursor.close()
connection.close()
