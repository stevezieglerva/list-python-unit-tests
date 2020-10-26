
grep -e "class \|def test_" test*.py > grep.txt

python3 list_python_unit_tests.py grep.txt



