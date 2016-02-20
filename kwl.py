# coding: utf-8
"""A standalone KWL interpretor."""

from kwl2text import kwl2text
from kwl2text.generator import Generator
import kwl2text.semantics as semantics
import kasahorow as k
import data
import logging
from kwl2text import grammar as m
import re
import sys
import text2kwl.parse_text as t2k

def get_lc(language):
  return k.get_kasa_from_language(language)

def extract_kwl(text, tag='kwl'):
  stories = re.findall(r"(<%(tag)s.*?%(tag)s>)" % {'tag': tag}, text, re.S|re.M|re.DOTALL)
  return stories

def parse_kwl(kwl):
  kwl = kwl.strip()
  if not kwl:
    return ''
  psr = kwl2text.kwl2textParser()
  sem = semantics.Semantics()

  if '<kwl' != kwl[0:4]:
    kwl = u'<kwl %s ;' % kwl  # Convert into a proper KWL story
  ast = psr.parse(kwl, 'kwl2text', semantics=sem, parseinfo=True)
  if not ast['v']:
    raise ValueError('FAILED to parse %s as KWL' % kwl)

  return ast


def localize(kwl, language, lexicon={}):
  """Convert <kwl> code into language."""
  lexicon = lexicon if len(lexicon) else data.load_td('english', language)
  tg = Generator(get_lc(language), language, m, ast=parse_kwl(kwl), lexicon=lexicon)
  kwl_l10n = tg.generate()
  return kwl_l10n


def text_to_kwl(text, lexicon={}):
  lexicon = lexicon if len(lexicon) else data.load_td('english', 'english')
  return t2k.text_to_kwl(text, lexicon) 


def kwl_to_text(kwl_text, language):
  return localize(kwl_text, language)
