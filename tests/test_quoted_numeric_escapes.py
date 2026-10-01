"""Numeric escape decoding must receive literal backslashes from the caller."""

import unittest

import pyparsing as pp


class TestQuotedNumericEscapes(unittest.TestCase):
    def test_numeric_escapes(self):
        for escaped, expected in [
            (r"\101", "A"),
            (r"\043", "#"),
            (r"\267", "·"),
            (r"\x41", "A"),
            (r"\x43", "C"),
            (r"\u0041", "A"),
            (r"\u00b7", "·"),
            (r"\u263a", "☺"),
        ]:
            with self.subTest(escaped=escaped):
                quoted = pp.QuotedString('"', esc_char="\\")
                self.assertEqual(
                    quoted.parse_string('"' + escaped + '"', parse_all=True).as_list(),
                    [expected],
                )

    def test_null_and_whitespace_escapes(self):
        quoted = pp.QuotedString('"', esc_char="\\")
        self.assertEqual(quoted.parse_string(r'"\0\n\t"')[0], "\x00\n\t")

    def test_disabled_conversion_keeps_existing_behavior(self):
        quoted = pp.QuotedString('"', esc_char="\\", convert_whitespace_escapes=False)
        self.assertEqual(quoted.parse_string(r'"\101\x41\u0041"')[0], "101x41u0041")

    def test_quoted_results_preserve_escapes(self):
        quoted = pp.QuotedString('"', esc_char="\\", unquote_results=False)
        self.assertEqual(
            quoted.parse_string(r'"\101\x41\u0041"')[0], r'"\101\x41\u0041"'
        )
