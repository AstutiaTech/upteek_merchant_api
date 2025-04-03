USER_TYPES={
    'admin': {
        'num': 1,
        'name': 'Admin',
        'roles': {
            'super': {
                'num': 1,
                'name': 'Super Admin'
            },
            'auth': {
                'num': 2,
                'name': 'Authorizer'
            },
            'entry': {
                'num': 3,
                'name': 'Data Entry'
            },
        },
    },
    'bank': {
        'num': 2,
        'name': 'Bank',
        'roles': {
            'auth': {
                'num': 1,
                'name': 'Authorizer'
            },
            'clerk': {
                'num': 2,
                'name': 'Entry Clerk/Entry Agent'
            },
            'entry': {
                'num': 3,
                'name': 'Loan Entry'
            },
        },
    },
    'merchant': {
        'num': 3,
        'name': 'Merchant',
        'roles': {
            'super': {
                'num': 1,
                'name': 'Owner'
            },
            'auth': {
                'num': 2,
                'name': 'Authorizer'
            },
            'entry': {
                'num': 3,
                'name': 'Entry Clerk/Entry Agent'
            },
        },
    },
    'customer': {
        'num': 4,
        'name': 'Customer',
    },
}