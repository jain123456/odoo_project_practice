{
    'name': 'Tutorial theme',
    'description': 'A description for your theme.',
    'version': '1.0',
    'author': 'radh',
    'category': 'Theme/Creative',

    'depends': ['website'],
    'data': [
        'views/layout.xml',
        'views/pages.xml',
        'views/snippets.xml',
        'views/options.xml',
    ],
    
    'assets':{
        'web.assets_frontend': [
            'theme_tutorial/static/scss/style.scss',
        ],
        # 'web._assets_primary_variables': [
        #     'theme_tutorial/static/scss/primary_variables.scss',
        # ],
        'website.assets_editor': [
            'theme_tutorial/static/js/tutorial_editor.js',
        ],
    },
}