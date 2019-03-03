
# LOGIN
'/login/'
'/login/register/'
'/login/reset-pass/'
'/login/fb-login/'

# WELCOME
##############################################			'/user/welcome/'
##############################################			'/user/welcome/set-farm/'
##############################################			'/user/welcome/set-sys/'
##### SET FARM ########
# /name/location/area/process
# /name/state/start-date/crop/area/type/summary/confirm/welcome/
##### SET SYS ########
# /turn-on/qr-code/install/pump/confirm/welcome/

# USER 
'/user'
	# SETTINGS
	'/user/settings/'
	'/user/settings/payment/'
	'/user/settings/payment/edit/'
	'/user/settings/profile/'
	'/user/settings/profile/edit/'
	'/user/settings/profile/edit-pass/'
	'/user/settings/confirm-email/'
	'/user/settings/confirm-phone/'
	# USER MENU
	'/user/menu/' 						# this always there at first as nav item
	'/user/menu/welcome/' 				# initial set up (farm and agrimodule)
	'/user/menu/farm-status/'
	'/user/menu/crop-status/'
	'/user/menu/farmer-plan/'
	'/user/menu/new-farm/'
	'/user/menu/new-field/'
	'/user/menu/crop-analyzer/'
	'/user/menu/health-analyzer/'
	'/user/menu/market/'
	'/user/menu/settings/'
	'/user/menu/logout/'

	# MARKET
	'/user/market/'
	'/user/market/cart/'
	'/user/market/cart/edit/'
	'/user/market/checkout/'
	'/user/market/search/'
	'/user/market/search/product/'
	'/user/market/search/product/add-t-cart/'
	'/user/market/search/product/rem-f-cart/'
	
	# FARM
##############################################				'/user/farm/'

		# WEATHER
		'/user/farm/weather/'
		'/user/farm/weather/history/'
		'/user/farm/weather/predictions/'
		'/user/farm/weather/forecast/'
		'/user/farm/weather/daily/'
		'/user/farm/weather/weekly/'
		'/user/farm/weather/monthly/'

		# ALERTS
		'/user/farm/alerts/'
		'/user/farm/alerts/farmer/'
		'/user/farm/alerts/manager/'
		'/user/farm/alerts/crop/'
		'/user/farm/alerts/field/'
		'/user/farm/alerts/farm/'
		'/user/farm/alerts/market/'
		'/user/farm/alerts/agrimodule/'
		'/user/farm/alerts/agripump/'
		'/user/farm/alerts/agrisensor/'

		# FIELDS
##############################################					'/user/farm/field/'
			# AGRIMODULE
##############################################						'/user/farm/field/agrimodule/'
			'/user/farm/field/agrimodule/settings/'
			'/user/farm/field/agrimodule/add-sensor'
			'/user/farm/field/agrimodule/edit/<agrimodule_id>'
			'/user/farm/field/agrimodule/delete/<agrimodule_id>'
			'/user/farm/field/agrimodule/notifications/'
			'/user/farm/field/agrimodule/weather/'
			'/user/farm/field/agrimodule/weather/radiation/'
			'/user/farm/field/agrimodule/weather/temp/'
			'/user/farm/field/agrimodule/weather/humidity/'
			'/user/farm/field/agrimodule/weather/presure/'
			'/user/farm/field/agrimodule/soil/'
			'/user/farm/field/agrimodule/soil/ph/'
			'/user/farm/field/agrimodule/soil/temp/'
			'/user/farm/field/agrimodule/soil/moist/'
			'/user/farm/field/agrimodule/soil/nutrients/'
			# AGRIPUMP
##############################################						'/user/farm/field/agripump/'
			'/user/farm/field/agripump/settings/'
			'/user/farm/field/agripump/notifications/'
			'/user/farm/field/agripump/on/'
			'/user/farm/field/agripump/off/'
			'/user/farm/field/agripump/flow/' # refers to a graph
			'/user/farm/field/agripump/delete/<agripump_id>'
			'/user/farm/field/agripump/change-pump/'
			'/user/farm/field/agripump/schedule/'
			# CROP
##############################################						'/user/farm/field/crop-status/'

		# FARMER
		'/user/farm/farmer/'
			# PLAN
			'/user/farm/farmer/plan/'
			'/user/farm/farmer/plan/add-task/'
			'/user/farm/farmer/plan/rem-task/'
			'/user/farm/farmer/plan/edit-task/'
			'/user/farm/farmer/plan/task/'
			'/user/farm/farmer/plan/task/how-to/'
			# RESOURCES
			'/user/farm/farmer/resources/'
			'/user/farm/farmer/resources/history/'
			'/user/farm/farmer/resources/stage/'
			'/user/farm/farmer/resources/stage/time' # time refers to daily, weekly,  and stage. seedling, grow, fruit..
			# CROP ANALYZER
			'/user/farm/farmer/crop-analyzer/'
			'/user/farm/farmer/crop-analyzer/history/'
			'/user/farm/farmer/crop-analyzer/inputs/'
			'/user/farm/farmer/crop-analyzer/suggestion/'
			'/user/farm/farmer/crop-analyzer/suggestion/crop/'
			# HEALTH ANALYZER
			'/user/farm/farmer/health-analyzer/'
			'/user/farm/farmer/health-analyzer/history/'
			'/user/farm/farmer/health-analyzer/inputs/'
			'/user/farm/farmer/health-analyzer/inputs/suggestion/'
			'/user/farm/farmer/health-analyzer/inputs/suggestion/suggestion-one/'

		# MANAGER
		'/user/farm/manager/'
		'/user/farm/manager/balance/'
		'/user/farm/manager/production/'
		'/user/farm/manager/clients/'
		'/user/farm/manager/orders/'
		'/user/farm/manager/precurement/'

	











