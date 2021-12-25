import requests


BASE_URL = "https://api.hh.ru"
vac_url = f'{BASE_URL}/vacancies/49310240'

r = requests.get(vac_url)

a = r.json()

id_id = a['id']
company_name = a['employer']
title = a['name']
city = a['area']
salary = a['salary']
work_experience = a['experience']
employment_type = a['employment']

# 'name',
# 'area',
# 'salary',
# 'experience',

# 'employment',
# 'description',
# 'alternate_url')

print(id_id,
title,
company_name['name'],
city['name'],
salary['from'],
salary['to'],
work_experience['name'],
employment_type['name'],

sep='\n')
