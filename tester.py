import email
# December 18, 2005 at 1:07:59 PM PST
# February 3, 2006 at 12:22:14 PM EST
test_email = email.email('Grant', 'Test subject', 'December 18, 2005 at 1:07:59 AM PST', 'Bob', 'Hello world', 'Standard')
test_email.parse_to_datetime()