

class Constants:
    """List of payfast constants. Most constants were derived form the payfast
    .. _documentation: https://developers.payfast.co.za/documentation/#checkout-page
    """

    # Setup
    ACTION_URL = 'action_url'
    HOST_IP = 'host_ip'

    # https://developers.payfast.co.za/documentation/#notify-page-itn (Security step two)
    VALID_PAYFAST_HOSTS = (
        'www.payfast.co.za',
        'sandbox.payfast.co.za',
        'w1w.payfast.co.za',
        'w2w.payfast.co.za'
    )

    # Merchant details

    MERCHANT_ID = 'merchant_id'
    MERCHANT_KEY = 'merchant_key'
    RETURN_URL = 'return_url'
    CANCEL_URL = 'cancel_url'
    NOTIFY_URL = 'notify_url'
    PASSPHRASE = 'passphrase'

    #Buyer details

    NAME_FIRST = 'name_first'
    NAME_LAST = 'name_last'
    EMAIL_ADDRESS = 'email_address'
    CELL_NUMBER = 'cell_number'

    # Transaction details

    M_PAYMENT_ID = 'm_payment_id'
    AMOUNT = 'amount'
    ITEM_NAME = 'item_name'
    ITEM_DESCRIPTION = 'item_description'

    # Transaction options

    EMAIL_CONFIRMATION = 'email_confirmation'
    CONFIRMATION_ADDRESS = 'confirmation_address'

    # Payment method

    PAYMENT_METHOD = 'payment_method'

    #Security

    SIGNATURE = 'signature'
    SIGNER = 'signer'

    # Notification constants

    PF_PAYMENT_ID = 'pf_payment_id'
    PAYMENT_STATUS = 'payment_status'
    AMOUNT_GROSS = 'amount_gross'
    AMOUNT_FEE = 'amount_fee'
    AMOUNT_NET = 'amount_net'

    # Recurring / Subscription constants

    TOKEN = 'token'

    # Dev Defaults

    MERCHANT_ID_DEV = 10000100
    MERCHANT_KEY_DEV = '46f0cd694581a'
    USER_NAME_DEV = 'sbtu01@payfast.co.za'
    USER_PASS_DEV = 'clientpass'
    ACTION_URL_DEV = 'https://sandbox.payfast.co.za/eng/process'
    VALIDATE_URL_DEV = 'https://sandbox.payfast.co.za/eng/query/validate'
    QUERY_URL_DEV = 'https://api.payfast.co.za/process/query/'

    # Live Defaults
    ACTION_URL_LIVE = 'https://payfast.co.za/eng/process'
    VALIDATE_URL_LIVE = 'https://payfast.co.za/eng/query/validate'
    QUERY_URL_LIVE = 'https://api.payfast.co.za/process/query/'

    #Payment results

    PAYMENT_RESULT_COMPLETE = 'COMPLETE'
    PAYMENT_RESULT_CANCELLED = 'CANCELLED'



