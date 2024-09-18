

const CDN_URL = "https://cdn.jsdelivr.net/gh/tmltsang/Backyard-Insight";
const FULL_HEART = `${CDN_URL}/assets/images/ui/Hud_Heart_Neutral.png`;
const EMPTY_HEART = `${CDN_URL}/assets/images/ui/Hud_Heart_Blank.png`;
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
        hover_data: function(hoverData, clickData, currMatchDf, currAsukaStatsDf) {
            const dataDict = {};
            let x = null;
            data = hoverData || clickData;
            if (data !== undefined) {
                x = data.points[0].x;
                const currState = currMatchDf[x] || null;
                for (const player of [P1, P2]) {
                    if (currState) {
                        dataDict[player] = {};
                        for (const value of ['health', 'tension', 'burst', 'counter', 'curr_damaged', 'round_count']) {
                            dataDict[player][value] = currState[`${player}_${value}`];
                        }
                        if (player === P1) {
                            const p1RoundWinProb = Math.round(currState.smooth_round_pred * 100 * 10) / 10;
                            window.dash_clientside.set_props('round_win_prob_bar', {'style':{"--w": `${p1RoundWinProb}%`}})
                            window.dash_clientside.set_props('p1_round_win_text', {'children':[`${p1RoundWinProb}%`]})
                            window.dash_clientside.set_props('p2_round_win_text', {'children':[`${Math.round((100 - p1RoundWinProb) * 10) / 10 }%`]})

                            const p1SetWinProb = Math.round(currState.smooth_set_pred * 100 * 10) / 10;
                            window.dash_clientside.set_props('set_win_prob_bar', {'style':{"--w": `${p1SetWinProb}%`}})
                            window.dash_clientside.set_props('p1_match_win_text', {'children':[`${p1SetWinProb}%`]})
                            window.dash_clientside.set_props('p2_match_win_text', {'children':[`${Math.round((100 - p1SetWinProb) * 10) / 10}%`]})

                        }
                    }
                    if (currAsukaStatsDf) {
                        if (currAsukaStatsDf[player]) {
                            const currAsukaState = currAsukaStatsDf[player][x] || null;
                            if (currAsukaState) {
                                let spells = Array.from({ length: 4 }, (_, num) => currAsukaState[`asuka_spell_${num + 1}`]);
                                for (let i = 0; i < 4; i++) {
                                    window.dash_clientside.set_props(`${player}_spell_${i+1}`, {
                                        src: `${CDN_URL}/assets/images/spells/${spells[i]}.png`,
                                        style: {
                                            'opacity': spells[i] !== 'used_spell' ? 1.0 : 0.0}
                                    });
                                }
                                window.dash_clientside.set_props(`${player}_spell`, {style : {}})
                                window.dash_clientside.set_props(`${player}_spell_percentile`, {'children': `${currAsukaState.spell_percentile_mlp}%`});
                            }
                        }
                    }
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
                        window.dash_clientside.set_props(`${playerSide}_${bar}_bar`, {'style': backgroundStyle, 'className': backgroundClassName});
                        window.dash_clientside.set_props(`${playerSide}_${bar}_text`, {'children':[`${value}%` ], 'style': { "--w": `${value}%` }, 'className': barClassName});
                    }

                    window.dash_clientside.set_props(`${playerSide}_counter`, {'children': [data.counter]});

                    const heartSide = playerSide === P2 ? P1 : P2;
                    if (data.round_count == 0){
                        window.dash_clientside.set_props(`${heartSide}_sub_heart`, {'src': FULL_HEART});
                        window.dash_clientside.set_props(`${heartSide}_main_heart`, {'src': FULL_HEART});
                    } else if (data.round_count == 1) {
                        window.dash_clientside.set_props(`${heartSide}_sub_heart`, {'src': EMPTY_HEART});
                        window.dash_clientside.set_props(`${heartSide}_main_heart`, {'src': FULL_HEART});
                    } else {
                        window.dash_clientside.set_props(`${heartSide}_sub_heart`, {'src': EMPTY_HEART});
                        window.dash_clientside.set_props(`${heartSide}_main_heart`, {'src': EMPTY_HEART});
                    }
                }
            }
            return [
                window.dash_clientside.no_update
            ];
        }
    }
});

