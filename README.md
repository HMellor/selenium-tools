# Selenium Tools
A wrapper around `selenium` for quick and simple implementations

## Installation
```bash
pip install git+https://github.com/HMellor/selenium-tools.git#egg=selenium-tools
# or
git clone https://github.com/HMellor/selenium-tools.git
pip install ./selenium_tools
```

## Usage
```python
from selenium_tools import browser, selector

chrome_browser = browser.Browser("chrome")
chrome_browser.navigate_to("https://github.com/HMellor/selenium-tools")

actions = selector.find_element(
    find_by="class",
    selector="pagehead-actions",
    in_parent=chrome_browser.driver,
    condition="located",
)
action_buttons = selector.find_element(
    find_by="class",
    selector="btn",
    in_parent=actions,
    condition="all_located",
    highlight=True
)

```