import mysql.connector
import pandas as pd

import numpy as np

def get_statistics():
    # 创建数据库连接
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="my_database"
    )

    # 创建一个游标对象
    cursor = conn.cursor()

    # 执行SQL查询
    cursor.execute("SELECT * FROM my_table")

    # 获取查询结果
    result = cursor.fetchall()

    # 将结果转换为DataFrame
    data = pd.DataFrame(result, columns=[column[0] for column in cursor.description])

    # 统计不同国家出现的数量
    country_counts = data['国家'].value_counts().to_dict()

    # 将 country_counts 转换为列表
    country_data = [{'name': country, 'value': count} for country, count in country_counts.items()]

    # 统计不同导演出现的数量
    director_counts = data['导演'].value_counts().to_dict()

    # 展开列表并统计各流派出现的频率
    genre_counts = data['流派'].str.strip().str.split(',').explode().str.strip().value_counts().to_dict()

    # 将演员列中的字符串拆分为列表
    data['演员'] = data['演员'].str.split(',')
    # 展开列表并统计各演员出现的频率
    actor_counts = data['演员'].explode().value_counts().to_dict()

    # 计算电影评分的五个统计量
    movie_ratings = data['电影评分']
    q1 = np.percentile(movie_ratings, 25)
    median = np.percentile(movie_ratings, 50)
    q3 = np.percentile(movie_ratings, 75)

    rating_stats = {
        'max': movie_ratings.max(),
        'min': movie_ratings.min(),
        'mean': movie_ratings.mean(),
        'median': median,
        'std': movie_ratings.std(),
        'q1': q1,
        'q3': q3
    }
    print(rating_stats)
    # 计算电影年份的分布
    year_distribution = data['年份'].value_counts().to_dict()

    # 将所有统计结果存储在一个字典中并返回
    statistics = {
        'country_data': country_data,
        'director_counts': director_counts,
        'genre_counts': genre_counts,
        'actor_counts': actor_counts,
        'rating_stats': rating_stats,
        'year_distribution': year_distribution,
        'movie_ratings': movie_ratings.tolist()  # 添加 movie_ratings 键
    }

    return statistics
