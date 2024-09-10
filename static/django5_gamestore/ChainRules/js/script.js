// base
// $("#grammar-text-area").val("S → ACB | Cbb | B \nA → da | BC \nB → g | λ \nC → h |  λ");
$("#grammar-text-area").val("S → aA | B\nA → a | B\nB → bB | C\nC → b");
$("#grammar-text-area").focus();
let Alphabet = /^[a-zA-Z]+$/;
let UpperCase = /^[A-Z]+$/;
let lowerCase = /^[a-z]+$/;
let symbols = "λ|";
let number = /^[0-9]+$/;

// global variables, list, dictionary
let grammar = {};
let starters = [];
let emptiness = {};
let soloVar = {};
let char = '';
let start = '';
let n = 0;
let startBan = [];
let no_use = {};

// typewriter animation
let text = "";
let timeOut;
let character = 0;
let speed = 50;

// add symbols to textarea
function addToText(btn) {
    let symbol = btn.value;
    let currentText = $("#grammar-text-area").val();
    let cursorPosition = $('#grammar-text-area').prop("selectionStart");
    let txt_area = document.getElementById("grammar-text-area");
    let tmp = "";

    for (let i = 0; i < currentText.length; i++) {
        tmp += currentText[i];
        if (i === cursorPosition - 1) {
            tmp += symbol;
        }
    }
    $("#grammar-text-area").val(tmp);
    txt_area.focus();
    txt_area.selectionEnd = cursorPosition + 1;

}

// change input to symbol
function changeToSymbol(textarea) {
    let currentText = $(textarea).val();
    let len = currentText.length;
    let sym = "";
    let tmp = "";
    let rewrite = false;
    let cursorPosition = $('#grammar-text-area').prop("selectionStart");
    if (currentText[cursorPosition - 1] === "1") {
        sym = "→";
        rewrite = true;
    } else if (currentText[cursorPosition - 1] === "2") {
        sym = "|";
        rewrite = true;
    } else if (currentText[cursorPosition - 1] === "3") {
        sym = "λ";
        rewrite = true;
    }

    if (rewrite) {
        for (let i = 0; i < len; i++) {
            if (i === cursorPosition - 1) {
                tmp += sym;
            } else {
                tmp += currentText[i];
            }
        }
        $(textarea).val(tmp);
        textarea.focus();
        textarea.selectionEnd = cursorPosition;
    }
}

// main
function main() {
    nullAll();
    let lines = getGrammar();
    if (checkGrammarSyntax(lines) && lines !== false) {
        grammar = separateGrammarLines(lines);
        let var_and_terminal = getVarTerminal(lines);
        while (n < 20) {
            soloVariables();
            convertSolo();
            n++;
        }
        removeNoUsedVars();
        showResult();

        // console.log(grammar);
        // console.log(var_and_terminal);
        // console.log(emptiness);
        // console.log(startBan);
        // console.log(soloVar)
    } else {
        Swal.fire({
            title: "Grammar is not valid :(",
            icon: "error",
        });
    }
}

// get grammar
function getGrammar() {
    let currentText = $("#grammar-text-area").val();
    let lines = [];
    let line = '';
    let c = 0;

    if (currentText !== "") {
        for (let i = 0; i < currentText.length; i++) {
            if (currentText[i] === '\n') {
                lines[c] = line;
                line = '';
                c++;
            } else if (currentText[i] !== " ") {
                line += currentText[i];
            }
            if (i === currentText.length - 1) {
                lines[c] = line;
            }
        }
        return lines;
    }
    return false;
}
// check grammar syntax ! not reliable
function checkGrammarSyntax(lines) {
    for (let i = 0; i < lines.length; i++) {
        if (UpperCase.test(lines[i][0]) && lines[i][1] === '→') { } else {
            return false;
        }
        for (let j = 2; j < lines[i].length; j++) {
            if (Alphabet.test(lines[i][j]) || symbols.includes(lines[i][j])) { } else {
                return false;
            }
        }
    }
    return true;
}
// each line output(s)
function separateGrammarLines(lines) {
    starters = []
    let grammar = {};
    let outputs = []; // things that come after →
    let start = lines[0][0];
    let string = '';
    // get line starter and outputs
    for (let i = 0; i < lines.length; i++) {
        start = lines[i][0];
        starters.push(start);
        for (j = 2; j < lines[i].length; j++) {
            if (lines[i][j] !== '|') {
                string += lines[i][j];
            } else {
                outputs.push(string);
                string = "";
            }
            if (lines[i][j] === "λ") {
                emptiness[start] = true;
            }
            if (j === lines[i].length - 1) {
                outputs.push(string);
                string = "";
            }
        }
        if (emptiness[start] !== true) {
            emptiness[start] = false;
        }
        grammar[start] = outputs;
        outputs = [];
    }

    return grammar;
}
// get variable and terminals individually
function getVarTerminal(lines) {
    let var_terminals = {};
    let variable = [];
    let terminals = [];
    for (let i = 0; i < lines.length; i++) {
        for (let j = 0; j < lines[i].length; j++) {
            if (lowerCase.test(lines[i][j])) {
                terminals.push(lines[i][j]);
            } else if (UpperCase.test(lines[i][j])) {
                variable.push(lines[i][j]);
            }
        }
    }
    var_terminals["var"] = [...new Set(variable)];
    var_terminals["terminal"] = [...new Set(terminals)];

    return var_terminals
}


// find all solo variables
function soloVariables() {
    let soloList = [];
    for (let i = 0; i < starters.length; i++) {
        start = starters[i];
        grammar[start].forEach(element => {
            if (element.length === 1 && UpperCase.test(element)) {
                soloList.push(element);
                startBan.push(element);
            }
        });
        soloVar[start] = soloList;
        soloList = [];
    }
}

// convert solos 
function convertSolo() {
    for (let i = 0; i < starters.length; i++) {
        start = starters[i];
        for (let j = 0; j < soloVar[start].length; j++) {
            replaceVar(soloVar[start][j], start);
        }
    }
}

function replaceVar(varR, startVar) {
    let index = grammar[startVar].indexOf(varR);
    for (let i = 0; i < grammar[varR].length; i++) {
        if (grammar[varR][i] !== startVar) {
            if (i === 0) {
                grammar[startVar][index] = grammar[varR][i]
            } else {
                grammar[startVar].push(grammar[varR][i])
            }
        }
    }
    grammar[startVar] = [...new Set(grammar[startVar])]
}

// remove unnecessary variables ToDo!
function removeNoUsedVars() {
    no_use[starters[0]] = false;
    for (let i = 0; i < starters.length; i++) {
        start = starters[i];
        grammar[start].forEach(element => {
            for (let j = 0; j < element.length; j++) {
                if (UpperCase.test(element[j]) && element[j] !== start) {
                    no_use[element[j]] = false;
                }
            }
        });
    }
    console.log(no_use)
}

// function checkSolo() { !!!
//     for (let i = 0; i < starters.length; i++) {
//         start = starters[i]
//         grammar[start].forEach(element => {
//             if (element.length === 1 && UpperCase.test(element)) {
//                 return true;
//             }
//         });
//     }
//     return false;
// }


// show result

function showResult() {
    text = "";
    let length = 0;
    for (let i = 0; i < starters.length; i++) {
        start = starters[i];
        if (no_use[start] === false) {
            text += start + " → ";
            length = grammar[start].length;
            for (let j = 0; j < length; j++) {
                if (j === length - 1) {
                    text += grammar[start][j];
                } else {
                    text += grammar[start][j] + " | ";
                }
            }
            text += "<br>";
        }
    }
    character = 0;
    document.getElementById("result").innerHTML = "";
    document.getElementById("check-btn").disabled = true;
    typeWriter();
}

// // typewriter animation
function typeWriter() {
    if (text[character] === '<') {
        document.getElementById("result").innerHTML += "<br>";
        character += 4;
    }
    if (character > text.length - 1) {
        clearTimeout(timeOut);
        document.getElementById("check-btn").disabled = false;
        return true;
    }
    document.getElementById("result").innerHTML += text[character];
    character++;
    setTimeout(typeWriter, speed);
}

// reset all for new grammar
function nullAll() {
    grammar = {};
    starters = [];
    emptiness = {};
    soloVar = {};
    char = '';
    start = '';
    n = 0;
    startBan = [];
    no_use = {};
}