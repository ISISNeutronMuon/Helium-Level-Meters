#!/usr/bin/python
import cx_Oracle
import datetime
from collections import OrderedDict

print "Content-Type: text/html"
print "refresh: 900"
print

# The items above provide html header information for rendering of the page to a web browser.
stale_row_name = 'oldrow'
no_data = 'noData'
button_name = 'showHideButton'

currentDT = datetime.datetime.now()

print """<html>
<head>

  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js">  </script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js">   </script>

<style>
table, th, td {
    border: 3px solid turquoise;
    border-collapse:collapse;
}
</style>
</head>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery.tablesorter/2.30.6/js/jquery.tablesorter.js"></script>
<body>"""
print """
<table id='myTable' class='tablesorter' style=width:100%>
<thead>"""


# Items that are relatively constant, the column list, and a delimiter list.
def header_print(headings):
    for heading_id, label in headings.iteritems():
        print("<th id={} width=20% style=font-family:verdana;font-size:18px;cursor:pointer;>{}</th>".format(heading_id, label))


link = " class='arrows' src=https://cdn2.iconfinder.com/data/icons/music-player-icons-filled/46/Drop_{}-512.png"
down_link = link.format("Down")
up_link = link.format("Up")

style = " style='width:5%; display:none;'"

titles = OrderedDict()
titles["coord"] = "Coordinator <img" + down_link + style + " id='downcoord'><img" + up_link + style + " id='upcoord'>"
titles["coordloc"] = "Coordinator Location <img" + down_link + style + " id='downcoordloc'><img" + up_link + style + " id='upcoordloc'>"
titles["dev"] = "Device <img" + down_link + style + " id='downdev'><img" + up_link + style + " id='updev'>"
titles["meas"] = "Measurement <img" + down_link + style + " id='downmeas'><img" + up_link + style + " id='upmeas'>"
titles["d_t"] = "Date/Time <img" + down_link + style + " id='downd_t'><img" + up_link + style + " id='upd_t'>"

header_print(titles)
print"</thead>" \
     "<tbody>"


# The print statement is of necessity long winded for this, as such it has been placed into a
# function of it's own, note that the default fill is a space.
# This uses the string manipulation mini-language, to allow for at least some level of presentation.
def print_row(print_line, id_tag="", other_tags=""):
    print("<tr {} id={}>".format(other_tags, id_tag))
    for item in print_line:
        print("<td>{}</td>".format(item))
    print("</tr>")


# Connect to the database, note that REPORT can only see this view, and has nothing but SELECT abilities.
connection = cx_Oracle.connect("REPORT", "$REPORT", "NDAHEMON")
# Create a cursor to collate and read the data.
cursor = connection.cursor()
# Use the cursor to get all the data from the view.
cursor.execute("""SELECT * FROM REPORT_VIEW""")

# Loop through the cursor entries, convert the datetime to a string for display and print the data.
entries = list(cursor)

print"</tbody>"


def get_key(item):
    return item[0]

last_coord = ""
entries = sorted(entries, key=get_key, reverse=True)
for entry in entries:
    entry = list(entry)
    start_delta = datetime.timedelta(weeks=1)
    one_week_ago = currentDT - start_delta
    is_old = one_week_ago > entry[4]

    last_word = entry[0].split()[-1]
    if last_coord != entry[0]:
        other_tags = "data-toggle='collapse' style=cursor:pointer data-target='.{}'".format(last_word)
    else:
        other_tags = "class='{} collapse in'".format(last_word)

    if entry[3] is None:
        print_row(entry, no_data, other_tags)
    elif is_old:
        print_row(entry, stale_row_name, other_tags)
    else:
        print_row(entry, other_tags = other_tags)  # Close out the items created.
    last_coord = entry[0]
cursor.close()
connection.close()


def search_id(id_to_search_for):
    return "document.getElementById('{}')".format(id_to_search_for)


def get_background_colour(id_to_search_for):
    return search_id(id_to_search_for) + """.style.backgroundColor"""


print """<script>
window.onload=function old_row_flash() {
    setInterval(function(){
    if (""" + get_background_colour(stale_row_name) + """ ==='lightgrey') {
    	""" + get_background_colour(stale_row_name) + """ ='white';
    }
    else {
    	""" + get_background_colour(stale_row_name) + """ ='lightgrey';
        
    }}, 1000);
               
    setInterval(function(){ 
    if (""" + get_background_colour(no_data) + """ ==='red'){
    	""" + get_background_colour(no_data) + """ ='white';
    }
    else {
    	""" + get_background_colour(no_data) + """ ='red';
    
    }}, 1000);       
}

$(document).ready(function() 
    { 
        $("#myTable").tablesorter(); 
    }
); 

function upDown(down_arrow, up_arrow) {
    var x = document.getElementsByClassName("arrows");
    for (var i = 0; i < x.length; i++) {
        if (x[i].id!==down_arrow && x[i].id!==up_arrow) {
            x[i].style.display = "none";
        }
    }
    var down = document.getElementById(down_arrow);
    var up = document.getElementById(up_arrow);
    if (down.style.display === "") {
        down.style.display = "none";
        up.style.display = '';
    } else {
        down.style.display = "";
        up.style.display = 'none';
    }
    
}
"""


def headings_functions(heading_id, down_arrow, up_arrow):
    return search_id(heading_id) + ".addEventListener('click', function() {{upDown('{}', '{}');}} )".format(down_arrow,
                                                                                                            up_arrow)


print headings_functions('coord', 'downcoord', 'upcoord')
print headings_functions('coordloc', 'downcoordloc', 'upcoordloc')
print headings_functions('dev', 'downdev', 'updev')
print headings_functions('meas', 'downmeas', 'upmeas')
print headings_functions('d_t', 'downd_t', 'upd_t')
print "</script>"


def change_display(id_to_search_for):
    return search_id(id_to_search_for) + ".style.display"


def change_button_text(id_to_search_for):
    return search_id(id_to_search_for) + ".innerHTML"


def show_hide(change):
    return "Click to {} stale data".format(change)


print """
<button  id=""" + button_name + """ onclick='hideData()' style=cursor:pointer>""" + show_hide('hide') + """</button>
<script>

function hideData(){
    
    if(""" + change_display(stale_row_name) + """ === '') {
       	""" + change_display(stale_row_name) + """ = 'none';
        """ + change_button_text(button_name) + """ = '""" + show_hide('show') + """';
    }
    else {   
    	""" + change_display(stale_row_name) + """ = '';
       
        """ + change_button_text(button_name) + """ = '""" + show_hide('hide') + """';
    }
}

setInterval(function(){
    window.location.reload();
},300000);

</script>    
</table>
</body>
</html>"""
