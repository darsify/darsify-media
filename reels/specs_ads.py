"""Arabic explainer ads (Meta campaigns): AD-T1 tutors, AD-S1 schools.
Every claim is checked against claude/darsify-product-features.md and claude/darsify-for-schools.md.
Schools ad shows only what is live today (no fees, transport or timetable modules).
Platform screens stay in English (the platform is not in Arabic yet); narration is Egyptian Arabic.
Slogan stays English. CTA always darsify.net."""
import json, pathlib
S = pathlib.Path(__file__).parent / 'specs'
END = lambda words=None, **kw: dict(type='end', d=4.4, words=words or [], **kw)
M = lambda who, ex, x=390, y=1200, w=300, t=.2, **kw: dict(who=who, ex=ex, x=x, y=y, w=w, t=t, **kw)
trio = lambda y=1150, t=.2: [M('dars', [[0, 'happy']], 130, y + 30, 270, t, jump=[t + .6]), M('ustaz', [[0, 'proud']], 400, y, 300, t + .1),
                             M('dara', [[0, 'happy']], 690, y + 30, 270, t + .2, ph=2, jump=[t + .9])]
TILT = [[0, 540, 960, .9, -14, 8, .01], [.1, 540, 960, 1, 0, 0, 1.2], [3.4, 540, 1020, 1.08, 4, 2, 1.6]]
R = {}

# ------------------------------------------------------------------ tutors
R['AD-T1'] = dict(title='Darsify للمدرسين: من كل الزوايا', lang='ar', family='orange', bpm=116, key=2, mood='warm', seed=901, cover=15.0, scenes=[
  dict(type='story', d=10.4, open='class', boardtitle='Darsify', lines=[
    dict(who='dars', t=.4, text='مستر، إنت إزاي بتلحق كل ده؟', ex='thinking'),
    dict(who='ustaz', t=2.9, text='Darsify بيعمل نص الشغل عني.', ex='proud', react={'dars': 'surprised'}),
    dict(who='dara', t=5.4, text='طب وإحنا؟ وأهالينا؟', ex='surprised'),
    dict(who='ustaz', t=7.5, text='كلكم معانا. تعالوا أوريكم.', ex='happy', shot='boardwide'),
  ], board=[dict(t=7.9, write='المدرس · الطالب · ولي الأمر', y=150, size=42, c='#ff9a6e')], cast={'dara': dict(jump=[5.6])}),

  # 1 · the tutor
  dict(type='hook', d=2.4, tin='whip', family='blue', kicker='١ · من ناحية المدرس', head=['حصتك', '*بتمشي لوحدها.*'], size=140, y=440,
       mascots=[M('ustaz', [[0, 'proud']], 390, 1150, 320, .3)]),
  dict(type='ui', d=6.2, tin='dolly', family='blue', head=['حدد الميعاد', '*والباقي علينا.*'], size=96, y=250, py=500, cam=TILT,
       panel=dict(crumb='Sessions  /  Sunday 7:00 PM', title='SAT · Group A', sub='Students pay by card, wallet, InstaPay or Fawry', blocks=[
         dict(row=dict(l='Omar K.', m='InstaPay', chip='pend', ctext='Pending', to='paid', totext='Paid', at=1.0)),
         dict(row=dict(l='Mariam S.', m='Wallet', chip='pend', ctext='Pending', to='paid', totext='Paid', at=1.4)),
         dict(row=dict(l='Youssef A.', m='Card', chip='pend', ctext='Pending', to='paid', totext='Paid', at=1.8)),
         dict(btn=dict(label='Send link to paid students', at=2.8, toast='Link sent to paid students only')),
         dict(note='After class: <b style="color:#fff">recording, AI summary and attendance</b>, automatically')])),
  dict(type='chips', d=4.6, tin='whip', family='blue', head=['امتحانات بالـ AI', '*وإنت اللي بتوافق.*'], size=100, y=290, drift=5, chips=[
       dict(text='أسئلة بأسلوبك إنت', x=90, y=760, t=.6), dict(text='من فيديوهاتك وكتبك', x=400, y=890, t=.85),
       dict(text='تصحيح مقترح بالـ AI', x=110, y=1020, t=1.1), dict(text='ولا درجة من غير موافقتك', x=300, y=1150, t=1.35, bg='#f26229'),
       dict(text='نسخة مختلفة لكل طالب', x=130, y=1280, t=1.6)]),
  dict(type='list', d=5.8, tin='flip', family='ink', head=['محتواك', '*صعب يتسرب.*'], size=120, gap=200, items=[
       dict(title='فيديو محمي', desc='من غير تحميل، والتسجيل بيطلع شاشة سودا', icon='doc'),
       dict(title='اسم الطالب على كل فيديو وملف', desc='ولو اتسرب، تعرف مين', icon='person'),
       dict(title='حد أقصى للأجهزة', desc='الحساب ما يتقسمش على كذا حد', icon='users'),
       dict(title='تتبع الورقة المتسربة', desc='من صورة أو نص منسوخ', icon='exam')]),
  dict(type='tiles', d=5.4, tin='dolly', family='ink', head=['وفريقك', '*معاك جوه.*'], size=110, gap=235, tiles=[
       dict(title='مساعدين بصلاحيات', desc='كل واحد يشوف اللي إنت تسمح بيه', icon='users', c='#2655a3'),
       dict(title='واتساب جوه البوابة', desc='ترد على الطلبة والأهالي من مكان واحد', icon='chat', c='#f26229'),
       dict(title='متجر لكتبك ومذكراتك', desc='تبيع المحتوى بتاعك جوه المنصة', icon='cart', c='#2655a3'),
       dict(title='Agent بالـ AI', desc='تطلب منه وهو يجهز، وإنت توافق', icon='ai', c='#f26229')]),

  # 2 · the student
  dict(type='hook', d=2.2, tin='whip', family='orange', kicker='٢ · من ناحية الطالب', head=['مذاكرة', '*بخطة واضحة.*'], size=140, y=440,
       mascots=[M('dara', [[0, 'happy']], 400, 1160, 300, .3, jump=[.8])]),
  dict(type='story', d=7.2, tin='dolly', open='class', boardtitle="Dara · Today's plan", lines=[
    dict(who='dara', t=.3, text='وأنا كطالبة؟ إيه اللي يفرق معايا؟', ex='thinking'),
    dict(who='ustaz', t=2.7, text='خطة كل يوم، وغلطاتك بترجعلك تمرين.', ex='proud', shot='boardwide'),
    dict(who='dara', t=5.9, text='كده أحسن بكتير!', ex='celebrate', react={'dars': 'happy'}),
  ], board=[dict(t=3.1, panel=dict(crumb='Student portal  /  Today', title="Today's plan", blocks=[
      dict(row=dict(l='Mock 4 · SAT Math', tick=3.7)), dict(row=dict(l='Practise: Linear equations', tick=4.3)),
      dict(row=dict(l='Review 6 mistakes', chip='pend', ctext='Due')), dict(bar=dict(l='Score trend', w=78, v='+12%', at=4.8, c='#f26229'))]), x=20, y=75, scale=.66)],
     cast={'dara': dict(jump=[6.1])}),
  dict(type='ui', d=5.6, tin='dolly', family='orange', head=['الـ AI بيشرحله', '*غلط فين بالظبط.*'], size=96, y=250, py=520, cam=TILT,
       panel=dict(crumb='Results  /  Mock 4  /  Question 7', title='Why was this wrong?', sub='3x − 7 = 2x + 5', blocks=[
         dict(row=dict(l='Your answer: x = −2', chip='bad', ctext='Wrong')),
         dict(note='<b style="color:#fff">AI:</b> you moved the 7 to the wrong side. Move the numbers first, then x.'),
         dict(bar=dict(l='Linear equations', w=41, v='41%', at=1.6, c='#f26229')),
         dict(btn=dict(label='Practise this', at=3.0, toast="Added to today's plan"))])),
  dict(type='exam', d=5.8, tin='dolly', family='blue', tabs=['SAT', 'EST', 'ACT', 'IGCSE', 'ثانوية عامة'], on=0, ey=640, section='Math', qn='12 of 22',
       q='The function f is defined by f(x) = 3x² − 12x + 7. For what value of x does f reach its minimum?', choices=['−2', '0', '2', '4'],
       pick=2, pick_at=2.8, next_at=3.6, c0=.2, c1=5.6, tfrom=1908, tto=1903, head=['امتحان تجريبي', '*زي الحقيقي بالظبط.*'], size=92, y=250,
       cam=[[0, 540, 1000, .8, -24, 16, .01], [.15, 540, 980, 1, 0, 0, 1.4], [1.9, 470, 1080, 1.3, 7, 4, .8], [3.7, 540, 960, 1, 0, 0, .8]]),
  dict(type='chips', d=4.0, tin='whip', family='blue', head=['ومن غير غش.'], size=120, y=330, drift=5, chips=[
       dict(text='التطبيق بيقفل الجهاز', x=90, y=640, t=.5), dict(text='الكاميرا بتراقب', x=470, y=770, t=.75),
       dict(text='مفيش شاشة تانية', x=110, y=900, t=1.0), dict(text='موبايل في الإيد؟ الامتحان يقف', x=150, y=1030, t=1.25, bg='#f26229')],
       mascots=[M('dars', [[0, 'focus']], 400, 1240, 290, .3)]),

  # 3 · the parent
  dict(type='hook', d=2.4, tin='whip', family='ink', kicker='٣ · ولي الأمر', head=['بيعرف كل حاجة', '*من غير ما يسأل.*'], size=120, y=440,
       mascots=[M('ustaz', [[0, 'happy']], 390, 1150, 320, .3)]),
  dict(type='chat', d=5.8, family='ink', name='تقرير عمر الأسبوعي', av='D', status='واتساب', unread=True, py=330, ph=920,
       msgs=[dict(text='الحضور: ٤ من ٤ حصص', t=.3, time='الجمعة ٩:٠٠ م'), dict(text='امتحان ٣: ٨٢٪', t=.9, time='الجمعة ٩:٠٠ م'),
             dict(text='نقطة ضعف: النسب، والتمرين اتبعتله', t=1.5, time='الجمعة ٩:٠٠ م'), dict(text='مطلوب الأسبوع الجاي: ٣ واجبات', t=2.1, time='الجمعة ٩:٠٠ م'),
             dict(text='تنبيه: عمر غاب حصة النهارده', t=3.4, time='الأحد ٧:١٥ م')],
       mascots=[M('ustaz', [[0, 'focus'], [3.6, 'proud']], 720, 1330, 250, .2)]),

  dict(type='story', d=6.4, tin='whip', open='class', boardtitle='Darsify', lines=[
    dict(who='dars', t=.3, text='يعني كله في مكان واحد؟', ex='surprised'),
    dict(who='ustaz', t=2.3, text='وأنا بركز في الشرح بس.', ex='proud'),
    dict(who='dara', t=4.3, text='وإحنا بنذاكر أحسن.', ex='celebrate', react={'dars': 'celebrate'}),
  ], cast={'dars': dict(jump=[4.6]), 'dara': dict(jump=[4.5])}),
  dict(type='hook', d=2.6, tin='whip', en=True, head=['Teach more.', '*Chase less.*'], size=160, y=480, mascots=trio()),
  END(['الحصص', 'الدفع', 'الامتحانات', 'الـ AI', 'الحماية', 'التقارير'], btn='ابدأ مجانًا', join='ابدأ مجانًا على <b>darsify.net</b>')],
  caption=dict(
    ar="مدرس؟ شوف Darsify من ٣ زوايا:\n\nإنت: تحدد ميعاد الحصة، الطلبة يدفعوا بالكارت أو المحفظة أو إنستاباي أو فوري، واللينك يوصل للي دفع بس. امتحانات بالـ AI بأسلوبك، والـ AI يقترح الدرجة وإنت توافق. ومحتواك صعب يتسرب، ولو اتسرب تعرف مين.\n\nطالبك: خطة كل يوم، وغلطاته بترجعله تمرين لحد ما يتقنها، وامتحانات تجريبية زي الحقيقي.\n\nولي الأمر: تقرير أسبوعي على واتساب، وتنبيه لو ابنه غاب.\n\nTeach more. Chase less. ابدأ مجانًا على darsify.net\n\n#WeplanYouteach #TeachMoreChaseLess",
    headline='ابدأ مجانًا على darsify.net'))

# ------------------------------------------------------------------ schools
R['AD-S1'] = dict(title='Darsify للمدارس: سيستم واحد للكل', lang='ar', family='blue', bpm=112, key=5, mood='bright', seed=902, cover=13.6, scenes=[
  dict(type='story', d=10.6, open='class', boardtitle='Darsify for Schools', lines=[
    dict(who='dara', t=.4, text='مستر، هي المدرسة كلها هتشتغل على Darsify؟', ex='thinking'),
    dict(who='ustaz', t=3.3, text='الإدارة والمدرسين والطلبة وأولياء الأمور.', ex='proud', shot='boardwide'),
    dict(who='dars', t=6.6, text='كلهم على سيستم واحد؟', ex='surprised', react={'dara': 'surprised'}),
    dict(who='ustaz', t=8.5, text='سيستم واحد بالـ AI.', ex='happy'),
  ], board=[dict(t=3.7, write='الإدارة', y=120, size=54), dict(t=4.3, write='المدرسين', y=195, size=54),
            dict(t=4.9, write='الطلبة', y=270, size=54), dict(t=5.5, write='أولياء الأمور', y=345, size=54, c='#ff9a6e')],
     cast={'dars': dict(jump=[6.8])}),

  # leadership
  dict(type='hook', d=2.4, tin='whip', family='ink', kicker='١ · للإدارة', head=['المدرسة كلها', '*في شاشة واحدة.*'], size=125, y=440,
       mascots=[M('ustaz', [[0, 'focus']], 390, 1150, 320, .3)]),
  dict(type='ui', d=6.0, tin='dolly', family='ink', head=['نتايج، نقاط ضعف،', '*وطلبة محتاجين متابعة.*'], size=88, y=250, py=520, cam=TILT,
       panel=dict(crumb='Insights  /  All groups', title='This term', blocks=[
         dict(bar=dict(l='Group 9A', w=82, v='82%', at=.8)), dict(bar=dict(l='Group 9B', w=74, v='74%', at=1.1)),
         dict(bar=dict(l='Group 9C', w=61, v='61%', at=1.4, c='#f26229')),
         dict(row=dict(l='At-risk students', chip='bad', ctext='6', **{'in': 2.0})),
         dict(row=dict(l='Weakest topic, Group 9C', m='Fractions', chip='info', ctext='Practice set', **{'in': 2.5})),
         dict(btn=dict(label='Export PDF', at=3.6, toast='Report ready'))])),
  dict(type='ui', d=6.2, tin='whip', family='ink', head=['اسأل الـ AI', '*يجهز، وإنت توافق.*'], size=96, y=250, py=540,
       panel=dict(crumb='Agent', title='Workspace agent', sub='Approvals ON · nothing changes without your OK', blocks=[
         dict(type=dict(label='YOU ASKED', text='Which students have overdue work?', t0=.4, t1=1.7)),
         dict(row=dict(l='14 students in 3 groups', chip='info', ctext='Found', **{'in': 2.2})),
         dict(row=dict(l='Reminders to students and parents', chip='pend', ctext='Drafted', to='paid', totext='Approved', at=3.8, **{'in': 2.7})),
         dict(btn=dict(label='Approve', at=3.8, toast='Sent on WhatsApp'))])),

  # teachers
  dict(type='chips', d=4.8, tin='flip', family='blue', head=['٢ · للمدرسين:', '*شغل ورق أقل.*'], size=100, y=290, drift=5, chips=[
       dict(text='امتحانات بالـ AI من المنهج', x=80, y=760, t=.6), dict(text='تصحيح مقترح، والمدرس يوافق', x=180, y=890, t=.85, bg='#f26229'),
       dict(text='نسخة مختلفة لكل طالب', x=90, y=1020, t=1.1), dict(text='مواد ومحاضرات محمية', x=330, y=1150, t=1.35),
       dict(text='واجبات بتذكير تلقائي', x=120, y=1280, t=1.6)]),

  # students
  dict(type='exam', d=5.6, tin='dolly', family='blue', tabs=['IGCSE', 'American', 'IB', 'ثانوية عامة'], on=0, ey=640, section='Mathematics', qn='8 of 30',
       q='A shop reduces the price of a jacket by 20%. The new price is 640 EGP. What was the original price?', choices=['768', '800', '820', '960'],
       pick=1, pick_at=2.8, next_at=3.6, c0=.2, c1=5.4, tfrom=2700, tto=2695, head=['٣ · للطلبة:', '*امتحان زي الحقيقي.*'], size=92, y=250,
       cam=[[0, 540, 1000, .8, -24, 16, .01], [.15, 540, 980, 1, 0, 0, 1.4], [1.9, 470, 1080, 1.3, 7, 4, .8], [3.7, 540, 960, 1, 0, 0, .8]]),
  dict(type='list', d=5.6, tin='whip', family='ink', head=['والغش', '*صعب جدًا.*'], size=120, gap=200, items=[
       dict(title='التطبيق بيقفل الجهاز', desc='لحد ما الطالب يخلص', icon='exam'),
       dict(title='صورة من الكاميرا كل ٣ ثواني', desc='موبايل في الإيد؟ الامتحان يقف', icon='person'),
       dict(title='مفيش شاشة تانية', desc='الامتحان ما يبدأش غير لما تتفصل', icon='x'),
       dict(title='اسم الطالب على كل ورقة', desc='ولو اتسربت، تعرف مين', icon='doc')]),
  dict(type='story', d=6.6, tin='whip', open='class', boardtitle='Dars · Weak points', lines=[
    dict(who='dars', t=.3, text='وأنا بعد الامتحان؟', ex='thinking'),
    dict(who='ustaz', t=2.2, text='غلطاتك بترجعلك تمرين لحد ما تتقنها.', ex='proud', shot='boardwide'),
    dict(who='dars', t=5.3, text='اتفقنا!', ex='celebrate', react={'dara': 'happy'}),
  ], board=[dict(t=2.6, panel=dict(crumb='Practice  /  Weak points', title='Clear these to unlock the next mock', blocks=[
      dict(bar=dict(l='Fractions', w=45, v='45%', at=3.1, c='#f26229')), dict(bar=dict(l='Percentages', w=58, v='58%', at=3.4)),
      dict(row=dict(l='Practise your mistakes', chip='pend', ctext='10 questions', to='paid', totext='Cleared', at=4.6))]), x=20, y=75, scale=.66)],
     cast={'dars': dict(jump=[5.5])}),

  # parents
  dict(type='hook', d=2.4, tin='whip', family='ink', kicker='٤ · لأولياء الأمور', head=['كل أسبوع', '*على واتساب.*'], size=140, y=440,
       mascots=[M('dara', [[0, 'happy']], 400, 1160, 300, .3)]),
  dict(type='chat', d=5.4, family='ink', name='تقرير مريم الأسبوعي', av='D', status='واتساب', unread=True, py=330, ph=900,
       msgs=[dict(text='الحضور: ٥ من ٥ أيام', t=.3, time='الجمعة ٩:٠٠ م'), dict(text='اختبار الرياضيات: ٩٠٪', t=.9, time='الجمعة ٩:٠٠ م'),
             dict(text='محتاجة تركيز في: الكسور، والتمرين اتبعتلها', t=1.5, time='الجمعة ٩:٠٠ م'),
             dict(text='تنبيه: مريم غابت حصة العلوم النهارده', t=3.0, time='الثلاثاء ٨:٤٠ ص')],
       mascots=[M('dara', [[0, 'focus'], [3.2, 'proud']], 720, 1330, 250, .2)]),
  dict(type='hook', d=2.6, tin='whip', en=True, head=['Teach more.', '*Chase less.*'], size=160, y=480, mascots=trio()),
  END(['الإدارة', 'المدرسين', 'الطلبة', 'أولياء الأمور', 'الـ AI', 'الأمان'], btn='انضم لينا')],
  caption=dict(
    ar="مدرسة؟ جامعة؟ سنتر؟ Darsify بيربط الكل على سيستم واحد بالـ AI:\n\nالإدارة: نتايج كل مجموعة، نقاط الضعف، والطلبة اللي محتاجين متابعة. واسأل الـ AI، هو يجهز وإنت توافق.\n\nالمدرسين: امتحانات بالـ AI، تصحيح مقترح والمدرس يوافق، ومحتوى محمي.\n\nالطلبة: امتحانات زي الحقيقي بمراقبة، وغلطاتهم بترجعلهم تمرين.\n\nأولياء الأمور: تقرير أسبوعي على واتساب، وتنبيه لو الطالب غاب.\n\nTeach more. Chase less. انضم لينا على darsify.net\n\n#WeplanYouteach #TeachMoreChaseLess",
    headline='انضم لينا على darsify.net'))

for k, v in R.items():
    v['id'] = k; (S / f'{k}.json').write_text(json.dumps(v, ensure_ascii=False, indent=1)); print(k, round(sum(s['d'] for s in v['scenes']), 1), 's')
