import json
import os
import logging
REPO_BASE = os.path.dirname(os.path.realpath(__file__))

LOGGER = logging.getLogger(__name__)

class RegPageLocators(object):
    """A class for main page locators. All main page locators should come here"""

    def __init__(self, config_path="valuation_site_locator_repository.json"):
        self.config_path = config_path
        self.config = None
        self.read_config()

    def read_config(self):
        """
        Read the json repository config, if given a full path, else assume the default repository location
        :return:
        """
        if os.path.isfile(self.config_path):
            with open(self.config_path, 'r') as locator_config:
                self.config = json.load(locator_config)
        else:
            with open(os.path.join(REPO_BASE, self.config_path), "r") as locator_config:
                self.config = json.load(locator_config)

    def get_element_locator(self, site, page=None):
        """
        Function to retrieve the element locator based on locator mapped in the config.
        :param site: The site for the evaluation attempt
        :param page: The page of the evaluation site
        :return:
        """
        if not self.config:
            self.read_config()

        if site in self.config:
            try:
                if page:
                    return self.config[site][page]
                return self.config[site]
            except KeyError as k_error:
                LOGGER.error(f"page does not exist in the inventory, {k_error}")
        return None
