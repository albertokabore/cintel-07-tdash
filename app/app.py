# ===========================================
# 1. Imports
# ==============================================
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

# ==============================================
# 2. Load Data
# ==============================================
df = palmerpenguins.load_penguins()

# ==============================================
# 3. Define Page Layout and Title
# ==============================================
ui.page_opts(title="Albert’s Penguin Explorer", fillable=True)

# ==============================================
# 4. Sidebar: Input Controls and External Links
# ==============================================
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    ui.hr()
    ui.h6("Helpful Resources for PyShiny and This Project")
    ui.a("GitHub Source", href="https://github.com/denisecase/cintel-07-tdash", target="_blank")
    ui.a("GitHub App", href="https://denisecase.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/denisecase/cintel-07-tdash/issues", target="_blank")
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Template: Basic Dashboard", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")
    ui.a("See also", href="https://github.com/denisecase/pyshiny-penguins-dashboard-express", target="_blank")

# ==============================================
# 5. Value Boxes: Summary Statistics
# ==============================================
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Total Penguins Displayed"
        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Avg Bill Length (mm)"
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Avg Bill Depth (mm)"
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# ==============================================
# 6. Cards with Charts and Interactive Table
# ==============================================
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    with ui.card(full_screen=True):
        ui.card_header("Penguin Data Table (Interactive)")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

# ==============================================
# 7. Reactive Calculation for Filtered Data
# ==============================================
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
