// base
$("#grammar-text-area").val("S → ACB | Cbb | Ba \nA → da | BC \nB → g | λ \nC → h |  λ");
$("#grammar-text-area").focus();
let Alphabet = /^[a-zA-Z]+$/;
let UpperCase = /^[A-Z]+$/;
let lowerCase = /^[a-z]+$/;
let symbols = "λ|";
let number = /^[0-9]+$/;

// global variables, list, dictionary
let starters = [];
let emptiness = {};
let firsts = {};
let follows = {};
let outputEmptiness = {};
let first = "";
let char = '';
let start = '';

// typewriter animation
let text = "";
let textFollow = "";
let timeOutFirst;
let timeOutFollow;
let characterFirst = 0;
let characterFollow = 0;
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
// // remove char from textarea
// function deleteChar() {
//     let currentText = $("#grammar-text-area").val();
//     let newText = "";
//     for (let i = 0; i < currentText.length - 1; i++) {
//         newText += currentText[i];
//     }
//     $("#grammar-text-area").val(newText);
//     $("#grammar-text-area").focus();
// }


// main
function main() {
    nullAll();
    let lines = getGrammar();
    if (checkGrammarSyntax(lines) && lines !== false) {
        let grammar = separateGrammarLines(lines);
        // let var_and_terminal = getVarTerminal(lines);
        getFirst(grammar); // reliable
        getFollow(grammar);
        showResult();
        // console.log(grammar);
        // console.log(var_and_terminal);
        // console.log(emptiness);
        // console.log(starters);
        // console.log(firsts);
        // console.log(follows);
    } else {
        Swal.fire({
            title: "Grammar is not valid :(",
            icon: "error",
        });
    }
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


// get firsts too messy !
function getFirst(grammar) {
    let tmp = "";
    let tmp2 = "";

    first = "";
    char = '';

    checkEmptiness(grammar);

    for (let i = 0; i < starters.length; i++) {
        first = "";
        char = starters[i]
        grammar[char].forEach(element => {
            first += element[0];
            let c = 0;
            while (true) {
                if (UpperCase.test(element[c]) && emptiness[element[c]] === true) {
                    c++;
                    if (c < element.length) {
                        first += element[c];
                    } else {
                        emptiness[char] = true;
                    }
                } else {
                    break;
                }
            }
        });
        firsts[char] = first;
    }

    // replace variables
    let Capital = false;
    let n = 0;
    while (n < 10) {
        for (let i = 0; i < starters.length; i++) {
            let first = firsts[starters[i]];
            // check for variables
            for (let j = 0; j < first.length; j++) {
                if (UpperCase.test(first[j])) {
                    Capital = true;
                    break;
                }
            }
            // remove variables
            if (Capital) {
                tmp = "";
                for (let j = 0; j < first.length; j++) {
                    if (UpperCase.test(first[j])) {
                        tmp += firsts[first[j]];
                    } else {
                        tmp += first[j];
                    }
                }
                firsts[starters[i]] = tmp;
            }
            tmp2 = "";
            if (outputEmptiness[starters[i]] === false && emptiness[starters[i]] === false) {
                // remove all lambda
                tmp = firsts[starters[i]];
                for (let j = 0; j < tmp.length; j++) {
                    if (tmp[j] === "λ") { } else {
                        tmp2 += tmp[j]
                    }
                }
                firsts[starters[i]] = tmp2;
            }
        }
        n++;
    }

    // remove duplicate
    let firstsList = [];
    for (let i = 0; i < starters.length; i++) {
        char = starters[i];
        first = firsts[char];
        for (let j = 0; j < first.length; j++) {
            if (UpperCase.test(first[j])) { } else {
                firstsList.push(first[j]);
            }
        }
        firsts[char] = [...new Set(firstsList)];
        firstsList = [];
    }
}

// check output emptiness
function checkEmptiness(grammar) {
    let empty = true;
    char = '';

    // check emptiness ! no terminal & all var include lambda
    for (let i = 0; i < starters.length; i++) {
        char = starters[i]

        grammar[char].forEach(element => {
            empty = true;
            for (let j = 0; j < element.length; j++) {
                if (element[j] === "λ") {
                    break;
                }
                if (lowerCase.test(element[j]) || emptiness[element[j]] === false) {
                    empty = false;
                    break;
                }
            }
            if (outputEmptiness[char] === true) { } else {
                outputEmptiness[char] = empty;
                if (empty) {
                    emptiness[char] = true;
                }
            }
        });
    }
}

// follow rules
// 1) FOLLOW(S) = { $ }   // where S is the starting Non-Terminal OK

// 2) If A -> pBq is a production, where p, B and q are any grammar symbols,
//    then everything in FIRST(q)  except Є is in FOLLOW(B). OK

// 3) If A->pB is a production, then everything in FOLLOW(A) is in FOLLOW(B).

// 4) If A->pBq is a production and FIRST(q) contains Є, 
//    then FOLLOW(B) contains { FIRST(q) – Є } U FOLLOW(A) OK 

// get follows
function getFollow(grammar) {
    start = '';
    let length = starters.length;
    let count = 0;
    // pre add empty string to prevent undefined 
    for (let i = 0; i < length; i++) {
        start = starters[i];
        follows[start] = "";
    }
    follows[starters[0]] += "3$,"
    for (let i = 0; i < length; i++) {
        start = starters[i];
        grammar[start].forEach(element => {
            if (UpperCase.test(element[0])) {
                addFollow(element, 0)
            }
            count = 0;
            while (count < element.length) {
                if (UpperCase.test(element[count])) {
                    addFollow(element, count)
                }
                count++;
            }

        });
    }
    // rule 3 checker
    rule3check(grammar);

    // convert first, fix, follow and remove lambda
    let n = 0;
    let followList = [];
    let operation = [];
    let follow = "";
    let tmp = "";
    while (n < 10) {
        followList = [];
        operation = [];
        follow = "";
        tmp = "";
        for (let i = 0; i < length; i++) {
            start = starters[i];
            followList = follows[start].split(",");
            for (let j = 0; j < followList.length; j++) {
                operation = followList[j];
                if (operation !== "" && operation.length > 1) {
                    if (operation[0] === "1") {
                        if (UpperCase.test(operation[1])) {
                            firsts[operation[1]].forEach(element => {
                                if (element !== 'λ' && element !== "") {
                                    follow += element + ",";
                                }
                            });
                        } else {
                            follow += operation[1] + ",";
                        }
                    }
                    else if (operation[0] === "2") {
                        tmp = follows[operation[1]];
                        for (let k = 0; k < tmp.length; k++) {
                            if (number.test(tmp[k]) || tmp[k] === " " || UpperCase.test(tmp[k])) { } else {
                                follow += tmp[k] + ",";
                            }
                        }
                    }
                    else if (operation[0] === "3") {
                        follow += '$' + ",";
                    }
                } else if (operation !== "") {
                    follow += operation + ",";
                }
            }
            follows[start] = follow;
            follow = "";
        }
        n++;
    }

    // remove duplicates
    for (let i = 0; i < length; i++) {
        start = starters[i];
        followList = follows[start].split(",");
        followList.pop();
        follows[start] = [...new Set(followList)];
    }
}

function addFollow(element, c) {
    let count = c;
    while (count < element.length) {
        if (UpperCase.test(element[c])) {
            for (let j = count + 1; j < element.length; j++) {
                follows[element[c]] += "1" + element[j] + ",";
            }
        }
        count++;
    }
}
// A->pB
function rule3check(grammar) {
    let length = starters.length;

    for (let i = 0; i < length; i++) {
        start = starters[i];
        grammar[start].forEach(element => {
            if (UpperCase.test(element[element.length - 1])) {
                follows[element[element.length - 1]] += "2" + start + ",";
                for (let j = element.length - 1; j >= 0; j--) {
                    if (UpperCase.test(element[j]) && emptiness[element[j]]) {
                        if (j !== 0) {
                            j--;
                        } else {
                            break;
                        }
                        if (UpperCase.test(element[j])) {
                            follows[element[j]] += "2" + start + ",";
                            j++;
                        }
                    } else {
                        break;
                    }
                }
            }
        });
    }
}


// reset all for new grammar
function nullAll() {
    starters = [];
    emptiness = {};
    firsts = {};
    follows = {};
    outputEmptiness = {};
    first = "";
    char = '';
}

// show first and follow 
function showResult() {
    text = "";
    textFollow = "";
    for (let i = 0; i < starters.length; i++) {
        text += "first(" + starters[i] + ") = {" + firsts[starters[i]] + "} <br>";
        textFollow += "follow(" + starters[i] + ") = {" + follows[starters[i]] + "} <br>";
    }
    characterFirst = 0;
    characterFollow = 0;
    document.getElementById("first").innerHTML = "";
    document.getElementById("follow").innerHTML = "";
    document.getElementById("check-btn").disabled = true;
    typeWriterFirst();
}

// typewriter animation
function typeWriterFirst() {
    if (text[characterFirst] === '<') {
        document.getElementById("first").innerHTML += "<br>";
        characterFirst += 4;
    }
    if (characterFirst > text.length - 1) {
        clearTimeout(timeOutFirst);
        typeWriterFollow();
        return true;
    }
    document.getElementById("first").innerHTML += text[characterFirst];
    characterFirst++;
    setTimeout(typeWriterFirst, speed);
}
function typeWriterFollow() {
    if (textFollow[characterFollow] === '<') {
        document.getElementById("follow").innerHTML += "<br>";
        characterFollow += 4;
    }
    if (characterFollow > textFollow.length - 1) {
        clearTimeout(timeOutFollow);
        document.getElementById("check-btn").disabled = false;
        return true;
    }
    document.getElementById("follow").innerHTML += textFollow[characterFollow];
    characterFollow++;
    setTimeout(typeWriterFollow, speed);
}