# Module 7 Final: Modified Penguins Dashboard - Albert Kabore

# ----------------------------------------------
# IMPORTS
# ----------------------------------------------
import seaborn as sns
from faicons import icon_svg
from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins

# -----------------------------------------------
# LOAD DATA
# -----------------------------------------------
df = palmerpenguins.load_penguins()

# -----------------------------------------------
# PAGE OPTIONS
# -----------------------------------------------
ui.page_opts(title="Albert Kabore – Penguins Dashboard", fillable=True)

# -----------------------------------------------
# SIDEBAR
# -----------------------------------------------
with ui.sidebar(title="Filter Controls"):
    ui.input_slider("mass", "Max Body Mass (g)", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    ui.hr()
    ui.h6("Helpful Links")
    
    # PERSONALIZED LINKS FOR ALBERT KABORE
    ui.a("GitHub Source (Albert Kabore)", href="https://github.com/albertokabore/cintel-07-tdash", target="_blank")
    ui.a("Deployed App", href="https://albertokabore.github.io/cintel-07-tdash/", target="_blank")
    ui.a("GitHub Issues", href="https://github.com/albertokabore/cintel-07-tdash/issues", target="_blank")
    ui.a("PyShiny Docs", href="https://shiny.posit.co/py/", target="_blank")
    ui.a("Dashboard Template", href="https://shiny.posit.co/py/templates/dashboard/", target="_blank")

# -----------------------------------------------
# VALUE BOXES
# -----------------------------------------------
with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "Number of Penguins"
        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Average Bill Length"
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Average Bill Depth"
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# -----------------------------------------------
# CHARTS AND DATA TABLE
# -----------------------------------------------
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Depth (by Species)")

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

# -----------------------------------------------
# REACTIVE CALCULATION FOR FILTERING DATA
# -----------------------------------------------
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
