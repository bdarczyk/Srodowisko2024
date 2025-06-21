import matplotlib.pyplot as plt

class ChartGenerator:
    """
    Generuje wykresy ze słownika report_data = [
      {'name':…, 'length':…, 'category':…, 'rating':…, 'comfort':…, 'monthly_comfort':[…]},
      …
    ]
    """

    def __init__(self, report_data: list[dict]):
        self.data = report_data

    def generate_length_bar_chart(self, filename="lengths.png") -> str:
        # Sortujemy rosnąco po długości
        sorted_data = sorted(self.data, key=lambda x: getattr(x, 'length_km', x['length']))
        names  = [d['name']   for d in sorted_data]
        values = [d['length'] for d in sorted_data]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(names, values)
        ax.set_xlabel("Długość (km)")
        ax.set_ylabel("Trasa")
        ax.set_title("Histogram długości tras")
        fig.tight_layout()
        fig.savefig(filename, dpi=150)
        plt.close(fig)
        return filename

    def generate_category_pie_chart(self, filename="categories.png") -> str:
        # Zliczamy kategorie
        counts = {}
        for d in self.data:
            cat = d['category']
            counts[cat] = counts.get(cat, 0) + 1

        labels = list(counts.keys())
        sizes  = list(counts.values())

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        ax.set_title("Rozkład kategorii tras")
        fig.tight_layout()
        fig.savefig(filename, dpi=150)
        plt.close(fig)
        return filename

    def generate_rating_bar_chart(self, filename="ratings.png") -> str:
        # Sortujemy malejąco po ocenie
        sorted_data = sorted(self.data, key=lambda x: x['rating'], reverse=True)
        names  = [d['name']   for d in sorted_data]
        values = [d['rating'] for d in sorted_data]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(names, values)
        ax.set_ylabel("Ocena (0–5)")
        ax.set_xlabel("Trasa")
        ax.set_title("Oceny użytkowników")
        plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
        fig.tight_layout()
        fig.savefig(filename, dpi=150)
        plt.close(fig)
        return filename

