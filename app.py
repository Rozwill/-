from flask import Flask, render_template,request
from database import get_statistics
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import Pagination
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:123456@localhost/my_database'
db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'my_table'  # 你的表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    电影名称 = db.Column(db.String(255))
    电影评分 = db.Column(db.Float)
    评分人数 = db.Column(db.Integer)
    导演 = db.Column(db.String(255))
    编剧 = db.Column(db.String(255))
    流派 = db.Column(db.String(255))
    中文名 = db.Column(db.String(255))
    年份 = db.Column(db.Integer)
    MPAA = db.Column(db.String(255))
    时长 = db.Column(db.String(255))
    演员 = db.Column(db.Text)
    预算 = db.Column(db.BigInteger)
    北美票房 = db.Column(db.BigInteger)
    首周末北美票房 = db.Column(db.BigInteger)
    全球票房 = db.Column(db.BigInteger)
    电影链接 = db.Column(db.String(255))
    国家 = db.Column(db.String(255))
    评论数量 = db.Column(db.Integer)
    核心句 = db.Column(db.Text)


@app.route('/')
def index():
    # 获取所有的统计信息
    statistics = get_statistics()
    return render_template('index.html', statistics=statistics)


@app.route('/movies.html')
def movies():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.paginate(page=page,per_page=20)  # 每页显示20部电影
    return render_template('movies.html', movies=movies)  # 将电影数据传递给模板

@app.route('/test2.html')
def test():
    # 获取统计信息
    statistics = get_statistics()

    return render_template('test2.html',country_counts=statistics['country_data'])

@app.route('/search')
def search():
    query = request.args.get('q')
    type = request.args.get('type')
    page = request.args.get('page', 1, type=int)  # 获取请求的页码，默认为第一页

    # 根据搜索类型，从数据库中查询匹配的电影
    if type == '中文名':
        results = Movie.query.filter(Movie.中文名.contains(query))
    elif type == '英文名':
        results = Movie.query.filter(Movie.电影名称.contains(query))
    elif type == '导演':
        results = Movie.query.filter(Movie.导演.contains(query))
    else:
        results = Movie.query

    # 对查询结果进行分页处理
    results = results.paginate(page=page, per_page=10, error_out=False)  # 根据需要修改 `per_page`

    searched = bool(query)
    # 打印查询结果以进行调试
    print(results.items)  # 打印当前页面的搜索结果
    print(results.has_prev)  # 检查是否有前一页
    print(results.has_next)  # 检查是否有下一页
    return render_template('search_results.html', results=results, searched=searched)

if __name__ == '__main__':
    app.run(debug=True)

