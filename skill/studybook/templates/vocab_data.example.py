# -*- coding: utf-8 -*-
# Topic vocabulary for the summer-speech studio. Grouped by the five themes.
# Each entry: (korean, english). Dictionary forms; audio pronounces them.
# clip id = 'v%d' in flattened order.

VOCAB = [
 ('날씨 · Weather', [
   ('여름', 'summer'),
   ('날씨', 'weather'),
   ('덥다', 'to be hot'),
   ('습하다', 'to be humid'),
   ('건조하다', 'to be dry'),
   ('바람', 'wind'),
   ('장마', 'the rainy season'),
   ('온도', 'temperature'),
   ('에어컨', 'air conditioner'),
   ('선풍기', 'electric fan'),
   ('시원하다', 'to be cool'),
   ('춥다', 'to be cold'),
 ]),
 ('옷 · Clothes', [
   ('옷', 'clothes'),
   ('반바지', 'shorts'),
   ('긴팔', 'long sleeves'),
   ('긴바지', 'long pants'),
   ('유니폼', 'uniform'),
   ('출근하다', 'to go to work'),
   ('햇빛', 'sunlight'),
   ('편하다', 'to be comfortable'),
 ]),
 ('음식 · Food', [
   ('음식', 'food'),
   ('국물', 'broth, soup'),
   ('국수', 'noodles'),
   ('냉면', 'cold noodles'),
   ('삼계탕', 'ginseng chicken soup'),
   ('뜨겁다', 'to be hot (to the touch)'),
   ('채소', 'vegetables'),
   ('고기', 'meat'),
   ('끓이다', 'to boil'),
   ('계절', 'season'),
   ('맛', 'taste, flavor'),
 ]),
 ('더위 피하기 · Escaping the heat', [
   ('더위', 'the heat'),
   ('피하다', 'to avoid, escape'),
   ('수영장', 'swimming pool'),
   ('강', 'river'),
   ('공원', 'park'),
   ('캠핑', 'camping'),
   ('산', 'mountain'),
   ('나무', 'tree'),
   ('친구', 'friend'),
 ]),
 ('발표 · Talking about it', [
   ('발표', 'presentation'),
   ('소개하다', 'to introduce'),
   ('차이', 'difference'),
   ('다르다', 'to be different'),
   ('비슷하다', 'to be similar'),
   ('익숙하다', 'to be used to'),
   ('영향', 'effect, influence'),
   ('건강', 'health'),
   ('생활', 'daily life'),
   ('기억하다', 'to remember'),
 ]),
 ('하늘 · Sky', [
   ('하늘', 'sky'),
   ('구름', 'cloud'),
   ('해', 'the sun'),
   ('맑다', 'to be clear, sunny'),
   ('흐리다', 'to be cloudy, overcast'),
   ('그늘', 'shade'),
   ('소나기', 'a sudden shower'),
 ]),
 ('여름 물건 · Summer things', [
   ('손선풍기', 'a handheld (mini) fan'),
   ('양산', 'a parasol (sun umbrella)'),
   ('우산', 'an umbrella'),
   ('선크림', 'sunscreen'),
   ('모자', 'a hat, cap'),
   ('선글라스', 'sunglasses'),
   ('헬멧', 'a helmet'),
   ('물병', 'a water bottle'),
 ]),
 ('비교 · Comparing', [
   ('비교하다', 'to compare'),
   ('차이점', 'a difference (point)'),
   ('공통점', 'a common point'),
   ('같다', 'to be the same'),
   ('처럼', 'like, as (attached: 나처럼)'),
   ('더', 'more'),
   ('덜', 'less'),
   ('둘 다', 'both'),
   ('반면에', 'on the other hand'),
 ]),
 ('느낌 · Feelings & body', [
   ('졸리다', 'to be sleepy'),
   ('피곤하다', 'to be tired'),
   ('답답하다', 'to feel stuffy, frustrated'),
   ('상쾌하다', 'to feel refreshed'),
   ('불편하다', 'to be uncomfortable'),
   ('땀', 'sweat'),
   ('목마르다', 'to be thirsty'),
   ('지치다', 'to be worn out'),
 ]),
 ('동사 · Useful verbs', [
   ('입다', 'to wear (clothes)'),
   ('쓰다', 'to wear / use (hat, umbrella)'),
   ('벗다', 'to take off'),
   ('켜다', 'to turn on'),
   ('끄다', 'to turn off'),
   ('쉬다', 'to rest'),
   ('사용하다', 'to use'),
 ]),
]

def clips():
    out = []; j = 0
    for _title, items in VOCAB:
        for (ko, en) in items:
            out.append(('v%d' % j, ko)); j += 1
    return out
