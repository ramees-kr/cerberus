def strip_http_from_lines(lines):
    stripped_lines = []
    for line in lines:
        if line.strip().startswith("http://") or line.strip().startswith("https://"):
            # Remove 'http://' or 'https://' from the beginning of the line
            stripped_line = line.strip().split("://", 1)[1]
            stripped_lines.append(stripped_line)
        else:
            # If the line doesn't start with 'http://' or 'https://', keep it unchanged
            stripped_lines.append(line.strip())
    return stripped_lines

# Sample input
input_lines = [
    "https://www.standardtrscredit.com Standard Credit active",
    "https://www.cannabisshopaustralia.com Cannabis Shop Australia active auscammer dog2gone",
    "https://www.caliweedsonline.com Cali Weeds Online active dog2gone",
    "http://www.livestockempireltd.net Livestock Empire Ltd active dog2gone",
]

# Call the function
stripped_lines = strip_http_from_lines(input_lines)

# Print the result
for line in stripped_lines:
    print(line)
