import util 

features_dna = util.FEATURE_KEYS_DNA
td0 = ('allele', 'allele')

features_prt = util.FEATURE_KEYS_PRT
tp1 = ('BINDING', 'BINDING')

print 'td0 is %s: %s' % (td0, td0 == features_dna[0])
print 'there are %i dna features: %s' % (63, 63==len(features_dna))

print 'tp1 is %s: %s' % (tp1, tp1 == features_prt[1])
print 'there are %i prt features: %s' % (39, 39==len(features_prt))


# <!DOCTYPE html>
# {% extends 'sequencelistings/base.html' %}
# {% block content %}
# {% load staticfiles %}
# 
# <h2>WELCOME</h2>
# <p>Welcome to the xml sequence listing authoring tool.</p>
# <p>This is a prototype (so limited functionality!) built only for demonstration purposes. The tool enables the user to:
# </p>
# <ol>
#         <li>create a sequence listing, i.e. 
#             <ul>
#                 <li>create the general information section</li>
#                 <li>create the the sequence data section (create sequence, feature, qualifier)</li>
#             </ul>
#         </li>
#         <li>Store and display previously created sequence listings
#         </li>
#         <li>Export the sequence listing as XML file
#         </li>
#         <li>Display in the browser the generated XML file (by using XSLT stylesheet)
#         </li>
#         
#     </ol>
# 
# <h2>SEQUENCE LISTING PORTOFOLIO</h2>
# <p>This section enables you to navigate to previously created sequence listings.</p>
# {% if sequenceListings %}
#     <table>
#         <tr>
#             <th>file name</th>
#             <th>invention title</th>
#             <th>number of sequences</th>
#         </tr>
#         {% for sl in sequenceListings %}
#             <tr>
#                 <td><a href="{% url 'sequencelistings:detail' sl.id %}">{{ sl.fileName }}</a></td>
#                 <td>{{sl.inventionTitle}}</td>
#                 <td>{{sl.sequenceTotalQuantity}}</td>
#             </tr>
#         {% endfor %}
#     </table>
# {% else %}
#     <p>No sequence listings are available.</p>
# {% endif %}
# <h2>SEQUENCE LISTING GENERATOR</h2>
# <p>This section enables you to create a new sequence listing.</p>
# <a href='/sequencelistings/add_sequencelisting/'>Add new sequence listing</a>
# {% endblock %}