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
legacy = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
header = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;"
edge = "endArrow=block;html=1;rounded=0;"

# Context diagram
cells = []
cells.append(cell("title", "C4 Context. MVP открытия депозитов онлайн", header, "1", "0", x=20, y=20, w=1300, h=40))

nodes = {
    "client": ("Клиент банка", person, 80, 170, 90, 120),
    "new_client": ("Новый клиент", person, 80, 420, 90, 120),
    "back_deposit": ("Бэк-офис депозитов", person, 1180, 130, 120, 120),
    "back_credit": ("Бэк-офис кредитов", person, 1180, 330, 120, 120),
    "cc_operator": ("Оператор кол-центра", person, 1180, 540, 120, 120),

    "site": ("Сайт банка", system, 280, 430, 190, 80),
    "ibank": ("Интернет-банк", system, 280, 180, 190, 80),
    "deposit_platform": ("Платформа депозитных заявок и ставок<br><b>новый домен MVP</b>", new, 580, 250, 270, 150),
    "abs": ("АБС<br>core banking", legacy, 930, 230, 210, 100),
    "cc": ("Система кол-центра", system, 930, 540, 210, 90),
    "sms": ("СМС-шлюз телеком-оператора", external, 580, 570, 250, 80),
}

for id_, (label, style, x, y, w, h) in nodes.items():
    cells.append(cell(id_, label, style, "1", "0", x=x, y=y, w=w, h=h))

flows = [
    ("client", "ibank", "подаёт заявку на депозит"),
    ("new_client", "site", "оставляет заявку и телефон"),
    ("ibank", "deposit_platform", "создание заявки, получение ставок, СМС-подтверждение"),
    ("site", "deposit_platform", "создание заявки, получение публичных ставок"),
    ("deposit_platform", "abs", "контролируемая интеграция без прямого доступа к БД"),
    ("deposit_platform", "sms", "СМС-коды и уведомления"),
    ("sms", "client", "уведомления"),
    ("sms", "new_client", "уведомления"),
    ("back_deposit", "abs", "обработка заявки и открытие депозита"),
    ("back_deposit", "deposit_platform", "управление ставками и статусами"),
    ("back_credit", "deposit_platform", "данные для специальных ставок"),
    ("cc_operator", "cc", "работа с обращениями клиентов"),
    ("deposit_platform", "cc", "передача заявок с сайта / статусов"),
]

for i, (src, tgt, label) in enumerate(flows):
    cells.append(cell(f"edge_{i}", label, edge, "0", "1", source=src, target=tgt))

cells.append(cell("note", "MVP: онлайн-каналы принимают заявки, но финальное подтверждение и открытие депозита выполняет бэк-офис через АБС. Прямая интеграция интернет-банка с БД АБС в новом процессе не используется.", new, "1", "0", x=170, y=720, w=1040, h=80))

make_mxfile(cells, "Task3/c4-context-online-deposits-mvp.drawio")

# Container diagram
cells = []
cells.append(cell("title", "C4 Container. MVP открытия депозитов онлайн", header, "1", "0", x=20, y=20, w=1500, h=40))

nodes = {
    "client": ("Клиент банка", person, 60, 140, 90, 120),
    "new_client": ("Новый клиент", person, 60, 400, 90, 120),
    "back": ("Бэк-офис депозитов", person, 1360, 130, 120, 120),
    "credit": ("Бэк-офис кредитов", person, 1360, 360, 120, 120),

    "site_front": ("Website UI<br>PHP + React.js", system, 230, 420, 210, 80),

    "ibank_ui": ("Internet Bank UI / Deposit Module<br>ASP.NET MVC 4.5", system, 230, 140, 240, 90),
    "ibank_db": ("Internet Bank DB<br>MS SQL", database, 250, 260, 190, 80),

    "app_api": ("Deposit Application Service<br>Java Spring Boot / REST API", new, 600, 190, 260, 100),
    "app_db": ("Deposit Applications DB<br>PostgreSQL или MS SQL", database, 630, 330, 210, 80),

    "rates_api": ("Deposit Rates Service<br>ставки, продукты, версии", new, 600, 470, 260, 100),
    "rates_db": ("Deposit Rates DB<br>история ставок и аудит", database, 630, 610, 210, 80),

    "abs_adapter": ("ABS Integration Adapter<br>контроль нагрузки, retry, API facade", new, 930, 220, 260, 100),
    "sms_adapter": ("SMS Adapter<br>коды и уведомления", new, 930, 470, 220, 90),

    "abs_client": ("ABS Desktop Client<br>Delphi", legacy, 1230, 130, 210, 80),
    "abs_logic": ("ABS Business Logic<br>PL/SQL procedures", legacy, 1230, 260, 230, 90),
    "abs_db": ("ABS DB<br>Oracle", database, 1250, 400, 190, 90),

    "sms_gateway": ("SMS Gateway<br>телеком-оператор", external, 1230, 560, 220, 80),
    "cc_system": ("Call Center System<br>React + Java Spring Boot + PostgreSQL", system, 930, 680, 280, 90),
}

for id_, (label, style, x, y, w, h) in nodes.items():
    cells.append(cell(id_, label, style, "1", "0", x=x, y=y, w=w, h=h))

flows = [
    ("client", "ibank_ui", "подаёт заявку"),
    ("new_client", "site_front", "оставляет заявку"),
    ("ibank_ui", "ibank_db", "текущие данные интернет-банка"),
    ("ibank_ui", "app_api", "REST: создать заявку, подтвердить СМС"),
    ("ibank_ui", "rates_api", "REST: получить ставки"),
    ("site_front", "app_api", "REST: заявка нового клиента"),
    ("site_front", "rates_api", "REST: публичные ставки"),
    ("app_api", "app_db", "заявки, статусы, аудит"),
    ("app_api", "rates_api", "проверка условий"),
    ("rates_api", "rates_db", "ставки, версии, аудит"),
    ("app_api", "abs_adapter", "передать заявку / получить статус"),
    ("abs_adapter", "abs_logic", "контролируемые вызовы процедур/API"),
    ("abs_logic", "abs_db", "операции core banking"),
    ("back", "abs_client", "обработка заявки в MVP"),
    ("abs_client", "abs_logic", "операции открытия депозита"),
    ("credit", "rates_api", "параметры для специальных ставок"),
    ("app_api", "sms_adapter", "отправить код/уведомление"),
    ("sms_adapter", "sms_gateway", "SMS API"),
    ("sms_gateway", "client", "СМС"),
    ("sms_gateway", "new_client", "СМС"),
    ("app_api", "cc_system", "заявки с сайта / статусы для звонков"),
]

for i, (src, tgt, label) in enumerate(flows):
    cells.append(cell(f"edge_{i}", label, edge, "0", "1", source=src, target=tgt))

cells.append(cell("note", "Детализация: интернет-банк остаётся монолитом, но новый депозитный процесс вынесен во внешние сервисы. АБС остаётся системой учёта, доступ к ней закрыт адаптером. Ставки и заявки вынесены из Excel/email в управляемые сервисы.", new, "1", "0", x=180, y=860, w=1180, h=80))

make_mxfile(cells, "Task3/c4-container-online-deposits-mvp.drawio")

print("Created Task3/c4-context-online-deposits-mvp.drawio")
print("Created Task3/c4-container-online-deposits-mvp.drawio")
