import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


def highlight(element, seconds: float = 0.2):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, s
        )

    original_style = element.get_attribute("style")
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(seconds)
    apply_style(original_style)


def find_element(
    find_by,
    selector,
    in_parent,
    condition,
    wait=1,
    ignore_timeout=False,
    highlight=False,
):
    finders = {
        "class": By.CLASS_NAME,
        "css": By.CSS_SELECTOR,
        "id": By.ID,
        "link": By.LINK_TEXT,
        "name": By.NAME,
        "partial_link": By.PARTIAL_LINK_TEXT,
        "tag": By.TAG_NAME,
        "xpath": By.XPATH,
    }
    conditions = {
        "clickable": EC.element_to_be_clickable,
        "located": EC.presence_of_element_located,
        "all_located": EC.presence_of_all_elements_located,
    }
    assert find_by in finders.keys(), logger.exception(
        '"find_by" must be one of [{}]'.format(finders.keys())
    )
    assert condition in conditions.keys(), logger.exception(
        '"condition" must be one of [{}]'.format(conditions.keys())
    )
    finder = (finders[find_by], selector)
    try:
        if wait > 0:
            w = WebDriverWait(in_parent, wait)
            element = w.until(conditions[condition](finder))
        else:
            if "all" in condition:
                element = in_parent.find_elements(*finder)
            else:
                element = in_parent.find_element(*finder)
        if highlight:
            if "all" in condition:
                [highlight(e) for e in element]
            else:
                highlight(element)
    except:
        if not ignore_timeout:
            logger.warn("Element with {}='{}' not found".format(find_by, selector))
        element = None
    return element
