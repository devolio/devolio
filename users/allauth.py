from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    """Customized allauths redirect url"""
    def get_login_redirect_url(self, request):
        """Sends the user to his 'me' page"""
        return '/me'
