import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Automated Infographic Generator",
    page_icon="📊",
    layout="wide"
)


# ============================================================
# PROFESSIONAL UI STYLING
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f8fa;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #172033;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #667085;
    margin-bottom: 25px;
}

h2, h3 {
    color: #172033;
}

[data-testid="stFileUploader"] {
    background-color: white !important;
    border: 1px solid #d9dee8 !important;
    border-radius: 12px !important;
    padding: 15px !important;
}

[data-testid="stFileUploader"] label {
    color: #172033 !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button {
    background-color: #172033 !important;
    color: white !important;
    border: 1px solid #172033 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}

[data-testid="stFileUploader"] button p {
    color: white !important;
}

[data-testid="stFileUploader"] section {
    color: #172033 !important;
}

[data-testid="stFileUploader"] small {
    color: #667085 !important;
}

.stButton > button {
    width: 100%;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: 700;
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 8px;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">📊 Automated Infographic Generator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Transform raw data into professional, presentation-ready infographics.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# ============================================================
# CSV UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload your CSV file",
    type=["csv"]
)


# ============================================================
# FUNCTION TO PREPARE DATA
# ============================================================

def prepare_data(data):

    data = data.copy()

    # Remove duplicate rows
    data = data.drop_duplicates()

    # Convert Posts to numeric
    if "Posts" in data.columns:

        data["Posts"] = pd.to_numeric(
            data["Posts"],
            errors="coerce"
        )

    # Convert Engagement to numeric
    if "Engagement" in data.columns:

        data["Engagement"] = pd.to_numeric(
            data["Engagement"],
            errors="coerce"
        )

    # Required columns
    required_columns = [
        "Category",
        "Engagement"
    ]

    # Remove missing values
    data = data.dropna(
        subset=required_columns
    )

    return data


# ============================================================
# INFOGRAPHIC GENERATOR
# ============================================================

def generate_infographic(df, template):

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_posts = (
        df["Posts"].sum()
        if "Posts" in df.columns
        else len(df)
    )

    total_engagement = df["Engagement"].sum()

    average_engagement = df["Engagement"].mean()

    highest_engagement = df["Engagement"].max()

    lowest_engagement = df["Engagement"].min()


    # --------------------------------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------------------------------

    category_engagement = (
        df.groupby("Category")["Engagement"]
        .mean()
        .sort_values(ascending=False)
    )

    best_category = category_engagement.idxmax()

    best_average = category_engagement.max()

    lowest_category = category_engagement.idxmin()

    lowest_average = category_engagement.min()


    # --------------------------------------------------------
    # BEST CATEGORY SHARE
    # --------------------------------------------------------

    best_category_total = (
        df[df["Category"] == best_category]["Engagement"].sum()
    )

    best_category_share = (
        best_category_total /
        total_engagement *
        100
    )


    # --------------------------------------------------------
    # TOP 5 RECORDS
    # --------------------------------------------------------

    top_records = (
        df.nlargest(5, "Engagement")
        .copy()
    )

    top_records["Record"] = [
        f"Record {i + 1}"
        for i in range(len(top_records))
    ]


    # ========================================================
    # TEMPLATE 1 — EXECUTIVE
    # ========================================================

    if template == "Executive":

        fig = plt.figure(
            figsize=(16, 10)
        )

        fig.patch.set_facecolor(
            "#F5F7FA"
        )


        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = fig.add_axes(
            [0, 0.88, 1, 0.12]
        )

        header.set_facecolor(
            "#101C36"
        )

        header.axis("off")


        header.text(
            0.05,
            0.60,
            "AUTOMATED DATA INSIGHT REPORT",
            fontsize=25,
            fontweight="bold",
            color="white"
        )


        header.text(
            0.05,
            0.25,
            "Data-driven performance analysis",
            fontsize=11,
            color="#D6DCE8"
        )


        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        kpis = [

            (
                "TOTAL POSTS",
                f"{total_posts:,.0f}"
            ),

            (
                "TOTAL ENGAGEMENT",
                f"{total_engagement:,.0f}"
            ),

            (
                "AVERAGE ENGAGEMENT",
                f"{average_engagement:,.0f}"
            ),

            (
                "PEAK ENGAGEMENT",
                f"{highest_engagement:,.0f}"
            )
        ]


        positions = [
            0.05,
            0.285,
            0.52,
            0.755
        ]


        for x, (label, value) in zip(
            positions,
            kpis
        ):

            ax = fig.add_axes(
                [x, 0.73, 0.20, 0.11]
            )

            ax.set_facecolor(
                "white"
            )

            ax.set_xticks([])
            ax.set_yticks([])


            for spine in ax.spines.values():
                spine.set_visible(False)


            card = FancyBboxPatch(
                (0, 0),
                1,
                1,
                boxstyle="round,pad=0.015",
                linewidth=1,
                edgecolor="#D9DEE8",
                facecolor="white"
            )

            ax.add_patch(card)


            ax.text(
                0.08,
                0.72,
                label,
                fontsize=8,
                fontweight="bold",
                color="#667085"
            )


            ax.text(
                0.08,
                0.28,
                value,
                fontsize=17,
                fontweight="bold",
                color="#101C36"
            )


        # ----------------------------------------------------
        # CATEGORY CHART
        # ----------------------------------------------------

        ax1 = fig.add_axes(
            [0.06, 0.43, 0.41, 0.24]
        )


        category_sorted = (
            category_engagement
            .sort_values()
        )


        bars = ax1.barh(
            category_sorted.index,
            category_sorted.values
        )


        ax1.set_title(
            "Average Engagement by Category",
            fontsize=14,
            fontweight="bold",
            loc="left"
        )


        ax1.set_xlabel(
            "Average Engagement"
        )


        ax1.grid(
            axis="x",
            linestyle="--",
            alpha=0.25
        )


        ax1.set_axisbelow(True)


        for spine in ax1.spines.values():
            spine.set_visible(False)


        for bar in bars:

            value = bar.get_width()

            ax1.text(
                value,
                bar.get_y() +
                bar.get_height() / 2,
                f" {value:,.0f}",
                va="center",
                fontsize=8
            )


        # ----------------------------------------------------
        # TOP 5 CHART
        # ----------------------------------------------------

        ax2 = fig.add_axes(
            [0.54, 0.43, 0.41, 0.24]
        )


        top_sorted = (
            top_records
            .sort_values("Engagement")
        )


        bars2 = ax2.barh(
            top_sorted["Record"],
            top_sorted["Engagement"]
        )


        ax2.set_title(
            "Top 5 Performing Records",
            fontsize=14,
            fontweight="bold",
            loc="left"
        )


        ax2.set_xlabel(
            "Engagement"
        )


        ax2.grid(
            axis="x",
            linestyle="--",
            alpha=0.25
        )


        ax2.set_axisbelow(True)


        for spine in ax2.spines.values():
            spine.set_visible(False)


        for bar in bars2:

            value = bar.get_width()

            ax2.text(
                value,
                bar.get_y() +
                bar.get_height() / 2,
                f" {value:,.0f}",
                va="center",
                fontsize=8
            )


        # ----------------------------------------------------
        # KEY INSIGHTS
        # ----------------------------------------------------

        fig.text(
            0.06,
            0.34,
            "KEY INSIGHTS",
            fontsize=15,
            fontweight="bold",
            color="#101C36"
        )


        insight = (
            f"Best category: {best_category}\n"
            f"Average engagement: {best_average:,.0f}\n"
            f"Lowest category: {lowest_category}\n"
            f"Average engagement: {lowest_average:,.0f}\n"
            f"Top category share: {best_category_share:.1f}%"
        )


        fig.text(
            0.06,
            0.17,
            insight,
            fontsize=11,
            linespacing=1.7,
            color="#333333"
        )


    # ========================================================
    # TEMPLATE 2 — VISUAL
    # ========================================================

    elif template == "Visual":

        fig = plt.figure(
            figsize=(12, 14)
        )

        fig.patch.set_facecolor(
            "#F4F6F8"
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        fig.text(
            0.08,
            0.95,
            "PERFORMANCE SNAPSHOT",
            fontsize=28,
            fontweight="bold",
            color="#101010"
        )


        fig.text(
            0.08,
            0.925,
            "Automated visual performance report",
            fontsize=11,
            color="#333333"
        )


        # ----------------------------------------------------
        # TOTAL ENGAGEMENT
        # ----------------------------------------------------

        fig.text(
            0.08,
            0.83,
            f"{total_engagement:,.0f}",
            fontsize=40,
            fontweight="bold",
            color="#101010"
        )


        fig.text(
            0.08,
            0.795,
            "TOTAL ENGAGEMENT",
            fontsize=11,
            color="#333333"
        )


        # ----------------------------------------------------
        # AVERAGE ENGAGEMENT
        # ----------------------------------------------------

        fig.text(
            0.50,
            0.83,
            f"{average_engagement:,.0f}",
            fontsize=28,
            fontweight="bold",
            color="#101010"
        )


        fig.text(
            0.50,
            0.795,
            "AVERAGE ENGAGEMENT",
            fontsize=10,
            color="#333333"
        )


        # ----------------------------------------------------
        # PEAK ENGAGEMENT
        # ----------------------------------------------------

        fig.text(
            0.72,
            0.83,
            f"{highest_engagement:,.0f}",
            fontsize=28,
            fontweight="bold",
            color="#101010"
        )


        fig.text(
            0.72,
            0.795,
            "PEAK ENGAGEMENT",
            fontsize=10,
            color="#333333"
        )


        # ----------------------------------------------------
        # CATEGORY CHART
        # ----------------------------------------------------

        ax = fig.add_axes(
            [0.08, 0.49, 0.84, 0.23]
        )


        category_sorted = (
            category_engagement
            .sort_values()
        )


        ax.barh(
            category_sorted.index,
            category_sorted.values
        )


        ax.set_title(
            "CATEGORY PERFORMANCE",
            fontsize=15,
            fontweight="bold",
            loc="left"
        )


        ax.set_xlabel(
            "Average Engagement"
        )


        ax.grid(
            axis="x",
            linestyle="--",
            alpha=0.25
        )


        ax.set_axisbelow(True)


        for spine in ax.spines.values():
            spine.set_visible(False)


        # ----------------------------------------------------
        # TOP 5
        # ----------------------------------------------------

        ax2 = fig.add_axes(
            [0.08, 0.25, 0.84, 0.17]
        )


        top_sorted = (
            top_records
            .sort_values("Engagement")
        )


        ax2.barh(
            top_sorted["Record"],
            top_sorted["Engagement"]
        )


        ax2.set_title(
            "TOP 5 PERFORMING RECORDS",
            fontsize=15,
            fontweight="bold",
            loc="left"
        )


        ax2.set_xlabel(
            "Engagement"
        )


        ax2.grid(
            axis="x",
            linestyle="--",
            alpha=0.25
        )


        ax2.set_axisbelow(True)


        for spine in ax2.spines.values():
            spine.set_visible(False)


        # ----------------------------------------------------
        # KEY TAKEAWAY
        # ----------------------------------------------------

        fig.text(
            0.08,
            0.17,
            "KEY TAKEAWAY",
            fontsize=14,
            fontweight="bold",
            color="#101010"
        )


        fig.text(
            0.08,
            0.12,
            f"{best_category} is the strongest category "
            f"with average engagement of "
            f"{best_average:,.0f}.",
            fontsize=11,
            color="#333333"
        )


    # ========================================================
    # TEMPLATE 3 — ANALYTICAL
    # ========================================================

    else:

        fig = plt.figure(
            figsize=(14, 12)
        )

        fig.patch.set_facecolor(
            "white"
        )


        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        fig.text(
            0.06,
            0.95,
            "ANALYTICAL PERFORMANCE REPORT",
            fontsize=25,
            fontweight="bold",
            color="#101010"
        )


        fig.text(
            0.06,
            0.91,
            "Automated statistical summary",
            fontsize=11,
            color="#333333"
        )


        # ----------------------------------------------------
        # STATISTICS
        # ----------------------------------------------------

        stats = (
            f"Total Posts          : {total_posts:,.0f}\n"
            f"Total Engagement     : {total_engagement:,.0f}\n"
            f"Average Engagement   : {average_engagement:,.0f}\n"
            f"Highest Engagement   : {highest_engagement:,.0f}\n"
            f"Lowest Engagement    : {lowest_engagement:,.0f}"
        )


        fig.text(
            0.06,
            0.80,
            stats,
            fontsize=12,
            linespacing=1.8,
            color="#222222"
        )


        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        category_table = (
            df.groupby("Category")["Engagement"]
            .agg(["count", "sum", "mean"])
            .sort_values(
                "mean",
                ascending=False
            )
        )


        ax_table = fig.add_axes(
            [0.06, 0.48, 0.88, 0.25]
        )


        ax_table.axis("off")


        table_data = []


        for category, row in category_table.iterrows():

            table_data.append(
                [
                    category,
                    int(row["count"]),
                    f"{row['sum']:,.0f}",
                    f"{row['mean']:,.0f}"
                ]
            )


        table = ax_table.table(
            cellText=table_data,
            colLabels=[
                "Category",
                "Posts",
                "Total Engagement",
                "Average Engagement"
            ],
            loc="center",
            cellLoc="center"
        )


        table.auto_set_font_size(
            False
        )


        table.set_fontsize(
            10
        )


        table.scale(
            1,
            1.8
        )


        # ----------------------------------------------------
        # COMPARISON CHART
        # ----------------------------------------------------

        ax3 = fig.add_axes(
            [0.08, 0.22, 0.84, 0.18]
        )


        ax3.bar(
            category_engagement.index,
            category_engagement.values
        )


        ax3.set_title(
            "Average Engagement Comparison",
            fontsize=14,
            fontweight="bold",
            color="#101010"
        )


        ax3.set_ylabel(
            "Average Engagement"
        )


        ax3.tick_params(
            axis="x",
            rotation=25
        )


        ax3.grid(
            axis="y",
            linestyle="--",
            alpha=0.25
        )


        ax3.set_axisbelow(True)


        for spine in ax3.spines.values():
            spine.set_visible(False)


        # ----------------------------------------------------
        # AUTOMATED CONCLUSION
        # ----------------------------------------------------

        fig.text(
            0.06,
            0.14,
            "AUTOMATED CONCLUSION",
            fontsize=14,
            fontweight="bold",
            color="#101010"
        )


        conclusion = (
            f"{best_category} is the highest-performing category "
            f"with an average engagement of {best_average:,.0f}. "
            f"{lowest_category} has the lowest average engagement "
            f"at {lowest_average:,.0f}. "
            f"The top category contributes "
            f"{best_category_share:.1f}% of total engagement."
        )


        fig.text(
            0.06,
            0.09,
            conclusion,
            fontsize=11,
            color="#333333"
        )


    # ========================================================
    # SAVE PNG
    # ========================================================

    os.makedirs(
        "output",
        exist_ok=True
    )


    png_path = (
        "output/generated_infographic.png"
    )


    fig.savefig(
        png_path,
        dpi=300,
        bbox_inches="tight",
        facecolor=fig.get_facecolor()
    )


    # ========================================================
    # SAVE PDF
    # ========================================================

    pdf_path = (
        "output/generated_infographic.pdf"
    )


    with PdfPages(pdf_path) as pdf:

        pdf.savefig(
            fig,
            bbox_inches="tight"
        )


    return fig, png_path, pdf_path


# ============================================================
# STREAMLIT INTERFACE
# ============================================================

if uploaded_file is not None:

    try:

        # ----------------------------------------------------
        # READ CSV
        # ----------------------------------------------------

        raw_df = pd.read_csv(
            uploaded_file
        )


        st.success(
            "CSV uploaded successfully!"
        )


        # ----------------------------------------------------
        # SHOW DATA
        # ----------------------------------------------------

        st.subheader(
            "Preview of Uploaded Data"
        )


        st.dataframe(
            raw_df.head(10),
            use_container_width=True
        )


        # ----------------------------------------------------
        # PREPARE DATA
        # ----------------------------------------------------

        df = prepare_data(
            raw_df
        )


        # ----------------------------------------------------
        # CHECK REQUIRED COLUMNS
        # ----------------------------------------------------

        required = [
            "Category",
            "Engagement"
        ]


        missing = [
            col
            for col in required
            if col not in df.columns
        ]


        if missing:

            st.error(
                "Missing required columns: "
                + ", ".join(missing)
            )


        else:

            st.success(
                f"Data ready! {len(df)} records available."
            )


            # ------------------------------------------------
            # TEMPLATE SELECTOR
            # ------------------------------------------------

            template = st.selectbox(
                "Select Infographic Template",
                [
                    "Executive",
                    "Visual",
                    "Analytical"
                ]
            )


            # ------------------------------------------------
            # GENERATE BUTTON
            # ------------------------------------------------

            if st.button(
                "🚀 Generate Infographic",
                use_container_width=True
            ):

                with st.spinner(
                    "Generating infographic..."
                ):

                    fig, png_path, pdf_path = (
                        generate_infographic(
                            df,
                            template
                        )
                    )


                st.success(
                    "Infographic generated successfully!"
                )


                # ------------------------------------------------
                # DISPLAY INFOGRAPHIC
                # ------------------------------------------------

                st.pyplot(
                    fig
                )


                plt.close(
                    fig
                )


                # ------------------------------------------------
                # DOWNLOAD SECTION
                # ------------------------------------------------

                st.subheader(
                    "Download Your Infographic"
                )


                # PNG DOWNLOAD

                with open(
                    png_path,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇️ Download PNG",
                        data=file,
                        file_name="infographic.png",
                        mime="image/png"
                    )


                # PDF DOWNLOAD

                with open(
                    pdf_path,
                    "rb"
                ) as file:

                    st.download_button(
                        label="⬇️ Download PDF",
                        data=file,
                        file_name="infographic.pdf",
                        mime="application/pdf"
                    )


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )