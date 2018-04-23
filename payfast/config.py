from django.utils.module_loading import import_string


def get_config():
    """Returns an instance of the configured config class.

    :return: Project's defined Payfast configuration.
    :rtype: :class:`AbstractPayfastConfig`

    By default, this function will return an instance of
    :class:`payfast.settings_config.WebIntegrationConfig`. If
    :data:`PAYFAST_CONFIG_CLASS` is defined, it will try to load this class and
    return an instance of this class instead. Currently there is only a single config
    class. This can be used for future enhancements.

    .. note::

        This function expects :data:`PAYFAST_CONFIG_CLASS` to be a string that
        represent the python import path of the Payfast config class, such as
        ``payfast.settings_config.WebIntegrationConfig``.

    """
    config_class_string = 'payfast.settings_config.WebIntegrationConfig'

    return import_string(config_class_string)()


class AbstractPayfastConfig:
    """Abstract class for an Payfast config class.

    Plugin users that want to create their own Payfast config class must comply
    with this interface.
    """
    def get_merchant_id(self):
        """Get Payfast merchant identifier.

        :return: Payfast merchant identifier as string.
        """
        raise NotImplementedError

    def get_action_url(self):
        """Get Payfast secret passphrase if set.

        :return: Payfast secret passphrase if set.
        """
        raise NotImplementedError

    def get_passphrase(self):
        """Get Payfast URL to post payment request form to.

        :return: Payfast gateway URL.
        """
        raise NotImplementedError

    def get_merchant_key(self):
        """Get Payfast merchant key.

        :return: Payfast merchant key.
        """
        raise NotImplementedError

    def get_ip_address_header(self):
        """Get the request HTTP header used to get customer's IP.

        :return: appropriate request HTTP header.
        """
        raise NotImplementedError
