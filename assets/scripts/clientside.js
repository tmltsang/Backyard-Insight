

const CDN_URL = "https://cdn.jsdelivr.net/gh/tmltsang/Backyard-Insight";
const FULL_HEART = 'assets/images/ui/Hud_Heart_Neutral.png';
const EMPTY_HEART = 'assets/images/ui/Hud_Heart_Blank.png';
const DEFAULT_HEALTH = 1;
const DEFAULT_TENSION = 0;
const DEFAULT_BURST = 1;
const DEFAULT_COUNTER = 0;
const DEFAULT_CURR_DAMAGED = false;
const DEFAULT_ROUND_COUNT = 0;
const DEFAULT_WIN_PROB = 50;
const P1 = 'p1';
const P2 = 'p2';

const DEFAULT_PRED_HD = {
    P1: {
        set_win_prob: DEFAULT_WIN_PROB,
        health: DEFAULT_HEALTH,
        tension: DEFAULT_TENSION,
        burst: DEFAULT_BURST,
        counter: DEFAULT_COUNTER,
        curr_damaged: DEFAULT_CURR_DAMAGED,
        round_count: DEFAULT_ROUND_COUNT,
        round_win_prob: DEFAULT_WIN_PROB
    },
    P2: {
        set_win_prob: DEFAULT_WIN_PROB,
        health: DEFAULT_HEALTH,
        tension: DEFAULT_TENSION,
        burst: DEFAULT_BURST,
        counter: DEFAULT_COUNTER,
        curr_damaged: DEFAULT_CURR_DAMAGED,
        round_count: DEFAULT_ROUND_COUNT,
        round_win_prob: DEFAULT_WIN_PROB
    }
};

function createDiv(children, style={}, className="") {
    return {
        'type': 'Div',
        'namespace': 'dash_html_components',
        'props': {
            'children': children,
            'className': className,
            'style': style,
        }
    };
}

function createImg(src, style={}, className="") {
    return {
        'type': 'Img',
        'namespace': 'dash_html_components',
        'props': {
            'src': src,
            'className': className,
            'style': style,
        }
    };
}

window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        hover_data: function(hoverData, currMatchDf, currAsukaStatsDf) {
            let bars = {
                p1: {
                    round_count:  window.dash_clientside.no_update,
                    health:  window.dash_clientside.no_update,
                    burst:  window.dash_clientside.no_update,
                    tension:  window.dash_clientside.no_update,
                    counter:  window.dash_clientside.no_update,
                },
                p2: {
                    round_count:  window.dash_clientside.no_update,
                    health:  window.dash_clientside.no_update,
                    burst:  window.dash_clientside.no_update,
                    tension:  window.dash_clientside.no_update,
                    counter:  window.dash_clientside.no_update,
                },
                round_win_prob:  window.dash_clientside.no_update,
                set_win_prob:  window.dash_clientside.no_update
            };
            const dataDict = {};
            const spellData = {};
            let x = null;
            console.log(hoverData)
            if (hoverData !== undefined) {
                x = hoverData.points[0].x;
                const currState = currMatchDf[x] || null;
                for (const player of [P1, P2]) {
                    if (currState) {
                        dataDict[player] = {};
                        for (const value of ['health', 'tension', 'burst', 'counter', 'curr_damaged', 'round_count']) {
                            dataDict[player][value] = currState[`${player}_${value}`];
                        }
                        if (player === P1) {
                            const p1RoundWinProb = Math.round(currState.smooth_round_pred * 100 * 10) / 10;
                            bars.round_win_prob = createDiv([
                                createDiv([`${p1RoundWinProb}%`]),
                                createDiv([`${Math.round(100 - p1RoundWinProb * 10) / 10}%`])
                            ], style={ "--w": `${p1RoundWinProb}%` }, className="win_prob_bar bar_text");
                            const p1SetWinProb = Math.round(currState.smooth_set_pred * 100 * 10) / 10;
                            bars.set_win_prob = createDiv([
                                createDiv([`${p1SetWinProb}%`]),
                                createDiv([`${Math.round(100 - p1SetWinProb * 10) / 10}%`])
                            ], style={ "--w": `${p1SetWinProb}%` }, className="win_prob_bar bar_text");
                        }
                    }
                    if (currAsukaStatsDf) {
                        if (currAsukaStatsDf[player]) {
                            const currAsukaState = currAsukaStatsDf[player][x] || {};
                            if (currAsukaState) {
                                spellData[player] = {};
                                spellData[player].spells = Array.from({ length: 4 }, (_, num) => currAsukaState[`asuka_spell_${num + 1}`]);
                                spellData[player].percentile = currAsukaState.spell_percentile_mlp;
                            }
                        }
                    }
                }
                //const spells = displayAsukaSpellData(spellData, default_value = no_update);
            } else {
                //dataDict = DEFAULT_PRED_HD;
                //const spells = displayAsukaSpellData(spellData);
            }
            for (const playerSide in dataDict) {
                const data = dataDict[playerSide];
                for (const bar of ["health", "burst", "tension"]) {
                    const value = Math.round(100 * data[bar] * 100) / 100;
                    const backgroundStyle = {};
                    const barClassName = `${playerSide}_${bar} bar_text`;
                    let backgroundClassName = `bar_container ${playerSide}`;
                    if (bar === "health" && data.curr_damaged) {
                        backgroundClassName += " curr_dmg";
                        backgroundStyle["--cd_w"] = `${value + 10}%`;
                    } else if (bar === "burst") {
                        backgroundStyle.width = "40%";
                    }
                    console.log(dataDict)
                    if (bar === "health"){
                        window.dash_clientside.set_props(`${playerSide}_${bar}_bar`, {'style': backgroundStyle, 'className': backgroundClassName});
                        window.dash_clientside.set_props(`${playerSide}_${bar}_text`, {'children':[`${value}%` ], 'style': { "--w": `${value}%` }, 'className': barClassName});
                    }
                    bars[playerSide][bar] = createDiv([
                        createDiv([], style={ "--w": `${value}%` }, className=barClassName)
                    ], style=backgroundStyle, className=backgroundClassName);
                }

                bars[playerSide].counter = createDiv([data.counter], className=`bar_label ${playerSide}`, style={ "fontSize": "30px" });

                let currHearts = [createImg(src=`${CDN_URL}/${FULL_HEART}`, className="sub_heart"), createImg(src=`${CDN_URL}/${FULL_HEART}`, className="main_heart")];
                for (let i = 0; i < data.round_count; i++) {
                    currHearts[i].src = `${CDN_URL}/${EMPTY_HEART}`
                }
                const heartSide = playerSide === P2 ? "p1" : "p2";
                currHearts = heartSide === P1 ? currHearts : currHearts.reverse();
                bars[heartSide].round_count = createDiv(currHearts);
            }
            return [
                window.dash_clientside.no_update
            ];
        }
    }
});

