#!/usr/bin/env python3
"""
Система аналитики для кампании "Digitalizacija Biznesa"
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
import telebot
import schedule
import time
import threading

load_dotenv()

class AnalyticsSystem:
    def __init__(self):
        self.leads_db_path = 'data/digitalizacija_leads.db'
        self.posts_db_path = 'data/digitalizacija_posts.db'
        self.reports_path = 'reports/'
        
        # Создаем папку для отчетов
        os.makedirs(self.reports_path, exist_ok=True)
        
        # Настройки для графиков
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def get_leads_statistics(self, days=30):
        """Получение статистики лидов"""
        conn = sqlite3.connect(self.leads_db_path)
        
        # Общая статистика
        total_leads = pd.read_sql_query(
            'SELECT COUNT(*) as total FROM leads', conn
        ).iloc[0]['total']
        
        # Лиды за период
        date_filter = datetime.now() - timedelta(days=days)
        recent_leads = pd.read_sql_query(
            'SELECT COUNT(*) as recent FROM leads WHERE created_at >= ?', 
            conn, params=[date_filter]
        ).iloc[0]['recent']
        
        # Статистика по стадиям воронки
        funnel_stats = pd.read_sql_query('''
            SELECT current_stage, COUNT(*) as count
            FROM leads 
            GROUP BY current_stage
            ORDER BY count DESC
        ''', conn)
        
        # Статистика по источникам
        source_stats = pd.read_sql_query('''
            SELECT source, COUNT(*) as count
            FROM leads 
            GROUP BY source
            ORDER BY count DESC
        ''', conn)
        
        # Конверсии по дням
        conversions_daily = pd.read_sql_query('''
            SELECT DATE(timestamp) as date, COUNT(*) as conversions
            FROM conversions 
            WHERE timestamp >= ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', conn, params=[date_filter])
        
        # Активность пользователей
        activity_stats = pd.read_sql_query('''
            SELECT action, COUNT(*) as count
            FROM interactions 
            WHERE timestamp >= ?
            GROUP BY action
            ORDER BY count DESC
        ''', conn, params=[date_filter])
        
        conn.close()
        
        return {
            'total_leads': total_leads,
            'recent_leads': recent_leads,
            'funnel_stats': funnel_stats,
            'source_stats': source_stats,
            'conversions_daily': conversions_daily,
            'activity_stats': activity_stats
        }
    
    def get_posts_statistics(self, days=30):
        """Получение статистики постов"""
        conn = sqlite3.connect(self.posts_db_path)
        
        date_filter = datetime.now() - timedelta(days=days)
        
        # Общая статистика постов
        posts_stats = pd.read_sql_query('''
            SELECT 
                COUNT(*) as total_posts,
                COUNT(CASE WHEN status = 'sent' THEN 1 END) as sent_posts,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending_posts
            FROM posts
            WHERE created_at >= ?
        ''', conn, params=[date_filter])
        
        # Статистика по типам постов
        post_types_stats = pd.read_sql_query('''
            SELECT post_type, COUNT(*) as count
            FROM posts 
            WHERE created_at >= ?
            GROUP BY post_type
            ORDER BY count DESC
        ''', conn, params=[date_filter])
        
        # Статистика по каналам
        channels_stats = pd.read_sql_query('''
            SELECT channel_id, COUNT(*) as count
            FROM posts 
            WHERE created_at >= ?
            GROUP BY channel_id
            ORDER BY count DESC
        ''', conn, params=[date_filter])
        
        # Статистика просмотров и вовлеченности
        engagement_stats = pd.read_sql_query('''
            SELECT 
                SUM(views) as total_views,
                SUM(likes) as total_likes,
                SUM(comments) as total_comments,
                SUM(shares) as total_shares,
                AVG(views) as avg_views,
                AVG(likes) as avg_likes
            FROM posts 
            WHERE status = 'sent' AND created_at >= ?
        ''', conn, params=[date_filter])
        
        conn.close()
        
        return {
            'posts_stats': posts_stats,
            'post_types_stats': post_types_stats,
            'channels_stats': channels_stats,
            'engagement_stats': engagement_stats
        }
    
    def create_funnel_chart(self, funnel_stats):
        """Создание графика воронки продаж"""
        plt.figure(figsize=(10, 6))
        
        stages = ['awareness', 'interest', 'consideration', 'intent', 'purchase']
        stage_names = ['Осведомленность', 'Интерес', 'Рассмотрение', 'Намерение', 'Покупка']
        
        counts = []
        for stage in stages:
            count = funnel_stats[funnel_stats['current_stage'] == stage]['count'].iloc[0] if len(funnel_stats[funnel_stats['current_stage'] == stage]) > 0 else 0
            counts.append(count)
        
        # Создаем воронку
        plt.bar(stage_names, counts, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        
        # Добавляем значения на столбцы
        for i, count in enumerate(counts):
            plt.text(i, count + max(counts) * 0.01, str(count), 
                    ha='center', va='bottom', fontweight='bold')
        
        plt.title('Воронка продаж - "Digitalizacija Biznesa"', fontsize=16, fontweight='bold')
        plt.ylabel('Количество лидов', fontsize=12)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Сохраняем график
        filename = f"{self.reports_path}funnel_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_conversions_chart(self, conversions_daily):
        """Создание графика конверсий по дням"""
        plt.figure(figsize=(12, 6))
        
        if not conversions_daily.empty:
            plt.plot(conversions_daily['date'], conversions_daily['conversions'], 
                    marker='o', linewidth=2, markersize=6)
            plt.fill_between(conversions_daily['date'], conversions_daily['conversions'], 
                           alpha=0.3)
        
        plt.title('Конверсии по дням', fontsize=16, fontweight='bold')
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Количество конверсий', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        filename = f"{self.reports_path}conversions_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def create_engagement_chart(self, post_types_stats):
        """Создание графика типов постов"""
        plt.figure(figsize=(10, 6))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        plt.pie(post_types_stats['count'], labels=post_types_stats['post_type'], 
               autopct='%1.1f%%', colors=colors, startangle=90)
        
        plt.title('Распределение типов постов', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        filename = f"{self.reports_path}post_types_chart_{datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        return filename
    
    def generate_daily_report(self):
        """Генерация ежедневного отчета"""
        print("📊 Генерация ежедневного отчета...")
        
        # Получаем статистику
        leads_stats = self.get_leads_statistics(days=1)
        posts_stats = self.get_posts_statistics(days=1)
        
        # Создаем отчет
        report = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'leads': {
                'new_leads': leads_stats['recent_leads'],
                'total_leads': leads_stats['total_leads'],
                'funnel_distribution': leads_stats['funnel_stats'].to_dict('records')
            },
            'posts': {
                'new_posts': posts_stats['posts_stats'].iloc[0]['total_posts'],
                'sent_posts': posts_stats['posts_stats'].iloc[0]['sent_posts'],
                'engagement': {
                    'total_views': posts_stats['engagement_stats'].iloc[0]['total_views'] or 0,
                    'total_likes': posts_stats['engagement_stats'].iloc[0]['total_likes'] or 0,
                    'avg_views': posts_stats['engagement_stats'].iloc[0]['avg_views'] or 0
                }
            },
            'conversions': len(leads_stats['conversions_daily'])
        }
        
        # Сохраняем отчет
        filename = f"{self.reports_path}daily_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Ежедневный отчет сохранен: {filename}")
        return report
    
    def generate_weekly_report(self):
        """Генерация еженедельного отчета"""
        print("📊 Генерация еженедельного отчета...")
        
        # Получаем статистику
        leads_stats = self.get_leads_statistics(days=7)
        posts_stats = self.get_posts_statistics(days=7)
        
        # Создаем графики
        funnel_chart = self.create_funnel_chart(leads_stats['funnel_stats'])
        conversions_chart = self.create_conversions_chart(leads_stats['conversions_daily'])
        engagement_chart = self.create_engagement_chart(posts_stats['post_types_stats'])
        
        # Создаем отчет
        report = {
            'period': f"{datetime.now() - timedelta(days=7):%Y-%m-%d} - {datetime.now():%Y-%m-%d}",
            'leads': {
                'new_leads': leads_stats['recent_leads'],
                'total_leads': leads_stats['total_leads'],
                'funnel_distribution': leads_stats['funnel_stats'].to_dict('records'),
                'top_sources': leads_stats['source_stats'].to_dict('records'),
                'conversions': len(leads_stats['conversions_daily'])
            },
            'posts': {
                'total_posts': posts_stats['posts_stats'].iloc[0]['total_posts'],
                'sent_posts': posts_stats['posts_stats'].iloc[0]['sent_posts'],
                'post_types': posts_stats['post_types_stats'].to_dict('records'),
                'engagement': posts_stats['engagement_stats'].to_dict('records')[0]
            },
            'charts': {
                'funnel': funnel_chart,
                'conversions': conversions_chart,
                'engagement': engagement_chart
            }
        }
        
        # Сохраняем отчет
        filename = f"{self.reports_path}weekly_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Еженедельный отчет сохранен: {filename}")
        return report
    
    def generate_monthly_report(self):
        """Генерация ежемесячного отчета"""
        print("📊 Генерация ежемесячного отчета...")
        
        # Получаем статистику
        leads_stats = self.get_leads_statistics(days=30)
        posts_stats = self.get_posts_statistics(days=30)
        
        # Создаем графики
        funnel_chart = self.create_funnel_chart(leads_stats['funnel_stats'])
        conversions_chart = self.create_conversions_chart(leads_stats['conversions_daily'])
        engagement_chart = self.create_engagement_chart(posts_stats['post_types_stats'])
        
        # Анализ трендов
        trends = self.analyze_trends(leads_stats, posts_stats)
        
        # Создаем отчет
        report = {
            'period': f"{datetime.now() - timedelta(days=30):%Y-%m-%d} - {datetime.now():%Y-%m-%d}",
            'summary': {
                'total_leads': leads_stats['total_leads'],
                'new_leads': leads_stats['recent_leads'],
                'conversion_rate': self.calculate_conversion_rate(leads_stats),
                'avg_engagement': posts_stats['engagement_stats'].iloc[0]['avg_views'] or 0
            },
            'leads': {
                'funnel_distribution': leads_stats['funnel_stats'].to_dict('records'),
                'top_sources': leads_stats['source_stats'].to_dict('records'),
                'activity_breakdown': leads_stats['activity_stats'].to_dict('records'),
                'conversions_timeline': leads_stats['conversions_daily'].to_dict('records')
            },
            'posts': {
                'total_posts': posts_stats['posts_stats'].iloc[0]['total_posts'],
                'sent_posts': posts_stats['posts_stats'].iloc[0]['sent_posts'],
                'post_types': posts_stats['post_types_stats'].to_dict('records'),
                'channels_performance': posts_stats['channels_stats'].to_dict('records'),
                'engagement_metrics': posts_stats['engagement_stats'].to_dict('records')[0]
            },
            'trends': trends,
            'charts': {
                'funnel': funnel_chart,
                'conversions': conversions_chart,
                'engagement': engagement_chart
            },
            'recommendations': self.generate_recommendations(leads_stats, posts_stats)
        }
        
        # Сохраняем отчет
        filename = f"{self.reports_path}monthly_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"✅ Ежемесячный отчет сохранен: {filename}")
        return report
    
    def analyze_trends(self, leads_stats, posts_stats):
        """Анализ трендов"""
        trends = {
            'leads_growth': 'stable',
            'conversion_trend': 'stable',
            'engagement_trend': 'stable',
            'content_performance': 'stable'
        }
        
        # Анализируем рост лидов
        if leads_stats['recent_leads'] > 10:
            trends['leads_growth'] = 'increasing'
        elif leads_stats['recent_leads'] < 5:
            trends['leads_growth'] = 'decreasing'
        
        # Анализируем конверсии
        conversions_count = len(leads_stats['conversions_daily'])
        if conversions_count > 5:
            trends['conversion_trend'] = 'increasing'
        elif conversions_count < 2:
            trends['conversion_trend'] = 'decreasing'
        
        # Анализируем вовлеченность
        avg_views = posts_stats['engagement_stats'].iloc[0]['avg_views'] or 0
        if avg_views > 100:
            trends['engagement_trend'] = 'increasing'
        elif avg_views < 50:
            trends['engagement_trend'] = 'decreasing'
        
        return trends
    
    def calculate_conversion_rate(self, leads_stats):
        """Расчет конверсии"""
        total_leads = leads_stats['total_leads']
        conversions = len(leads_stats['conversions_daily'])
        
        if total_leads > 0:
            return round((conversions / total_leads) * 100, 2)
        return 0
    
    def generate_recommendations(self, leads_stats, posts_stats):
        """Генерация рекомендаций"""
        recommendations = []
        
        # Анализ воронки
        funnel_data = leads_stats['funnel_stats']
        awareness_count = funnel_data[funnel_data['current_stage'] == 'awareness']['count'].iloc[0] if len(funnel_data[funnel_data['current_stage'] == 'awareness']) > 0 else 0
        purchase_count = funnel_data[funnel_data['current_stage'] == 'purchase']['count'].iloc[0] if len(funnel_data[funnel_data['current_stage'] == 'purchase']) > 0 else 0
        
        if awareness_count > 0 and purchase_count == 0:
            recommendations.append("Улучшить конверсию в продажи: добавить больше продающих постов и ограниченных предложений")
        
        if awareness_count < 10:
            recommendations.append("Увеличить приток лидов: запустить рекламные кампании и улучшить SEO")
        
        # Анализ контента
        engagement_avg = posts_stats['engagement_stats'].iloc[0]['avg_views'] or 0
        if engagement_avg < 50:
            recommendations.append("Улучшить вовлеченность: оптимизировать заголовки и время публикации")
        
        # Анализ активности
        activity_data = leads_stats['activity_stats']
        if len(activity_data) < 5:
            recommendations.append("Увеличить активность пользователей: добавить больше интерактивного контента")
        
        return recommendations
    
    def send_report_to_telegram(self, report, report_type):
        """Отправка отчета в Telegram"""
        bot_token = os.getenv('BOT_TOKEN')
        admin_id = os.getenv('ADMIN_ID')
        
        if not bot_token or not admin_id:
            print("❌ Не настроены BOT_TOKEN или ADMIN_ID для отправки отчетов")
            return
        
        bot = telebot.TeleBot(bot_token)
        
        # Формируем текст отчета
        if report_type == 'daily':
            text = f"""
📊 **Ежедневный отчет - {report['date']}**

👥 **Лиды:**
• Новых лидов: {report['leads']['new_leads']}
• Всего лидов: {report['leads']['total_leads']}
• Конверсий: {report['conversions']}

📝 **Посты:**
• Новых постов: {report['posts']['new_posts']}
• Отправлено: {report['posts']['sent_posts']}
• Просмотров: {report['posts']['engagement']['total_views']}
• Лайков: {report['posts']['engagement']['total_likes']}
            """
        elif report_type == 'weekly':
            text = f"""
📊 **Еженедельный отчет - {report['period']}**

👥 **Лиды:**
• Новых лидов: {report['leads']['new_leads']}
• Всего лидов: {report['leads']['total_leads']}
• Конверсий: {report['leads']['conversions']}

📝 **Посты:**
• Всего постов: {report['posts']['total_posts']}
• Отправлено: {report['posts']['sent_posts']}
• Средние просмотры: {report['posts']['engagement']['avg_views']}
            """
        else:  # monthly
            text = f"""
📊 **Ежемесячный отчет - {report['period']}**

📈 **Сводка:**
• Всего лидов: {report['summary']['total_leads']}
• Новых лидов: {report['summary']['new_leads']}
• Конверсия: {report['summary']['conversion_rate']}%
• Средняя вовлеченность: {report['summary']['avg_engagement']}

🎯 **Рекомендации:**
{chr(10).join([f"• {rec}" for rec in report['recommendations'][:3]])}
            """
        
        try:
            bot.send_message(admin_id, text, parse_mode='Markdown')
            print(f"✅ Отчет {report_type} отправлен в Telegram")
        except Exception as e:
            print(f"❌ Ошибка отправки отчета: {e}")
    
    def run_scheduler(self):
        """Запуск планировщика отчетов"""
        print("📅 Запуск планировщика отчетов...")
        
        # Ежедневный отчет в 9:00
        schedule.every().day.at("09:00").do(self.run_daily_report)
        
        # Еженедельный отчет по воскресеньям в 10:00
        schedule.every().sunday.at("10:00").do(self.run_weekly_report)
        
        # Ежемесячный отчет в первый день месяца в 11:00
        schedule.every().month.at("11:00").do(self.run_monthly_report)
        
        print("✅ Планировщик отчетов запущен")
        print("📅 Ежедневный отчет: 9:00")
        print("📅 Еженедельный отчет: воскресенье 10:00")
        print("📅 Ежемесячный отчет: 1-е число 11:00")
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    
    def run_daily_report(self):
        """Запуск ежедневного отчета"""
        report = self.generate_daily_report()
        self.send_report_to_telegram(report, 'daily')
    
    def run_weekly_report(self):
        """Запуск еженедельного отчета"""
        report = self.generate_weekly_report()
        self.send_report_to_telegram(report, 'weekly')
    
    def run_monthly_report(self):
        """Запуск ежемесячного отчета"""
        report = self.generate_monthly_report()
        self.send_report_to_telegram(report, 'monthly')

def main():
    """Основная функция"""
    analytics = AnalyticsSystem()
    
    # Генерируем отчеты
    print("📊 Генерация отчетов...")
    
    daily_report = analytics.generate_daily_report()
    weekly_report = analytics.generate_weekly_report()
    monthly_report = analytics.generate_monthly_report()
    
    print("✅ Все отчеты сгенерированы")
    
    # Запускаем планировщик
    analytics.run_scheduler()

if __name__ == "__main__":
    main() 