import csv
import logging
from schema_transformer.transformer import CSVTransformer

from main import Institution

logger = logging.getLogger(__name__)
logging.basicConfig()

IPEDS_FILE = 'hd2013.csv'

class IpedsTransformer(CSVTransformer):
	def _transform_string(self, val, doc):
		val = (val)
		return super(IpedsTransformer, self)._transform_string(val, doc)
	def load(self, doc):
		return doc

schema = {
	'name': 'INSTNM',
	'location': {
		'street_address': 'ADDR',
		'city': 'CITY',
		'state': 'STABBR',
		'ext_code': 'ZIP'
	},
	'web_url': 'WEBADDR',
	'_id': ('UNITID', lambda x: int(x)),
	'public': ('CONTROL', lambda x: int(x) ==  2),
	'for_profit': ('CONTROL', lambda x: int(x) == 3),
	'degree': ('UGOFFER', lambda x: int(x) == 1)
}

f = open(IPEDS_FILE)
reader = csv.reader(f)

transformer = IpedsTransformer(schema, next(reader))

while reader:
	transformed = transformer.transform(next(reader))
	logger.info('Adding {0}.'.format(transformed['name']))
	try:
		inst = Institution(country='United States', **transformed)
		inst.save()
	except:
		pass
