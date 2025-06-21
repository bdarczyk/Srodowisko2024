import os
from src.data_handlers.route_data_manager import RouteDataManager
from src.data_handlers.weather_data_manager import WeatherDataManager
from src.analyzers.text_processor import TextProcessor
from src.analyzers.review_analyzer import ReviewAnalyzer
from src.recommenders.route_recommender import RouteRecommender
from src.ui.user_interface import UserInterface
from src.reporters.chart_generator import ChartGenerator
from src.reporters.pdf_report_generator import PDFReportGenerator

def main():
    # 0. folder na raporty i wykresy
    os.makedirs('reports', exist_ok=True)

    # 1. dane tras + recenzje i pogodę
    route_mgr = RouteDataManager('data/routes/trasy.csv', reviews_file='data/routes/reviews.csv')
    weather_mgr = WeatherDataManager('data/weather/pogoda.csv')
    routes = route_mgr.load_routes()
    weather_map = weather_mgr.load_weather()

    # 2. Ekstrakcja danych z opisów (TextProcessor)
    tp = TextProcessor()
    for r in routes:
        r.extracted = {
            'duration_min': tp.extract_duration(r.description),
            'elevations':   tp.extract_elevation_points(r.description),
            'coords':       tp.standardize_gps(tp.extract_gps_coords(r.description)),
            'alerts':       tp.extract_alerts(r.description),
            'pois':         tp.extract_points_of_interest(r.description),
        }

    # 3. Analiza recenzji (ReviewAnalyzer)
    ra = ReviewAnalyzer()
    for r in routes:
        r.ratings      = [ra.extract_rating(txt) for txt in r.reviews]
        r.sentiments   = [ra.analyze_sentiment(txt) for txt in r.reviews]
        r.aspects      = [ra.extract_aspects(txt) for txt in r.reviews]
        r.review_dates = [d for txt in r.reviews for d in ra.extract_dates(txt)]
        r.rating = round(sum(r.ratings) / len(r.ratings), 1) if r.ratings else 0.0

    # 4. preferencje użytkownika, uzyskaj rekomendacje
    ui = UserInterface()
    prefs = ui.get_user_preferences()
    recommendations = RouteRecommender(prefs, weather_map).recommend_routes(routes, prefs.selected_date)

    # 5. dane do raportu
    report_data = []
    for r in recommendations:
        r.estimate_time()
        report_data.append({
            'name':         r.name,
            'length':       r.length_km,
            'category':     r.categorize_route(),
            'rating':       r.rating,
            'comfort':      r.comfort_index,
            'alerts':       r.extracted['alerts'],
            'aspects':      sum(r.aspects, []),
            'review_dates': r.review_dates,
            'duration_min': r.extracted.get('duration_min'),
            'pois':         r.extracted.get('pois', []),
        })

    # 6. wykresy (ChartGenerator)
    charts = ChartGenerator(report_data)
    chart_paths = {
        'lengths':    charts.generate_length_bar_chart(filename='reports/lengths.png'),
        'categories': charts.generate_category_pie_chart(filename='reports/categories.png'),
        'ratings':    charts.generate_rating_bar_chart(filename='reports/ratings.png'),
    }

    # 7. raport PDF
    params = {'region': prefs.location_id, 'date': prefs.selected_date}
    PDFReportGenerator(
        routes_data=report_data,
        params=params,
        charts_paths=chart_paths,
        filename='reports/raport.pdf'
    ).generate_pdf()

    print("Wygenerowano raport: reports/raport.pdf")

if __name__ == '__main__':
    main()
