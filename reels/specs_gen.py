"""Writes specs/RL-02..RL-14.json (RL-01 is hand-written)."""
import json, pathlib
S = pathlib.Path(__file__).parent / 'specs'
END = lambda words=None, **kw: dict(type='end', d=4.4, words=words or [], **kw)
M = lambda who, ex, x=390, y=1200, w=300, t=.2, **kw: dict(who=who, ex=ex, x=x, y=y, w=w, t=t, **kw)
trio = lambda y=1150, t=.2, jump=True: [M('dars', [[0, 'happy']], 130, y + 30, 270, t, **({'jump': [t + .6]} if jump else {})),
                                        M('ustaz', [[0, 'proud']], 400, y, 300, t + .1),
                                        M('dara', [[0, 'happy']], 690, y + 30, 270, t + .2, ph=2, **({'jump': [t + .9]} if jump else {}))]
R = {}
R['RL-02'] = dict(title='POV: a parent messages you at 11:47 PM', family='orange', bpm=112, key=2, mood='warm', seed=22, cover=2.0, scenes=[
  dict(type='hook', d=2.8, kicker='POV:', head=["It's 11:47 PM.", 'A parent', '*messages you.*'], size=140, y=380,
       mascots=[M('ustaz', [[0, 'sleeping'], [1.6, 'surprised']], 390, 1180, 320, .4, jump=[1.6])]),
  dict(type='chat', d=5.0, name="Mrs. Hala (Omar's mom)", av='H', status='online', unread=True, py=330, ph=900,
       msgs=[dict(text='Sorry for the late message', t=.4, time='11:47 PM'), dict(text='How is Omar doing this month?', t=1.2, time='11:47 PM'),
             dict(text="Did he attend Sunday's class?", t=2.0, time='11:48 PM'), dict(text='And what did he get on the mock?', t=2.8, time='11:48 PM')],
       mascots=[M('ustaz', [[0, 'concerned'], [2.6, 'annoyed']], 720, 1330, 250, .2)]),
  dict(type='hook', d=2.4, head=['Now imagine', 'she *already*', '*knows.*'], size=150, y=480,
       mascots=[M('ustaz', [[0, 'thinking'], [1.2, 'happy']], 390, 1150, 320, .2)]),
  dict(type='ui', d=5.2, head=['Every Sunday.', '*Automatically.*'], size=96, y=280, py=560,
       panel=dict(crumb='Group A  /  Parent reports', title='Weekly report', sub="Omar K. · week of 18 Oct", blocks=[
         dict(bar=dict(l='Attendance', w=100, v='4 / 4', at=.5, c='#5e8bc8')), dict(bar=dict(l='Mock 3', w=82, v='82%', at=.8, c='#f26229')),
         dict(bar=dict(l='Homework', w=83, v='5 / 6', at=1.1, c='#5e8bc8')), dict(note='Weak topic: <b style="color:#fff">Ratios</b> · practice sent'),
         dict(btn=dict(label='Send to parent', at=2.6, toast='Sent on WhatsApp'))]),
       mascots=[M('ustaz', [[0, 'focus'], [2.9, 'proud']], 720, 1420, 250, .3)]),
  dict(type='chat', d=2.6, name="Mrs. Hala (Omar's mom)", av='H', status='online', py=560, ph=520,
       msgs=[dict(text='Got the report, thank you! We will practice Ratios at home.', t=.3, time='Sun 6:02 PM')],
       mascots=[M('ustaz', [[0, 'celebrate']], 390, 1180, 300, .2, jump=[.9])]),
  END(['Attendance', 'Mocks', 'Homework', 'Weak topics', 'Reports', 'WhatsApp'])],
  caption=dict(
    ig="POV: it's 11:47 PM and a parent wants a full update.\n\nAttendance. Mock score. Homework. Right now.\n\nWith Darsify, every parent gets their child's week on WhatsApp, every Sunday, without you writing a single message.\n\nTeach more. Chase less. Join us now at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #tutors #teachers #parents",
    fb="الساعة ١١:٤٧ بالليل… وولي أمر عايز تقرير كامل عن ابنه.\nمع Darsify، كل ولي أمر بيوصله تقرير أسبوعي على واتساب كل حد، من غير ما تكتب رسالة واحدة.\n\nTeach more. Chase less. انضم لينا على darsify.net\n\n—\n\nPOV: it's 11:47 PM and a parent wants a full update. With Darsify, every parent gets their child's week on WhatsApp, automatically.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="POV: 11:47 PM and a parent wants a full update. Darsify sends it every Sunday on WhatsApp. #WeplanYouteach #TeachMoreChaseLess #teachersoftiktok #tutor #parents"))

R['RL-03'] = dict(title='AI marks. You approve.', family='blue', bpm=120, key=5, mood='drive', seed=33, cover=1.4, scenes=[
  dict(type='hook', d=2.6, kicker='Marking night', head=['30 essays.', '*One evening.*'], size=160, y=400,
       mascots=[M('ustaz', [[0, 'sleeping']], 390, 1150, 320, .4)]),
  dict(type='counter', d=3.4, kicker='With Darsify', **{'from': 0, 'to': 30}, t0=.2, t1=1.5, label='essays with a *suggested* grade'.replace('*', ''), sub='Marked against your own rubric.', y=480,
       mascots=[M('ustaz', [[0, 'surprised'], [1.6, 'happy']], 390, 1230, 280, .2)]),
  dict(type='ui', d=5.6, head=['Check it in', '*seconds.*'], size=100, y=280, py=560,
       panel=dict(crumb='Marking  /  Essay', title='Should schools replace textbooks?', sub='Omar K. · Question 2', blocks=[
         dict(bar=dict(l='Clear position', w=67, v='2 / 3', at=.5)), dict(bar=dict(l='Evidence', w=75, v='3 / 4', at=.8)), dict(bar=dict(l='Organisation', w=67, v='2 / 3', at=1.1)),
         dict(row=dict(l='AI suggests', chip='info', ctext='7 / 10')),
         dict(btn=dict(label='Approve 7/10', at=3.0, toast='Sent to Omar with feedback'))]),
       mascots=[M('ustaz', [[0, 'focus'], [3.2, 'proud']], 720, 1440, 250, .3)]),
  dict(type='hook', d=2.8, head=['AI suggests.', '*You approve.*'], size=150, y=460, sub='Nothing reaches a student until you say so.', subt=1.0, suby=820,
       mascots=[M('ustaz', [[0, 'proud']], 390, 1150, 320, .3)]),
  END(['Essays', 'Rubrics', 'Feedback', 'Grades', 'Approve', 'Send'])],
  caption=dict(
    ig="30 essays. One evening.\n\nDarsify reads every written answer against your rubric and suggests a grade with the reasons.\n\nYou check it, adjust it, approve it. Nothing reaches a student until you say so.\n\nAI suggests. You approve.\n\nTeach more. Chase less. Join us now at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #teachers #tutors #edtech",
    fb="٣٠ مقال في ليلة واحدة؟\nDarsify بيصحح كل إجابة مكتوبة حسب معاييرك ويقترح الدرجة بالأسباب، وإنت اللي بتعتمد. مفيش درجة بتوصل للطالب غير لما توافق.\n\nTeach more. Chase less. darsify.net\n\n—\n\n30 essays, one evening. Darsify suggests a grade against your rubric; you approve it.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="30 essays, one evening. AI suggests the grade, you approve it. #WeplanYouteach #TeachMoreChaseLess #teachersoftiktok #edtech #AI"))

R['RL-04'] = dict(title='3 automations every tutor needs', family='orange', bpm=124, key=7, mood='bright', seed=44, cover=1.5, scenes=[
  dict(type='hook', d=2.6, kicker='Save this', head=['3 automations', 'every tutor', '*needs.*'], size=140, y=400,
       mascots=[M('ustaz', [[0, 'happy']], 390, 1180, 320, .4)]),
  dict(type='list', d=6.0, head=['Set them once.'], size=110, y=280, ly=470, gap=260, istep=1.3, items=[
       dict(title='Link after payment', desc='Paid students get the class link on their own.', icon='link'),
       dict(title='Reminders before class', desc="Goodbye, 'is class today?'", icon='bell'),
       dict(title='Weekly parent reports', desc="Every parent gets their child's week on WhatsApp.", icon='chat')],
       mascots=[M('ustaz', [[0, 'focus'], [4.0, 'proud']], 720, 1400, 250, .3)]),
  dict(type='hook', d=2.6, head=['They run', '*every week.*', 'You teach.'], size=150, y=430, mascots=trio()),
  END(['Links', 'Reminders', 'Reports', 'Payments', 'Attendance', 'Mocks'])],
  caption=dict(
    ig="3 automations every tutor needs (save this):\n\n1. The class link goes out automatically once a student pays.\n2. Reminders go out before every class.\n3. Every parent gets a weekly report on WhatsApp.\n\nSet them once in Darsify. They run every week.\n\nTeach more. Chase less. Join us now at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #tutors #teachers #productivity",
    fb="٣ حاجات أي مدرس محتاجها تشتغل لوحدها:\n١. اللينك يوصل للطالب أول ما يدفع\n٢. تذكير قبل كل حصة\n٣. تقرير أسبوعي لكل ولي أمر على واتساب\nتظبطها مرة واحدة على Darsify وهي تشتغل كل أسبوع.\n\nTeach more. Chase less. darsify.net\n\n—\n\n3 automations every tutor needs: link after payment, reminders before class, weekly parent reports.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="3 automations every tutor needs. Save this. #WeplanYouteach #TeachMoreChaseLess #teachersoftiktok #tutor #productivity"))

R['RL-05'] = dict(title='Meet the Darsify crew', family='ink', bpm=110, key=0, mood='chill', seed=55, cover=1.6, scenes=[
  dict(type='hook', d=2.6, head=['Meet the', '*Darsify crew.*'], size=150, y=420, mascots=trio(1100, .5, False)),
  dict(type='hook', d=2.9, kicker='The tutor', head=['*Ustaz*'], size=200, y=380, sub='Announcements, feedback and reminders. The voice of the teacher.', subt=.6, suby=600,
       mascots=[M('ustaz', [[0, 'happy'], [1.4, 'proud']], 330, 930, 420, .3)]),
  dict(type='hook', d=2.9, kicker='The student', head=['*Dars*'], size=200, y=380, sub='Your study buddy. Celebrates every finished mock.', subt=.6, suby=600,
       mascots=[M('dars', [[0, 'happy'], [1.4, 'celebrate']], 330, 960, 400, .3, jump=[1.4])]),
  dict(type='hook', d=2.9, kicker='The student', head=['*Dara*'], size=200, y=380, accent='#e0567f', sub='Keeps the streak alive with daily reading and vocab.', subt=.6, suby=600,
       mascots=[M('dara', [[0, 'reading'], [1.4, 'proud']], 330, 960, 400, .3)]),
  dict(type='hook', d=2.6, head=['Together, they', 'keep students', '*on track.*'], size=130, y=420, mascots=trio(1120)),
  END(['Ustaz', 'Dars', 'Dara', 'Streaks', 'Reviews', 'Reminders'])],
  caption=dict(
    ig="Meet the Darsify crew.\n\nUstaz, the voice of the teacher: announcements, feedback and reminders.\nDars, the study buddy who celebrates every finished mock.\nDara, who keeps the streak alive with daily reading and vocab.\n\nWho's your favourite? Tell us below.\n\nTeach more. Chase less. darsify.net (link in bio)\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify #students #tutors",
    fb="قابلوا فريق Darsify:\nأستاذ: صوت المدرس، الإعلانات والملاحظات والتذكيرات.\nدارس: رفيق المذاكرة اللي بيحتفل بكل امتحان تجريبي.\nدارة: بتحافظ على الاستمرارية بالقراءة اليومية والمفردات.\nمين المفضل عندك؟\n\n—\n\nMeet the Darsify crew: Ustaz, Dars and Dara.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="Meet the Darsify crew: Ustaz, Dars and Dara. Who's your favourite? #WeplanYouteach #Darsify #students #studytok #edtech"))

R['RL-06'] = dict(title='The real exam, before the real exam', family='blue', bpm=126, key=-3, mood='drive', seed=66, cover=1.5, scenes=[
  dict(type='hook', d=2.8, head=['The real exam.', '*Before* the', 'real exam.'], size=140, y=420,
       mascots=[M('dars', [[0, 'focus']], 400, 1180, 300, .4)]),
  dict(type='exam', d=5.6, tabs=['SAT', 'EST', 'ACT', 'IGCSE', 'Thanwya'], on=0, ey=640, section='Math', qn='12 of 22',
       q='The function f is defined by f(x) = 3x² − 12x + 7. For what value of x does f reach its minimum?', choices=['−2', '0', '2', '4'],
       pick=2, pick_at=2.6, next_at=3.4, c0=.4, c1=5.4, tfrom=1908, tto=1902, head=['Timed. Real format.'], size=96, y=280,
       mascots=[M('dars', [[0, 'thinking'], [2.6, 'happy']], 760, 1450, 220, .3)]),
  dict(type='chips', d=3.6, head=['Same timer.', 'Same tools.', '*Same pressure.*'], size=120, y=300, chips=[
       dict(text='Mark for review', x=90, y=860, t=.6), dict(text='Answer eliminator', x=420, y=990, t=.85), dict(text='Question navigator', x=110, y=1120, t=1.1),
       dict(text='Countdown timer', x=470, y=1250, t=1.35), dict(text='Auto-graded', x=200, y=1380, t=1.6, bg='#f26229')]),
  dict(type='hook', d=2.8, head=['So exam day', '*feels familiar.*'], size=140, y=440, sub='Authentic mocks for SAT, EST, ACT, IGCSE and Thanwya Amma.', subt=.9, suby=760,
       mascots=[M('dars', [[0, 'celebrate']], 400, 1160, 300, .2, jump=[.8])]),
  END(['SAT', 'EST', 'ACT', 'IGCSE', 'Thanwya Amma', 'Mocks'])],
  caption=dict(
    ig="The real exam, before the real exam.\n\nDarsify mocks look and feel like the real thing: the timer, mark for review, the answer eliminator, the question navigator.\n\nSAT, EST, ACT, IGCSE and Thanwya Amma. Auto-graded, with weak topics after every paper.\n\nSo exam day feels familiar.\n\nTeach more. Chase less. Join us now at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #SAT #IGCSE #Thanwya",
    fb="الامتحان الحقيقي… قبل الامتحان الحقيقي.\nامتحانات Darsify التجريبية بنفس شكل الامتحان: التايمر، المراجعة، استبعاد الإجابات، والتنقل بين الأسئلة. SAT وEST وACT وIGCSE والثانوية العامة.\nعلشان يوم الامتحان يبقى مألوف.\n\nTeach more. Chase less. darsify.net\n\n—\n\nAuthentic mocks for SAT, EST, ACT, IGCSE and Thanwya Amma.\n\n#WeplanYouteach #TeachMoreChaseLess #SAT #Thanwya",
    tiktok="The real exam, before the real exam. Mocks that feel like exam day. #WeplanYouteach #SAT #IGCSE #Thanwya #studytok"))

R['RL-07'] = dict(title='Your center. Now online too.', family='orange', bpm=118, key=4, mood='warm', seed=77, cover=1.5, scenes=[
  dict(type='hook', d=2.8, kicker='Run a center?', head=['Your center.', '*Now online too.*'], size=140, y=420,
       mascots=[M('ustaz', [[0, 'happy']], 390, 1180, 320, .4)]),
  dict(type='tiles', d=5.4, head=['Darsify for', '*Academies*'], size=120, y=280, ty=600, gap=280, tiles=[
       dict(title='All your tutors', desc='Every tutor gets their own Darsify workspace.', icon='users', c='#0b1e30'),
       dict(title='All your students', desc='Groups, attendance and results in one account.', icon='school', c='#2655a3'),
       dict(title='Online + on-ground', desc='Your own online academy, under your name.', icon='globe', c='#0b1e30')]),
  dict(type='ui', d=5.0, head=['One view of', '*everything.*'], size=100, y=280, py=560,
       panel=dict(crumb='Nile Academy  /  Overview', title='This week', sub='3 branches · online and on-ground', blocks=[
         dict(big=dict(t0=.4, t1=1.6, **{'from': 0, 'to': 1240}, l='students across all tutors')),
         dict(row=dict(l='Tutors', m='18 active', chip='paid', ctext='All synced')),
         dict(bar=dict(l='Attendance', w=92, v='92%', at=1.4)), dict(bar=dict(l='Fees collected', w=87, v='87%', at=1.7, c='#f26229'))]),
       mascots=[M('ustaz', [[0, 'focus'], [2.4, 'proud']], 720, 1440, 250, .3)]),
  dict(type='hook', d=2.6, head=['One academy.', '*One system.*'], size=150, y=480, mascots=trio()),
  END(['Tutors', 'Students', 'Branches', 'Online', 'On-ground', 'Fees'], btn='BOOK A DEMO', join='Book a demo at <b>Darsify.net</b>')],
  caption=dict(
    ig="Run a center or an academy? Here's Darsify for Academies.\n\nEvery tutor gets their own Darsify workspace. You see all your students, groups, attendance, results and fees in one account.\n\nAnd your center gets its own online academy, alongside the classes on the ground.\n\nOne academy. One system. Book a demo at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #edtech #education #Egypt",
    fb="عندك سنتر أو أكاديمية؟\nمع Darsify for Academies كل مدرس عنده مساحة شغل خاصة بيه، وإنت شايف كل الطلبة والمجموعات والحضور والنتايج والمصاريف في حساب واحد.\nوالسنتر بتاعك يبقى أكاديمية أونلاين جنب الأونجراوند.\n\nاحجز ديمو على darsify.net\n\n—\n\nDarsify for Academies: every tutor, every student, online and on-ground, in one system.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="Your center. Now online too. Darsify for Academies. #WeplanYouteach #edtech #education #Egypt #tutor"))

R['RL-08'] = dict(title='From the canteen to the exams', family='blue', bpm=122, key=2, mood='bright', seed=88, cover=1.6, scenes=[
  dict(type='hook', d=2.8, kicker='Schools & universities', head=['From the *canteen*', 'to the *exams.*'], size=130, y=420,
       mascots=[M('ustaz', [[0, 'happy']], 390, 1180, 320, .4)]),
  dict(type='chips', d=4.8, head=['One school.', 'Too many systems.'], size=120, y=280, merge=3.2, my=900, mtext='One ecosystem', chips=[
       dict(text='Attendance', x=90, y=640, t=.4), dict(text='Grades', x=600, y=600, t=.6), dict(text='Fees', x=140, y=800, t=.8), dict(text='Canteen', x=560, y=780, t=1.0),
       dict(text='Bus', x=90, y=970, t=1.2), dict(text='Announcements', x=430, y=1000, t=1.4), dict(text='Exams', x=150, y=1170, t=1.6), dict(text='Student affairs', x=500, y=1200, t=1.8)]),
  dict(type='list', d=6.0, head=['Darsify for', '*Schools & Universities*'], size=96, y=280, ly=560, gap=270, istep=1.2, items=[
       dict(title='Leadership to classroom', desc='Principal, heads, teachers, students and parents, connected.', icon='building'),
       dict(title='AI does the paperwork', desc='Reports, marking, reminders and records, ready for approval.', icon='ai'),
       dict(title='Parents in the loop', desc='A weekly report per child on WhatsApp.', icon='chat')]),
  dict(type='hook', d=2.6, head=['Less paper.', '*More learning.*'], size=150, y=480, sub='Book a demo at Darsify.net', subt=.9, suby=820, mascots=trio()),
  END(['Canteen', 'Grades', 'Fees', 'Exams', 'Bus', 'Reports'], btn='BOOK A DEMO', join='Book a demo at <b>Darsify.net</b>')],
  caption=dict(
    ig="From the canteen to the exams. Darsify for Schools & Universities.\n\nOne ecosystem that connects leadership, heads of department, teachers, students, parents and student affairs.\n\nAI and automation take the paperwork: reports, marking, reminders and records, ready for staff to approve.\n\nBook a demo at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #edtech #schools #universities",
    fb="من الكانتين لحد الامتحانات.\nDarsify for Schools & Universities: سيستم واحد بيربط الإدارة ورؤساء الأقسام والمدرسين والطلبة وأولياء الأمور وشؤون الطلبة.\nوالـ AI والأتمتة بيشيلوا الشغل الورقي، والإدارة بتعتمد.\n\nاحجز ديمو على darsify.net\n\n—\n\nFrom the canteen to the exams: one ecosystem for schools and universities.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="From the canteen to the exams. One ecosystem for schools and universities. #WeplanYouteach #edtech #schools #university #AI"))

R['RL-09'] = dict(title='Guess the weak topic', family='orange', bpm=116, key=9, mood='drive', seed=99, cover=1.5, scenes=[
  dict(type='hook', d=2.6, kicker='Quiz time', head=['Guess the', '*weak topic.*'], size=160, y=420, sub='Comment your guess before the end.', subt=1.0, suby=760,
       mascots=[M('dars', [[0, 'thinking']], 400, 1180, 300, .4)]),
  dict(type='ui', d=5.8, head=["Omar's last", '4 mocks'], size=100, y=280, py=560,
       panel=dict(crumb='Insights  /  Weak points', title='Omar K.', sub='Correct answers per topic, last 4 mocks', blocks=[
         dict(bar=dict(l='Data analysis', w=88, v='88%', at=.5)), dict(bar=dict(l='Geometry', w=72, v='72%', at=.9)),
         dict(bar=dict(l='Ratios', w=63, v='63%', at=1.3)), dict(bar=dict(l='Linear equations', w=41, v='41%', at=1.7, c='#f26229'))],
         stamp=dict(text='Weak topic', t=3.2, x=380, y=520)),
       mascots=[M('dars', [[0, 'focus'], [3.2, 'surprised']], 740, 1440, 230, .3)]),
  dict(type='hook', d=2.8, head=['Darsify finds it', '*after every mock.*'], size=120, y=440, sub='Then sends practice on exactly that topic.', subt=.9, suby=760,
       mascots=[M('dars', [[0, 'happy']], 400, 1160, 300, .2)]),
  END(['Ratios', 'Geometry', 'Algebra', 'Data', 'Practice', 'Mocks'])],
  caption=dict(
    ig="Quiz: which topic keeps costing Dara marks?\n\nComment your guess.\n\nDarsify tags every question by topic, so after each mock you see exactly where the marks went, and practice on that topic goes out automatically.\n\nNo more guessing who needs help with what.\n\nTeach more. Chase less. darsify.net (link in bio)\n\n#WeplanYouteach #TeachMoreChaseLess #SAT #tutors #teachers",
    fb="خمّن: أنهي موضوع بيضيّع على دارة أكتر درجات؟ اكتب إجابتك في الكومنتات.\nDarsify بيصنّف كل سؤال حسب الموضوع، فبعد كل امتحان تجريبي تعرف الدرجات راحت فين، والتدريب على الموضوع ده بيوصل للطالب لوحده.\n\nTeach more. Chase less. darsify.net\n\n—\n\nGuess the weak topic. Darsify finds it after every mock.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="Guess the weak topic before the end. Comment your answer. #WeplanYouteach #SAT #teachersoftiktok #studytok #tutor"))

R['RL-10'] = dict(title='How many WhatsApp groups do you manage?', family='blue', bpm=124, key=5, mood='bright', seed=101, cover=1.4, scenes=[
  dict(type='hook', d=2.6, head=['How many', '*WhatsApp groups*', 'do you manage?'], size=125, y=420,
       mascots=[M('ustaz', [[0, 'thinking']], 390, 1180, 320, .4)]),
  dict(type='counter', d=3.0, **{'from': 1, 'to': 14}, t0=.2, t1=1.4, label='groups. One tutor.', y=520, ncolor='#f26229',
       mascots=[M('ustaz', [[0, 'concerned'], [1.4, 'annoyed']], 390, 1230, 280, .2, shake=1.5)]),
  dict(type='chat', d=4.4, name='Group B · Students', av='B', status='87 participants', unread=True, py=330, ph=920,
       msgs=[dict(text='Is class today?', t=.3, time='6:41 PM'), dict(text='Sir, the link?', t=.8, time='6:52 PM'), dict(text="I didn't get the PDF", t=1.3, time='6:53 PM'),
             dict(text='Can you resend it?', t=1.8, time='6:53 PM'), dict(text='Is the mock on Sunday?', t=2.3, time='6:55 PM'), dict(text='Sir??', t=2.8, time='6:58 PM')],
       mascots=[M('ustaz', [[0, 'annoyed'], [2.6, 'sulk']], 720, 1330, 250, .2)]),
  dict(type='hook', d=2.8, head=['One portal.', '*Everything in it.*'], size=140, y=440, sub='Links, files, reminders and announcements, without the group chaos.', subt=.9, suby=760, mascots=trio()),
  END(['Links', 'Files', 'Reminders', 'Announcements', 'Mocks', 'Reports'])],
  caption=dict(
    ig="How many WhatsApp groups do you manage right now? Be honest.\n\n\"Is class today?\" \"Sir, the link?\" \"Can you resend it?\"\n\nDarsify gives your students one portal: the links, the files, the reminders and the announcements, all in one place.\n\nTeach more. Chase less. Join us now at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #teachers #tutors #teacherlife",
    fb="عندك كام جروب واتساب دلوقتي؟ قول الحقيقة.\n\"الحصة النهارده؟\" \"اللينك يا مستر؟\" \"ممكن تبعته تاني؟\"\nمع Darsify الطلبة عندهم بوابة واحدة فيها اللينكات والملفات والتذكيرات والإعلانات.\n\nTeach more. Chase less. darsify.net\n\n—\n\nHow many WhatsApp groups do you manage? Darsify puts it all in one portal.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="How many WhatsApp groups do you manage? Be honest. #WeplanYouteach #teachersoftiktok #teacherlife #tutor #TeachMoreChaseLess"))

R['RL-11'] = dict(title='لسه بتلاحق الفلوس؟', lang='ar', family='orange', bpm=114, key=0, mood='warm', seed=111, cover=1.5, scenes=[
  dict(type='hook', d=2.8, kicker='سؤال سريع', head=['لسه *بتلاحق*', 'الفلوس؟'], size=170, y=420,
       mascots=[M('ustaz', [[0, 'annoyed']], 390, 1180, 320, .4)]),
  dict(type='chat', d=4.6, name='مجموعة السبت', av='س', status='متصل الآن', unread=True, py=330, ph=900,
       msgs=[dict(text='مستر أنا حولتلك', t=.3, time='٦:٤٠ م'), dict(text='بعتلك سكرين التحويل', t=1.0, time='٦:٤١ م'),
             dict(text='اتأكدت من الفلوس؟', t=1.7, time='٦:٤٥ م'), dict(text='اللينك فين يا مستر؟', t=2.4, time='٦:٥٢ م')],
       mascots=[M('ustaz', [[0, 'concerned'], [2.4, 'annoyed']], 720, 1330, 250, .2)]),
  dict(type='split', d=5.6, head=['قبل وبعد'], size=120, y=280, ly=520,
       left=dict(title='قبل', t=.3, items=[dict(text='تفتح الشات', t=.6, strike=3.6), dict(text='تدور على السكرين', t=1.0, strike=3.8), dict(text='تأكد التحويل', t=1.4, strike=4.0), dict(text='تبعت اللينك', t=1.8, strike=4.2)]),
       right=dict(title='Darsify مع', t=2.2, items=[dict(text='الطالب بيدفع', t=2.5), dict(text='الدفع بيتأكد', t=2.9), dict(text='اللينك بيوصل لوحده', t=3.3)])),
  dict(type='hook', d=2.6, en=True, head=['Teach more.', '*Chase less.*'], size=160, y=480, mascots=trio()),
  END(['الدفع', 'اللينك', 'التذكير', 'الحضور', 'التقارير', 'الامتحانات'])],
  caption=dict(
    ig="لسه بتلاحق الفلوس قبل كل حصة؟\n\nتفتح الشات، تدور على السكرين، تأكد التحويل، تبعت اللينك… وتكرر.\n\nمع Darsify الطالب بيدفع بالكارت أو المحفظة أو إنستاباي، الدفع بيتأكد، واللينك بيوصل لوحده.\n\nTeach more. Chase less. انضم لينا على darsify.net (اللينك في البايو)\n\n#WeplanYouteach #TeachMoreChaseLess #Thanwya #tutors #مدرسين",
    fb="لسه بتلاحق الفلوس قبل كل حصة؟\nتفتح الشات، تدور على السكرين، تأكد التحويل، تبعت اللينك… وتكرر.\nمع Darsify الطالب بيدفع بالكارت أو المحفظة أو إنستاباي، الدفع بيتأكد، واللينك بيوصل لوحده.\n\nTeach more. Chase less. انضم لينا على darsify.net\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="لسه بتلاحق الفلوس قبل كل حصة؟ Darsify بيأكد الدفع ويبعت اللينك لوحده. #WeplanYouteach #مدرسين #ثانوية_عامة #TeachMoreChaseLess"))

R['RL-12'] = dict(title='Mistakes come back as practice', family='blue', bpm=112, key=7, mood='chill', seed=121, cover=1.5, scenes=[
  dict(type='hook', d=2.6, kicker='Truth', head=['Students forget', '*their mistakes.*'], size=130, y=420,
       mascots=[M('dara', [[0, 'wrong']], 400, 1180, 300, .4)]),
  dict(type='timeline', d=5.2, head=['So Darsify', 'brings them *back.*'], size=110, y=280, ly=640, gap=170, rows=[
       dict(time='Day 1', text='Wrong on the mock', t=.4, c='#e5484d'), dict(time='Day 3', text='First review', t=1.1), dict(time='Day 7', text='Second review', t=1.8),
       dict(time='Day 14', text='Locked in', t=2.5, c='#22a06b', tag='Mastered')],
       mascots=[M('dara', [[0, 'thinking'], [2.6, 'happy']], 740, 1430, 230, .3)]),
  dict(type='ui', d=5.0, head=["Today's review"], size=100, y=280, py=520,
       panel=dict(crumb='Practice  /  Review', title='Due today', sub='From your last 3 mocks', blocks=[
         dict(row=dict(l='3x − 7 = 2x + 5', chip='pend', ctext='Due', to='paid', totext='Got it', at=1.2)),
         dict(row=dict(l="Meaning of 'mitigate'", chip='pend', ctext='Due', to='paid', totext='Got it', at=2.0)),
         dict(row=dict(l='Area of a sector', chip='pend', ctext='Due', to='bad', totext='Again in 2 days', at=2.8))]),
       mascots=[M('dara', [[0, 'focus'], [3.0, 'proud']], 740, 1430, 230, .3)]),
  dict(type='hook', d=2.6, head=['Mistakes', 'become *practice.*'], size=150, y=460, sub='Automatically, for every student.', subt=.9, suby=780, mascots=trio()),
  END(['Mistakes', 'Reviews', 'Practice', 'Streaks', 'Mocks', 'Progress'])],
  caption=dict(
    ig="Students forget their mistakes. Darsify doesn't.\n\nEvery wrong answer on a mock comes back as a review: on day 3, day 7, and again until it's locked in.\n\nAutomatically, for every student in every group.\n\nTeach more. Chase less. Join us now at darsify.net (link in bio).\n\n#WeplanYouteach #TeachMoreChaseLess #students #tutors #studytips",
    fb="الطلبة بينسوا غلطاتهم… Darsify لأ.\nكل إجابة غلط في الامتحان التجريبي بترجع للطالب كمراجعة: بعد ٣ أيام، وبعد أسبوع، لحد ما يتقنها. لوحدها، لكل طالب.\n\nTeach more. Chase less. darsify.net\n\n—\n\nEvery mistake comes back as practice until it's locked in.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="Students forget their mistakes. Darsify brings them back as practice. #WeplanYouteach #studytok #studytips #tutor #TeachMoreChaseLess"))

R['RL-13'] = dict(title="A tutor's evening, before Darsify", family='orange', bpm=120, key=2, mood='drive', seed=131, cover=1.5, scenes=[
  dict(type='hook', d=2.6, kicker='Before Darsify', head=["A tutor's", '*evening.*'], size=170, y=420,
       mascots=[M('ustaz', [[0, 'neutral']], 390, 1180, 320, .4)]),
  dict(type='timeline', d=6.2, head=['The *after-class* shift'], size=100, y=280, ly=560, gap=160, rows=[
       dict(time='5:00 PM', text='Check payment screenshots', t=.3, strike=3.6), dict(time='6:00 PM', text='Resend the Zoom link', t=.8, strike=3.85),
       dict(time='6:45 PM', text='Attendance by hand', t=1.3, strike=4.1), dict(time='9:00 PM', text='25 parent updates', t=1.8, strike=4.35),
       dict(time='11:47 PM', text='"One quick question"', t=2.3, strike=4.6)],
       mascots=[M('ustaz', [[0, 'annoyed'], [2.3, 'sleeping'], [3.6, 'surprised'], [4.8, 'happy']], 720, 1440, 250, .3)]),
  dict(type='hook', d=2.8, head=['With Darsify,', '*it runs itself.*'], size=140, y=440, sub='So your evening goes back to teaching. Or resting.', subt=.9, suby=760, mascots=trio()),
  END(['Payments', 'Links', 'Attendance', 'Reports', 'Questions', 'Reminders'])],
  caption=dict(
    ig="A tutor's evening, before Darsify:\n\n5:00 PM payment screenshots\n6:00 PM resend the Zoom link\n6:45 PM attendance by hand\n9:00 PM 25 parent updates\n11:47 PM \"one quick question\"\n\nWith Darsify, all of that runs itself. Your evening goes back to teaching. Or resting.\n\nTeach more. Chase less. darsify.net (link in bio)\n\n#WeplanYouteach #TeachMoreChaseLess #teacherlife #tutors #teachers",
    fb="مساء أي مدرس قبل Darsify:\n٥ م سكرينات التحويل\n٦ م تبعت لينك الزووم تاني\n٦:٤٥ م الحضور بإيدك\n٩ م ٢٥ رسالة لأولياء الأمور\n١١:٤٧ م \"سؤال صغير بس\"\nمع Darsify كل ده بيشتغل لوحده.\n\nTeach more. Chase less. darsify.net\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="A tutor's evening before Darsify. Which one hits hardest? #WeplanYouteach #teacherlife #teachersoftiktok #tutor #TeachMoreChaseLess"))

R['RL-14'] = dict(title='One engine. Three ways to use it.', family='ink', bpm=118, key=0, mood='bright', seed=141, cover=1.5, scenes=[
  dict(type='hook', d=2.8, head=['One engine.', '*Three ways*', 'to use it.'], size=150, y=420, mascots=trio(1150, .5, False)),
  dict(type='tiles', d=5.6, head=['Darsify is', 'built for'], size=110, y=280, ty=560, gap=290, tiles=[
       dict(title='Tutors', desc='Mocks, marking, payments and parent reports.', icon='person', c='#f26229'),
       dict(title='Academies', desc='All your tutors and students, online and on-ground.', icon='building', c='#2655a3'),
       dict(title='Schools & universities', desc='From the canteen to the exams, one ecosystem.', icon='school', c='#f26229')]),
  dict(type='hook', d=2.8, head=['All powered by', '*AI + automation.*'], size=125, y=440, sub='Less paperwork. More teaching.', subt=.9, suby=740, mascots=trio()),
  END(['Tutors', 'Academies', 'Schools', 'Universities', 'AI', 'Automation'])],
  caption=dict(
    ig="One engine. Three ways to use it.\n\nDarsify for Tutors: mocks, marking, payments and parent reports.\nDarsify for Academies: all your tutors and students, online and on-ground.\nDarsify for Schools & Universities: from the canteen to the exams, one ecosystem.\n\nAll powered by AI and automation.\n\nTeach more. Chase less. darsify.net (link in bio)\n\n#WeplanYouteach #TeachMoreChaseLess #edtech #AI #education",
    fb="محرك واحد… ٣ طرق تستخدمه:\nDarsify للمدرسين، للأكاديميات والسنترات، وللمدارس والجامعات. وكله شغال بالـ AI والأتمتة.\n\nTeach more. Chase less. darsify.net\n\n—\n\nOne engine, three ways: tutors, academies, schools & universities.\n\n#WeplanYouteach #TeachMoreChaseLess #Darsify",
    tiktok="One engine, three ways: tutors, academies, schools and universities. #WeplanYouteach #edtech #AI #education #TeachMoreChaseLess"))

for k, v in R.items():
    v['id'] = k; (S / f'{k}.json').write_text(json.dumps(v, ensure_ascii=False, indent=1)); print(k, sum(s['d'] for s in v['scenes']))
EOF_MARK = None
