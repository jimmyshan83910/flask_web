import re

string = ["麥當勞-復興二店","BURGER KING漢堡王 敦南店"]
for item in string:
    if re.search("漢堡王", item):
        print(item)