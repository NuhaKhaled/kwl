#!/usr/bin/env python
# coding: utf-8

import data
import kwl as g
import pronounce as p
import sys
import unittest

# Grammar coverage per language
COVERAGE = {
  'children': ['adj_nom', 'det_nom', 'inf', 'plural', 'pos_nom', 'tdy', 'tmw', 'ydy'],
  'learner': ['and', 'command', 'or', 'question', 'statement', 'subject_verb', 'verb_object', 'date'],
  'advanced': ['done_tdy', 'done_tmw', 'done_ydy', 'from', 'in', 'may', 'not_tdy', 'not_tmw', 'not_ydy']
}

DATA_TESTS = {
  'akan': {
    'adj_nom': [('adj:new_nom:house', 'dan foforo'),
                ('adj:1_nom:house', 'dan 1'),
                ('adj:two(adj:good_nom:thing)', 'ade papa abien'),
               ],
    'adj_sci': [('adj:one_sci:atom', u'atɔm koro')],
    'and': [('raw(A) and raw(B)', 'A na B')],
    'command': [('cmd(tu(act:sit_adv:down))!', 'Tena ase!'), ('cmd(tu(act:come_adv:here))!', 'Bra ha!'), ('cmd(tu(act:eat)) nom:sugar!', 'Di asikyire!')],
    'date': [('date(2015-11-12)', u'Yawda. Ɔberɛfɛw da 12, afe 2015')],
    'det_nom': [('det:the_nom:dog', u'\u0254twea no')],
    'done_tdy': [('done_tdy(il(act:finish))', 'awie')],
    'done_ydy': [('done_ydy(il(act:finish))', 'awie')],
    'in': [('in(nom:Jesus)', u'wɔ Yesu mu'), ('nom:faith, in(nom:Jesus)', u'gyedi, wɔ Yesu mu'), ('act:jump in(adj:perfect_nom:peace)', u'huruw wɔ asomudwoe pɛ mu')],
    'inf':[('inf(act:walk)', 'nantew')],
    'may': [('may(tu(act:follow))', u'bɛtumi adi ... akyiri'), ('may(je(act:have))', u'b\u025btumi anya')],
    'not_tdy': [('not_tdy(act:sleep)', 'nnda')],
    'on': [('pre:on(det:the_nom:table)', 'pon no so')],
    'or': [('raw(A) or raw(B)', 'A anaa B')],
    'plural': [('plural(nom:chair)', 'ngua'), ('plural(nom:child)', 'mba'),
               ('plural(nom:doctor)', u'adɔktafo'),
               ('plural(adj:two_nom:chair)', 'ngua abien')],
    'pos_nom': [('pos:my_nom:house', 'me dan')],
    'question': [('pro:I tdy(je(act:love)) pro:you?', u'Me dɔ wo?'),
                 ('nom:love tdy(il(act:be)) pro:what?', u'Dɔ yɛ dɛn?'),
                 ('raw(Mary) tdy(elle(act:be)) pro:who?',u'Mary yɛ woana?'),
                 ('raw(Mary) tdy(elle(act:walk_adv:how))?',u'Mary nantew sɛdea?'),
                 ('raw(Mary) tdy(elle(act:cry_adv:why))?',u'Mary su adɛn?'),
                 ('raw(Mary), pro:you tdy(tu(act:cry_adv:why))?',u'Mary, wo su adɛn?'),
                ],
    'statement':[('pro:I tdy(je(act:love)) pro:you.', u'Me dɔ wo.')],
    'tdy': [('tdy(tu(act:follow))', u'di ... akyiri'), ('tdy(je(act:have))', u'w\u0254')],
    'tmw': [('tmw(tu(act:follow))', u'bɛdi ... akyiri'), ('tmw(je(act:have))', u'b\u025bnya')],
    'verb_object': [('tdy(tu(act:follow)) det:the_nom:dog', u'di \u0254twea no akyiri'), ('act:govern nom:Ghana!', 'Bu Gaana man!')],
    'ydy': [('ydy(tu(act:follow))', u'diee ... akyiri'), ('ydy(je(act:have))', u'nyaee')],
    'quote': [('quote(raw(1 2 3))', '"1 2 3"')],
    'raw': [('raw(12:6)', '12:6')],
    'science_noun': [('sci:atom', u'atɔm'), ('adj:one_sci:atom', u'atɔm koro')],
    'subject_verb': [('det:the_nom:man tmw(il(act:come))', u'banyin no bɛba')],
    'when': [('act:eat when adj:rich', 'di abere a bafuu')],
  },
  'amarinya': {
    'and': [('raw(A) and raw(B)', u'A እና B')],
    'adj_nom': [('adj:white_nom:book', u'ነጭ መፅሀፍ')],
    'or': [('raw(A) or raw(B)', u'A ወይም B')],
    'pos_nom': [('pos:my_nom:book', u'የእኔ መፅሀፍ')],
    'punctuation': [('raw(A).', u'A።'), ('raw(A), raw(B)', u'A፣ B')],
    'inf': [('inf(act:walk)', u'መራመድ')],
  },
  'bemba': {
  },
  'chewa': {
    'adj_nom': [('adj:new_nom:carpet', 'kapeti yatsopano')],
    'det_nom': [('det:the_nom:book', u'bukhu')],
    'plural': [('plural(nom:dog)', 'galu')],
    'pos_nom': [('pos:my_nom:house', 'nyumba yanga')],
    'inf':[('inf(act:walk)', 'kuyenda')],
    'tdy': [('tdy(je(act:walk))', 'ndimayenda'), ('tdy(tu(act:walk))', 'umayenda'),
            ('tdy(elle(act:walk))', 'amayenda'), ('tdy(il(act:eat))', 'amaidya'),
            ('tdy(nous(act:walk))', 'timayenda'), ('tdy(vous(act:walk))', 'mumayenda'),
            ('tdy(ils(act:walk))', 'amayenda'), ],
    'tmw': [('tmw(je(act:walk))', 'ndidzayenda'), ('tmw(tu(act:walk))', 'udzayenda'),
            ('tmw(il(act:walk))', 'adzayenda'), ('tmw(ils(act:walk))', 'adzayenda'),
            ('tmw(nous(act:walk))', 'tidzayenda'), ('tmw(vous(act:walk))', 'mudzayenda'), ],
    'ydy': [('ydy(je(act:walk))', 'ndinayenda'),
            ('ydy(tu(act:walk))', 'unayenda'), ('ydy(vous(act:walk))', 'munayenda'),
            ('ydy(ils(act:walk))', 'anayenda')],
  },
  'dinka': {
  },
  'english': {
    'adj_nom': [('adj:red_nom:book', u'red book')],
    'det_nom': [('det:the_nom:book', u'the book'),
                ('det:a_nom:animal', 'an animal')],
    'pos_nom': [('pos:my_nom:book', u'my book'),
                ('pos:her_nom:freedom', 'her freedom')],
    'inf': [('inf(act:walk)', u'to walk')],
    'tdy': [('tdy(je(act:walk))', u'gehe'), ('tdy(tu(act:learn))', 'lernst')],
    'act_adv': [('act:eat_adv:quickly', 'eat quickly')],
    'command': [('cmd(tu(act:sit_adv:down))!', 'Sit down!'), ('cmd(tu(act:come_adv:here))!', 'Come here!'), ('cmd(tu(act:add)) nom:sugar!', 'Add sugar!')],
    'compounds': [('exc:thank#you', 'thank you')],
    'date': [('date(2015-11-12)', u'Thursday. November 12, 2015')],
    'done_tdy': [('done_tdy(il(act:finish))', 'has finished')],
    'done_ydy': [('done_ydy(il(act:finish))', 'had finished')],
    'in': [('in(nom:Jesus)', 'in Jesus'), ('nom:faith, in(nom:Jesus)', 'faith, in Jesus'), ('act:jump in(adj:perfect_nom:peace)', 'jump in perfect peace')],
    'of': [('nom:glass of nom:water', 'glass of water')],
    'plural': [('plural(nom:child)', 'children'), ('plural(nom:dog)', 'dogs'),
               ('plural(nom:pitch)', 'pitches')],
    'question': [('raw(Mary) tdy(elle(act:be)) pro:who?', 'Mary is who?'),
                 ('nom:love tdy(il(act:be)) pro:what?', 'What is love?'),
                 ('pro:who ydy(il(act:help)) raw(Kofi)?', 'Who helped Kofi?'),
                 ('raw(Kofi) ydy(il(act:help)) pro:who?', 'Kofi helped who?'),
                 ('pro:you tdy(tu(act:eat_adv:how)) det:the_nom:food?', 'The food how eat you?'),
                 ('raw(Mary) tdy(tu(act:cry_adv:why)) pro:you?',u'Why do you cry Mary?'),
                 ('act:eat_adv:quickly?', 'Quickly eat?'), # Order changes when a question
                ],
    'statement': [('pro:you tdy(tu(act:be)) det:a(adj:important_nom:person)', 'you are an important person'), ('pro:she tmw(il(act:bring)) {nom:wealth and nom:happiness}', 'she will bring wealth and happiness')],
    'tdy': [('tdy(je(act:be))', 'am'), ('tdy(je(act:walk))', 'walk'), ('tdy(elle(act:walk))', 'walks'), ('tdy(je(act:be)) at(nom:home)', 'am at home'),
            ('tdy(il(act:run)) to(nom:school)', 'runs to school')],
    'tmw': [('tmw(je(act:be))', 'will be'), ('tmw(je(act:walk))', 'will walk')],
    'ydy': [('ydy(je(act:be))', 'was'), ('ydy(elle(act:walk))', 'walked')],
    'when': [('act:eat when adj:hungry', 'eat when hungry')],
  },
  'french': {
    'adj_nom': [('adj:each_nom:book', 'chaque livre')],
    'and': [('if pro:you tdy(tu(act:eat)) nom:food then pro:you tmw(tu(act:grow))',
             'si tu manges nourriture alors tu grandiras')],
    'det_nom': [('det:the_nom:book', u'le livre')],
    'plural': [('plural(nom:dog)', 'chiens')],
    'pos_nom': [('pos:my_nom:book', u'mon livre')],
    'inf': [('inf(act:walk)', u'marcher')],
    'tdy': [('tdy(je(act:walk))', u'marche'), ('tdy(i(act:walk))', u'marche'),
            ('tdy(nous(act:eat))', 'mangeons'), ('tdy(m(act:be))', 'est')],
    'tmw': [('tmw(je(act:walk))', u'marcherai')],
    'ydy': [('ydy(je(act:walk))', u'marchais')],
  },
  'fula': {
    'adj_nom': [('adj:strong_nom:spirit', u'jomoti sembigol')],
    'and': [('raw(A) and raw(B)', u'A e B')],
    'det_nom': [('det:the_nom:soul', u'yonki o'), ('det:a_nom:soul', u'yonki')],
    'or': [('raw(A) or raw(B)', u'A maa B')],
    'plural': [('plural(nom:farmer)', u'ndɛmooɓe')],
    'pos_nom': [('pos:my_nom:soul', u'yonki am'), ('pos:your_nom:house', 'suudu ma')],
    'inf': [('inf(act:come)', u'arde')],
    'tdy': [('tdy(je(act:come))', u'ɗo ara'), ('tdy(nous(act:come))', u'ɗɛn ngara'), 
            ('tdy(f(act:come))', u'ɗi ara'),
            ('tdy(nous(act:come))', u'ɗɛn ngara')],
    'tmw': [('tmw(m(act:come))', u'arat')],
    'ydy': [('ydy(m(act:come))', u'ari')],
  },
  'gadangme': {
    'adj_nom': [('adj:new_nom:book', u'wolo ehee')],
    'det_nom': [('det:the_nom:book', u'wolo lɛ')],
    'plural': [('plural(nom:dog)', 'gbeei')],
    'pos_nom': [('pos:my_nom:book', u'mi wolo')],
    'inf': [('inf(act:walk)', u'nyiɛ')],
    'tdy': [('tdy(je(act:walk))', u'mnyiɛ')],
    'tmw': [('tmw(je(act:walk))', u'baanyiɛ')],
    'ydy': [('ydy(je(act:walk))', u'nyiɛ omo')],
  },
  'gbe': {
    'adj_nom': [('adj:every_nom:book', 'agbale sia agbale'), ('adj:good_nom:person', 'ame nyuie')],
    'det_nom': [('det:the_nom:book', u'agbale la')],
    'plural': [('plural(nom:dog)', 'avuwo')],
    'pos_nom': [('pos:my_nom:book', u'nye agbale')],
    'inf': [('inf(act:walk)', u'z\u0254')],
    'iwe': [('raw(Mary) tdy(il(act:be)) pro:who?', 'Amekae nye Mary?'),],
    'statement': [('pro:she now_tdy(elle(act:love)) pos:her_nom:country', u'e le eƒe duk\u0254 l\u0254m'), ('pro:she now_tdy(elle(act:love)) pos:her_nom:country.', u'E le eƒe duk\u0254 l\u0254m.'), ('pro:we tdy(nous(act:love)) pro:him', u'mi lɔ e')],
    'tdy': [('now_tdy(je(act:walk))', u'le ... z\u0254m')],
    'tmw': [('tmw(je(act:walk))', u'az\u0254')],
    'verb_object': [('now_tdy(je(act:walk)) nom:home', u'le afeme z\u0254m')],
    'ydy': [('ydy(je(act:walk))', u'z\u0254')],
  },
  'deutsch': {
    'adj_nom': [('adj:new_nom:book', 'neu buch')],
    'det_nom': [('det:the_nom:book', u'die buch')],
    'plural': [('plural(nom:dog)', 'hunden')],
    'pos_nom': [('pos:my_nom:book', u'mein buch')],
    'inf': [('inf(act:walk)', u'gehen')],
    'tdy': [('tdy(je(act:walk))', u'gehe'), ('tdy(tu(act:learn))', 'lernst')],
    'tmw': [('tmw(je(act:walk))', u'werde gehen')],
    'ydy': [('ydy(je(act:walk))', u'ging')],
  },
  'gikuyu': {
    'adj_nom': [('adj:new_nom:house', 'nyomba njeru')],
    'det_nom': [('det:the_nom:book', u'iuku')],
    'plural': [('plural(nom:dog)', 'ngui')],
    'pos_nom': [('pos:his_nom:book', 'iuku we')],
    'inf': [('inf(act:listen)', u'gũthikiria')],
    'tdy': [('tdy(je(act:listen))', u'nĩthikiria')],
    'tmw': [('tmw(je(act:listen))', u'ndĩgathikiria')],
    'ydy': [('ydy(je(act:listen))', u'nĩthikirire')],
  },
  'hausa': {
    'adj_nom': [('adj:new_nom:book', 'sabon littafi')],
    'det_nom': [('det:the_nom:book', u'littafi n')],
    'plural': [('plural(nom:dog)', 'karen')],
    'pos_nom': [('pos:my_nom:house', u'gida na')],
    'inf': [('inf(act:walk)', u'yi tafiya')],
    'question': [('pro:I tdy(je(act:love)) pro:youe?', u'Na son ki?'),
                 ('nom:love tdy(il(act:be)) pro:what?', u'Soyayya ne mene?')],
    'tdy': [('tdy(je(act:love))', u'son')],
    'tmw': [('tmw(je(act:walk))', u'za tafiya')],
    'ydy': [('ydy(je(act:walk))', u'tafiya')],
  },
  'igbo': {
    'adj_nom': [('adj:new_nom:book', u'akwụkwọ ọhụrụ')],
    'det_nom': [('det:the_nom:book', u'akwụkwọ ahụ')],
    'plural': [('plural(nom:dog)', u'nkịta')],
    'pos_nom': [('pos:my_nom:book', u'akwụkwọ m')],
    'inf': [('inf(act:walk)', 'ruo ejeije')],
    'tdy': [('tdy(je(act:walk))', 'na-ejeije')],
    'tmw': [('tmw(je(act:walk))', 'ga-ejeije')],
    'ydy': [('ydy(je(act:walk))', 'ejeije')],
  },
  'kongo': {  # Does not change by pronoun class so just testing with 1st person
    'adj_nom': [('adj:one_nom:dog', 'yimbua mosi')],
    'det_nom': [('det:the_nom:dog', u'yimbua')],
    'plural': [('plural(nom:dog)', 'yimbua')],
    'pos_nom': [('adj:good_nom:gift', 'lukau ya mbote')],
    'inf': [('inf(act:walk)', 'kuzieta')],
    'tdy': [('tdy(je(act:walk))', 'kezieta')],
    'tmw': [('tmw(je(act:walk))', 'tazieta'), ],
    'ydy': [('ydy(je(act:walk))', 'zietaka')],
  },
  'lingala': {
    'adj_nom': [('adj:new_nom:house', 'ndako ya sika')],
    'and': [('raw(A) and raw(B)', 'A na B')],
    'command': [('cmd(tu(act:come_adv:here))!', 'Yaka awa!'),],
    'date': [('date(2015-11-12)',
              u'Mokolo ya minei. Sanza ya zomi na moko 12, 2015')],
    'det_nom': [('det:the_nom:book', u'buku oyo')],
    'inf': [('inf(act:walk)', 'kotambola')],
    'of': [('nom:glass of nom:water', 'kopo ya mayi')],
    'or': [('raw(A) or raw(B)', 'A o B')],
    'plural': [('plural(nom:dog)', 'mbwa')],
    'pos_nom': [('pos:his_nom:country', 'mboka naye')],
    'question': [('raw(Mary) tdy(f(act:be)) pro:who?', 'Mary azali nani?'),],
    'statement': [('raw(Mary) tdy(f(act:be)) det:a_nom:doctor.',
                   'Mary azali monganga ya.'),],
    'subject_verb': [('det:the_nom:man tmw(il(act:walk))',
                     u'mobali ya oyo akotambola')],
    'tdy': [('tdy(je(act:walk))', 'natamboli'), ('tdy(nous(act:walk))', 'totamboli'),
            ('tdy(tu(act:walk))', 'otamboli'), ('tdy(vous(act:walk))', 'botamboli'),
            ('tdy(elle(act:walk))', 'atamboli'), ('tdy(il(act:walk))', 'atamboli'), ('tdy(ils(act:walk))', 'batamboli'), ('tdy(i(act:be))', 'ezali'), ('tdy(m(act:be))', 'azali'),
           ],
    'tmw': [('tmw(je(act:walk))', 'nakotambola'), ('tmw(nous(act:walk))', 'tokotambola'),
            ('tmw(tu(act:walk))', 'okotambola'), ('tmw(vous(act:walk))', 'bokotambola'),
            ('tmw(il(act:walk))', 'akotambola'), ('tmw(ils(act:walk))', 'bakotambola')],
    'verb_object': [('tdy(tu(act:follow)) det:the_nom:dog',
                     'olandi mbwa ya oyo'),],
    'ydy': [('ydy(tu(act:walk))', 'otambolaki'), ('ydy(vous(act:walk))', 'botambolaki'),
            ('ydy(ils(act:walk))', 'batambolaki')],
  },
  'luganda': {
    'adj_nom': [('adj:good_nom:dog', 'embwa lungi')],
    'det_nom': [('det:the_nom:book', u'ekitabo eyo')],
    'done_tdy': [('done_tdy(il(act:do))', 'akoze')],
    'not_tdy': [('not_tdy(il(act:do))', 'takola')],
    'plural': [('plural(nom:dog)', 'embwa')],
    'pos_nom': [('pos:my_nom:book', u'ekitabo nge'), ('pos:her_nom:car', 'emmotoka e')],
    'inf': [('inf(act:walk)', u'okutambula')],
    'iwe': [('raw(Mary) tdy(il(act:be)) pro:who?', 'Mary y\'ani?'),
            ('raw(Unity Song) tdy(i(act:be)) pro:what?', 'Unity Song kye ki?'),
           ],
    'statement':[('pro:we tdy(nous(act:love)) raw(Kofi).',
                 u'Ffe tukwaagala Kofi.'),
    ],
    'tdy': [('tdy(je(act:eat))', 'nlya'), ('tdy(tu(act:do))', 'okola')],
    'tmw': [('tmw(je(act:walk))', u'nditambula')],
    'ydy': [('ydy(je(act:walk))', u'natambula'), ('ydy(f(act:eat))', 'yalya')],
  },
  'luwo': {
    'adj_nom': [('adj:good_nom:house', 'ot ber')],
    'and': [('raw(A) and raw(B)', 'A gi B')],
    'det_nom': [('det:the_nom:book', u'buk')],
    'or': [('raw(A) or raw(B)', 'A kata B')],
    'plural': [('plural(nom:dog)', 'guok')],
    'pos_nom': [('pos:my_nom:book', u'buk mara')],
    'inf': [('inf(act:walk)', u'wuotho')],
    'iwe': [('raw(Mary) tdy(il(act:be)) pro:who?', 'Mary en ng\'a?'),],
    'tdy': [('tdy(je(act:walk))', 'awuotho'), ('tdy(nous(act:walk))', 'wawuotho'),],
    'tmw': [('tmw(je(act:walk))', 'abiro wuotho'), ('tmw(nous(act:walk))', 'wabiro wuotho'), ],
    'ydy': [('ydy(je(act:walk))', 'ne awuotho'), ('ydy(nous(act:walk))', 'ne wawuotho')],
  },
  'malagasy': {
    'adj_nom': [('adj:new_nom:book', 'boky vaovao')],
    'det_nom': [('det:the_nom:book', u'ny boky')],
    'plural': [('plural(nom:dog)', 'alika')],
    'pos_nom': [('pos:my_nom:book', u'boky ko')],
    'inf': [('inf(act:walk)', u'andeha')],
    'iwe': [('raw(Mary) tdy(il(act:be)) pro:who?', 'Iza moa i Mary?'),],
    'tdy': [('tdy(je(act:walk))', 'mandeha')],
    'tmw': [('tmw(je(act:walk))', 'handeha')],
    'ydy': [('ydy(je(act:walk))', 'nandeha')],
  },
  'oromoo': {
    'adj_nom': [('adj:one_nom:book', 'kitaaba tokko')],
    'det_nom': [('det:the_nom:book', u'kitaaba icha')],
    'plural': [('plural(nom:dog)', 'saree')],
    'pos_nom': [('pos:my_nom:book', u'kitaaba ko')],
    'inf': [('inf(act:walk)', u'deemaa')],
    'tdy': [('tdy(je(act:eat))', 'nyaachaan jiraa')],
    'tmw': [('tmw(je(act:eat))', u'ni nyaadhaa')],
    'ydy': [('ydy(je(act:eat))', 'nyaachee')],
  },
  'portuguesa': {
    'adj_nom': [('adj:new_nom:book', 'livro novo')],
    'det_nom': [('det:this_nom:book', u'este livro')],
  },
  'shona': {
    'adj_nom': [('adj:each_nom:book', 'bhuku ese')],
    'det_nom': [('det:the_nom:book', u'bhuku')],
    'plural': [('plural(nom:thing)', 'zvinhu')],
    'pos_nom': [('pos:my_nom:dog', u'imbwa yangu')],
    'inf': [('inf(act:walk)', u'kufamba')],
    'iwe': [('raw(Mary) tdy(il(act:be)) pro:who?', 'Mary ndiani?'),],
    'tdy': [('tdy(je(act:walk))', u'ndinofamba'),
            ('tdy(je(act:be))', 'ndiri'),
            ('tdy(elle(act:be))', 'ari'),
            ('tdy(il(act:be))', 'ari')],
    'tmw': [('tmw(je(act:walk))', u'ndichafamba')],
    'ydy': [('ydy(je(act:walk))', u'ndakafamba')],
  },
  'sinhala': {
    'pos_nom': [('pos:my_nom:book', u'මගේ පොත')],
  },
  'soomaali': {
    'adj_nom': [('adj:red_nom:boat', 'doon cas')],
    'det_nom': [('det:a_nom:bird', u'shimbir'),
                ('det:the_nom:bed', 'sariirta')],
    'plural': [('plural(nom:banana)', 'muuska')],
    'pos_nom': [('pos:my_nom:mouth', u'afkayga')],
    #'inf': [('inf(act:walk)', u'')],
    #'tdy': [('tdy(je(act:walk))', u'')],
    #'tmw': [('tmw(je(act:walk))', u'')],
    #'ydy': [('ydy(je(act:walk))', u'')],
  },
  'espanyol': {
    'adj_nom': [('adj:new_nom:book', 'nuevo libro')],
    'det_nom': [('det:the_nom:book', u'el libro')],
    'plural': [('plural(nom:dog)', 'perros')],
    'pos_nom': [('pos:my_nom:book', u'mi libro')],
    'inf': [('inf(act:walk)', u'caminar')],
    'tdy': [('tdy(je(act:walk))', u'camino'), ('tdy(nous(act:walk))', u'caminamos'),
            ('tdy(tu(act:walk))', u'caminas'), ('tdy(vous(act:walk))', u'caminavos'),
            ('tdy(elle(act:walk))', u'camina'), ('tdy(ils(act:walk))', u'caminan'),],
    'tmw': [('tmw(je(act:walk))', u'caminaré')],
    'ydy': [('ydy(je(act:walk))', u'caminé')],
  },
  'swahili': {
    'adj_nom': [('adj:each_nom:book', 'kitabu kila'), ('adj:each_nom:day', 'kila siku')],
    'and': [('raw(A) and raw(B)', 'A na B')],
    'command': [('cmd(tu(act:sit_adv:down))!', 'Kaa chini!'), ('cmd(tu(act:come_adv:here))!', 'Kuja hapa!'),],
    'date': [('date(2015-11-12)', u'Alhamisi. Tarehe 12 Novemba mwaka wa 2015')],
    'det_nom': [('det:the_nom:book', u'kitabu')],
    'inf': [('inf(act:walk)', u'kutembea')],
    'or': [('raw(A) or raw(B)', 'A au B')],
    'plural': [('nom:name', 'jina'),  ('plural(nom:name)', 'majina'),
               ('plural(nom:dog)', 'mbwa'),
               ('nom:book', 'kitabu'), ('plural(nom:book)', 'vitabu'), ('nom:chair', 'kiti'), ('plural(nom:chair)', 'viti'), # ki/vi-plurals
              ],
    'pos_nom': [('pos:my_nom:house', 'nyumba yangu')],
    'question': [('raw(Mary) tdy(f(act:be)) pro:who?', 'Mary ni nani?'),],
    'statement': [('raw(Mary) tdy(f(act:be)) det:a_nom:doctor.', 'Mary ni daktari.'),],
    'subject_verb': [('det:the_nom:man tmw(il(act:walk))', u'mwanaume atatembea')],
    'tdy': [('tdy(je(act:walk))', u'ninatembea'), ('tdy(il(act:be))', 'ni'),
            ('tdy(tu(act:ask))', 'unauliza'), ('tdy(i(act:be))', 'ni')],
    'tmw': [('tmw(je(act:walk))', u'nitatembea')],
    'verb_object': [('tdy(tu(act:follow)) det:the_nom:dog', u'unafuata mbwa'),],
    'ydy': [('ydy(je(act:walk))', u'nilitembea')],
  },
  'swati': {
  },
  'tigrinya': {
    'adj_nom': [('adj:green_nom:book', u'ቀጠልያ መጽሐፍ')],
    'plural': [('plural(nom:animal)', u'እንስሳታት')],
  },
  'ururimi': {
    'adj_nom': [('adj:new_nom:dog', 'imbwa gishya')],
    'det_nom': [('det:the_nom:dog', u'imbwa')],
    'plural': [('plural(nom:word)', 'amajambo')],
    'pos_nom': [('pos:my_nom:book', u'igitabo cyanjye')],
    'inf': [('inf(act:walk)', u'kugenda')],
    'tdy': [('tdy(je(act:eat))', u'ndarya'), ('tdy(nous(act:eat))', 'turarya'),
            ('tdy(tu(act:eat))', 'urarya'), ('tdy(vous(act:eat))', 'murarya'),
            ('tdy(elle(act:eat))', 'ararya'), ('tdy(ils(act:eat))', 'bararya'),
            ('tdy(je(act:be))', 'ni'), ('tdy(tu(act:be))', 'ni'),
            ('tdy(nous(act:be))', 'ni'), ('tdy(i(act:be))', 'ni'),
           ],
    'tmw': [('tmw(je(act:walk))', u'nzagenda')],
    'ydy': [('ydy(je(act:walk))', u'nagiye')],
  },
  'wolof': {
    'adj_nom': [('adj:new_nom:machine', 'masin bu bees')],
    'det_nom': [('det:the_nom:child', u'doom bi')],
    'plural': [('plural(nom:dog)', 'xaj yi')],
    'pos_nom': [('pos:my_nom:book', u'sama téere')],
    'inf': [('inf(act:walk)', u'dox')],
    'tdy': [('tdy(je(act:walk))', u'maa ngi dox')],
    'tmw': [('tmw(je(act:walk))', u'dinaa dox')],
    'ydy': [('ydy(je(act:walk))', u'dox naa')],
  },
  'xhosa': {
    'adj_nom': [('adj:white_nom:dog', 'inja mhlophe')],
    'det_nom': [('det:the_nom:dog', u'inja')],
    'inf': [('inf(act:bark)', u'ukukhonkotha'),
            ('inf(act:speak)', 'ukuthetha')],
    'plural': [('plural(nom:dog)', 'izinja'), ('plural(nom:woman)', 'abafazi')],
    'pos_nom': [('pos:my_nom:dog', u'inja yam')],
    'now_tdy': [('now_tdy(je(act:speak))', u'ndathethile')],
    'tdy': [('tdy(je(act:speak))', u'ndithetha'), ('tdy(nous(act:speak))', u'sithetha'),
            ('tdy(tu(act:speak))', u'uthetha'), ('tdy(vous(act:speak))', u'wethetha'),
            ('tdy(il(act:speak))', u'uthetha'), ('tdy(elles(act:speak))', u'bethetha'),
           ],
    'tmw': [('tmw(je(act:speak))', u'ndizothetha')],
    'ydy': [('ydy(je(act:speak))', u'ndathetha')],
  },
  'yoruba': {
    'adj_nom': [('adj:new_nom:book', 'iwe tuntun')],
    'and': [('raw(A) and raw(B)', 'A ati B')],
    #'command': [('cmd(tu(act:come_adv:here))', '')],
    'det_nom': [('det:the_nom:book', u'iwe naa')],
    'inf': [('inf(act:walk)', u'lati rin'),],
    'or': [('raw(A) or raw(B)', 'A tabi B')],
    'plural': [('plural(nom:dog)', 'aja')],
    'pos_nom': [('pos:my_nom:book', u'mi iwe')],
    #'question': [('raw(Mary) tdy(f(act:be)) pro:who?', 'Mary ni nani?'),],
    #'statement': [('raw(Mary) tdy(f(act:be)) det:a_nom:doctor.', 'Mary ni daktari.'),],
    'tdy': [('tdy(je(act:walk))', u'nrin')],
    'tmw': [('tmw(je(act:walk))', u'maarin')],
    'ydy': [('ydy(je(act:walk))', u'rin lana')],
  },
  'zulu': {
    'adj_nom': [('adj:good_nom:dog', 'inja kahle')],
    'det_nom': [('det:the_nom:dog', u'inja')],
    'plural': [('plural(nom:dog)', 'izinja')],
    'pos_nom': [('pos:my_nom:letter', u'incwadi wami')],
    'inf': [('inf(act:walk)', u'ukuhamba')],
    'tdy': [('tdy(je(act:walk))', 'ngiyahamba'), ('tdy(nous(act:walk))', 'siyahamba'),
            ('tdy(tu(act:walk))', 'uyahamba'), ('tdy(vous(act:walk))', 'niyahamba'),
            ('tdy(elle(act:walk))', 'uyahamba'), ('tdy(il(act:walk))', 'uyahamba'), ('tdy(ils(act:walk))', 'bayahamba'),],
    'tmw': [('tmw(je(act:walk))', 'ngizohamba'), ('tmw(nous(act:walk))', 'sizohamba'),
            ('tmw(tu(act:walk))', 'uzohamba'), ('tmw(vous(act:walk))', 'nizohamba'),
            ('tmw(il(act:walk))', 'uzohamba'), ('tmw(ils(act:walk))', 'bazohamba'),],
    'ydy': [('ydy(je(act:walk))', 'ngihambile'), ('ydy(nous(act:walk))', 'sihambile'),
            ('ydy(tu(act:walk))', 'nihambile'), ('ydy(vous(act:walk))', 'nihambile'),
            ('ydy(il(act:walk))', 'uhambile'), ('ydy(ils(act:walk))', 'bahambile')],
  },
}

class Text2KWL(unittest.TestCase):
  def testData(self):
    self.assertEquals('tdy(je(act:be))', g.text_to_kwl('am'))
    self.assertEquals('plural(nom:child)', g.text_to_kwl('children'))

class KWLTest(unittest.TestCase):
  def setUp(self):
    self.tm = {
    }
    self.longMessage = True
    pass


  def testEnvironment(self):
    self.assertEquals('ak', g.localize('kg:kasa', 'akan'))
    self.assertEquals('akan', g.localize('kg:language', 'akan')),

  def testWords(self):
    # Unrecognized
    self.assertEquals('xbrxbbx',
                      g.localize("nom:xbrxbbx", 'english'))
    self.assertEquals('[xbrxbbx]',
                      g.localize("nom:xbrxbbx", 'akan'))
    self.assertEquals('xbr-xbbx',
                      g.localize("nom:xbr-xbbx", 'english'))


  def testInbuiltFunctionsOfWords(self):
    en_tm = data.load_td('english', 'english', False)
    self.assertEquals(en_tm['dog-noun-defn'],
                      g.localize("defn(nom:dog)", 'english'))  # defn()
    self.assertEquals(en_tm['dog-noun-sample'],
                      g.localize("sample(nom:dog)", 'english'))  # sample()

    ak_tm = data.load_td('english', 'akan', False)
    self.assertEquals(ak_tm['dog-noun-defn'],
                      g.localize("defn(nom:dog)", 'akan'))  # defn()
    self.assertEquals(ak_tm['dog-noun-sample'],
                      g.localize("sample(nom:dog)", 'akan'))  # sample()

  def testJoins(self):
    # and
    self.assertEquals('table and chair',
                      g.localize('nom:table and nom:chair', 'english'))
    self.assertEquals('pon na agua',
                      g.localize('nom:table and nom:chair', 'akan'))

    # colon
    self.assertEquals('good child: good food',
                      g.localize('adj:good_nom:child : adj:good_nom:food', 'english'))
    self.assertEquals(u'me se: wo se',
                      g.localize('pro:I act:say: pro:you act:say', 'akan'))

    # comma
    self.assertEquals('good child, good food',
                      g.localize('adj:good_nom:child, adj:good_nom:food', 'english'))

    # or
    self.assertEquals('table or chair',
                      g.localize('nom:table or nom:chair', 'english'))
    self.assertEquals('pon anaa agua',
                      g.localize('nom:table or nom:chair', 'akan'))

    # of
    self.assertEquals('child of god',
                      g.localize('nom:child of nom:god', 'english'))
    self.assertEquals('nyame ne ba',
                      g.localize('nom:child of nom:god', 'akan'))

    # if-then
    self.assertEquals('if good child then good food',
                      g.localize('if adj:good_nom:child then adj:good_nom:food', 'english'))

    # so
    self.assertEquals('good child so good food',
                      g.localize('adj:good_nom:child so adj:good_nom:food', 'english'))

  def testPhrases(self):
    # Noun-Noun
    self.assertEquals('car park',
                      g.localize('nom:car_nom:park', 'english'))
    self.assertEquals('kaar [park]',
                      g.localize('nom:car_nom:park', 'akan'))
    self.assertEquals('[park] ya motuka',
                      g.localize('nom:car_nom:park', 'lingala'))

    # Prep-Noun
    self.assertEquals('from Africa',
                      g.localize('pre:from_nom:Africa', 'english'))
    self.assertEquals('firi abibiman',
                      g.localize('pre:from_nom:Africa', 'akan'))

    # Det(Noun-Adjective)
    self.assertEquals('the black table',
                      g.localize('det:the(adj:black_nom:table)', 'english'))
    self.assertEquals('pon tuntum no',
                      g.localize('det:the(adj:black_nom:table)', 'akan'))

    # Pronoun-Noun
    self.assertEquals('my table',
                      g.localize('pos:my_nom:table', 'english'))
    self.assertEquals('me pon',
                      g.localize('pos:my_nom:table', 'akan'))

    # Adv-Verb
    self.assertEquals('live today',
                      g.localize('act:live_adv:today', 'english'))
    self.assertEquals(u'te ndɛ',
                      g.localize('act:live_adv:today', 'akan'))

  def testVerbConjugationJE(self):
    self.assertEquals('I will eat',
                      g.localize('pro:I tmw(je(act:eat))', 'english'))
    self.assertEquals('I ate',  # with substitutions in place
                      g.localize('pro:I ydy(je(act:eat))', 'english'))
    self.assertEquals('je mange',
                      g.localize('pro:I tdy(je(act:eat))', 'french'))

  def testVerbConjugationTU(self):
    self.assertEquals('wo di',
                      g.localize('pro:you tdy(tu(act:eat))', 'akan'))
    self.assertEquals('you eat',
                      g.localize('pro:you tdy(tu(act:eat))', 'english'))
    self.assertEquals('tu manges',
                      g.localize('pro:you tdy(tu(act:eat))', 'french'))
    self.assertEquals('olya',
                      g.localize('tdy(tu(act:eat))', 'luganda'))
    self.assertEquals('rafaa jirtaa',
                      g.localize('tdy(tu(act:sleep))', 'oromoo'))
    self.assertEquals('rafee',
                      g.localize('ydy(tu(act:sleep))', 'oromoo'))
    self.assertEquals('ni rafttaa',
                      g.localize('tmw(tu(act:sleep))', 'oromoo'))
    self.assertEquals('uliuliza',
                      g.localize('ydy(tu(act:ask))', 'swahili'))
    self.assertEquals('utauliza',
                      g.localize('tmw(tu(act:ask))', 'swahili'))


  def testVerbConjugationIL(self):
    self.assertEquals(u'ɔ di',
                      g.localize('pro:he tdy(il(act:eat))', 'akan'))
    self.assertEquals('he eats',
                      g.localize('pro:he tdy(il(act:eat))', 'english'))
    self.assertEquals('elle mange',
                      g.localize('pro:she tdy(elle(act:eat))', 'french'))
    self.assertEquals('il mange',
                      g.localize('pro:he tdy(il(act:eat))', 'french'))
    self.assertEquals('alya',
                      g.localize('tdy(il(act:eat))', 'luganda'))
    self.assertEquals('alei',  # 'alii' becomes 'alei' after substitution
                      g.localize('tdy(il(act:eat))', 'lingala'))
    self.assertEquals('atunaki',
                      g.localize('ydy(il(act:ask))', 'lingala'))
    self.assertEquals('akolia',
                      g.localize('tmw(il(act:eat))', 'lingala'))
    self.assertEquals('rafaa jiraa',
                      g.localize('tdy(il(act:sleep))', 'oromoo'))
    self.assertEquals('rafee',
                      g.localize('ydy(il(act:sleep))', 'oromoo'))
    self.assertEquals('ni rafaa',
                      g.localize('tmw(il(act:sleep))', 'oromoo'))
    self.assertEquals('rafaa jirtii',
                      g.localize('tdy(elle(act:sleep))', 'oromoo'))
    self.assertEquals('rafee',
                      g.localize('ydy(elle(act:sleep))', 'oromoo'))
    self.assertEquals('ni raftii',
                      g.localize('tmw(elle(act:sleep))', 'oromoo'))
    self.assertEquals('anauliza',
                      g.localize('tdy(il(act:ask))', 'swahili'))
    self.assertEquals('aliuliza',
                      g.localize('ydy(il(act:ask))', 'swahili'))
    self.assertEquals('atauliza',
                      g.localize('tmw(il(act:ask))', 'swahili'))



  def testVerbConjugationILS(self):
    self.assertEquals('ils mangent',
                      g.localize('pro:they tdy(ils(act:eat))', 'french'))
    self.assertEquals('balya',
                      g.localize('tdy(ils(act:eat))', 'luganda'))

  def testSentences(self):
    self.assertEquals('I love food',
                      g.localize('pro:I act:love nom:food', 'english'))
    self.assertEquals(u'me dɔ aduane',
                      g.localize('pro:I act:love nom:food', 'akan'))

    self.assertEquals('I know you',
                      g.localize('pro:I act:know pro:you', 'english'))
    self.assertEquals(u'me nyim wo',
                      g.localize('pro:I act:know pro:you', 'akan'))

    self.assertEquals('Africa Be Continent',
                      g.localize('headline(nom:Africa act:be nom:continent)', 'english'))
    self.assertEquals(u'Abibiman yɛ asaasetaw.',
                      g.localize('nom:Africa act:be nom:continent.', 'akan'))

    self.assertEquals('Billion people live there.',
                      g.localize('adj:billion_nom:people act:live nom:there.', 'english'))

    self.assertEquals('4323 football pitches',
                      g.localize('plural(adj:4323(nom:football_nom:pitch))', 'english'))
    self.assertEquals(u'bɔɔlbɔ [pitch] 4323',
                      g.localize('plural(adj:4323(nom:football_nom:pitch))', 'akan'))


def create_function(test, l, tt, lexicon):
  def do_expected(self):
    self.assertEquals(test[1], g.localize(test[0], l, lexicon), '%s %s' % (tt, test))
  return do_expected

language = sys.argv[1] if len(sys.argv) > 1 else None
if language in DATA_TESTS:
  DATA_TESTS = {language: DATA_TESTS[language]}

for l in DATA_TESTS:
  lexicon = data.load_td('english', l, False)
  for tt in DATA_TESTS[l]:
    for k, test in enumerate(DATA_TESTS[l][tt]):
      test_method = create_function(test, l, tt, lexicon)
      test_method.__name__ = 'test_kwl_%s_%s_%s' % (l, tt, k)
      setattr (KWLTest, test_method.__name__, test_method)


PRONUNCIATION_TESTS = {
  'amaarignaa': {
    'latinization': [(u'አማርኛ', u'amaarignaa')],
  },
  'geez': {
    'alphabet': [(x[1], x[0]) for x in p.GEEZ],
  },
  'sinhala': {
    'latinization': [(u'මම', u'mama')],
  },
  'tigirignaa': {
    'latinization': [(u'ትግርኛ', u'tigirignaa'), (u'ሦማሊ', u'somaali')],
  },
  'kirundi': {
    'kirundi': [('cyane', 'cane'), ('jya', 'ja'), ('shyira', 'shira'), ('bye', 'vye')],
  },
  'kinyarwanda': {
    'kinyarwanda': [('cyane', 'cyane'), ('jya', 'jya'), ('shyira', 'shyira'), ('bye', 'bye')],
  },
  'yoruba': {
    'diacritics': [('muh', u'mú'),],
  }
}

def create_pronunciation(test, l, tt):
  def do_expected(self):
    self.assertEquals(test[1], p.get_phonetic(test[0], l), '%s %s' % (tt, test))
  return do_expected

class PronounceTest(unittest.TestCase):
  def setUp(self):
    self.longMessage = True

  def testGeezTokenizer(self):
    self.assertEquals(['so', 'maa', 'li'], p.tokenize_geez('somaali'))
    self.assertEquals(['a', 'maa', 'ri', 'gnaa'], p.tokenize_geez('amaarignaa'))


if language in PRONUNCIATION_TESTS:
  PRONUNCIATION_TESTS = {language: PRONUNCIATION_TESTS[language]}

for l in PRONUNCIATION_TESTS:
  for tt in PRONUNCIATION_TESTS[l]:
    for k, test in enumerate(PRONUNCIATION_TESTS[l][tt]):
      test_method = create_pronunciation(test, l, tt)
      test_method.__name__ = 'test_pronunciation_%s_%s_%s' % (l, tt, k)
      setattr (PronounceTest, test_method.__name__, test_method)


class VoiceTest(unittest.TestCase):
  def testVoice(self):
    self.assertEquals(u'Tukwaagala Kofi.',
                      g.localize('pro:we tdy(nous(act:love)) raw(Kofi).',
                                 'luganda', {}, 'kintu')) # Test voices


if __name__ == '__main__':
  if not language:
    unittest.main()
  else:
    runner = unittest.TextTestRunner()
    suite = unittest.TestLoader().loadTestsFromTestCase(KWLTest)
    suite2 = unittest.TestLoader().loadTestsFromTestCase(PronounceTest)
    runner.run(suite)
    runner.run(suite2)
