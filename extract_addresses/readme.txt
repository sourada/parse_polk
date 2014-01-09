extract_addresses attempts to extract addresses from OCR results from Polk directories. Run it like:

python extract_addresses/main.py foo.txt bar.txt baz.txt

to extract and print addresses from the three listed OCR text files.

A basic test framework was begun in test.py. The tests in there are not perfect, they're just helpful to judge progress or regressions as the parsing code is modified.
