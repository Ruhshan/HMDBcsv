import xml.etree.ElementTree as etree
import re, csv
def get_properties(path):
	tree = etree.parse(path)
	id=re.search('HMDB\d+',path).group()
	root = tree.getroot()
	name=root.find('name').text
	pred_prop=root.find('predicted_properties')
	property_value={'logp':'NA', 'logs':'NA','solubility':'NA','pka_strongest_basic':'NA','average_mass':'NA',
						'polar_surface_area':'NA','refractivity':'NA','polarizability':'NA','rotatable_bond_count':'NA',
						'acceptor_count':'NA','donor_count':'NA','physiological_charge':'NA','pka_strongest_acidic':'NA'}
	for prop in pred_prop.findall('property'):
		#print(prop.find('kind').text,prop.find('value').text,prop.find('source').text)
		p=prop.find('kind').text
		if p in property_value.keys():
			v=prop.find('value').text
			property_value[p]=v
	##removing unit from solubility
	property_value['solubility']=property_value['solubility'].replace(' g/L','')
	##adding name and id
	property_value['name']=name
	property_value['id']=id
	return property_value

paths=open('all_id_list','r').read().split()

final={}
c=0
first=0
print("Properties collected:",end='\n\t')
for p in paths:
	 properties=get_properties(p)
	 final[properties['id']]=properties
	 c+=1
	 print("\r\t",c,end='')

c=0
print("\n*******************************")
print("Printed to file:",end='\n\t')
with open('all_hmdb.csv','w') as f:
	fields=('id','name','average_mass','solubility','logp','logs','pka_strongest_acidic','pka_strongest_basic',
	'physiological_charge','refractivity','polarizability','polar_surface_area','rotatable_bond_count','acceptor_count',
	'donor_count')
	f.write(";".join(fields)+"\n")
	writer = csv.DictWriter(f, fields, delimiter=';',lineterminator='\n')
	for d in final.keys():
		writer.writerow(final[d])
		c+=1
		print("\r\t",c,end='')
print("\n")
