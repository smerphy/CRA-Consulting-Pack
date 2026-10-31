"""Shared styling, layout and chart helpers for the CRA pack Excel workbooks (client-neutral)."""
import re

from openpyxl.chart.axis import ChartLines
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.chart.text import RichText, Text
from openpyxl.chart.title import Title
from openpyxl.drawing.line import LineProperties
from openpyxl.drawing.text import CharacterProperties, Font as DFont, Paragraph, ParagraphProperties, RegularTextRun
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter, column_index_from_string
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.worksheet.hyperlink import Hyperlink
from openpyxl.worksheet.page import PageMargins
from openpyxl.worksheet.table import Table

C = dict(
    ink900="0E1A2B", ink700="26364D", ink500="56667E", ink300="C5CDD8", ink100="EEF1F5",
    paper="FAFAF7", white="FFFFFF", acc700="0A5753", acc600="0F6E6A", acc400="2E9C93", acc100="DCEFEC",
    signal="C2410C", red="B42318", amber="B54708", green="027A48", grey="8A94A6",
    blue="0000FF", link="008000", black="000000",
    navy="1F3A5F", steel="5B8DB8", sand="C9A66B", rust="B9573E",
    heat0="B42318", heat1="E07A5F", heat2="E9C46A", heat3="7FB8A4", heat4="0F6E6A",
)
BODY = "Arial"
DISPLAY = "Georgia"
FOOTER = "Illustrative"  # set per pack by set_footer()


def set_footer(ctx):
    """Print footer for every sheet: '<codename> · Illustrative · <issue date>'."""
    global FOOTER
    FOOTER = f"{ctx.codename} · Illustrative · {ctx.issue}"

NF_EUR = '#,##0;(#,##0);"-"'
NF_EUR1 = '#,##0.0;(#,##0.0);"-"'
NF_EUR2 = '#,##0.00;(#,##0.00);"-"'
NF_PCT0 = '0%;(0%);"-"'
NF_PCT1 = '0.0%;(0.0%);"-"'
NF_PCT2 = '0.00%;(0.00%);"-"'
NF_X = '0.0"x"'
NF_DEC1 = '0.0;(0.0);"-"'
NF_DEC2 = '0.00;(0.00);"-"'
NF_INT = '0;(0);"-"'
NF_DATE = 'd mmm yyyy'
NF_MONTH = 'mmm yyyy'
NF_EURM_SCALED = '"EUR "#,##0.0,,"m"'

PURE_LINK = re.compile(r"^=(?:'[^']+'|[A-Za-z0-9_\.]+)!\$?[A-Z]{1,3}\$?\d+$")


def fill(hex_):
    return PatternFill("solid", start_color=hex_, end_color=hex_)


def side(color, style="thin"):
    return Side(style=style, color=color)


B_ROW = Border(bottom=side(C["ink300"]))
B_NONE = Border()
B_TOTAL = Border(top=side(C["ink900"]), bottom=side(C["ink900"]))
B_SUB = Border(top=side(C["ink500"]))
B_BOX = Border(left=side(C["ink300"]), right=side(C["ink300"]), top=side(C["ink300"]), bottom=side(C["ink300"]))


def font(color=None, size=9, bold=False, italic=False, name=BODY, underline=None):
    return Font(name=name, size=size, bold=bold, italic=italic, color=color or C["ink900"], underline=underline)


def formula_color(value):
    """Modelling convention: pure cross-sheet link = green; any other formula = black."""
    if isinstance(value, str) and value.startswith("="):
        return C["link"] if PURE_LINK.match(value) else C["black"]
    return None


def put(ws, ref, value, kind="auto", fmt=None, bold=False, size=9, align=None, wrap=False, border=None,
        fill_hex=None, italic=False, color=None, valign="center", indent=0):
    """Write a value with the house style.
    kind: 'input' (blue on teal tint), 'label' (ink), 'auto' (formula colour convention or ink for text/numbers),
          'output' (white on teal), 'muted' (ink500)."""
    cell = ws[ref]
    cell.value = value
    if kind == "input":
        col = C["blue"]
        fill_hex = fill_hex or C["acc100"]
    elif kind == "output":
        col = C["white"]
        fill_hex = fill_hex or C["acc600"]
        bold = True
    elif kind == "muted":
        col = C["ink500"]
    elif kind == "label":
        col = C["ink900"]
    else:
        col = formula_color(value) or C["ink900"]
    if color:
        col = color
    cell.font = font(col, size=size, bold=bold, italic=italic)
    if fmt:
        cell.number_format = fmt
    h = align
    if h is None:
        h = "left" if (isinstance(value, str) and not value.startswith("=")) else None
    cell.alignment = Alignment(horizontal=h, vertical=valign, wrap_text=wrap, indent=indent)
    if border is not None:
        cell.border = border
    if fill_hex:
        cell.fill = fill(fill_hex)
    return cell


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


def col_range(c1, c2):
    a, b = column_index_from_string(c1), column_index_from_string(c2)
    return [get_column_letter(i) for i in range(a, b + 1)]


def band(ws, row, text, c1="B", c2="N", size=9):
    """Section band: ink-100 fill, bold ink-900 text."""
    for col in col_range(c1, c2):
        ws[f"{col}{row}"].fill = fill(C["ink100"])
    put(ws, f"{c1}{row}", text, kind="label", bold=True, size=size)
    ws.row_dimensions[row].height = 18


def header(ws, row, labels, c1="B", height=30, wrap=True, align_numeric_right=None):
    """Dark header row: ink-900 fill, white bold text. labels: list aligned from c1."""
    start = column_index_from_string(c1)
    for i, lab in enumerate(labels):
        col = get_column_letter(start + i)
        cell = ws[f"{col}{row}"]
        cell.value = lab
        cell.font = font(C["white"], size=9, bold=True)
        cell.fill = fill(C["ink900"])
        right = align_numeric_right and i in align_numeric_right
        cell.alignment = Alignment(horizontal="right" if right else "left", vertical="center", wrap_text=wrap)
    ws.row_dimensions[row].height = height


def title_block(ws, label, title, subtitle, link_col=None, title_size=15):
    put(ws, "B1", label, kind="muted", bold=True, size=8)
    c = put(ws, "B2", title, kind="label", bold=True, size=title_size)
    c.font = Font(name=DISPLAY, size=title_size, bold=True, color=C["ink900"])
    c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=False)
    ws.row_dimensions[2].height = 26
    put(ws, "B3", subtitle, kind="muted", size=9)
    if link_col:
        cell = ws[f"{link_col}1"]
        cell.value = "Back to Cover"
        cell.hyperlink = Hyperlink(ref=f"{link_col}1", location="'Cover'!A1", display="Back to Cover")
        cell.font = font(C["acc600"], size=8, bold=True, underline="single")
        cell.alignment = Alignment(horizontal="right")
    ws.sheet_view.showGridLines = False


def source_line(ws, ref, text):
    put(ws, ref, text, kind="muted", size=8, italic=True)


def add_list_dv(ws, rng, formula1, prompt=None, error=None):
    dv = DataValidation(type="list", formula1=formula1, allow_blank=True)
    if prompt:
        dv.promptTitle = "Select"
        dv.prompt = prompt
        dv.showInputMessage = True
    dv.error = error or "Choose a value from the list."
    dv.errorTitle = "Not in list"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)
    return dv


def add_whole_dv(ws, rng, lo, hi):
    dv = DataValidation(type="whole", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True)
    dv.error = f"Enter a whole number from {lo} to {hi}."
    dv.errorTitle = "Out of range"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)


def add_decimal_dv(ws, rng, lo, hi):
    dv = DataValidation(type="decimal", operator="between", formula1=str(lo), formula2=str(hi), allow_blank=True)
    dv.error = f"Enter a number from {lo} to {hi}."
    dv.errorTitle = "Out of range"
    dv.showErrorMessage = True
    ws.add_data_validation(dv)
    dv.add(rng)


def cf_text(ws, rng, text, bg, fg="FFFFFF", bold=True):
    ws.conditional_formatting.add(
        rng, CellIsRule(operator="equal", formula=[f'"{text}"'], fill=fill(bg), font=Font(color=fg, bold=bold)))


def cf_formula(ws, rng, formula, bg=None, fg=None, bold=None, border=None):
    kw = {}
    if bg:
        kw["fill"] = fill(bg)
    if fg or bold is not None:
        kw["font"] = Font(color=fg, bold=bold)
    if border:
        kw["border"] = border
    ws.conditional_formatting.add(rng, FormulaRule(formula=[formula], **kw))


def cf_checks(ws, rng):
    cf_text(ws, rng, "OK", C["green"])
    cf_text(ws, rng, "CHECK", C["red"])


def cf_rag(ws, rng):
    cf_text(ws, rng, "Red", C["red"])
    cf_text(ws, rng, "Amber", C["amber"])
    cf_text(ws, rng, "Green", C["green"])
    cf_text(ws, rng, "Grey", C["grey"])


def add_table(ws, name, ref):
    t = Table(displayName=name, ref=ref)
    ws.add_table(t)
    return t


def print_setup(ws, header_left, title_rows=None, area=None, landscape=True, fit_height=0):
    ws.page_setup.orientation = "landscape" if landscape else "portrait"
    ws.page_setup.paperSize = ws.PAPERSIZE_A4
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = fit_height
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_margins = PageMargins(left=0.4, right=0.4, top=0.6, bottom=0.6, header=0.25, footer=0.25)
    ws.print_options.horizontalCentered = True
    ws.oddHeader.left.text = header_left
    ws.oddHeader.left.size = 8
    ws.oddHeader.left.font = "Arial"
    ws.oddHeader.left.color = C["ink500"]
    ws.oddHeader.right.text = "&A"
    ws.oddHeader.right.size = 8
    ws.oddHeader.right.font = "Arial"
    ws.oddHeader.right.color = C["ink500"]
    ws.oddFooter.left.text = FOOTER
    ws.oddFooter.left.size = 8
    ws.oddFooter.left.font = "Arial"
    ws.oddFooter.left.color = C["ink500"]
    ws.oddFooter.right.text = "Page &P of &N"
    ws.oddFooter.right.size = 8
    ws.oddFooter.right.font = "Arial"
    ws.oddFooter.right.color = C["ink500"]
    if title_rows:
        ws.print_title_rows = title_rows
    if area:
        ws.print_area = area


def link_cell(ws, ref, sheet, display=None, size=9, bold=False):
    cell = ws[ref]
    cell.value = display or sheet
    cell.hyperlink = Hyperlink(ref=ref, location=f"'{sheet}'!A1", display=display or sheet)
    cell.font = font(C["acc600"], size=size, bold=bold, underline="single")
    cell.alignment = Alignment(horizontal="left", vertical="center")
    return cell


# ---------------- charts ----------------

def _cp(size=800, color=None, bold=False):
    return CharacterProperties(sz=size, b=bold, solidFill=color or C["ink500"], latin=DFont(typeface="Arial"))


def rich(size=800, color=None, bold=False):
    cp = _cp(size, color, bold)
    return RichText(p=[Paragraph(pPr=ParagraphProperties(defRPr=cp), endParaRPr=cp)])


def chart_title(text, size=1000):
    cp = _cp(size, C["ink900"], True)
    para = Paragraph(pPr=ParagraphProperties(defRPr=cp), r=[RegularTextRun(rPr=cp, t=text)])
    return Title(tx=Text(rich=RichText(p=[para])), overlay=False)


def style_axes(chart, y_fmt="0.0", gridlines=True):
    for ax in (chart.x_axis, chart.y_axis):
        ax.delete = False
        ax.txPr = rich(800, C["ink700"])
        ax.spPr = GraphicalProperties(ln=LineProperties(solidFill=C["ink300"]))
    chart.y_axis.numFmt = y_fmt
    chart.y_axis.number_format = y_fmt
    if gridlines:
        gl = ChartLines()
        gl.spPr = GraphicalProperties(ln=LineProperties(solidFill=C["ink100"]))
        chart.y_axis.majorGridlines = gl
    else:
        chart.y_axis.majorGridlines = None
    chart.x_axis.majorGridlines = None


def data_labels(size=800, fmt="0.0", color=None, pos=None):
    dl = DataLabelList()
    dl.showVal = True
    dl.showSerName = False
    dl.showCatName = False
    dl.showLegendKey = False
    dl.showPercent = False
    dl.numFmt = fmt
    dl.txPr = rich(size, color or C["ink900"], True)
    if pos:
        dl.position = pos
    return dl


def color_series(series, hex_, line=False, width=28575):
    gp = series.graphicalProperties
    if line:
        gp.line.solidFill = hex_
        gp.line.width = width
        series.smooth = False
    else:
        gp.solidFill = hex_
        gp.line.solidFill = hex_
