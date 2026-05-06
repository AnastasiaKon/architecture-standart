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
    <mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1600" pageHeight="1200" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {''.join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    Path(filename).write_text(xml, encoding="utf-8")

box = "rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;"
system = "rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;"
external = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;"
manual = "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;"
bad = "rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;"
header = "rounded=0;whiteSpace=wrap;html=1;fillColor=#e1d5e7;strokeColor=#9673a6;fontStyle=1;"
edge = "endArrow=block;html=1;rounded=0;"

# --- Diagram 1: IT landscape map ---
cells = []
cells.append(cell("title", "Task1. Карта текущего IT-ландшафта банка «Стандарт»", header, "1", "0", x=20, y=20, w=1220, h=40))

cols = [
    "Маркетинг и информация о продуктах",
    "Продажи и консультации",
    "Заявки на депозит",
    "Расчёт и согласование ставок",
    "Открытие депозитов и счетов",
    "Платежи",
    "Уведомления клиентов",
    "IT-разработка и сопровождение",
]
rows = [
    ("Сайт", "PHP + React.js", ["Сайт показывает маркетинговую информацию", "", "", "", "", "", "", "Собственная разработка банка"]),
    ("Интернет-банк", "ASP.NET MVC 4.5 + MS SQL", ["", "", "", "", "Открытие текущих счетов / дебетовых карт", "Платежи", "", "Платформа подрядчика, банк может дорабатывать часть функциональности"]),
    ("АБС", "Delphi client + Oracle + PL/SQL", ["", "", "Получает обращения из кол-центра", "Хранит клиентские и банковские данные, данные кредитного риска", "Учёт операций, открытие депозитов сотрудником фронт-офиса", "Банковский учёт операций", "Отправляет команды в СМС-шлюз", "Разработка внутри банка"]),
    ("Система кол-центра банка", "React.js + Java Spring Boot + PostgreSQL", ["", "Операторы консультируют клиентов", "Заводит обращения, передаёт в АБС", "", "", "", "", "Поддержка подрядчиком, возможны расширения"]),
    ("Партнёрский кол-центр", "Внешняя система партнёра", ["", "Работает по скриптам банка", "", "", "", "", "", "Внешняя система, API-интеграции нет"]),
    ("Excel-файлы ставок", "XLS + email", ["", "", "", "Основной инструмент расчёта ставок депозитов", "", "", "", "Ручной процесс, высокий операционный риск"]),
    ("Email", "Корпоративная почта", ["", "", "Передача запросов между отделением и бэк-офисом", "Передача ставок и данных между депозитами и кредитами", "", "", "", "Ручные согласования"]),
    ("СМС-шлюз", "Внешний телеком-оператор", ["", "", "", "", "", "", "СМС клиенту о ставке и необходимости прийти в отделение", "Поддержка IT банка + оператор"]),
]

x0, y0 = 20, 90
row_h = 70
col_w = 150
left_w = 210

cells.append(cell("org_header", "Система / участник", header, "1", "0", x=x0, y=y0, w=left_w, h=row_h))
for i, col in enumerate(cols):
    cells.append(cell(f"col_{i}", col, header, "1", "0", x=x0+left_w+i*col_w, y=y0, w=col_w, h=row_h))

for r, (name, tech, values) in enumerate(rows):
    y = y0 + row_h * (r + 1)
    cells.append(cell(f"row_{r}", f"<b>{name}</b><br>{tech}", header, "1", "0", x=x0, y=y, w=left_w, h=row_h))
    for c, val in enumerate(values):
        style = system if val and name not in ["Excel-файлы ставок", "Email"] else manual if val else "rounded=0;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#cccccc;"
        if "руч" in val.lower() or "риск" in val.lower() or "напрямую" in val.lower():
            style = bad
        cells.append(cell(f"cell_{r}_{c}", val, style, "1", "0", x=x0+left_w+c*col_w, y=y, w=col_w, h=row_h))

cells.append(cell("note", "Ключевые проблемы As-Is: прямой доступ интернет-банка к БД АБС, ручной расчёт ставок в Excel, согласования через email, высокая нагрузка на бэк-офис, отсутствие цифрового открытия депозитов.", bad, "1", "0", x=20, y=730, w=1220, h=70))

make_mxfile(cells, "Task1/current-it-landscape.drawio")

# --- Diagram 2: Integration diagram ---
cells = []
cells.append(cell("title", "Task1. Схема интеграции приложений As-Is", header, "1", "0", x=20, y=20, w=1200, h=40))

nodes = {
    "client": ("Клиент", box, 60, 130, 150, 60),
    "branch": ("Сотрудник отделения<br>фронт-офис", box, 60, 300, 180, 70),
    "cc_operator": ("Оператор кол-центра банка", box, 60, 470, 180, 70),
    "partner_cc": ("Партнёрский кол-центр", external, 60, 620, 180, 70),

    "site": ("Сайт<br>PHP + React.js", system, 330, 90, 190, 70),
    "ibank": ("Интернет-банк<br>ASP.NET MVC 4.5 + MS SQL", system, 330, 210, 210, 80),
    "abs": ("АБС<br>Delphi + Oracle + PL/SQL", system, 670, 260, 230, 90),
    "cc_system": ("Система кол-центра<br>React + Java Spring Boot + PostgreSQL", system, 330, 450, 240, 90),
    "partner_system": ("Внешняя система партнёрского кол-центра", external, 330, 620, 240, 70),

    "excel": ("Excel-файлы ставок<br>ежедневное обновление", manual, 670, 90, 220, 70),
    "email": ("Email<br>ручные согласования", manual, 670, 470, 220, 70),
    "sms": ("СМС-шлюз<br>телеком-оператор", external, 1000, 280, 190, 70),

    "deposit_back": ("Бэк-офис депозитов", box, 1000, 90, 190, 70),
    "credit_back": ("Бэк-офис кредитов", box, 1000, 470, 190, 70),
}

for id_, (label, style, x, y, w, h) in nodes.items():
    cells.append(cell(id_, label, style, "1", "0", x=x, y=y, w=w, h=h))

flows = [
    ("client", "site", "просмотр маркетинговой информации"),
    ("client", "ibank", "платежи и открытие текущих счетов"),
    ("ibank", "abs", "прямой доступ к БД АБС<br><b>проблемная интеграция</b>"),
    ("client", "branch", "визит для открытия депозита"),
    ("branch", "abs", "создание депозита, загрузка документов"),
    ("client", "cc_operator", "звонок с вопросом о депозите"),
    ("cc_operator", "cc_system", "создание обращения"),
    ("cc_system", "abs", "передача обращения в АБС"),
    ("abs", "sms", "СМС клиенту о ставке/визите"),
    ("sms", "client", "уведомление"),
    ("deposit_back", "excel", "расчёт депозитной ставки"),
    ("credit_back", "abs", "анализ кредитного риска клиента"),
    ("credit_back", "email", "передача данных риска"),
    ("email", "deposit_back", "ручное согласование специальных ставок"),
    ("branch", "email", "запрос ставки, если клиент пришёл без звонка"),
    ("email", "branch", "ответ со ставкой"),
    ("partner_cc", "partner_system", "работа по скриптам"),
]

for i, (src, tgt, label) in enumerate(flows):
    cells.append(cell(f"edge_{i}", label, edge, "0", "1", source=src, target=tgt))

cells.append(cell("problem", "Проблемы As-Is: депозит нельзя открыть онлайн; ставка рассчитывается вручную; бэк-офис участвует в каждом сложном кейсе; интернет-банк напрямую интегрирован с БД АБС; партнёрский кол-центр не получает актуальные ставки автоматически.", bad, "1", "0", x=60, y=760, w=1130, h=80))

make_mxfile(cells, "Task1/application-integration-as-is.drawio")

print("Created Task1/current-it-landscape.drawio")
print("Created Task1/application-integration-as-is.drawio")
