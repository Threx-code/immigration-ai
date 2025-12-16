#======================= MONO Endpoints ==========================
ACCOUNT = 'v2/accounts/'
MONO_ACCOUNT_INITIATE = f'{ACCOUNT}initiate'
MONO_ACCOUNT_AUTH = f'{ACCOUNT}auth'
MONO_ACCOUNT_DETAILS = f'{ACCOUNT}/account_id'
MONO_ACCOUNT_IDENTITY = f'{ACCOUNT}account_id/identity'
MONO_ACCOUNT_INCOME = f'{ACCOUNT}account_id/income'
MONO_ACCOUNT_INCOME_RECORDS = f'{ACCOUNT}account_id/income-records'
MONO_ALL_ACCOUNTS = ACCOUNT
MONO_BANKS = 'v3/lookup/banks'
MONO_INSTITUTIONS = '/v3/institutions'
MONO_ACCOUNT_TRANSACTION = f'{ACCOUNT}account_id/transactions'
MONO_ACCOUNT_TRANSACTION_METADATA = f'{ACCOUNT}account_id/transactions/metadata'
MONO_ACCOUNT_BALANCE = f"{ACCOUNT}account_id/balance"

BVN_LOOKUP = 'v2/lookup/bvn'
MONO_BVN_INITIATE = f'{BVN_LOOKUP}/initiate'
MONO_BVN_VERIFY = f'{BVN_LOOKUP}/verify'
MONO_BVN_DETAILS = f'{BVN_LOOKUP}/details'




#======================= MONO Endpoints ==========================




#====================== LOCAL Endpoints ==========================
ACCOUNT_CONNECTED_SUCCESS = "bank_account:link-account-complete"