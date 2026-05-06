from pathlib import Path
from xml.sax.saxutils import escape
import uuid

def cell(id_, value="", style="", vertex="0", edge="0", parent="1", source=None, target=None, x=None, y=None, w=None, h=None):
    attrs = [f'id="{id_}"']
    if value:
        attrs.append(f'value="{escape(value)}"')
    if style:
        attrs.append(f'style="{style}"')
    attrs.append(f'vertex="{vertex}"')
    attrs.append(f'edge="{edge}"')
    attrs.append(f'parent="{parent}"')
    if source:
        attrs.append(f'source="{source}"')
    if target:
        attrs.append(f'target="{target}"')
    if vertex == "1":
        geom = f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>'
    elif edge == "1":
        geom = '<mxGeometry relative="1" as="geometry"/>'
    else:
        geom = ""
    return f'<mxCell {" ".join(attrs)}>{geom}</mxCell>'

def make_mxfile(cells, filename):
    xml = f'''<mxfile host="app.diagrams.net">
  <diagram name="Page-1" id="{uuid.uuid4()}">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1700" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {''.join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    Path(filename).write_text(xml, encoding="utf-8")

person = "shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;outlineConnect=0;"
system = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
new = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
external = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
database = "shape=cylinder3d;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=15;fillColor=#e1d5e7;strokeColor=#9673a6;"
manual = "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
legacy = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
header = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;"
phase = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
done = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
risk = "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
edge = "endArrow=block;html=1;rounded=0;"

# Context diagram
cells = []
cells.append(cell("title", "C4 Context. Передача ставок в кол-центры", header, "1", "0", x=20, y=20, w=1350, h=40))

nodes = {
    "client": ("Клиент", person, 60, 180, 90, 120),
    "operator": ("Оператор внутреннего кол-центра", person, 60, 430, 130, 120),
    "partner_operator": ("Оператор партнёрского кол-центра", person, 60, 650, 140, 120),
    "back": ("Бэк-офис депозитов", person, 1180, 150, 120, 120),
    "credit": ("Бэк-офис кредитов", person, 1180, 360, 120, 120),

    "rates": ("Deposit Rates Service<br><b>единый источник ставок</b>", new, 520, 250, 260, 120),
    "internal_cc": ("Система кол-центра банка", system, 350, 430, 240, 90),
    "export": ("Rate Export Service", new, 820, 520, 220, 90),
    "sftp": ("SFTP<br>файловый обмен", external, 820, 680, 220, 80),
    "partner_cc": ("Система партнёрского кол-центра", external, 350, 650, 260, 90),
    "site_ibank": ("Сайт и интернет-банк", system, 350, 120, 240, 90),
}

for id_, (label, style, x, y, w, h) in nodes.items():
    cells.append(cell(id_, label, style, "1", "0", x=x, y=y, w=w, h=h))

flows = [
    ("back", "rates", "обновляет базовые ставки"),
    ("credit", "rates", "параметры специальных условий"),
    ("site_ibank", "rates", "получают ставки для онлайн-каналов"),
    ("internal_cc", "rates", "получает актуальные ставки через API/адаптер"),
    ("operator", "internal_cc", "консультирует клиента"),
    ("client", "operator", "звонок по депозиту"),
    ("rates", "export", "актуальная версия ставок"),
    ("export", "sftp", "публикация CSV/XLSX"),
    ("sftp", "partner_cc", "загрузка файла"),
    ("partner_operator", "partner_cc", "консультации по файлу ставок"),
    ("client", "partner_operator", "звонок при перегрузке банка"),
]

for i, (src, tgt, label) in enumerate(flows):
    cells.append(cell(f"edge_{i}", label, edge, "0", "1", source=src, target=tgt))

cells.append(cell("note", "MVP: внутренний кол-центр получает ставки из Deposit Rates Service, партнёрский кол-центр получает файл через SFTP. Персональные данные в файл не передаются.", new, "1", "0", x=200, y=820, w=1060, h=70))

make_mxfile(cells, "Task4/c4-context-call-center-rates.drawio")

# Component diagram
cells = []
cells.append(cell("title", "C4 Component. Компоненты передачи ставок в кол-центры", header, "1", "0", x=20, y=20, w=1500, h=40))

nodes = {
    "back": ("Бэк-офис депозитов", person, 60, 120, 120, 120),
    "credit": ("Бэк-офис кредитов", person, 60, 330, 120, 120),
    "operator": ("Оператор кол-центра", person, 60, 570, 120, 120),

    "rates_admin": ("Rates Admin UI<br>управление ставками", new, 270, 120, 220, 80),
    "rates_api": ("Deposit Rates API<br>REST", new, 550, 160, 230, 90),
    "rates_db": ("Deposit Rates DB<br>версии, аудит, продукты", database, 560, 300, 210, 90),

    "cc_adapter": ("Call Center Rates Adapter<br>sync/cache/format mapping", new, 850, 420, 260, 100),
    "cc_db": ("Call Center DB<br>локальный кеш ставок", database, 870, 560, 220, 80),
    "cc_ui": ("Call Center UI<br>экран консультации", system, 850, 690, 260, 90),

    "export_service": ("Rate Export Service<br>CSV/XLSX generator", new, 850, 150, 250, 100),
    "export_log": ("Export Journal DB<br>статусы и аудит", database, 870, 290, 220, 80),
    "sftp": ("Bank SFTP Server<br>protected file exchange", external, 1180, 180, 230, 90),
    "partner": ("Partner Call Center System<br>external", external, 1180, 360, 250, 90),
    "monitoring": ("Monitoring & Alerts", system, 1180, 560, 230, 80),
}

for id_, (label, style, x, y, w, h) in nodes.items():
    cells.append(cell(id_, label, style, "1", "0", x=x, y=y, w=w, h=h))

flows = [
    ("back", "rates_admin", "вносит ставки"),
    ("credit", "rates_admin", "параметры спец. условий"),
    ("rates_admin", "rates_api", "сохранить версию"),
    ("rates_api", "rates_db", "read/write"),
    ("cc_adapter", "rates_api", "получает актуальные ставки"),
    ("cc_adapter", "cc_db", "обновляет кеш"),
    ("cc_ui", "cc_db", "читает ставки"),
    ("operator", "cc_ui", "консультирует клиента"),
    ("export_service", "rates_api", "получает версию ставок"),
    ("export_service", "export_log", "статус экспорта"),
    ("export_service", "sftp", "публикует файл"),
    ("partner", "sftp", "забирает файл"),
    ("export_service", "monitoring", "метрики и ошибки"),
    ("cc_adapter", "monitoring", "метрики sync"),
]

for i, (src, tgt, label) in enumerate(flows):
    cells.append(cell(f"edge_{i}", label, edge, "0", "1", source=src, target=tgt))

cells.append(cell("note", "Компонентная схема показывает только изменения для кейса ставок. Ключевые решения: единый источник ставок, кеш для внутреннего кол-центра, файловый экспорт через SFTP для партнёра, журнал и мониторинг экспорта.", new, "1", "0", x=220, y=860, w=1120, h=70))

make_mxfile(cells, "Task4/c4-component-call-center-rates.drawio")

# Roadmap diagram
cells = []
cells.append(cell("title", "RoadMap. MVP депозитов и передача ставок в кол-центры", header, "1", "0", x=20, y=20, w=1500, h=40))

# Timeline header
months = ["М1", "М2", "М3", "М4", "М5", "М6", "Год"]
x0, y0 = 220, 100
month_w = 160
for i, m in enumerate(months):
    cells.append(cell(f"m_{i}", m, header, "1", "0", x=x0+i*month_w, y=y0, w=month_w, h=50))

lanes = [
    ("Deposit Rates Service", [
        ("Модель ставок<br>версии и аудит", 0, 2, phase),
        ("API ставок<br>для сайта/ИБ/КЦ", 2, 2, phase),
        ("Расширение под авто-открытие", 6, 1, done),
    ]),
    ("Deposit Application Service", [
        ("API заявок<br>сайт + интернет-банк", 1, 2, phase),
        ("Статусы, аудит,<br>интеграция СМС", 3, 2, phase),
        ("Автоматизация открытия<br>без бэк-офиса", 6, 1, done),
    ]),
    ("Интернет-банк и сайт", [
        ("Формы заявки<br>и список депозитов", 1, 2, phase),
        ("СМС-подтверждение<br>и статусы", 3, 2, phase),
        ("Полностью онлайн<br>открытие депозита", 6, 1, done),
    ]),
    ("АБС и бэк-офис", [
        ("Интеграционный адаптер<br>и операции MVP", 2, 2, phase),
        ("Регламенты обработки<br>заявок MVP", 4, 1, risk),
        ("Убрать участие<br>бэк-офиса", 6, 1, done),
    ]),
    ("Внутренний кол-центр", [
        ("Скрипты консультаций<br>и требования", 0, 1, risk),
        ("Rates Adapter<br>и кеш ставок", 2, 2, phase),
        ("Экран ставок<br>для оператора", 4, 1, phase),
        ("Обучение операторов", 5, 1, risk),
    ]),
    ("Партнёрский кол-центр", [
        ("Согласовать формат<br>CSV/XLSX", 1, 1, risk),
        ("SFTP и тестовый обмен", 3, 1, phase),
        ("Промышленный<br>файловый экспорт", 4, 2, phase),
        ("Оптимизация SLA<br>и автоматизация", 6, 1, done),
    ]),
    ("Эксплуатация и безопасность", [
        ("TLS, доступы,<br>аудит", 1, 2, risk),
        ("Мониторинг,<br>alerting, retry", 3, 2, phase),
        ("DR-план<br>резервный ЦОД", 5, 1, risk),
        ("Целевой SLA 99,9%", 6, 1, done),
    ]),
]

lane_h = 95
for r, (lane, tasks) in enumerate(lanes):
    y = y0 + 60 + r * lane_h
    cells.append(cell(f"lane_{r}", lane, header, "1", "0", x=20, y=y, w=190, h=lane_h-10))
    for t, (label, start, duration, style) in enumerate(tasks):
        cells.append(cell(f"task_{r}_{t}", label, style, "1", "0", x=x0+start*month_w+5, y=y+10, w=duration*month_w-10, h=lane_h-30))

# Milestones
cells.append(cell("milestone_mvp", "<b>MVP через 6 месяцев</b><br>заявки онлайн + ставки в кол-центрах", done, "1", "0", x=x0+5*month_w+15, y=820, w=300, h=70))
cells.append(cell("milestone_year", "<b>Целевое состояние через год</b><br>депозит открывается автоматически без бэк-офиса", done, "1", "0", x=x0+6*month_w+5, y=820, w=190, h=90))

make_mxfile(cells, "Task4/roadmap-call-center-rates.drawio")

print("Created Task4/c4-context-call-center-rates.drawio")
print("Created Task4/c4-component-call-center-rates.drawio")
print("Created Task4/roadmap-call-center-rates.drawio")
