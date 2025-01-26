from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Connect to the running Chrome instance
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # Connect to the existing Chrome session

driver = webdriver.Chrome(options=options)

# Verify that we are connected to the correct tab
print("Title of the page:", driver.title)

# Function to find the captions element by its tag and class name
def find_captions_xpath(tag_name="div", class_name="iOzk7 XDPoIe"):
    elements = driver.find_elements(By.TAG_NAME, tag_name)
    for element in elements:
        if class_name in element.get_attribute("class"):
            xpath = driver.execute_script(
                "function absoluteXPath(element) {"
                "  var comp, comps = [];"
                "  var parent = null;"
                "  var xpath = '';"
                "  var getPos = function(element) {"
                "    var position = 1, curNode;"
                "    if (element.nodeType == Node.ATTRIBUTE_NODE) {"
                "      return null;"
                "    }"
                "    for (curNode = element.previousSibling; curNode; curNode = curNode.previousSibling) {"
                "      if (curNode.nodeName == element.nodeName) {"
                "        ++position;"
                "      }"
                "    }"
                "    return position;"
                "  };"

                "  if (element instanceof Document) {"
                "    return '/';"
                "  }"

                "  for (; element && !(element instanceof Document); element = element.nodeType == Node.ATTRIBUTE_NODE ? element.ownerElement : element.parentNode) {"
                "    comp = comps[comps.length] = {};"
                "    switch (element.nodeType) {"
                "      case Node.TEXT_NODE:"
                "        comp.name = 'text()';"
                "        break;"
                "      case Node.ATTRIBUTE_NODE:"
                "        comp.name = '@' + element.nodeName;"
                "        break;"
                "      case Node.ELEMENT_NODE:"
                "        comp.name = element.nodeName;"
                "        break;"
                "    }"
                "    comp.position = getPos(element);"
                "  }"

                "  for (var i = comps.length - 1; i >= 0; i--) {"
                "    comp = comps[i];"
                "    xpath += '/' + comp.name.toLowerCase();"
                "    if (comp.position !== null) {"
                "      xpath += '[' + comp.position + ']';"
                "    }"
                "  }"

                "  return xpath;"
                "}"
                "return absoluteXPath(arguments[0]);",
                element
            )
            return xpath
    return None

# Find the XPath of the captions box
captions_xpath = find_captions_xpath()
print("Captions XPath:", captions_xpath)

# Retrieve the text from the captions element
if captions_xpath:
    captions_element = driver.find_element(By.XPATH, captions_xpath)
    print("Captions Text:", captions_element.text)
else:
    print("Captions element not found.")

# Close the driver after some time
time.sleep(5)
driver.quit()
