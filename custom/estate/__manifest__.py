{
	'name':'Real Estate',
	'summary':'Hello! This is an E-state App.',	
    
	'depends':['website'],

	'data' : [

		'security/ir.model.access.csv',
        'wizard/add_offers_view.xml',
		'views/estate_property_views.xml',
		'views/estate_property_offer_views.xml',
		'views/estate_property_type_views.xml',
		'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/pages.xml',
        'views/templates.xml',
        'reports/estate_property_reports.xml',
        'reports/estate_property_templates.xml',
		# 'views/estate_menus.xml'

	]

}
