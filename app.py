import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

def load_sample_data():
    """Load sample data for the dashboard"""
    np.random.seed(42)
    dates = [datetime.now() - timedelta(days=x) for x in range(30, 0, -1)]
    data = {
        'date': dates,
        'sales': np.random.randint(100, 1000, 30),
        'profit': np.random.randint(10, 100, 30),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 30),
        'product': np.random.choice(['Product A', 'Product B', 'Product C'], 30)
    }
    return pd.DataFrame(data)

def read_csv_flexible(f):
    """尝试多种编码读取CSV，兼容中文Excel导出的文件"""
    for enc in ['utf-8-sig', 'gbk', 'utf-8']:
        try:
            f.seek(0)
            return pd.read_csv(f, encoding=enc)
        except UnicodeDecodeError:
            continue
    f.seek(0)
    return pd.read_csv(f)

def smart_detect(df):
    """智能识别列的类型：日期列 / 数值列 / 分类列"""
    date_col = None
    for c in df.columns:
        if df[c].dtype == 'datetime64[ns]':
            date_col = c
            break
        low = str(c).lower()
        if date_col is None and ('date' in low or any(k in str(c) for k in ['日期', '时间'])):
            try:
                df[c] = pd.to_datetime(df[c], errors='coerce')
                if df[c].notna().sum() > 0:
                    date_col = c
            except Exception:
                pass
    nums = df.select_dtypes(include=[np.number]).columns.tolist()
    cats = [c for c in df.columns if c not in nums and c != date_col]
    value_col = nums[0] if nums else None
    cat_col = cats[0] if cats else None
    return date_col, value_col, cat_col, nums, cats

def main():
    st.set_page_config(
        page_title="智能数据分析看板",
        page_icon="📊",
        layout="wide"
    )
    st.title("📊 智能数据分析看板")
    st.markdown("---")

    # ---------- 侧边栏：数据来源 ----------
    st.sidebar.header("📂 数据来源")
    uploaded_file = st.sidebar.file_uploader(
        "上传你的数据文件（CSV / Excel）",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(('xlsx', 'xls')):
                df = pd.read_excel(uploaded_file)
            else:
                df = read_csv_flexible(uploaded_file)
        except Exception as e:
            st.sidebar.error(f"读取文件失败：{e}")
            st.info("请检查文件格式；CSV 请用 UTF-8 或 GBK 编码保存。")
            return
    else:
        st.sidebar.info("未上传文件时，显示自动生成的示例数据")
        df = load_sample_data()

    # ---------- 智能识别列 ----------
    date_col, value_col, cat_col, nums, cats = smart_detect(df.copy())
    # 确保日期列是真正的日期类型（趋势分析需要）
    if date_col and df[date_col].dtype != 'datetime64[ns]':
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    st.sidebar.markdown("---")
    st.sidebar.header("🔧 列设置（自动识别，可手动修改）")
    all_cols = list(df.columns)

    date_sel = st.sidebar.selectbox("日期列（用于趋势图）", ["（无）"] + all_cols,
                                    index=(["（无）"] + all_cols).index(date_col) if date_col else 0)
    value_sel = st.sidebar.selectbox("数值列（用于求和/统计）", ["（无）"] + all_cols,
                                     index=(["（无）"] + all_cols).index(value_col) if value_col else 0)
    cat_sel = st.sidebar.selectbox("分类列（用于分组对比）", ["（无）"] + all_cols,
                                   index=(["（无）"] + all_cols).index(cat_col) if cat_col else 0)

    date_col = None if date_sel == "（无）" else date_sel
    value_col = None if value_sel == "（无）" else value_sel
    cat_col = None if cat_sel == "（无）" else cat_sel

    # ---------- 顶部标签页 ----------
    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["🏠 数据总览", "📈 趋势分析", "🧩 分类对比", "🔍 数据洞察", "📋 原始数据"]
    )

    # ============ Tab 1 数据总览 ============
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("记录数（行）", f"{len(df):,}")
        with col2:
            st.metric("字段数（列）", len(df.columns))
        with col3:
            st.metric("数值列个数", len(nums))
        with col4:
            if value_col:
                st.metric(f"{value_col} 总计", f"{df[value_col].sum():,.2f}")
            else:
                st.metric("数值总计", "请选择数值列")

        if value_col:
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric(f"{value_col} 平均值", f"{df[value_col].mean():,.2f}")
            with m2:
                st.metric(f"{value_col} 最大值", f"{df[value_col].max():,.2f}")
            with m3:
                st.metric(f"{value_col} 最小值", f"{df[value_col].min():,.2f}")

        st.subheader("数据预览（前 10 行）")
        st.dataframe(df.head(10), use_container_width=True)

    # ============ Tab 2 趋势分析 ============
    with tab2:
        if date_col and nums:
            freq = st.radio("时间粒度", ["日", "周", "月"], horizontal=True)
            rule = {"日": "D", "周": "W", "月": "ME"}[freq]
            pick_nums = st.multiselect("选择要查看的数值列", nums, default=nums[:2])
            if pick_nums:
                tmp = df[[date_col] + pick_nums].dropna().set_index(date_col).resample(rule).sum().reset_index()
                fig = px.line(tmp, x=date_col, y=pick_nums,
                              title=f"{freq}粒度趋势图",
                              markers=True)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("请至少选择一个数值列")
        else:
            st.info("需要同时有【日期列】和【数值列】才能画趋势图。可在左侧「列设置」中手动指定。")

    # ============ Tab 3 分类对比 ============
    with tab3:
        if cat_col:
            pick_value = st.selectbox("对比哪个数值？", nums if nums else ["（无数值列）"])
            agg = st.radio("统计方式", ["求和", "平均", "计数"], horizontal=True)
            if pick_value != "（无数值列）":
                if agg == "求和":
                    grouped = df.groupby(cat_col)[pick_value].sum()
                elif agg == "平均":
                    grouped = df.groupby(cat_col)[pick_value].mean()
                else:
                    grouped = df.groupby(cat_col)[pick_value].count()
                grouped = grouped.sort_values(ascending=False).reset_index()

                c1, c2 = st.columns(2)
                with c1:
                    fig1 = px.bar(grouped.head(15), x=cat_col, y=pick_value,
                                  title=f"按{cat_col}分组 {agg}（Top 15）",
                                  color=pick_value)
                    st.plotly_chart(fig1, use_container_width=True)
                with c2:
                    fig2 = px.pie(grouped.head(10), names=cat_col, values=pick_value,
                                  title=f"{cat_col}占比（Top 10）", hole=0.4)
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                # 纯分类列：看频次
                vc = df[cat_col].value_counts().reset_index()
                vc.columns = [cat_col, 'count']
                fig = px.bar(vc.head(15), x=cat_col, y='count', title=f"{cat_col} 频次分布")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("没有检测到分类列（文本类型的列）。")

    # ============ Tab 4 数据洞察 ============
    with tab4:
        st.subheader("📈 数值列统计摘要")
        if nums:
            st.dataframe(df[nums].describe().T, use_container_width=True)

            st.subheader("📉 数值分布直方图")
            hist_col = st.selectbox("选择数值列查看分布", nums)
            fig = px.histogram(df, x=hist_col, nbins=30, title=f"{hist_col} 的分布")
            st.plotly_chart(fig, use_container_width=True)

            if len(nums) >= 2:
                st.subheader("🔥 相关性热力图（越接近1越正相关，越接近-1越负相关）")
                corr = df[nums].corr(numeric_only=True)
                fig = px.imshow(corr, text_auto=".2f", color_continuous_scale="RdBu_r",
                                title="数值列相关性")
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("没有数值列，无法做统计分析。")

        st.subheader("❓ 每列缺失值数量")
        miss = df.isna().sum()
        miss = miss[miss > 0]
        if len(miss) > 0:
            fig = px.bar(x=miss.index, y=miss.values, labels={'x': '列名', 'y': '缺失数量'},
                         title="缺失值分布")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("所有列都没有缺失值 👍")

    # ============ Tab 5 原始数据 ============
    with tab5:
        keyword = st.text_input("🔎 搜索关键字（模糊筛选整表，留空显示全部）")
        show_df = df
        if keyword:
            mask = df.astype(str).apply(lambda row: row.str.contains(keyword, case=False, na=False).any(), axis=1)
            show_df = df[mask]
        st.dataframe(show_df, use_container_width=True)
        st.caption(f"共 {len(show_df):,} 行（上传数据共 {len(df):,} 行）")

        csv = show_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="⬇️ 下载当前筛选结果为 CSV",
            data=csv,
            file_name=f"analysis_result_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
