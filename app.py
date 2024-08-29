from dash import Dash, html, page_container, dcc, get_asset_url
import dash_bootstrap_components as dbc
import config
import constants

#### Start dash app with correct stylesheets ####
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
w3schools = 'https://www.w3schools.com/w3css/4/w3.css'
external_stylesheets = [dbc.themes.JOURNAL,  dbc.icons.FONT_AWESOME, dbc_css, w3schools]

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets, use_pages=True)
app.title = 'Backyard - Insight'
server = app.server

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href='#', id="about-navlink", n_clicks=0)),
        dbc.Modal([dbc.ModalHeader(dbc.ModalTitle("About")), dcc.Markdown(children=[open('assets/text/about.md', 'r').read()])], size='xl', id="about-modal"),
        dbc.NavItem(dbc.NavLink(html.I(className="fa-brands fa-github"), href="https://github.com/tmltsang/ggstrive_tournament_dashboard")),
    ],
    brand="Backyard Insight",
    brand_href="#",
    brand_style={'font-size': '1.5rem'},
    fluid=True,
    color="#cc0000",
    dark=True,
)
footer = html.Footer([
    "Backyard Insight is not endorsed by © ARC SYSTEM WORKS or any tournaments shown. "+
    "It is an unofficial statistics website made without input from anyone officially involved in © ARC SYSTEM WORKS, Arcsys World Tour or any other tournaments. "+
    "More info on Guilty Gear -Strive- can be found at ",
    html.A("https://www.guiltygear.com/ggst/en/", href="https://www.guiltygear.com/ggst/en/")
], className='footer')

app.layout = dbc.Container(
    [   navbar,
        page_container,
        html.Hr(),
        footer
    ],
    fluid=True,
    style={'padding': 0},
    className="dbc"
)
import pages.callbacks

### Starting the app ###
if __name__ == '__main__':
    if config.get(constants.IS_DOCKER_KEY, is_bool=True):
        app.run(debug=config.get(constants.DEBUG_KEY, is_bool=True), host="0.0.0.0", port=8080)
    else:
        app.run(debug=config.get(constants.DEBUG_KEY, is_bool=True))
