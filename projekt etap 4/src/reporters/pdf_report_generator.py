from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from matplotlib import font_manager
from src.reporters.chart_generator import ChartGenerator

# Zarejestruj czcionkę TrueType obsługującą polskie znaki
ttf_path = font_manager.findfont("DejaVu Sans")
pdfmetrics.registerFont(TTFont('DejaVuSans', ttf_path))

class PDFReportGenerator(SimpleDocTemplate):
    def __init__(self, routes_data, params, charts_paths: dict, filename='report.pdf'):
        super().__init__(filename, pagesize=A4)
        self.routes = routes_data
        self.params = params
        self.charts = charts_paths  # <— tu zapisujemy ścieżki
        self.styles = getSampleStyleSheet()
        for style in self.styles.byName.values():
            style.fontName = 'DejaVuSans'
        self.styles.add(
            ParagraphStyle(
                name='TOCHeading',
                parent=self.styles['Heading1'],
                fontName='DejaVuSans'
            )
        )
        self.story = []
        self._prepare_story()

    def _prepare_story(self):
        self._add_title_page()
        self._add_table_of_contents()
        self._add_executive_summary()
        self._add_detailed_routes()
        self._add_charts()
        self._add_summary_table()

    def _add_title_page(self):
        self.story.append(Paragraph("Raport Rekomendacji Tras Turystycznych", self.styles['Title']))
        self.story.append(Spacer(1, 2 * cm))
        self.story.append(Paragraph(f"Region: <b>{self.params.get('region','')}</b>", self.styles['Normal']))
        self.story.append(Paragraph(f"Data: <b>{self.params.get('date','')}</b>", self.styles['Normal']))
        self.story.append(PageBreak())

    def _add_table_of_contents(self):
        toc = TableOfContents()
        toc.levelStyles = [ParagraphStyle(name='TOCLevel1', fontName='DejaVuSans', fontSize=12, leftIndent=20, leading=14)]
        self.story.append(Paragraph('Spis Treści', self.styles['Heading1']))
        self.story.append(toc)
        self.story.append(PageBreak())

    def _add_executive_summary(self):
        self.story.append(Paragraph('1. Podsumowanie wykonawcze', self.styles['Heading1']))
        count = len(self.routes)
        avg_comfort = sum(r['comfort'] for r in self.routes)/count if count else 0
        avg_length = sum(r['length'] for r in self.routes)/count if count else 0
        text = f"Analiza {count} tras. Średnia długość: {avg_length:.1f} km. Średni komfort pogodowy: {avg_comfort:.0f}/100."
        self.story.append(Paragraph(text, self.styles['Normal']))
        self.story.append(PageBreak())

    def _add_detailed_routes(self):
        self.story.append(Paragraph('2. Szczegółowe opisy rekomendowanych tras', self.styles['Heading1']))
        for idx, r in enumerate(self.routes, start=1):
            self.story.append(Paragraph(f"2.{idx} {r['name']}", self.styles['Heading2']))
            # Podstawowe parametry
            details = (
                f"Długość: {r['length']} km<br/>"
                f"Kategoria: {r['category']}<br/>"
                f"Ocena: {r['rating']}/5<br/>"
                f"Komfort pogodowy: {r['comfort']}/100"
            )
            self.story.append(Paragraph(details, self.styles['Normal']))
            # Czas przejścia
            duration = r.get('duration_min')
            if duration is not None:
                hours = duration // 60
                mins = duration % 60
                time_str = f"{hours}h {mins}min" if hours > 0 else f"{mins}min"
                self.story.append(Paragraph(f"Czas przejścia: {time_str}", self.styles['Normal']))
            # Punkty charakterystyczne
            pois = r.get('pois', [])
            if pois:
                poi_list = [f"{typ.capitalize()}: {name}" for typ, name in pois]
                self.story.append(Paragraph("Punkty charakterystyczne: " + ", ".join(poi_list), self.styles['Normal']))
            # Ostrzeżenia
            alerts = r.get('alerts', [])
            if alerts:
                self.story.append(Paragraph("Ostrzeżenia: " + "; ".join(alerts), self.styles['Normal']))
            # Aspekty recenzji
            aspects = r.get('aspects', [])
            if aspects:
                flat = []
                for item in aspects:
                    if isinstance(item, list): flat.extend(item)
                    elif isinstance(item, str): flat.append(item)
                unique = set(flat)
                self.story.append(Paragraph("Aspekty recenzji: " + ", ".join(unique), self.styles['Normal']))
            # Sentymenty recenzji
            sentiments = r.get('sentiments', [])
            if sentiments:
                # Wybierz najczęściej występujący sentyment
                from collections import Counter
                most_common = Counter(sentiments).most_common(1)[0][0]
                self.story.append(
                    Paragraph(
                        "Sentyment: " + most_common,
                        self.styles['Normal']
                    )
                )
            # Daty recenzji
            dates = r.get('review_dates', [])
            if dates:
                self.story.append(Paragraph("Daty recenzji: " + ", ".join(map(str, dates)), self.styles['Normal']))
            self.story.append(Spacer(1, 0.5 * cm))
        self.story.append(PageBreak())

    def _add_charts(self):
        self.story.append(Paragraph('3. Wykresy porównawcze', self.styles['Heading1']))
        cg = ChartGenerator(self.routes)
        for func in [
            cg.generate_length_bar_chart,
            cg.generate_category_pie_chart,
            cg.generate_rating_bar_chart,
        ]:
            img = func()
            self.story.append(Image(img, width=16*cm, height=10*cm))
            self.story.append(Spacer(1, 0.5 * cm))
        self.story.append(PageBreak())

    def _add_summary_table(self):
        self.story.append(Paragraph('4. Tabela zbiorcza tras', self.styles['Heading1']))
        data = [['Lp', 'Nazwa', 'Długość', 'Kategoria', 'Ocena', 'Komfort']]
        for idx, r in enumerate(self.routes, start=1):
            data.append([
                idx,
                Paragraph(r['name'], self.styles['Normal']),
                r['length'],
                Paragraph(r['category'], self.styles['Normal']),
                r['rating'],
                r['comfort']
            ])
        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, -1), 'DejaVuSans')
        ]))
        self.story.append(table)
        self.story.append(PageBreak())

    def generate_pdf(self, filename=None):
        if filename:
            self.filename = filename
        super().build(self.story)