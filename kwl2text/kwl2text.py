#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

from grako.parsing import graken, Parser
from grako.util import re, RE_FLAGS  # noqa


__version__ = (2016, 2, 22, 3, 25, 39, 0)

__all__ = [
    'kwl2textParser',
    'kwl2textSemantics',
    'main'
]


class kwl2textParser(Parser):
    def __init__(self,
                 whitespace=None,
                 nameguard=None,
                 comments_re=None,
                 eol_comments_re=None,
                 ignorecase=None,
                 left_recursion=True,
                 **kwargs):
        super(kwl2textParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            **kwargs
        )

    @graken()
    def _kwl2text_(self):
        self._token('<kwl')

        def block1():
            self._sentence_()
            self._token(';')
        self._closure(block1)
        self.ast['@'] = self.last_node
        with self._optional():
            self._token('kwl>')

    @graken()
    def _sentence_(self):
        with self._choice():
            with self._option():
                self._command_()
            with self._option():
                self._question_()
            with self._option():
                self._statement_()
            with self._option():
                self._expression_()
            self._error('no available options')

    @graken()
    def _statement_(self):
        self._expression_()
        self.ast['@'] = self.last_node
        self._token('.')

    @graken()
    def _command_(self):
        self._expression_()
        self.ast['@'] = self.last_node
        self._token('!')

    @graken()
    def _question_(self):
        self._expression_()
        self.ast['@'] = self.last_node
        self._token('?')

    @graken()
    def _expression_(self):
        with self._choice():
            with self._option():
                self._conjunction_()
            with self._option():
                self._conjunct_()
            self._error('no available options')

    @graken()
    def _conjunction_(self):
        with self._choice():
            with self._option():
                self._conjunct_()
                self._join_()
                self._conjunct_()
            with self._option():
                self._token('if')
                self._conjunct_()
                self.ast['@'] = self.last_node
                self._token('then')
                self.ast['@'] = self.last_node
                self._conjunct_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _conjunct_(self):
        self._clause_()

    @graken()
    def _clause_(self):
        with self._choice():
            with self._option():
                self._subject_verb_object_()
            with self._option():
                self._subject_verb_()
            with self._option():
                self._verb_object_()
            with self._option():
                self._group_()
            self._error('no available options')

    @graken()
    def _subject_verb_object_(self):
        self._group_()
        self.ast['subject'] = self.last_node
        self._action_()
        self.ast['verb'] = self.last_node
        self._group_()
        self.ast['object'] = self.last_node

        self.ast._define(
            ['subject', 'verb', 'object'],
            []
        )

    @graken()
    def _subject_verb_(self):
        self._group_()
        self.ast['subject'] = self.last_node
        self._action_()
        self.ast['verb'] = self.last_node

        self.ast._define(
            ['subject', 'verb'],
            []
        )

    @graken()
    def _verb_object_(self):
        self._action_()
        self.ast['verb'] = self.last_node
        self._group_()
        self.ast['object'] = self.last_node

        self.ast._define(
            ['verb', 'object'],
            []
        )

    @graken()
    def _group_(self):
        with self._choice():
            with self._option():
                self._token('{')
                self._single_()
                self.ast['@'] = self.last_node
                self._token('}')
            with self._option():
                self._single_()
            with self._option():
                self._token('{')
                self._conjunction_()
                self.ast['@'] = self.last_node
                self._token('}')
            self._error('no available options')

    @graken()
    def _single_(self):
        with self._choice():
            with self._option():
                self._methods_()
            with self._option():
                self._triple_phrase_()
            with self._option():
                self._tuple_kwl_()
            with self._option():
                self._entry_()
            with self._option():
                self._raw_()
            self._error('no available options')

    @graken()
    def _action_(self):
        with self._choice():
            with self._option():
                self._token('{')
                self._action_()
                self.ast['@'] = self.last_node
                self._token('}')
            with self._option():
                self._conjugated_verb_()
            with self._option():
                self._tuple_verb_()
            with self._option():
                self._verb_()
            self._error('no available options')

    @graken()
    def _conjugated_verb_(self):
        with self._choice():
            with self._option():
                self._tenses_()
                self.ast['@'] = self.last_node
                self._token('(')
                self._conjugations_()
                self.ast['@'] = self.last_node
                self._token('(')
                self._verb_()
                self.ast['@'] = self.last_node
                self._token('))')
            with self._option():
                self._tenses_()
                self.ast['@'] = self.last_node
                self._token('(')
                self._conjugations_()
                self.ast['@'] = self.last_node
                self._token('(')
                self._tuple_verb_()
                self.ast['@'] = self.last_node
                self._token('))')
            self._error('no available options')

    @graken()
    def _tuple_verb_(self):
        self._verb_()
        self.ast['@'] = self.last_node
        self._token('_')
        self._adverb_()
        self.ast['@'] = self.last_node

    @graken()
    def _methods_(self):
        with self._choice():
            with self._option():
                self._modifiers_()
                self.ast['t'] = self.last_node
                self._token('(')
                self._methods_()
                self.ast['v'] = self.last_node
                self._token(')')
            with self._option():
                self._modifiers_()
                self.ast['t'] = self.last_node
                self._token('(')
                self._triple_phrase_()
                self.ast['v'] = self.last_node
                self._token(')')
            with self._option():
                self._modifiers_()
                self.ast['t'] = self.last_node
                self._token('(')
                self._tuple_kwl_()
                self.ast['v'] = self.last_node
                self._token(')')
            with self._option():
                self._modifiers_()
                self.ast['t'] = self.last_node
                self._token('(')
                self._entry_()
                self.ast['v'] = self.last_node
                self._token(')')
            with self._option():
                self._modifiers_()
                self.ast['t'] = self.last_node
                self._token('(')
                self._raw_()
                self.ast['v'] = self.last_node
                self._token(')')
            self._error('no available options')

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _triple_phrase_(self):
        self._entry_()
        self.ast['@'] = self.last_node
        self._token('(')
        self._tuple_kwl_()
        self.ast['@'] = self.last_node
        self._token(')')

    @graken()
    def _tuple_kwl_(self):
        with self._choice():
            with self._option():
                self._entry_()
                self.ast['@'] = self.last_node
                self._token('_')
                self._entry_()
                self.ast['@'] = self.last_node
            with self._option():
                self._entry_()
                self.ast['@'] = self.last_node
                self._token('_')
                self._raw_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _modifiers_(self):
        with self._choice():
            with self._option():
                self._partofspeech_()
            with self._option():
                self._conjugations_()
            with self._option():
                self._prepositions_()
            with self._option():
                self._tenses_()
            with self._option():
                self._formatting_()
            self._error('no available options')

    @graken()
    def _join_(self):
        with self._choice():
            with self._option():
                self._token(':')
            with self._option():
                self._token(',')
            with self._option():
                self._token('and')
            with self._option():
                self._token('but')
            with self._option():
                self._token('of')
            with self._option():
                self._token('or')
            with self._option():
                self._token('so')
            with self._option():
                self._token('then')
            with self._option():
                self._token('when')
            self._error('expecting one of: , : and but of or so then when')

    @graken()
    def _formatting_(self):
        with self._choice():
            with self._option():
                self._token('defn')
            with self._option():
                self._token('plural')
            with self._option():
                self._token('quote')
            with self._option():
                self._token('sample')
            with self._option():
                self._token('title')
            self._error('expecting one of: defn plural quote sample title')

    @graken()
    def _conjugations_(self):
        with self._choice():
            with self._option():
                self._token('f')
            with self._option():
                self._token('i')
            with self._option():
                self._token('je')
            with self._option():
                self._token('m')
            with self._option():
                self._token('tu')
            with self._option():
                self._token('il')
            with self._option():
                self._token('elle')
            with self._option():
                self._token('nous')
            with self._option():
                self._token('vous')
            with self._option():
                self._token('ils')
            with self._option():
                self._token('elles')
            self._error('expecting one of: elle elles f i il ils je m nous tu vous')

    @graken()
    def _prepositions_(self):
        with self._choice():
            with self._option():
                self._token('at')
            with self._option():
                self._token('for')
            with self._option():
                self._token('from')
            with self._option():
                self._token('in')
            with self._option():
                self._token('of')
            with self._option():
                self._token('on')
            with self._option():
                self._token('to')
            self._error('expecting one of: at for from in of on to')

    @graken()
    def _tenses_(self):
        with self._choice():
            with self._option():
                self._token('cmd')
            with self._option():
                self._token('done_tdy')
            with self._option():
                self._token('done_tmw')
            with self._option():
                self._token('done_ydy')
            with self._option():
                self._token('inf')
            with self._option():
                self._token('not_tdy')
            with self._option():
                self._token('not_tmw')
            with self._option():
                self._token('not_ydy')
            with self._option():
                self._token('now_tdy')
            with self._option():
                self._token('now_tmw')
            with self._option():
                self._token('now_ydy')
            with self._option():
                self._token('tdy')
            with self._option():
                self._token('tmw')
            with self._option():
                self._token('ydy')
            self._error('expecting one of: cmd done_tdy done_tmw done_ydy inf not_tdy not_tmw not_ydy now_tdy now_tmw now_ydy tdy tmw ydy')

    @graken()
    def _adjective_(self):
        self._token('adj')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _adverb_(self):
        self._token('adv')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _determiner_(self):
        self._token('det')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _noun_(self):
        self._token('nom')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _possessive_(self):
        self._token('pos')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _preposition_(self):
        self._token('pre')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _pronoun_(self):
        self._token('pro')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _raw_(self):
        with self._choice():
            with self._option():
                self._pattern(r'raw\((.*?)\)')
            with self._option():
                self._pattern(r'date\((.*?)\)')
            self._error('expecting one of: date\\((.*?)\\) raw\\((.*?)\\)')

    @graken()
    def _verb_(self):
        self._token('act')
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _entry_(self):
        self._partofspeech_()
        self.ast['t'] = self.last_node
        self._token(':')
        self._token_()
        self.ast['v'] = self.last_node

        self.ast._define(
            ['t', 'v'],
            []
        )

    @graken()
    def _partofspeech_(self):
        with self._choice():
            with self._option():
                self._token('act')
            with self._option():
                self._token('adj')
            with self._option():
                self._token('adv')
            with self._option():
                self._token('det')
            with self._option():
                self._token('exc')
            with self._option():
                self._token('kg')
            with self._option():
                self._token('nom')
            with self._option():
                self._token('pos')
            with self._option():
                self._token('pre')
            with self._option():
                self._token('pro')
            with self._option():
                self._token('sci')
            self._error('expecting one of: act adj adv det exc kg nom pos pre pro sci')

    @graken()
    def _token_(self):
        self._pattern(r'[a-zA-Z0-9#]*')


class kwl2textSemantics(object):
    def kwl2text(self, ast):
        return ast

    def sentence(self, ast):
        return ast

    def statement(self, ast):
        return ast

    def command(self, ast):
        return ast

    def question(self, ast):
        return ast

    def expression(self, ast):
        return ast

    def conjunction(self, ast):
        return ast

    def conjunct(self, ast):
        return ast

    def clause(self, ast):
        return ast

    def subject_verb_object(self, ast):
        return ast

    def subject_verb(self, ast):
        return ast

    def verb_object(self, ast):
        return ast

    def group(self, ast):
        return ast

    def single(self, ast):
        return ast

    def action(self, ast):
        return ast

    def conjugated_verb(self, ast):
        return ast

    def tuple_verb(self, ast):
        return ast

    def methods(self, ast):
        return ast

    def triple_phrase(self, ast):
        return ast

    def tuple_kwl(self, ast):
        return ast

    def modifiers(self, ast):
        return ast

    def join(self, ast):
        return ast

    def formatting(self, ast):
        return ast

    def conjugations(self, ast):
        return ast

    def prepositions(self, ast):
        return ast

    def tenses(self, ast):
        return ast

    def adjective(self, ast):
        return ast

    def adverb(self, ast):
        return ast

    def determiner(self, ast):
        return ast

    def noun(self, ast):
        return ast

    def possessive(self, ast):
        return ast

    def preposition(self, ast):
        return ast

    def pronoun(self, ast):
        return ast

    def raw(self, ast):
        return ast

    def verb(self, ast):
        return ast

    def entry(self, ast):
        return ast

    def partofspeech(self, ast):
        return ast

    def token(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None, nameguard=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = kwl2textParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace,
        nameguard=nameguard)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in kwl2textParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for kwl2text.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-n', '--no-nameguard', action='store_true',
                        dest='no_nameguard',
                        help="disable the 'nameguard' feature")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace,
        nameguard=not args.no_nameguard
    )
