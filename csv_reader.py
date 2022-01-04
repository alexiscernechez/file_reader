#!/usr/bin/env python3

import csv
from url_opener import open_url, url_builder
from scraper import *

import datetime

# class Reader(object):
# 	"""docstring for Reader"""
# 	def __init__(self, arg):
# 		super(Reader, self).__init__()
# 		self.arg = arg
		
class FileHandler:
	now = datetime.datetime.now()
	"""docstring for FileHandler"""

	def create_dict(file_location):
		compiled_list = csv.reader(open(file_location, 'r',errors='ignore'))

		dict_list = {}
		key = 0
		
		for v in compiled_list:
		   dict_list[key] = v
		   key += 1

		return dict_list

	def create_action_list(generator, audit_type):
		file_name = ''

		if audit_type == 1:
			file_name = 'active_users_no_contract'
		elif audit_type == 2:
			file_name = 'end_dates'
		elif audit_type == 3:
			file_name = 'ICs_in_L3_locations'
		elif audit_type == 4:
			file_name = 'multiple_contracts'
		elif audit_type == 5:
			file_name = 'fls_with_assets'
		elif audit_type == 6:
			file_name = 'current_whitelist'
		elif audit_type == 7:
			file_name = 'updated_whitelist'
		elif audit_type == 8:
			file_name = 'survey'
		elif audit_type == 9:
			file_name = 'affected'
		elif audit_type == 'adhoc':
			file_name = input("Please enter an output file name: ").strip()

		output_path = '/Users/jeffstock/Desktop/Output Files/' + file_name + '.csv'

		with open(output_path, 'w') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerows(generator)

	def __init__(self, arg):
		super(FileHandler, self).__init__()
		self.arg = arg

class Getters:
	"""docstring for Getters"""

	def get_users_with_mac_assets(rem, fl):

		rem_dict = FileHandler.create_dict(rem)
		fl_dict = FileHandler.create_dict(fl)

		combined_pc = DictHandler.dict_combiner(rem_dict, fl_dict)

		a = {}
		b = 0

		all_data = {}
		user_detail_counter = 0

		for user in combined_pc:

			user_details = {}

			ind_user_detail = combined_pc.get(user)

			user_details['User Details'] = ind_user_detail

			user_detail_counter += 1

			all_data[user_detail_counter] = user_details
		
		headers = all_data[1]['User Details']

		for data in all_data:
			pair = {}
			i = 0
			tester = all_data[data]['User Details']

			while i < len(headers):
				k = headers[i]
				v = tester[i]
				i += 1
				pair[k] = v
			b += 1
			a[b] = pair

		return a

	def get_users_with_pc_assets(rem, fl):
		output = []
		combined_list = []
		long_desc = []
		rough_list = []

		rem_dict = FileHandler.create_dict(rem)
		fl_dict = FileHandler.create_dict(fl)

		for i in rem_dict:
			test = rem_dict[i][len(rem_dict[i])-1]
			combined_list.append(test)

		for a in fl_dict:
			test = fl_dict[a][len(fl_dict[a])-1]
			combined_list.append(test)

		for b in combined_list:
			parts_1 = b.split(',')
			parts_2 = b.split('-')
			if len(parts_1) > 1:
				long_desc.append(parts_1)
			elif len(parts_2) > 2:
				long_desc.append(parts_2)
			else:
				rough_list.append(b)

		for c in long_desc:
			name = c[0].strip()
			rough_list.append(name)

		for d in rough_list:
			if d != '-' and d != 'Description':
				output.append(d)

		return output

	def get_active_users(file_location):
	
		user_list = FileHandler.create_dict(file_location)

		a = {}
		b = 0

		all_data = {}
		user_detail_counter = 0


		for user in user_list:

			user_details = {}

			ind_user_detail = user_list.get(user)[0]
			detail_list = ind_user_detail.split(';')

			user_details['User Details'] = detail_list

			user_detail_counter += 1

			all_data[user_detail_counter] = user_details
		
		# the length of the headers list is always 24
		headers = all_data[1]['User Details']

		

		for data in all_data:
			pair = {}
			i = 1
			tester = all_data[data]['User Details']

			while i < len(headers):
				k = headers[i-1]
				if i < len(tester):
					v = tester[i-1]
				else:
					v = ''
				i += 1
				pair[k] = v
			b += 1
			a[b] = pair


		return a

	def get_contracts(file_location):

		# complete_list = {}
		# complete_list_counter = 0

		contract_list = FileHandler.create_dict(file_location)

		headers = contract_list[0]

		a = {}
		b = 0
		

		for data in contract_list:
			pair = {}
			i = 1
			tester = contract_list[data]

			while i < len(tester):
				k = headers[i-1]
				v = tester[i-1]
				i += 1
				pair[k] = v
			b += 1
			a[b] = pair


		return a

	def get_raw_whitelist(file_location):
		info_list = FileHandler.create_dict(file_location)

		headers = info_list[0]

		a = {}
		b = 0
		

		for data in info_list:
			pair = {}
			i = 0
			tester = {}
			if data != 0:
				tester = info_list[data]
			
			if len(tester) > 0:
				while i < len(tester):
					k = headers[i]
					v = tester[i]
					i += 1
					pair[k] = v
				b += 1
				a[b] = pair


		return a

	def __init__(self, arg):
		super(Getters, self).__init__()
		self.arg = arg

class Finders:
	"""docstring for Finders"""
	def find_users_without_contracts(active_contracts, auwa):

		uids_contracts = []
		uids_users = []

		names_contracts = []
		names_users = []

		for c in active_contracts:
			uids_contracts.append(active_contracts[c]['Freelancer User ID'])
			names_contracts.append(active_contracts[c]['Freelancer Name'])

		for u in auwa:
			uid = auwa[u]['platformId']
			if uid != 'None':
				uids_users.append(uid)
				names_users.append(auwa[u]['Name'])

			

		filtered_by_uid = ListHandler.find_missing_from_list(uids_contracts,uids_users)
		filtered_by_name = ListHandler.find_missing_from_list(names_contracts,names_users)

		details = {}
		details_counter = 0

		for u in filtered_by_uid:
			for au in auwa:
				uid = auwa[au]['platformId']
				if u == uid:
					details_counter += 1
					details[details_counter] = auwa[au]
		
		filtered_by_name_and_cid = {}
		filtered_by_name_and_cid_counter = 0

		for u in filtered_by_name:
			for au in details:
				u_name = details[au]['Name']
				if u == u_name:
					filtered_by_name_and_cid_counter += 1
					filtered_by_name_and_cid[filtered_by_name_and_cid_counter] = details[au]

		output = [['platformId','Name','Email']]

		for i in filtered_by_name_and_cid:
			action_item = []
			action_item.append(filtered_by_name_and_cid[i]['platformId'])
			action_item.append(filtered_by_name_and_cid[i]['Name'])
			action_item.append(filtered_by_name_and_cid[i]['Email'])
			output.append(action_item)

		return output

	def find_end_dates(active_contracts):
		action_items = {}
		action_items_counter = 0
		now = datetime.datetime.now()

		date = now.strftime('%Y/%m/%d')

		for c in active_contracts:
			expired = {}
			expires_today = {}
			next_14 = {}

			if active_contracts[c]['End Date'] == 'End Date' or active_contracts[c]['End Date'] == '':
				end_year = 0
				end_month = 0
				end_day = 0
			else:
				end_year_raw = active_contracts[c]['End Date'][0:4]
				end_year = int(end_year_raw)
				end_month_raw = active_contracts[c]['End Date'][5:7]
				end_month = int(end_month_raw)
				end_day_raw = active_contracts[c]['End Date'][8:10]
				end_day = int(end_day_raw)

			# Expired contracts
			if end_year == now.year -1 or end_year == now.year -2 or end_year == now.year and end_month == now.month and end_day < now.day or end_year == now.year and end_month < now.month:
				
				expired = DictHandler.create_end_date_dict(active_contracts[c])

				action_items[c] = expired
			# Contracts ending today
			elif end_year == now.year and end_month == now.month and end_day == now.day:
				
				expires_today = DictHandler.create_end_date_dict(active_contracts[c])

				action_items[c] = expires_today

			# CONTRACTS ENDING THIS AND NEXT MONTH (needed to capture contract ends further out in advance of annual shutdown):

			if now.month == 11 or now.month == 12:
				if end_year == now.year + 1 and end_month == 1:

					expires_this_month = DictHandler.create_end_date_dict(active_contracts[c])

					action_items[c] = expires_this_month



		# THE FOLLOWING LOGIC IS FOR FINDING CONTRACTS ENDING IN THE NEXT TWO WEEKS



			# Contracts expiring this month within the next 14 days
			elif end_year == now.year and end_month == now.month and end_day > now.day and end_day <= (now.day + 14):
				action_items_counter += 1
				next_14 = DictHandler.create_end_date_dict(active_contracts[c])

				action_items[c] = next_14

			# Contracts expiring next month when end dates are within 14 days of today
			if now.day > 17:

				#December
				if now.month == 12:
					if end_year == now.year + 1 and end_month == 1 and end_day < (now.day + 14 - 31):

						next_14 = DictHandler.create_end_date_dict(active_contracts[c])

						action_items[c] = next_14

				#February
				elif now.month == 2:
					if now.year == 2020 or now.year == 2024:
						if end_year == now.year and end_month == (now.month +1) and end_day < (now.day + 14 - 29):
						
							next_14 = DictHandler.create_end_date_dict(active_contracts[c])
					else:
						if end_year == now.year and end_month == (now.month +1) and end_day < (now.day + 14 - 28):

							next_14 = DictHandler.create_end_date_dict(active_contracts[c])

						action_items[c] = next_14

			# 	# Months with 30 days (April, June, September, November)
			# 	# TODO
			# 	# USE THIS FOR TESTING
			# 	elif now.month == 4 or now.month == 6 or now.month == 9 or now.month == 11:
			# 		if end_year == now.year and end_month == (now.month +1) and end_day < (now.day + 14 - 30):

			# 			next_14 = DictHandler.create_end_date_dict(active_contracts[c])

			# 			action_items[c] = next_14

			# 	# TEST ABOVE

				# Contracts expiring this month within the next 14 days
				elif end_year == now.year and end_month == now.month and end_day > now.day and end_day <= (now.day + 14):
					action_items_counter += 1

					next_14 = DictHandler.create_end_date_dict(active_contracts[c])

					action_items[c] = next_14

				# Contracts expiring next month within 14 days for months with 31 days and end_day == (now.day + 14 - 31)
				if end_year == now.year and end_month == (now.month + 1) and end_day <= now.day + 14 - 31:

					next_14 = DictHandler.create_end_date_dict(active_contracts[c])

					action_items[c] = next_14

			elif now.day > 16:
				if now.month == 2:
					if now.year == 2020 or now.year == 2024:
						if end_year == now.year and end_month == (now.month +1) and end_day < (now.day + 14 - 29):
							
							next_14 = DictHandler.create_end_date_dict(active_contracts[c])
					else:
						if end_year == now.year and end_month == (now.month +1) and end_day < (now.day + 14 - 28):

							next_14 = DictHandler.create_end_date_dict(active_contracts[c])

						action_items[c] = next_14

				# Months with 30 days (April, June, September; except November, which is captured above for annual shutdown)

				elif now.month == 4 or now.month == 6 or now.month == 9:
					if end_year == now.year and end_month == (now.month +1) and end_day <= (now.day + 14 - 30):

						next_14 = DictHandler.create_end_date_dict(active_contracts[c])

						action_items[c] = next_14
				
				elif end_year == now.year and end_month == now.month and end_day > now.day and end_day <= (now.day + 14):

					next_14 = DictHandler.create_end_date_dict(active_contracts[c])

					action_items[c] = next_14



		output = [['Contract ID','User ID','Freelancer Name','Contact Person','Team Name','Start Date','End Date','Payment Structure','Expedited']]

		for i in action_items:
			action_item = []
			action_item.append(action_items[i]['Contract ID'])
			action_item.append(action_items[i]['User ID'])
			action_item.append(action_items[i]['Freelancer Name'])
			action_item.append(action_items[i]['Contact Person'])
			action_item.append(action_items[i]['Team Name'])
			action_item.append(action_items[i]['Start Date'])
			action_item.append(action_items[i]['End Date'])
			action_item.append(action_items[i]['Contract Type'])
			action_item.append(action_items[i]['Expedited'])
			output.append(action_item)

		return output

	def find_hourly_contracts_l3_countries(active_contracts, l3_countries_list, whitelist):
		action_items = {}
		action_items_counter = 0

		for c in active_contracts:
			freelancer_name = active_contracts[c]['Freelancer Name']
			access = active_contracts[c]['Systems Access']
			contract_id = active_contracts[c]['Contract ID']
			if contract_id not in whitelist and freelancer_name != 'Upwork Managed Services' and freelancer_name != 'Professionals Agency P' and access != 'Domestic Staffing Vendor Employee':
				location = active_contracts[c]['Freelancer location'].split(',')
				country = location[0]
				if country in l3_countries_list:
					action_items_counter += 1
					action_items[action_items_counter] = active_contracts[c]
 

		output = [['Contract ID','Freelancer Name','Location','Agency','Weekly Limit','Contact Person','Contract End Date','Notes']]

		for i in action_items:
			action_item = []
			
			action_item.append(action_items[i]['Contract ID'])
			action_item.append(action_items[i]['Freelancer Name'])
			action_item.append(action_items[i]['Freelancer location'])
			action_item.append(action_items[i]['Agency Name'])
			action_item.append(action_items[i]['Weekly Limit'])
			action_item.append(action_items[i]['Contact person'])
			action_item.append(action_items[i]['End Date'][0:10])
			
			# if contract_id in whitelist:
			# 	action_item.append('Yes')
			# else:
			# 	action_item.append('No')
			output.append(action_item)

		return output

	def find_fl_with_mac_assets(email_list, access_dict):
		output = {}
		counter = 0

		for i in access_dict:
			single = {}
			full_name = access_dict[i]['full_name']
			email = access_dict[i]['upwork_email']
			uid = access_dict[i]['worker_user_id']

			for k in email_list:
				if email in k:
					counter += 1
					single['Full Name'] = full_name
					single['User ID'] = uid
					single['Email Address'] = email

					output[counter] = single
		
		return output

	def find_fl_with_pc_assets(names_list, access_dict):
		output = {}
		counter = 0

		for i in access_dict:
			single = {}
			full_name = access_dict[i]['full_name']
			email = access_dict[i]['upwork_email']
			uid = access_dict[i]['worker_user_id']

			for a in names_list:
				if full_name == a:
					counter += 1
					single['Full Name'] = full_name
					single['User ID'] = uid
					single['Email Address'] = email

					output[counter] = single

		return output

	def find_location_and_agency(user_dict, contract_dict):
		output = [['Full Name','User ID','Email Address','Agency Name','Location']]

		for c in contract_dict:
			single = []
			for u in user_dict:
				if user_dict[u]['User ID'] == contract_dict[c]['Freelancer User ID']:
					single.append(user_dict[u]['Full Name'])
					single.append(user_dict[u]['User ID'])
					single.append(user_dict[u]['Email Address'])
					single.append(contract_dict[c]['Agency Name'])
					single.append(contract_dict[c]['Freelancer location'])

					output.append(single)

		return output

	def find_multiple_contracts(active_contracts):

		output = [['Contract ID','User ID','Freelancer Name','Contact Person','Team Name','End Date']]
		uids_all = []
		repeats = []
		for i in active_contracts:
			uid = active_contracts[i]['Freelancer User ID']
			if uid != 'odesk_managed':
				uids_all.append(uid)

		for c in active_contracts:
			uid = active_contracts[c]['Freelancer User ID']
			x = uids_all.count(uid)
			if x > 1 and uid not in repeats:
				repeats.append(uid)

		for a in active_contracts:
			action_item = []
			uid = active_contracts[a]['Freelancer User ID']
			if uid in repeats:
				action_item.append(active_contracts[a]['Contract ID'])
				action_item.append(active_contracts[a]['Freelancer User ID'])
				action_item.append(active_contracts[a]['Freelancer Name'])
				action_item.append(active_contracts[a]['Contact person'])
				action_item.append(active_contracts[a]['Team Name'])
				action_item.append(active_contracts[a]['End Date'][0:10])
				output.append(action_item)

		return output

	def find_location(contract_dict):

		users = {}
		counter = 0

		for c in contract_dict:
			ind_user_detail = {}
			loc = contract_dict[c]['Freelancer location'].split(',')
			ind_user_detail['uid'] = contract_dict[c]['Freelancer User ID']
			ind_user_detail['contact person'] = contract_dict[c]['Contact person']
			ind_user_detail['team'] = contract_dict[c]['Team Name']
			ind_user_detail['country'] = loc[0]
			if len(loc) == 2 and loc[1] != ' ':
				ind_user_detail['city'] = loc[1]
			elif len(loc) == 3:
				ind_user_detail['city'] = loc[2]
				ind_user_detail['state'] = loc[1]
			if len(ind_user_detail) > 0:
				counter += 1
				users[counter] = ind_user_detail


		return users


	def find_disaster_affected(contract_dict, users_dict, disaster_dict, countries_list, cities_list):

		affected = [['User ID', 'Freelancer Name', 'Contact Person', 'Location', 'Disaster Type', 'Severity','Team']]
				
		for u in users_dict:
			uid = users_dict[u]['uid']
			if 'city' in users_dict[u]:
				fl_city = users_dict[u]['city'].lower().strip()
				fl_country = users_dict[u]['country'].lower().strip()
				if users_dict[u]['country'] in countries_list:
					for d in disaster_dict:
						dis_city = disaster_dict[d][0].lower().strip()
						dis_country = disaster_dict[d][1].lower().strip()

						if dis_city == fl_city and dis_country == fl_country:
							ind_affected = []
							for c in contract_dict:
								if contract_dict[c]['Freelancer User ID'] == uid:
									fl_name = contract_dict[c]['Freelancer Name']
									contact_person = contract_dict[c]['Contact person']
									location = contract_dict[c]['Freelancer location']
									team = contract_dict[c]['Team Name']
									dis_type = disaster_dict[d][2]
									severity = disaster_dict[d][3]

									ind_affected.append(uid)
									ind_affected.append(fl_name)
									ind_affected.append(contact_person)
									ind_affected.append(location)
									ind_affected.append(dis_type)
									ind_affected.append(severity)
									ind_affected.append(team)
							if len(ind_affected) > 0:
								affected.append(ind_affected)


		return ListHandler.remove_duplicates_from_nested_list(affected)


	def __init__(self, arg):
		super(Finders, self).__init__()
		self.arg = arg
				
class ListHandler:
	"""docstring for ListHandler"""

	def list_combiner(base, additional):

		for i in additional:
			if i not in base:
				base.append(i)

		return base

	def gtnp_filter(complete_list):

		filtered_contracts = {}
		filter_counter = 0
		
		for c in complete_list:
			if 'Team Name' in complete_list[c]:
				parts = complete_list[c]['Team Name'].split('::')

				if len(parts) > 1:
					subteam = parts[1]
					if len(subteam) > 3:
						if subteam[0:4] != 'GTNP' and subteam != 'NLP Pygmalion Contributor':
							filter_counter += 1
							filtered_contracts[filter_counter] = complete_list[c]

		return filtered_contracts

	def fte_filter_mac_assets(user_list):
		email_address_list = []

		fl_with_assets = {}
		counter = 0

		for u in user_list:
			domain = user_list[u]['Username'].split('@')
			email = user_list[u]['Username']
			if len(domain) > 1 and domain[1] == 'cloud.upwork.com':
				counter += 1
				fl_with_assets[counter] = email

		output = []

		for i in fl_with_assets:
			single = []

			single.append(fl_with_assets[i])

			output.append(single)

		return output

	def fte_filter_user_list(complete_list):
		filtered_users = {}
		filtered_counter = 0

		if len(complete_list) > 0:
			for u in complete_list:
				parts = complete_list[u]['Email'].split('@')
				if len(parts) > 1:
					domain = parts[1]
					if domain != 'upwork.com':
						filtered_counter += 1
						filtered_users[filtered_counter] = complete_list[u]
		else:
			filtered_users[filtered_counter] = 'Empty'

		return filtered_users

	def payroll_filter(complete_list):
		filtered_contracts = {}
		filter_counter = 0
		
		for c in complete_list:
			agency = complete_list[c]['Agency Name']
			if agency != 'Upwork Payroll - iWorkGlobal' and agency != 'EOR-IWG-INTL':
				filter_counter += 1
				filtered_contracts[filter_counter] = complete_list[c]

		return filtered_contracts

	def fixed_price_filter(complete_list):
		filtered_contracts = {}
		filter_counter = 0
		
		for c in complete_list:
			structure = complete_list[c]['Contract type']
			if structure == 'Hourly':
				filter_counter += 1
				filtered_contracts[filter_counter] = complete_list[c]

		return filtered_contracts	

	def remove_duplicates_from_nested_list(nested_list):
		output = []
		tester = []

		for i in nested_list:
			name = i[0]
			if name not in tester:
				tester.append(name)
				output.append(i)

		return output

	def find_missing_from_list(list_1, list_2):
		missing_from_list = []
		
		for i in list_2:
			if i not in list_1:
				missing_from_list.append(i)

		return missing_from_list

	def find_common_between_lists(list_1,list_2):
		common_items = []

		for i in list_1:
			if i in list_2:
				common_items.append(i)

		return common_items

	def filter_whitelist(whitelist, list_type):
		filtered_list = []

		for i in whitelist:
			if whitelist[i]['Type'] == list_type:
				filtered_list.append(whitelist[i]['Name'])

		return filtered_list

	def filter_contracts_by(contract_dict, k_param, v_param):
		filtered_cid_list = []

		for i in contract_dict:
			cid = contract_dict[i]['Contract ID']
			s_key = contract_dict[i][k_param]
			if s_key == v_param:
				filtered_cid_list.append(cid)

		return filtered_cid_list

	def dict_creator(formatted_list):
		# INPUT: List of Lists; OUTPUT: Dictionary where key = column header, value = values
		headers = formatted_list[0]

		a = {}
		b = 0

		for x in formatted_list:
			pair = {}
			i = 0
			while i < len(headers):
				k = headers[i]
				v = x[i]
				i += 1
				pair[k] = v
			b += 1
			a[b] = pair

		return a

	
	def __init__(self, arg):
		super(ListHandler, self).__init__()
		self.arg = arg

class DictHandler:
	"""docstring for DictHandler"""
	
	def dict_combiner(base, additional):

		key = len(base) + 1

		for i in additional:
			base[key] = additional[i]
			key += 1

		return base

	def create_end_date_dict(base_item):
		output = {}

		whitelist = ListHandler.filter_whitelist(Getters.get_raw_whitelist('./static/whitelist.csv'), 'L3_country')

		country = base_item['Freelancer location'].split(',')[0]

		output['Contract ID'] = base_item['Contract ID']
		output['Freelancer Name'] = base_item['Freelancer Name']
		output['Start Date'] = base_item['Start Date'][0:10]
		output['End Date'] = base_item['End Date'][0:10]
		output['Contract Status'] = base_item['Status']
		output['User ID'] = base_item['Freelancer User ID']
		output['Team Name'] = base_item['Team Name']
		output['Contact Person'] = base_item['Contact person']
		output['Contract Type'] = base_item['Contract type']
		
		if country in whitelist:
			output['Expedited'] = 'No'
		else:
			output['Expedited'] = 'Yes'


		return output

	def create_affected_country_list(disaster_details_dict):
		# disaster_details_dict structure:
		# {1:['City', 'Country', 'Type', 'Severity']}

	  affected_countries_list = []
	  
	  for e in disaster_details_dict:
	  	country = disaster_details_dict[e][1]
	  	if country not in affected_countries_list:
	  		affected_countries_list.append(country)

	  return affected_countries_list

	def create_affected_cities_list(disaster_details_dict):
		affected_cities_list = []
		for e in disaster_details_dict:
			city = disaster_details_dict[e][0]
			if city not in affected_cities_list:
				affected_cities_list.append(city) 

		return affected_cities_list

	def __init__(self, arg):
		super(DictHandler, self).__init__()
		self.arg = arg

class WhitelistUpdater:
	"""docstring for WhitelistUpdater"""
	def current_whitelist(details, contracts):

		current = [['Contract ID','Offer ID','Company Name','Team Name','Freelancer User ID','Freelancer Name','Freelancer location','Agency Name','Title','Start Date','End Date','Status','Hourly Rate','Fixed Price Amount Agreed','Upfront Payment (%)','Weekly Salary','Weekly Limit','Contact person','Contract type','Milestone Status','Escrow Refund Status','Cost Center','Division','Systems Access','Geographic Zone','Level','Job Category','Imperative Team','isBYO']]
		

		for i in details:
			cid = details[i]['Contract ID']
			if cid in contracts:
				single = []
				for c in details[i]:
					single.append(details[i][c])
				current.append(single)

		return current

	def update(ended, contracts, whitelist):
		updated = [['Type','Name']]

		closed = []

		active = []
		for a in ended:
			cid = ended[a]['Contract ID']
			if cid in contracts:
				
				closed.append(cid)


		for b in whitelist:
			designation = whitelist[b]['Type']
			if designation == 'Contract':
				single = []
				cid = whitelist[b]['Name']
				if cid not in closed:
					single.append(designation)
					single.append(cid)
					updated.append(single)
			else:
				single = []
				for c in whitelist[b]:
					single.append(whitelist[b][c])
				updated.append(single)

		return updated


	def __init__(self, arg):
		super(WhitelistUpdater, self).__init__()
		self.arg = arg

class Adhoc:
	"""docstring for Adhoc"""

	c = ListHandler.gtnp_filter(Getters.get_contracts('./static/contracts.csv'))
	e = Getters.get_contracts('./static/ended_contracts.csv')
	# u = ListHandler.fte_filter_user_list(Getters.get_active_users('./static/user_data.csv'))

	def file_explorer():
		file_location = './static/' + input('Enter a file name: ') + '.csv'
		f = Getters.get_contracts(file_location)

		what = int(input('\nSELECTIONS:\n1. Column Headers\n2. Search by header\n\nPlease enter the number of your selection:\n'))

		just_the_tip = input('Exclude non-TIP information?')

		if just_the_tip == 'yes':
			no_gtnp = ListHandler.gtnp_filter(f)
			f = no_gtnp

		more = 'no'

		if what == 1:
			keys = f[1].keys()
			for k in keys:
				print(k)
		elif what == 2:
			Adhoc.param_filter(f)

		more = input('Would you like to explore further? ')

		if more == 'yes':
			Adhoc.file_explorer()
		elif more == 'no':
			print('\n Good Bye!\n')
			quit()

	def count_by_team():
		file_location = './static/' + input('Enter a file name: ') + '.csv'
		f = Getters.get_contracts(file_location)
		team_count = {}
		unique_teams = []
		for i in f:
			team = f[i]['Team Name']
			if team != 'Team Name' and team not in unique_teams:
				unique_teams.append(team)

		for a in unique_teams:
			count = 0
			for b in f:
				if f[b]['Team Name'] == a:
					count += 1
			team_count[a] = count

		for c in team_count:
			print(c, ' ;',team_count[c])

		return team_count



	def view_check(func_name):
		view = input('Do you want to view the results of ' + func_name +'?' )

		return view

	def returner(result):

		output_choice = input('Would you like to print or make a csv?').strip().lower()
		if output_choice == 'print':
			print(result)
		elif output_choice == 'make a csv':
			FileHandler.create_action_list(result,'adhoc')
		else:
			print('INVALID CHOICE!')

	def param_filter(contract_dict):
		func_name = 'param_filter'
		search_by = input('What would you like to search by? ').strip()

		search_for = ''
		loc_filter = 0

		if search_by == 'Location':
			loc_filter = int(input('Select a filter by number:\n1. Country\n2.State\n3. City\n'))
			if loc_filter == 1:
				search_for = input('Enter country name: ').strip()
			elif loc_filter == 2:
				search_for = input('Enter a state abbrevieation: ').strip()
		else:
			search_for = input('What would you like to search for? ').strip()
		
		output = [['Contract ID','Offer ID','Company Name','Team Name','Freelancer User ID','Freelancer Name','Freelancer location','Agency Name','Title','Start Date','End Date','Status','Hourly Rate','Fixed Price Amount Agreed','Upfront Payment (%)','Weekly Salary','Weekly Limit','Contact person','Contract type','Milestone Status','Escrow Refund Status','Cost Center','Division','Systems Access','Geographic Zone','Level','Job Category','Imperative Team','isBYO']]

		for c in contract_dict:
			i = contract_dict[c]
			if contract_dict[c]['Freelancer Name'] != 'Upwork Managed Services':
				t = ''
				if search_by == 'Location':
					loc = i['Freelancer location'].split(',')
					if loc_filter == 1:
						t = loc[0].strip()
					elif loc_filter == 2:
						if len(loc) > 1:
							t = loc[1].strip()
					elif loc_filter == 3:
						if len(loc) > 1:
							t = loc[2].strip()
				else:
					t = i[search_by]

				if search_for == '*' or search_for == 'all':
					if t != '':
						single_b = []
						for b in i:
							if i[b][t] not in single_b:
								single_b.append(i[b])
						output.append(single_b)
				elif t == search_for:
					single_a = []
					for a in i:
						single_a.append(i[a])
					output.append(single_a)

		view = Adhoc.view_check(func_name)
		if view == 'yes':
			Adhoc.returner(output)
		elif view == 'no':
			return output

	def contract_starts_or_ends_by_year(contract_dict):

		func_name = 'contract_starts_or_ends_by_year'
		year_filter = input('Please enter a four-digit year: ').strip()
		parameter = input('Starts or ends?').strip().lower()
		output = [['Contract ID','Offer ID','Company Name','Team Name','Freelancer User ID','Freelancer Name','Freelancer location','Agency Name','Title','Start Date','End Date','Status','Hourly Rate','Fixed Price Amount Agreed','Upfront Payment (%)','Weekly Salary','Weekly Limit','Contact person','Contract type','Milestone Status','Escrow Refund Status','Cost Center','Division','Systems Access','Geographic Zone','Level','Job Category','Imperative Team','isBYO']]

		filter_results = []

		out = []

		older = []

		for c in contract_dict:
			i = contract_dict[c]
			if parameter == 'starts':
				param_date = i['Start Date'].split('-')[0]
			elif parameter == 'ends':
				param_date = i['End Date'].split('-')[0]
			# TODO: account for other inputs, return some message.

			if param_date == year_filter:
				filter_results.append(i['Freelancer User ID'])
			elif param_date < year_filter:
				older.append(i['Freelancer User ID'])

		# p_users = Adhoc.create_filter_list(Adhoc.e,'Freelancer User ID')

		current_older = []

		for x in filter_results:
			if x in older:
				current_older.append(x)

		for a in filter_results:
			if a not in  older:
				out.append(a)

		for b in contract_dict:
			i = contract_dict[b]
			u = i['Freelancer User ID']
			if u in out:
				single = []
				for a in i:
					single.append(i[a])
				output.append(single)

		view = Adhoc.view_check(func_name)
		if view == 'yes':
			Adhoc.returner(output)
		elif view == 'no':
			return output

	def create_filter_list(dictionary, parameter):
		output = []

		for i in dictionary:
			searched = dictionary[i][parameter]
			if searched not in output:
				output.append(searched)

		return output

	def find_team_from_fl_name(name_list):

		output = [['Timestamp','Nominee Name','Nominee Start Date','Nomination Details','Nominated by Email','Team']]

		names = FileHandler.create_dict(name_list)

		for a in Adhoc.c:
			c_name = Adhoc.c[a]['Freelancer Name']
			for b in names:
				nom_name = names[b][1]
				if c_name == nom_name:
					names[b].append(Adhoc.c[a]['Team Name'].split('::')[0])
					output.append(names[b])

		FileHandler.create_action_list(output,'adhoc')

		return output

	#TODO: MAKE A UNIFIED FUNCTION FOR THIS:

	def contracts_by_year_and_param(contract_dict):

		Adhoc.param_filter(ListHandler.dict_creator(Adhoc.contract_starts_or_ends_by_year(ListHandler.payroll_filter(contract_dict))))

	# This will allow users to make a list of all contracts that either started or ended in a particular year filtered by user-selected parameter (currently only team name and location)

	def __init__(self, arg):
		super(Adhoc, self).__init__()
		self.arg = arg

class SurveyPreper:
	"""docstring for SurveyPreper"""
	def prepare(current_dict, access_dict, cc_list):
		
		prepared_list = [['Freelancer Name','Freelancer UID','Freelancer Email','Cost Center','Division','Section','Team','Contact Person Name']]

		cids_without_access = ListHandler.filter_contracts_by(current_dict,'Systems Access','Possible IC - No Access')

		unique_users = []

		for a in current_dict:
			c = current_dict[a]
			cid = c['Contract ID']
			if cid not in cids_without_access:
				single = []
				flname = c['Freelancer Name']
				uid = c['Freelancer User ID']
				if uid not in unique_users:
					unique_users.append(uid)
					email = 'BLANK'
					cc = 'TODO'

					team_name = c['Team Name'].split('::')
					division = team_name[0]
					section = team_name[1]
					if len(team_name) == 3:
						team = team_name[2]
					else:
						team = 'N/A'
					c_person = c['Contact person']

					single.append(flname)
					single.append(uid)
					single.append(email)
					single.append(cc)
					single.append(division)
					single.append(section)
					single.append(team)
					single.append(c_person)

					for u in access_dict:
						if single[1] == access_dict[u]['worker_user_id'] or single[0] == access_dict[u]['full_name']:
							single[2] = access_dict[u]['upwork_email']

					for d in cc_list:
						if c['Team Name'] == cc_list[d]['Team Name']:
							single[3] = cc_list[d]['Cost Center'][0:3]

					prepared_list.append(single)


		return prepared_list

	def __init__(self, arg):
		super(SurveyPreper, self).__init__()
		self.arg = arg

		
		
