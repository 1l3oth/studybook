# -*- coding: utf-8 -*-
# Shared Q&A data for the study page builder and the TTS audio generator.
# Answer audio ids: traps t0.. , deep d0..    Question audio ids: qt0.. , qd0..
# TRAPS item: (q_ko, q_en, a_ko, why)
# DEEP item:  (q_ko, q_en, a_ko, a_en, confirm)

TRAPS = [
 ('한국 여름 음식이 뭔데요?', 'So what is Korean summer food?',
  '한국에서는 여름에 냉면이나 삼계탕을 많이 먹습니다. 삼계탕은 닭과 인삼을 넣고 끓인 국물 음식인데, 여름에 더위를 이기려고 먹습니다.',
  'The script says Korea has summer food but never names one. Name 냉면 / 삼계탕.'),
 ('습한데 왜 피부가 건조해요?', 'It is humid, so why does your skin get dry?',
  '보통은 습하지만, 실내에서 에어컨을 오래 켜면 공기가 건조해져서 피부도 건조해집니다.',
  'The windless-day dry-air claim is weak. Reframe as AC + personal experience, do not defend it as fact.'),
 ('건강에 미치는 영향은요?', 'And the effect on health?',
  '더우면 잠을 잘 못 자고, 공기가 건조하면 피부가 나빠집니다. 그래서 물을 많이 마시고 로션을 바릅니다.',
  'Your opening promises 건강 (health). Be ready to pay it off.'),
]

DEEP = [
 ('옷 · Clothes', [
   ('다라봇 씨 회사에서도 반바지를 입습니까?', 'Does your company also allow shorts?', '네, 저희 회사도 날씨가 더울 때는 반바지를 입을 수 있습니다.', 'Yes, my company also lets us wear shorts when it is hot.', True),
   ('한국 여자들도 반바지를 입고 출근합니까?', 'Do Korean women also wear shorts to work?', '여자들은 반바지보다 시원한 치마나 원피스를 더 많이 입는 것 같습니다.', 'Women seem to wear cool skirts or dresses more than shorts.', False),
   ('캄보디아 사람들은 왜 더위보다 햇빛을 싫어합니까?', 'Why do Cambodians dislike the sun more than the heat?', '피부가 타는 것을 싫어해서, 그늘을 찾고 긴팔을 입습니다.', 'They dislike getting tanned, so they seek shade and wear long sleeves.', False),
 ]),
 ('날씨 · Weather', [
   ('한국의 장마를 압니까?', 'Do you know Korea’s rainy season (jangma)?', '네, 여름에 비가 많이 오는 장마가 있는데, 그때는 아주 습합니다.', 'Yes, there is a rainy season with heavy rain, and it is very humid then.', False),
   ('어떤 로션을 사용합니까?', 'What lotion do you use?', '특별한 것은 아니고, 평범한 수분 로션을 사용합니다.', 'Nothing special, just an ordinary moisturizing lotion.', False),
   ('밤에 너무 더울 때는 어떻게 합니까?', 'What do you do when it is too hot at night?', '에어컨이나 선풍기를 켜고 시원하게 하고 잡니다.', 'I turn on the AC or a fan to cool down, then sleep.', True),
   ('몇 도를 제일 좋아합니까?', 'What temperature do you like most?', '저는 25도나 26도가 제일 편합니다.', 'I am most comfortable at 25 or 26 degrees.', True),
 ]),
 ('음식 · Food', [
   ('한국에는 여름에 어떤 음식을 먹습니까?', 'What food do people eat in summer in Korea?', '냉면이나 삼계탕을 많이 먹습니다. 저도 냉면을 좋아합니다.', 'People eat naengmyeon or samgyetang a lot. I like naengmyeon too.', True),
   ('삼계탕이 무엇입니까?', 'What is samgyetang?', '닭과 인삼을 넣고 끓인 국물 음식인데, 여름에 힘을 내려고 먹습니다.', 'A soup boiled with chicken and ginseng, eaten in summer for energy.', False),
   ('꾸이띠아우는 어떤 맛입니까?', 'What does Kuy Teav taste like?', '국물이 시원하고 깔끔한 맛입니다.', 'The broth has a clean, refreshing taste.', False),
   ('스팅은 건강에 괜찮습니까?', 'Is Sting okay for your health?', '매일 마시지만 하루에 한 캔만 마셔서 괜찮다고 생각합니다.', 'I drink it daily but only one can a day, so I think it is fine.', True),
 ]),
 ('더위 피하기 · Escaping the heat', [
   ('한강 수영장에 자주 갑니까?', 'Do you go to the Han River pool often?', '여름에 친구들과 가끔 갑니다.', 'I go sometimes with friends in summer.', False),
   ('끼리롬까지 어떻게 갑니까?', 'How do you get to Kirirom?', '프놈펜에서 차로 두세 시간쯤 걸립니다.', 'It takes about two or three hours by car from Phnom Penh.', False),
   ('캠핑을 좋아합니까?', 'Do you like camping?', '네, 친구들과 자연에서 쉬는 것을 좋아합니다.', 'Yes, I like relaxing in nature with friends.', False),
 ]),
 ('전체 내용 · About the talk', [
   ('두 나라 여름의 가장 큰 차이는 무엇입니까?', 'What is the biggest difference between the two summers?', '캄보디아는 일 년 내내 덥지만, 한국은 여름에만 덥고 습합니다.', 'Cambodia is hot all year, but Korea is hot and humid only in summer.', False),
   ('한국에 와서 여름 습관이 바뀌었습니까?', 'Have your summer habits changed since coming to Korea?', '네, 이제는 로션도 바르고, 더위를 피하는 방법도 배웠습니다.', 'Yes, now I use lotion and have learned ways to escape the heat.', False),
   ('캄보디아 여름이 그립습니까?', 'Do you miss Cambodian summer?', '친구들과 끼리롬에 캠핑 가던 것이 그립습니다.', 'I miss going camping at Kirirom with friends.', False),
 ]),
]

def answer_clips():
    out = [('t%d' % i, a) for i, (q, qen, a, w) in enumerate(TRAPS)]
    j = 0
    for _t, items in DEEP:
        for (q, qen, a, aen, c) in items:
            out.append(('d%d' % j, a)); j += 1
    return out

def question_clips():
    out = [('qt%d' % i, q) for i, (q, qen, a, w) in enumerate(TRAPS)]
    j = 0
    for _t, items in DEEP:
        for (q, qen, a, aen, c) in items:
            out.append(('qd%d' % j, q)); j += 1
    return out
