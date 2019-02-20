import unittest
from JSONparser import *

class TestJSONParser(unittest.TestCase):
    """
    Test JSONparser.py to correctly parse JSON
    """

    lexer = lex.lex()
    parser = yacc.yacc()

    def test_JSONobject_one_stringvalue(self):
        line = r'{"foo":123}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONobject_many_stringvalues(self):
        line = r'{"foo":123, "bar":345, "hello":"world"}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONobject_one_nested(self):
        line = r'{"foo":{"bar":1}}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONobject_two_nested(self):
        line = r'{"foo":{"bar":{"hello":"world"}}}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONobject_empty(self):
        line = r'{}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONobject_stringvalue_with_end_comma(self):
        line = r'{"foo":123, "bar":345, "hello":"world",}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONarray_one_value(self):
        line = r'{"foo":["bar"]}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONarray_many_values(self):
        line = r'{"foo":["bar", "foo", 1235]}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONarray_empty(self):
        line = r'{"foo":[]}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONarray_comma(self):
        line = r'{"foo":[,abc]}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONarray_values_with_end_comma(self):
        line = r'{"foo":["bar", "foo", 1235,]}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONarray_wrong_value(self):
        line = r'{"foo":[abc]}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONvalue_true(self):
        line = r'{"foo":true}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONvalue_false(self):
        line = r'{"foo":false}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONvalue_null(self):
        line = r'{"foo":null}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONvalue_wrong_True(self):
        line = r'{"foo":True}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONvalue_wrong_False(self):
        line = r'{"foo":False}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONvalue_wrong_Null(self):
        line = r'{"foo":Null}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONvalue_empty(self):
        line = r'{"foo":}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONstring_alphabet(self):
        line = r'{"weather":1}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONstring_unicode(self):
        line = r'{"世界你好!!&*":1}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONstring_control_characters(self):
        line = r'{"bar\"to, 文化\\, look\/, \bhello, \fworld, \n\rtry, \tboot, food\u0243, yum\u4443":1}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONstring_empty(self):
        line = r'{"":1}'
        self.assertTrue(self.parser.parse, line)

    def test_JSONstring_3hexdigits(self):
        line = r'{"jack\u123of":1}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONstring_quotation(self):
        line = r'{"abc"":1}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSONstring_backslash(self):
        line = r'{"\champ":1}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSON_number_int(self):
        line = r'{"weather":345}'
        result = self.parser.parse(line)
        self.assertTrue(result)

    def test_JSON_number_zero(self):
        line = r'{"weather":0}'
        result = self.parser.parse(line)
        self.assertTrue(result)

    def test_JSON_number_float(self):
        line = r'{"weather":35.2345}'
        result = self.parser.parse(line)
        self.assertTrue(result)

    def test_JSON_number_zero_float(self):
        line = r'{"weather":0.1}'
        result = self.parser.parse(line)
        self.assertTrue(result)

    def test_JSON_number_zero_float_exponent(self):
        line = r'{"weather":0.1e+1}'
        result = self.parser.parse(line)
        self.assertTrue(result)

    def test_JSON_number_int_exponent(self):
        line = r'{"weather":345E-102}'
        result = self.parser.parse(line)
        self.assertTrue(result)

    def test_JSON_number_leading_zero(self):
        line = r'{"weather":000001}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSON_number_int_exponent_no_digit(self):
        line = r'{"weather":345e+}'
        self.assertRaises(SyntaxError, self.parser.parse, line)

    def test_JSON_longfile(self):
        file = open("unittest_long_json.json").read()
        in_text = file
        self.assertTrue(self.parser.parse, in_text)
