from browser_stack import BrowserStack

def bs_brow():
    """Tests an API call to get a TV show's info"""

    browser_instance = BrowserStack('projjolbanerji3', 'mdqnGVNZTupQbkyGz2QK')
    response = browser_instance.get_available_browsers()
    assert isinstance(response, list)

if __name__ == "__main__":
    bs_brow()