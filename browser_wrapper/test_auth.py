from browser_stack import BrowserStack

def bs_auth():
    """Tests an API call to get a TV show's info"""

    browser_instance = BrowserStack('projjolbanerji3', 'mdqnGVNZTupQbkyGz2QK')

    assert browser_instance.authorized, True

if __name__ == "__main__":
    bs_auth()