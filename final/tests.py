reminder_pattern='(reminder|rd)\s*(\w)?\s*(.*)'
import re

s='rd'

t=re.match(reminder_pattern,s)
print(t.groups())