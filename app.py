import requests
import streamlit as st
import app2
from pyecharts import options as opts
from pyecharts.charts import Pie, Line, Bar, Scatter, Radar
from pyecharts.render import make_snapshot
from pyecharts.globals import ThemeType
from snapshot_selenium import snapshot as driver
import random
from pyecharts.charts import Funnel, Gauge
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from pyecharts.charts import WordCloud


def get_data(url):
    data = []
    data = app2.process_data(url)
    print('----------------------')
    print(data)
    return data


def visualize_pie(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建饼图实例
    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("", [list(z) for z in zip(x_data, y_data)])
        .set_global_opts(
            title_opts=opts.TitleOpts(title="饼图"),
            legend_opts=opts.LegendOpts(
                orient="horizontal", pos_top="bottom")
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    # 生成静态图片
    file_path = "./pie.html"
    pie.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=900, height=1000)


def visualize_line(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建折线图实例
    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(
            x_data,
           
        )
        .add_yaxis("", y_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="折线图"),
                          xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45, font_style="italic"))
                          )
    )

    # 生成静态图片
    file_path = "./line.html"
    line.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=900, height=1000)


def visualize_bar(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建柱状图实例
    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x_data)
        .add_yaxis("", y_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="柱状图"),
            xaxis_opts=opts.AxisOpts(
                axislabel_opts=opts.LabelOpts(
                    rotate=-45,
                    font_style="italic",  # 设置斜体字体样式
                    rich={"textAlign": "center", "verticalAlign": "bottom"}  # 调整标签位置
                )
            )
        )
    )

    # 生成静态图片
    file_path = "./bar.html"
    bar.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=900, height=1000)



def visualize_wordcloud(data):
    # 提取词汇列表和词频列表
    words = [item['word'] for item in data]
    counts = [item['count'] for item in data]

    # 将词汇和词频列表转换为元组列表
    word_freq = list(zip(words, counts))

    # 创建词云图实例
    wordcloud = (
        WordCloud()
        .add(series_name="", data_pair=word_freq, word_size_range=[20, 100])
        .set_global_opts(title_opts=opts.TitleOpts(title="词云图"))
    )

    file_path = "./WordCloud.html"
    wordcloud.render(file_path)

    # 读取HTML文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示HTML文件
    st.components.v1.html(html, width=900, height=1000)


def visualize_scatter(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建散点图实例
    scatter = (
        Scatter(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x_data)
        .add_yaxis("", y_data)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="散点图"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_style='italic'))
            )
    )

    file_path = "./scatter.html"
    scatter.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=900, height=1000)


def visualize_radar(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建雷达图实例
    radar = (
        Radar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_schema(schema=[
            opts.RadarIndicatorItem(name=x, max_=max(y_data)) for x in x_data
        ])
        .add("", [y_data])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="雷达图"))
    )

    # # 生成静态图片
    # make_snapshot(driver, radar.render(), "chart.png")
    file_path = "./radar.html"
    radar.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=900, height=1000)





def visualize_funnel(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建漏斗图实例
    funnel = (
        Funnel(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("", [list(z) for z in zip(x_data, y_data)])
        .set_global_opts(title_opts=opts.TitleOpts(title="漏斗图"), legend_opts=opts.LegendOpts(orient='horizontal', pos_bottom='0%')
                         )
    )

    # 保存图表为本地文件
    file_path = "./funnel.html"
    funnel.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=900, height=600)

# 可视化函数
def visualize_gauge(data):
    # 提取x_data和y_data
    x_data = [item['word'] for item in data]
    y_data = [item['count'] for item in data]

    # 创建仪表盘实例
    gauge = (
        Gauge(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("", [list(z) for z in zip(x_data, y_data)])
        .set_global_opts(title_opts=opts.TitleOpts(title="仪表盘"))
    )

    # 保存图表为本地文件
    file_path = "./gauge.html"
    gauge.render(file_path)

    # 读取图表文件内容
    with open(file_path, 'r') as f:
        html = f.read()

    # 显示图表
    st.components.v1.html(html, width=800, height=400)




def main():
    st.sidebar.title("导航栏")
    navigation = st.sidebar.radio("选择页面", ["主页", "关于", "联系我们"])

    if navigation == "主页":
        st.title("网页数据可视化")
        url = st.text_input("请输入网址")
        chart_type = st.selectbox(
            "请选择图表类型", ["饼图", "折线图", "柱状图", "词云图", "散点图", "雷达图", "漏斗图", "仪表盘"])

        if st.button("获取数据"):
            if not url:
                st.warning("请输入网址")
            else:
                data = get_data(url)
                if chart_type == "饼图":
                    visualize_pie(data)
                elif chart_type == "折线图":
                    visualize_line(data)
                elif chart_type == "柱状图":
                    visualize_bar(data)
                elif chart_type == "词云图":
                    visualize_wordcloud(data)
                elif chart_type == "散点图":
                    visualize_scatter(data)
                elif chart_type == "雷达图":
                    visualize_radar(data)
                elif chart_type == "漏斗图":
                    visualize_funnel(data)
                elif chart_type == "仪表盘":
                    visualize_gauge(data)

                st.markdown("<br></br>", unsafe_allow_html=True)

    elif navigation == "关于":
        st.title("关于我们")
        st.write("这是一个数据可视化应用的示例。")

    elif navigation == "联系我们":
        st.title("联系我们")
        st.write("如果您有任何问题，请发送邮件至3227404687@qq.com。")
        
if __name__ == "__main__":
    main()
