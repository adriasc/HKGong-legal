import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "hkgong-cantonese-starter-guide.pdf"

INK = colors.HexColor("#191513")
MUTED = colors.HexColor("#5e5248")
RED = colors.HexColor("#a82924")
JADE = colors.HexColor("#2f7462")
BLUE = colors.HexColor("#386d9f")
PAPER = colors.HexColor("#fff8ed")
PAPER_STRONG = colors.HexColor("#fff3df")
LINE = colors.HexColor("#eadbc9")


def rows(*items):
    return list(items)


SECTIONS = [
    {
        "title": "Time Words",
        "intro": "Use these to place a sentence in time. Spoken forms are often more natural in daily Hong Kong Cantonese.",
        "rows": rows(
            ("尋日", "cam4 jat6", "yesterday", "Spoken"),
            ("昨天", "zok3 tin1", "yesterday", "Written / formal"),
            ("今日", "gam1 jat6", "today", ""),
            ("聽日", "ting1 jat6", "tomorrow", "Spoken"),
            ("後日", "hau6 jat6", "the day after tomorrow", ""),
            ("琴晚", "kam4 maan5", "last night", "Spoken"),
            ("早啲", "zou2 di1", "earlier", ""),
            ("之前", "zi1 cin4", "before", ""),
            ("而家", "ji4 gaa1", "now", "Spoken"),
            ("之後", "zi1 hau6", "after / later", ""),
            ("稍後", "saau2 hau6", "later", "Written / formal"),
            ("遲啲", "ci4 di1", "later", "Spoken"),
            ("下次", "haa6 ci3", "next time", ""),
            ("上次", "soeng6 ci3", "last time", ""),
            ("今次", "gam1 ci3", "this time", ""),
            ("然後", "jin4 hau6", "then / afterwards", "Written"),
            ("星期", "sing1 kei4", "week", ""),
            ("一日", "jat1 jat6", "one day", ""),
            ("早上", "zou2 soeng5", "morning", "Written"),
            ("中午", "zung1 ng5", "noon", ""),
            ("下晝", "haa6 zau3", "afternoon", "Spoken"),
            ("黃昏", "wong4 fan1", "dusk / evening", ""),
            ("晚上", "maan5 soeng5", "evening / night", "Written"),
            ("嗰陣", "go2 zan6", "at that time / back then", "Spoken"),
        ),
    },
    {
        "title": "People, Demonstratives, Places",
        "intro": "These are the building blocks for saying who, what, and where.",
        "rows": rows(
            ("我", "ngo5", "I / me", ""),
            ("你", "nei5", "you", ""),
            ("佢", "keoi5", "he / she / they", "Singular in basic use"),
            ("哋", "dei6", "plural marker", "我哋 = we"),
            ("位", "wai6", "person; polite classifier", ""),
            ("自己", "zi6 gei2", "oneself", ""),
            ("呢個", "ni1 go3", "this one", ""),
            ("嗰個", "go2 go3", "that one", ""),
            ("呢啲", "ni1 di1", "these", ""),
            ("嗰啲", "go2 di1", "those", ""),
            ("呢度", "ni1 dou6", "here", ""),
            ("嗰度", "go2 dou6", "there", ""),
            ("餐廳", "caan1 teng1", "restaurant", ""),
            ("學校", "hok6 haau6", "school", ""),
            ("街", "gaai1", "street", ""),
            ("路", "lou6", "road", ""),
            ("市場", "si5 coeng4", "market", "Written; 街市 is common in speech"),
            ("公司", "gung1 si1", "company / office", ""),
            ("酒店", "zau2 dim3", "hotel", ""),
            ("醫院", "ji1 jyun2", "hospital", ""),
            ("藥房", "joek6 fong2", "pharmacy", ""),
            ("洗手間", "sai2 sau2 gaan1", "restroom / toilet", ""),
            ("商店", "soeng1 dim3", "shop / store", "Written"),
        ),
    },
    {
        "title": "Negation, To Be, Possession",
        "intro": "These small words appear everywhere. Learn them early and sentences become much easier to parse.",
        "rows": rows(
            ("唔", "m4", "not", "Main spoken negator"),
            ("係", "hai6", "to be", "Identity: 我係..."),
            ("嘅", "ge3", "possessive / descriptive particle", "我嘅 = my"),
            ("有", "jau5", "have / there is", ""),
            ("冇", "mou5", "not have / there is not", ""),
            ("有去過", "jau5 heoi3 gwo3", "have been to / have gone before", "Experience pattern"),
        ),
    },
    {
        "title": "Modal Words and Helpers",
        "intro": "These words tell you about ability, desire, obligation, possibility, and future meaning.",
        "rows": rows(
            ("識", "sik1", "know how to / have the ability to", ""),
            ("想", "soeng2", "want / would like / think", ""),
            ("鍾意", "zung1 ji3", "like", "Spoken"),
            ("喜歡", "hei2 fun1", "like", "Written"),
            ("想要", "soeng2 jiu3", "want to have / really want", ""),
            ("必須", "bit1 seoi1", "must", "Formal"),
            ("要", "jiu3", "want / need / have to", ""),
            ("應該", "jing1 goi1", "should", ""),
            ("會", "wui5", "will / can / likely to", ""),
            ("將會", "zoeng1 wui5", "will / going to", "Written"),
            ("可以", "ho2 ji5", "can / may", ""),
            ("可能", "ho2 nang4", "maybe / possible", ""),
            ("或者", "waak6 ze2", "or / perhaps", ""),
        ),
    },
    {
        "title": "Adverbs and Connectors",
        "intro": "These words change the rhythm of a sentence: frequency, amount, sequence, and contrast.",
        "rows": rows(
            ("常常", "soeng4 soeng4", "often", ""),
            ("有時", "jau5 si4", "sometimes", ""),
            ("從來都", "cung4 loi4 dou1", "always / ever / never", "Meaning depends on context and negation"),
            ("成日", "seng4 jat6", "all the time", "Spoken"),
            ("經常", "ging1 soeng4", "frequently", ""),
            ("以前", "ji5 cin4", "before / used to", ""),
            ("好多", "hou2 do1", "a lot / many", ""),
            ("一啲", "jat1 di1", "a little / some", ""),
            ("時時", "si4 si4", "always / often", ""),
            ("好少", "hou2 siu2", "rarely / very little", ""),
            ("咁", "gam3", "so / that much", ""),
            ("仲", "zung6", "still / also", ""),
            ("已經", "ji5 ging1", "already", ""),
            ("再", "zoi3", "again", ""),
            ("多次", "do1 ci3", "many times", ""),
            ("夠", "gau3", "enough", ""),
            ("都", "dou1", "all / also / even", ""),
            ("就", "zau6", "then / just / precisely", ""),
            ("只有", "zi2 jau5", "only have / there is only", ""),
            ("另外", "ling6 ngoi6", "in addition / another", ""),
            ("反對", "faan2 deoi3", "oppose / be against", ""),
            ("如果", "jyu4 gwo2", "if", ""),
            ("但係", "daan6 hai6", "but", "Spoken"),
            ("所以", "so2 ji5", "so / therefore", ""),
        ),
    },
    {
        "title": "Core Verbs",
        "intro": "The old sheet had many excellent starter verbs. This version keeps them together with clearer English.",
        "rows": rows(
            ("行", "haang4", "walk", ""),
            ("去", "heoi3", "go", ""),
            ("回", "wui4", "return", "Written"),
            ("食", "sik6", "eat", ""),
            ("飲", "jam2", "drink", ""),
            ("加", "gaa1", "add", ""),
            ("聞", "man4", "smell", ""),
            ("賣", "maai6", "sell", ""),
            ("買", "maai5", "buy", ""),
            ("笑", "siu3", "laugh", ""),
            ("哭", "huk1", "cry", "Written"),
            ("喊", "haam3", "cry", "Spoken"),
            ("用", "jung6", "use", ""),
            ("做", "zou6", "do / make", ""),
            ("見", "gin3", "see / meet", ""),
            ("讀", "duk6", "read / study", ""),
            ("寫", "se2", "write", ""),
            ("知", "zi1", "know", ""),
            ("講", "gong2", "speak / say", ""),
            ("傾", "king1", "chat", "Spoken"),
            ("搭", "daap3", "take / ride", "Transport"),
            ("嚟", "lei4", "come", "Spoken"),
            ("打", "daa2", "hit / call / play", "Meaning depends on object"),
            ("坐", "co5", "sit / ride", ""),
            ("站", "zaam6", "stand", "Written"),
            ("揾", "wan2", "look for / find", "Spoken"),
            ("找", "zaau2", "find / look for", "Written; also settle a bill/change in some contexts"),
            ("住", "zyu6", "live / stay", ""),
            ("試", "si3", "try", ""),
            ("玩", "waan2", "play", ""),
            ("記", "gei3", "remember", ""),
            ("拉", "laai1", "pull", ""),
            ("推", "teoi1", "push", ""),
            ("睇", "tai2", "watch / see / read", "Spoken"),
            ("聽", "teng1", "listen / hear", ""),
            ("收", "sau1", "receive / accept", ""),
            ("比", "bei2", "compare / than", ""),
            ("畀", "bei2", "give / to", "Common Cantonese character"),
            ("俾", "bei2", "give / allow", "Variant form"),
            ("入", "jap6", "enter", ""),
            ("離開", "lei4 hoi1", "leave", ""),
            ("關", "gwaan1", "close", ""),
            ("開", "hoi1", "open / turn on", ""),
            ("明白", "ming4 baak6", "understand", ""),
            ("停", "ting4", "stop", ""),
            ("學", "hok6", "learn", ""),
            ("錫", "sek3", "kiss / cherish", "Spoken"),
            ("熄", "sik1", "turn off / extinguish", ""),
        ),
    },
    {
        "title": "Home and Everyday Nouns",
        "intro": "A practical set for describing rooms, furniture, and things around the home.",
        "rows": rows(
            ("啲嘢", "di1 je5", "things / something", "Spoken"),
            ("嘢", "je5", "stuff / thing", "Spoken"),
            ("房間", "fong4 gaan1", "room", ""),
            ("桌子", "coek3 zi2", "table", "Written; 枱 toi2 is common in speech"),
            ("椅子", "ji2 zi2", "chair", ""),
            ("公寓", "gung1 jyu6", "apartment", "Written"),
            ("廚房", "cyu4 fong2", "kitchen", ""),
            ("客廳", "haak3 teng1", "living room", ""),
            ("睡房", "seoi6 fong2", "bedroom", ""),
            ("臥室", "ngo6 sat1", "bedroom", "Written"),
            ("陽台", "joeng4 toi4", "balcony", ""),
            ("浴室", "juk6 sat1", "bathroom", ""),
            ("門", "mun4", "door", ""),
            ("窗", "coeng1", "window", ""),
            ("梳化", "so1 faa3", "sofa", "Loanword"),
            ("冰箱", "bing1 soeng1", "refrigerator", "Written; 雪櫃 syut3 gwai6 is common"),
            ("爐頭", "lou4 tau4", "stove", ""),
            ("微波爐", "mei4 bo1 lou4", "microwave", ""),
            ("洗衣機", "sai2 ji1 gei1", "washing machine", ""),
            ("乾衣機", "gon1 ji1 gei1", "dryer", ""),
            ("書架", "syu1 gaa3", "bookshelf", ""),
            ("櫃子", "gwai6 zi2", "cabinet", ""),
            ("風扇", "fung1 sin3", "fan", ""),
            ("燈", "dang1", "lamp / light", ""),
            ("空調", "hung1 tiu4", "air conditioner", "Written; 冷氣 laang5 hei3 is common"),
            ("窗簾", "coeng1 lim4", "curtain", ""),
            ("味", "mei6", "taste / smell / flavour", ""),
        ),
    },
    {
        "title": "Measure Words and Quantifiers",
        "intro": "Cantonese uses classifiers between numbers and nouns. 個 is common, but specific nouns often prefer specific measure words.",
        "rows": rows(
            ("個", "go3", "general classifier", "Very common"),
            ("每個", "mui5 go3", "every", ""),
            ("杯", "bui1", "cup / glass", ""),
            ("片", "pin3", "slice / piece", ""),
            ("頂", "deng2", "for hats / things on the head", ""),
            ("棵", "fo1", "for plants / trees", ""),
            ("隻", "zek3", "for animals / one of a pair", ""),
            ("架", "gaa3", "for vehicles / large machines", ""),
            ("行", "hong4", "line / row", ""),
            ("打", "daa1", "dozen", ""),
            ("篇", "pin1", "article / written piece", ""),
            ("碗", "wun2", "bowl", ""),
            ("粒", "nap1", "small round object", ""),
            ("餐", "caan1", "meal", ""),
            ("份", "fan6", "portion / copy / document", ""),
            ("啲", "di1", "some / plural-like amount", "Informal and very common"),
            ("全部", "cyun4 bou6", "all", ""),
            ("幾個", "gei2 go3", "a few / several", ""),
            ("少數", "siu2 sou3", "few / minority", ""),
            ("任何", "jam6 ho4", "any", ""),
            ("好多", "hou2 do1", "many / a lot", ""),
            ("各", "gok3", "each", ""),
            ("無數", "mou4 sou3", "countless", ""),
            ("其他", "kei4 taa1", "other", ""),
            ("所有", "so2 jau5", "all / every", ""),
            ("左右", "zo2 jau6", "about / approximately", ""),
        ),
    },
    {
        "title": "Question Words",
        "intro": "Many Cantonese question words stay in the place where the answer would appear.",
        "rows": rows(
            ("邊個", "bin1 go3", "who", ""),
            ("邊度", "bin1 dou6", "where", ""),
            ("點解", "dim2 gaai2", "why", ""),
            ("幾時", "gei2 si4", "when", ""),
            ("點", "dim2", "how", ""),
            ("邊", "bin1", "which", ""),
            ("幾多", "gei2 do1", "how many / how much", ""),
            ("做乜", "zou6 mat1", "why / what are you doing", "Colloquial"),
            ("乜", "mat1", "what", ""),
        ),
    },
    {
        "title": "Final Particles and Aspect Markers",
        "intro": "Particles carry tone, attitude, completion, and sentence texture. Do not translate them word for word.",
        "rows": rows(
            ("呀", "aa3", "softens tone / exclamation / choice question", "Very common"),
            ("吖", "aa1 / aa4", "soft suggestion / gentle ending", ""),
            ("喇", "laa3", "change of state / soft request / already", ""),
            ("啦", "laa1 / laa3", "let's / please / sentence ending", ""),
            ("架", "gaa3", "assertion / context marker", "Often combines with 嘅"),
            ("㗎", "gaa3", "assertive ending", "嘅 + 架"),
            ("嘞", "laak3", "completion / change", ""),
            ("咗", "zo2", "completed action", "Aspect marker"),
            ("緊", "gan2", "ongoing action", "Aspect marker"),
            ("過", "gwo3", "experience before", "Aspect marker"),
            ("住", "zyu6", "continuing state", "Aspect marker"),
        ),
    },
]


def p(text, style):
    escaped = escape(str(text))
    escaped = re.sub(
        r"([\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef]+)",
        r'<font name="STSong-Light">\1</font>',
        escaped,
    )
    return Paragraph(escaped, style)


def term_table(section, styles):
    data = [[p("Word", styles["TableHead"]), p("Jyutping", styles["TableHead"]), p("English", styles["TableHead"]), p("Use / note", styles["TableHead"])]]
    for hanzi, jyutping, english, note in section["rows"]:
        data.append(
            [
                p(hanzi, styles["HanziCell"]),
                p(jyutping, styles["SmallCell"]),
                p(english, styles["Cell"]),
                p(note or " ", styles["SmallCell"]),
            ]
        )

    table = Table(data, colWidths=[27 * mm, 32 * mm, 56 * mm, 50 * mm], repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#fffdf8")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fffdf8"), PAPER]),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def page_canvas(canvas, doc):
    canvas.saveState()
    width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 14 * mm, width - 18 * mm, 14 * mm)
    canvas.setFont("Helvetica-Bold", 7.5)
    canvas.setFillColor(RED)
    canvas.drawString(18 * mm, 9 * mm, "HKGong Cantonese Starter Reference")
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawRightString(width - 18 * mm, 9 * mm, f"hkgong.com  ·  {doc.page}")
    canvas.restoreState()


def build():
    registerFont(UnicodeCIDFont("STSong-Light"))

    base = getSampleStyleSheet()
    styles = {
        "Title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=31,
            leading=34,
            textColor=INK,
            spaceAfter=10,
        ),
        "Subtitle": ParagraphStyle(
            "Subtitle",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=12.5,
            leading=17,
            textColor=MUTED,
            spaceAfter=10,
        ),
        "Eyebrow": ParagraphStyle(
            "Eyebrow",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=RED,
            uppercase=True,
            spaceBefore=4,
            spaceAfter=6,
        ),
        "Heading": ParagraphStyle(
            "Heading",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=17,
            leading=20,
            textColor=INK,
            spaceBefore=13,
            spaceAfter=5,
        ),
        "Body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.7,
            leading=13.8,
            textColor=colors.HexColor("#3d352f"),
            spaceAfter=7,
        ),
        "Small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=11.2,
            textColor=MUTED,
            spaceAfter=4,
        ),
        "Hanzi": ParagraphStyle(
            "Hanzi",
            parent=base["BodyText"],
            fontName="STSong-Light",
            fontSize=23,
            leading=28,
            textColor=INK,
            spaceAfter=4,
        ),
        "TableHead": ParagraphStyle(
            "TableHead",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=colors.white,
        ),
        "Cell": ParagraphStyle(
            "Cell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.2,
            leading=10.4,
            textColor=colors.HexColor("#2f2a26"),
        ),
        "CellBold": ParagraphStyle(
            "CellBold",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=8.4,
            leading=10.6,
            textColor=INK,
        ),
        "SmallCell": ParagraphStyle(
            "SmallCell",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=9.6,
            textColor=MUTED,
        ),
        "HanziCell": ParagraphStyle(
            "HanziCell",
            parent=base["BodyText"],
            fontName="STSong-Light",
            fontSize=12.5,
            leading=15,
            textColor=INK,
        ),
    }

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="HKGong Cantonese Starter Reference",
        author="HKGong",
    )

    story = [
        p("HKGong Cantonese Starter Reference", styles["Title"]),
        p(
            "A cleaner English rebuild of the original Cantonese character/vocabulary sheet: core words, "
            "Jyutping, meanings, usage notes, particles, measure words, and home vocabulary.",
            styles["Subtitle"],
        ),
        Spacer(1, 7),
    ]

    overview = Table(
        [
            [p("How to read the tables", styles["TableHead"]), p("Why it matters", styles["TableHead"])],
            [
                p("Word = Cantonese characters. Jyutping = pronunciation. English = practical meaning. Use / note = spoken, written, formal, or pattern guidance.", styles["Cell"]),
                p("Cantonese is easier when you learn the sound, the written form, and the sentence job together instead of memorizing isolated translations.", styles["Cell"]),
            ],
            [
                p("Spoken", styles["CellBold"]),
                p("Natural in conversation. These are often the forms you hear in Hong Kong daily speech.", styles["Cell"]),
            ],
            [
                p("Written", styles["CellBold"]),
                p("More formal or closer to standard written Chinese. Useful for reading, signs, subtitles, and formal text.", styles["Cell"]),
            ],
        ],
        colWidths=[78 * mm, 87 * mm],
    )
    overview.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("BACKGROUND", (0, 1), (-1, -1), PAPER),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.extend(
        [
            overview,
            Spacer(1, 13),
            p("A first sentence to keep in mind", styles["Eyebrow"]),
            p("你好，我想學廣東話。", styles["Hanzi"]),
            p("nei5 hou2, ngo5 soeng2 hok6 gwong2 dung1 waa2.", styles["Body"]),
            p(
                "Hello, I want to learn Cantonese. Notice the pattern: greeting + I + want + learn + Cantonese. "
                "This reference is designed to help you see those parts clearly.",
                styles["Body"],
            ),
            PageBreak(),
        ]
    )

    for index, section in enumerate(SECTIONS):
        block = [
            p(section["title"], styles["Heading"]),
            p(section["intro"], styles["Small"]),
            term_table(section, styles),
            Spacer(1, 9),
        ]
        story.extend(block)
        if index in {1, 3, 5, 7}:
            story.append(PageBreak())

    story.extend(
        [
            PageBreak(),
            p("Mini Sentence Patterns", styles["Heading"]),
            p("Use these patterns as simple anchors while you study the vocabulary above.", styles["Small"]),
        ]
    )
    pattern_rows = [
        ["Pattern", "Example", "Meaning"],
        ["Subject + 唔 + Verb", "我唔識。 ngo5 m4 sik1.", "I do not know how."],
        ["Subject + 想 + Verb", "我想學。 ngo5 soeng2 hok6.", "I want to learn."],
        ["Subject + 係 + Noun", "佢係老師。 keoi5 hai6 lou5 si1.", "She/he is a teacher."],
        ["喺 + Place", "我喺睡房。 ngo5 hai2 seoi6 fong2.", "I am in the bedroom."],
        ["Verb + 咗", "我食咗。 ngo5 sik6 zo2.", "I ate / I have eaten."],
        ["Verb + 緊", "我學緊。 ngo5 hok6 gan2.", "I am learning."],
        ["有 + Noun", "呢度有餐廳。 ni1 dou6 jau5 caan1 teng1.", "There is a restaurant here."],
        ["Question word in place", "你去邊度？ nei5 heoi3 bin1 dou6?", "Where are you going?"],
    ]
    pattern_table = Table(
        [[p(cell, styles["TableHead"]) for cell in pattern_rows[0]]]
        + [[p(cell, styles["Cell"]) for cell in row] for row in pattern_rows[1:]],
        colWidths=[42 * mm, 60 * mm, 63 * mm],
        repeatRows=1,
    )
    pattern_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), INK),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#fffdf8"), PAPER]),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.extend(
        [
            pattern_table,
            Spacer(1, 14),
            p("Keep learning with HKGong", styles["Heading"]),
            p(
                "Open HKGong and connect the parts: sounds, words, sentence structure, examples, characters, listening, writing, and practice. "
                "The goal is not to memorize a sheet. The goal is to make Cantonese feel organized enough to keep going.",
                styles["Body"],
            ),
            p("Download HKGong: https://hkgong.com", styles["Body"]),
        ]
    )

    doc.build(story, onFirstPage=page_canvas, onLaterPages=page_canvas)


if __name__ == "__main__":
    build()
    print(f"Wrote {OUT}")
