"""v2 reels: story scenes (mascot dialogue in a classroom) and 3D camera.
Overwrites specs/RL-03, 05, 06, 09, 12, 14 (run after specs_gen.py)."""
import json, pathlib
S = pathlib.Path(__file__).parent / 'specs'
END = lambda words=None, **kw: dict(type='end', d=4.4, words=words or [], **kw)
M = lambda who, ex, x=390, y=1200, w=300, t=.2, **kw: dict(who=who, ex=ex, x=x, y=y, w=w, t=t, **kw)
trio = lambda y=1150, t=.2: [M('dars', [[0, 'happy']], 130, y + 30, 270, t, jump=[t + .6]), M('ustaz', [[0, 'proud']], 400, y, 300, t + .1),
                             M('dara', [[0, 'happy']], 690, y + 30, 270, t + .2, ph=2, jump=[t + .9])]
R = {}

# RL-03 — story: "When do we get our essays back?"
R['RL-03'] = dict(title='AI marks. You approve.', family='blue', bpm=112, key=5, mood='warm', seed=33, cover=6.2, scenes=[
  dict(type='story', d=12.8, open='class', boardtitle='Essays · Group A', lines=[
    dict(who='dars', t=.5, text='Sir, when do we get our essays back?', ex='thinking'),
    dict(who='ustaz', t=2.9, text='Tonight.', ex='proud', react={'dars': 'surprised'}),
    dict(who='dara', t=4.1, text='All 30 of them?!', ex='surprised'),
    dict(who='ustaz', t=5.7, text='Darsify marks them against my rubric.', ex='happy', shot='boardwide', react={'dara': 'thinking'}),
    dict(who='ustaz', t=8.7, text='Then I check and approve.', ex='focus', shot='boardwide'),
    dict(who='dars', t=10.9, text='That fast?!', ex='celebrate', shot='students', react={'dara': 'celebrate'}),
  ], board=[
    dict(t=6.2, panel=dict(crumb='Marking  /  Essay', title='Omar K. · Question 2', blocks=[
      dict(bar=dict(l='Clear position', w=67, v='2 / 3', at=6.8)), dict(bar=dict(l='Evidence', w=75, v='3 / 4', at=7.1)),
      dict(bar=dict(l='Organisation', w=67, v='2 / 3', at=7.4)), dict(row=dict(l='AI suggests', chip='info', ctext='7 / 10')),
      dict(btn=dict(label='Approve 7/10', at=9.9, toast='Sent with feedback'))]), x=20, y=75, scale=.66),
  ], cast={'dars': dict(jump=[11.2])}),
  dict(type='hook', d=3.0, tin='whip', head=['AI suggests.', '*You approve.*'], size=150, y=460, sub='Nothing reaches a student until you say so.', subt=1.0, suby=820,
       mascots=[M('ustaz', [[0, 'proud']], 390, 1150, 320, .3)]),
  END(['Essays', 'Rubrics', 'Feedback', 'Grades', 'Approve', 'Send'])])

# RL-05 — story: roll call, then a 3D ring of character cards
R['RL-05'] = dict(title='Meet the Darsify crew', family='ink', bpm=110, key=0, mood='chill', seed=55, cover=3.4, scenes=[
  dict(type='story', d=11.8, open='class', boardtitle='Roll call', lines=[
    dict(who='ustaz', t=.4, text='Good evening, class. Roll call!', ex='happy'),
    dict(who='dars', t=2.6, text='Dars, here! I celebrate every finished mock.', ex='celebrate'),
    dict(who='dara', t=5.3, text='Dara! My reading streak is 41 days.', ex='proud', react={'dars': 'surprised'}),
    dict(who='ustaz', t=8.0, text="And I'm Ustaz. I send the reminders.", ex='proud'),
    dict(who='dara', t=10.0, text='So nobody forgets!', ex='celebrate', shot='students', react={'dars': 'celebrate'}),
  ], board=[dict(t=3.1, write='Dars  ·  here', y=110), dict(t=5.8, write='Dara  ·  here', y=200), dict(t=8.5, write='Ustaz  ·  teacher', y=290, c='#ff9a6e')],
     cast={'dars': dict(jump=[2.9, 10.3]), 'dara': dict(jump=[10.2])}),
  dict(type='ring', d=5.8, tin='dolly', head=['Meet the', '*Darsify crew.*'], size=110, y=270, ry=760, r=420, steps=[[0, 0], [1.7, 1], [3.4, 2]], drift=5, tiles=[
    dict(title='Ustaz', desc='The tutor. Announcements, feedback and reminders.', mascot='ustaz-proud', bg='#2655a3'),
    dict(title='Dars', desc='The study buddy. Celebrates every finished mock.', mascot='dars-celebrate', bg='#12305c'),
    dict(title='Dara', desc='Keeps the streak alive with daily reading and vocab.', mascot='dara-happy', bg='#e0567f')]),
  END(['Ustaz', 'Dars', 'Dara', 'Streaks', 'Reviews', 'Reminders'])])

# RL-06 — story into a 3D fly-through of the exam screen
R['RL-06'] = dict(title='The real exam, before the real exam', family='blue', bpm=124, key=-3, mood='drive', seed=66, cover=8.6, scenes=[
  dict(type='story', d=6.2, open='class', boardtitle='Mock 3', lines=[
    dict(who='dara', t=.4, text='Sir, is the real SAT this hard?', ex='concerned'),
    dict(who='ustaz', t=2.5, text="Let's find out. Mock 3, timed.", ex='focus', shot='boardwide'),
    dict(who='dars', t=4.7, text='Now?!', ex='surprised', react={'dara': 'surprised'}),
  ], board=[dict(t=3.0, write='SAT MATH  ·  35 MIN', y=120, size=46), dict(t=3.7, write='Mock 3', y=200, size=90, c='#ff9a6e')]),
  dict(type='exam', d=6.4, tin='dolly', tabs=['SAT', 'EST', 'ACT', 'IGCSE', 'Thanwya'], on=0, ey=640, section='Math', qn='12 of 22',
       q='The function f is defined by f(x) = 3x² − 12x + 7. For what value of x does f reach its minimum?', choices=['−2', '0', '2', '4'],
       pick=2, pick_at=3.0, next_at=3.8, c0=.2, c1=6.2, tfrom=1908, tto=1902, head=['Timed. Real format.'], size=96, y=280,
       cam=[[0, 540, 1000, .8, -24, 16, .01], [.15, 540, 980, 1, 0, 0, 1.4], [1.9, 470, 1080, 1.3, 7, 4, .8], [3.9, 760, 700, 1.45, -6, 2, .6], [5.0, 540, 960, 1, 0, 0, .8]]),
  dict(type='chips', d=3.6, tin='whip', head=['Same timer.', 'Same tools.', '*Same pressure.*'], size=120, y=300, drift=6, chips=[
       dict(text='Mark for review', x=90, y=860, t=.6), dict(text='Answer eliminator', x=420, y=990, t=.85), dict(text='Question navigator', x=110, y=1120, t=1.1),
       dict(text='Countdown timer', x=470, y=1250, t=1.35), dict(text='Auto-graded', x=200, y=1380, t=1.6, bg='#f26229')]),
  dict(type='hook', d=2.8, tin='flip', head=['So exam day', '*feels familiar.*'], size=140, y=440, sub='Authentic mocks for SAT, EST, ACT, IGCSE and Thanwya Amma.', subt=.9, suby=760,
       mascots=[M('dara', [[0, 'celebrate']], 400, 1160, 300, .2, jump=[.8])]),
  END(['SAT', 'EST', 'ACT', 'IGCSE', 'Thanwya Amma', 'Mocks'])])

# RL-09 — quiz hook, then the answer as a classroom story
R['RL-09'] = dict(title='Guess the weak topic', family='orange', bpm=116, key=9, mood='drive', seed=99, cover=7.6, scenes=[
  dict(type='hook', d=2.6, kicker='Quiz time', head=['Guess the', '*weak topic.*'], size=160, y=420, sub='Comment your guess before the end.', subt=1.0, suby=760,
       mascots=[M('dara', [[0, 'thinking']], 400, 1180, 300, .4)], cam=[[0, 540, 960, 1, 0, 0, .01], [0, 540, 900, 1.1, 0, 0, 2.6]]),
  dict(type='story', d=11.6, tin='whip', open='class', boardtitle='Dara · last 4 mocks', lines=[
    dict(who='dara', t=.3, text='Sir, why do I keep losing marks?', ex='sulk'),
    dict(who='ustaz', t=2.5, text="Let's ask your last 4 mocks.", ex='thinking', shot='boardwide'),
    dict(who='dars', t=6.4, text="It's linear equations!", ex='surprised', react={'dara': 'surprised'}),
    dict(who='ustaz', t=8.3, text='Practice on it is already in your portal.', ex='proud'),
    dict(who='dara', t=10.3, text="Let's go!", ex='celebrate', react={'dars': 'happy'}),
  ], board=[
    dict(t=3.0, panel=dict(crumb='Insights  /  Weak points', title='Correct answers per topic', blocks=[
      dict(bar=dict(l='Data analysis', w=88, v='88%', at=3.5)), dict(bar=dict(l='Geometry', w=72, v='72%', at=3.8)),
      dict(bar=dict(l='Ratios', w=63, v='63%', at=4.1)), dict(bar=dict(l='Linear equations', w=41, v='41%', at=4.4, c='#f26229'))]), x=20, y=75, scale=.66),
    dict(t=5.6, stamp='Weak topic', x=170, y=465, size=46)], cast={'dara': dict(jump=[10.6])}),
  dict(type='hook', d=2.8, tin='whip', head=['Darsify finds it', '*after every mock.*'], size=120, y=440, sub='Then sends practice on exactly that topic.', subt=.9, suby=760,
       mascots=[M('ustaz', [[0, 'proud']], 400, 1160, 300, .2)]),
  END(['Ratios', 'Geometry', 'Algebra', 'Data', 'Practice', 'Mocks'])])

# RL-12 — 3D flip card + tilted review screen
R['RL-12'] = dict(title='Mistakes come back as practice', family='blue', bpm=112, key=7, mood='chill', seed=121, cover=4.9, scenes=[
  dict(type='hook', d=2.6, kicker='Truth', head=['Students forget', '*their mistakes.*'], size=130, y=420,
       mascots=[M('dara', [[0, 'wrong']], 400, 1180, 300, .4)], cam=[[0, 540, 960, 1, 0, 0, .01], [0, 540, 900, 1.12, -3, 0, 2.6]]),
  dict(type='flip', d=5.4, tin='dolly', head=["Darsify doesn't."], size=120, y=280, fy=560, at=2.0, drift=6,
       front=dict(kicker='Mock 3 · Question 14', title='Wrong answer', rows=['Marked wrong', 'Forgotten by Friday', 'Wrong again in the exam']),
       back=dict(kicker='With Darsify', title='Comes back as practice', rows=['Review on day 3', 'Again on day 7', 'Locked in by day 14']),
       mascots=[M('dara', [[0, 'concerned'], [2.4, 'happy']], 740, 1440, 230, .3)]),
  dict(type='ui', d=4.8, tin='whip', head=["Today's review"], size=100, y=280, py=520,
       cam=[[0, 540, 1050, .9, 20, -8, .01], [.1, 540, 960, 1, 0, 0, 1.1], [2.6, 540, 900, 1.1, -4, 2, 1.6]],
       panel=dict(crumb='Practice  /  Review', title='Due today', sub='From your last 3 mocks', blocks=[
         dict(row=dict(l='3x − 7 = 2x + 5', chip='pend', ctext='Due', to='paid', totext='Got it', at=1.2)),
         dict(row=dict(l="Meaning of 'mitigate'", chip='pend', ctext='Due', to='paid', totext='Got it', at=2.0)),
         dict(row=dict(l='Area of a sector', chip='pend', ctext='Due', to='bad', totext='Again in 2 days', at=2.8))]),
       mascots=[M('dara', [[0, 'focus'], [3.0, 'proud']], 740, 1430, 230, .3)]),
  dict(type='hook', d=2.6, tin='flip', head=['Mistakes', 'become *practice.*'], size=150, y=460, sub='Automatically, for every student.', subt=.9, suby=780, mascots=trio()),
  END(['Mistakes', 'Reviews', 'Practice', 'Streaks', 'Mocks', 'Progress'])])

# RL-14 — 3D carousel of the three products
R['RL-14'] = dict(title='One engine. Three ways to use it.', family='ink', bpm=118, key=0, mood='bright', seed=141, cover=4.6, scenes=[
  dict(type='hook', d=2.8, head=['One engine.', '*Three ways*', 'to use it.'], size=150, y=420, mascots=trio(1150, .5),
       cam=[[0, 540, 960, 1, 0, 0, .01], [0, 540, 920, 1.08, 2, 0, 2.8]]),
  dict(type='ring', d=6.2, tin='dolly', head=['Darsify is', 'built for'], size=110, y=270, ry=760, r=420, steps=[[0, 0], [2.0, 1], [3.9, 2]], drift=5, tiles=[
    dict(title='Tutors', desc='Mocks, marking, payments and parent reports.', icon='person', c='#f26229'),
    dict(title='Academies', desc='All your tutors and students, online and on-ground.', icon='building', c='#2655a3'),
    dict(title='Schools & universities', desc='From the canteen to the exams, one ecosystem.', icon='school', c='#f26229')]),
  dict(type='hook', d=2.8, tin='whip', head=['All powered by', '*AI + automation.*'], size=125, y=440, sub='Less paperwork. More teaching.', subt=.9, suby=740, mascots=trio()),
  END(['Tutors', 'Academies', 'Schools', 'Universities', 'AI', 'Automation'])])

for k, v in R.items():
    old = json.loads((S / f'{k}.json').read_text())
    v['id'] = k; v['caption'] = v.get('caption', old.get('caption'))
    (S / f'{k}.json').write_text(json.dumps(v, ensure_ascii=False, indent=1)); print(k, round(sum(s['d'] for s in v['scenes']), 1))
