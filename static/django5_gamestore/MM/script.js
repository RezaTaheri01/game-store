// base memory
let MS = 32;
let cells = 8;
let cell_array = [];
let p_counter = 0;
let unit_size = 4;
let last_add_index = 0;
let enough_space = false;
let total_waste = 0; // need to add third index for waste
let fade = true;

// sweetAlert and init func
async function getMemorySize() {
    const { value: memorySize } = await Swal.fire({
        title: "Choose your memory size :)",
        icon: "question",
        input: "range",
        inputLabel: "Memory Size(k)",
        allowOutsideClick: false,
        inputAttributes: {
            min: unit_size * 1,
            max: unit_size * 25,
            step: unit_size
        },
        inputValue: unit_size * 16,
    });
    MS = memorySize;
    cells = MS / unit_size;
    init();
}

function init() {
    for (let i = 0; i < cells; i++) {
        cell_array[i] = [];
        cell_array[i][0] = false;
        cell_array[i][1] = null;
        cell_array[i][2] = 0; //waste
        cell_array[i][3] = 0; //size
    }
    memorySize();
    drawMemory();
}
// end sweetAlert and init func

// visual section
function drawMemoryV1() {
    let memory = $("#memory")
    $(memory).empty()

    for (let i = 0; i < cells; i++) {
        if (cell_array[i][0] === true) {
            if (i === 0) {
                $(memory).append("<p class='cell danger rounded-top-2 cell-" + cell_array[i][1] + "' ondblclick='removeFromMemory(this)' onclick='findOnTable(this)'>" + cell_array[i][1] + "</p>");
            } else if (i === cells - 1) {
                $(memory).append("<p class='cell danger rounded-bottom-2 cell-" + cell_array[i][1] + "' ondblclick='removeFromMemory(this)' onclick='findOnTable(this)'>" + cell_array[i][1] + "</p>");
            } else {
                $(memory).append("<p class='cell danger cell-" + cell_array[i][1] + "' ondblclick='removeFromMemory(this)' onclick='findOnTable(this)'>" + cell_array[i][1] + "</p>");
            }
            if (last_add_index - 1 === i && enough_space === true) {
                $(".cell-" + cell_array[i][1]).animate({ width: "50px" }, 0);
                $(".cell-" + cell_array[i][1]).animate({ width: "85%" }, 1291);
            }
        } else {
            if (i === 0) {
                $(memory).append("<p class='cell p-0 rounded-top-2 cell-" + cell_array[i][1] + " m-0'></p>");
            } else if (i === cells - 1) {
                $(memory).append("<p class='cell p-0 rounded-bottom-2 cell-" + cell_array[i][1] + " m-0'></p>");
            } else {
                $(memory).append("<p class='cell p-0 cell-" + cell_array[i][1] + " m-0'></p>");
            }
        }
    }
}
function drawMemoryV2() {
    let memory = $("#memory")
    $(memory).empty()
    let classify = [""];
    let classSize = [];
    let cell_count = 0;
    let c = 0;
    let currentP = null;
    let first = true;
    for (let i = 0; i < cells; i++) {
        if (cell_array[i][0] === true) {
            if (currentP === null) {
                currentP = cell_array[i][1];
                classify[c] = " ";
            }
            if (currentP !== cell_array[i][1]) {
                currentP = cell_array[i][1];
                classSize[c] = cell_count;
                cell_count = 0;
                c++;
                classify[c] = " ";
                first = true;
            }
            if (first === true) {
                classify[c] += " <p class='cell-v2 first-cell danger rounded-1 cell-" + cell_array[i][1] + "' ondblclick='removeFromMemory(this)' onclick='findOnTable(this)'>" + cell_array[i][1] + "</p><span></span>";
                first = false;
                cell_count++;
            } else {
                classify[c] += " <p class='cell-v2 danger rounded-1 cell-" + cell_array[i][1] + "' ondblclick='removeFromMemory(this)' onclick='findOnTable(this)'>" + cell_array[i][1] + "</p><span></span>";
                cell_count++;
            }
            if (i === cells - 1) {
                classSize[c] = cell_count;
                cell_count = 0;
            }
        } else {
            classSize[c] = cell_count;
            cell_count = 0;
            if (currentP !== null) {
                c++;
            }
            classify[c] = " ";
            while (true) {
                if (cell_array[i][0] === false) {
                    classify[c] += " <p class='cell-v2 rounded-1 p-0 cell-" + cell_array[i][1] + " m-0'></p><span></span>"
                    cell_count++;
                } else {
                    i--;
                    classSize[c] = cell_count;
                    cell_count = 0;
                    first = true
                    currentP = null;
                    c++;
                    classify[c] = " ";
                    break;
                }
                if (i === cells - 1) {
                    classSize[c] = cell_count;
                    cell_count = 0;
                    break;
                }
                i++;
            }
        }
    }
    // append
    let current_index = 0
    for (let i = 0; i < classify.length; i++) {
        $(memory).append("<span class='p-0 m-0 text-start size-label float-end'>" + classSize[i] * unit_size + "k</span>") //It Works
        let in_array = classify[i].split('<span></span>')
        for (let j = 0; j < in_array.length - 1; j++) {
            $(memory).append(in_array[j])
            if (last_add_index - 1 === current_index && enough_space === true) {
                $(".cell-" + cell_array[current_index][1]).animate({ width: "50px" }, 0);
                $(".cell-" + cell_array[current_index][1]).animate({ width: "85%" }, 1291);
            }
            current_index++;
        }
        $(memory).append("<hr class='hr'>")
    }
}

function drawMemory() {
    let vis = $("#visual").val()
    if (vis === "Stable") {
        drawMemoryV1()
    } else {
        drawMemoryV2()
    }
}

function findOnTable(para) {
    let Value = $(para).html()
    Value = parseInt(Value)
    let th = document.getElementsByClassName("program-number")[Value]
    th.scrollIntoView({
        behavior: 'smooth',
    })
    th = document.getElementsByClassName("program-number")[Value + 1]
    if (fade) {
        // for (let i = 0; i < 2; i++) {
        $(th).fadeOut();
        $(th).fadeIn(322);
        // }
    } else {
        fade = true;
    }
}
// end visual section

// manage method
function manageMethods() {
    let size = $("#size").val()
    if (size !== "" && size !== 0) {
        let method = $("#method").val();
        if (method === 'First') {
            addToMemory();
        } else if (method === 'Next') {
            addMemoryNext();
        } else if (method === 'Best') {
            addToMemoryBest();
        } else { // Worst
            addToMemoryWorst();
        }
    } else {
        Swal.fire({
            title: "Value is empty",
            icon: "error",
        });
    }
}

// funcs on memory
// first fit
function addToMemory() {
    enough_space = false;
    let size = $("#size").val();
    let cell = (size / 4);
    if (cell % 1 !== 0) {
        cell = ~~cell + 1;
    }

    for (let i = 0; i < cells; i++) {
        if (cell_array[i][0] === false) {
            enough_space = true;
            for (let j = i; j < i + cell; j++) {
                if (j >= cells) {
                    enough_space = false;
                }
                else if (cell_array[j][0] === true) {
                    enough_space = false;
                }
                else if (i + cell > cells) {
                    enough_space = false;
                }
            }
            if (enough_space === true) {
                for (let j = i; j < i + cell; j++) {
                    cell_array[j][0] = true;
                    cell_array[j][1] = p_counter;
                    cell_array[j][2] = calWaste(size);
                }
                addToTable(p_counter, size, i, i + cell);
                i = i + cell;
                last_add_index = i;
                p_counter++;
                break;
            }
        }
    }

    if (enough_space === false) {
        Swal.fire({
            title: "Not Enough Memory :(",
            icon: "error",
        });
    }
    drawMemory();
}

// best fit
function addToMemoryBest() {
    enough_space = false;
    let empty_counter = 0;
    let empty_len_array = [];
    let index = 0;

    let size = $("#size").val();
    let cell = (size / 4);
    if (cell % 1 !== 0) {
        cell = ~~cell + 1;
    }

    // find all empty cells
    for (let i = 0; i < cells; i++) {
        if (cell_array[i][0] === false) {
            empty_counter++;
            if (i === cells - 1 && empty_counter != 0) {
                empty_len_array[index] = empty_counter;
                index += 1;
                empty_counter = 0;
            }
        } else if (empty_counter !== 0) {
            empty_len_array[index] = empty_counter;
            index += 1;
            empty_counter = 0;
        }
    }

    // check which part is the Best 
    let best_part_index = -1;
    let best_part_len = 10000;
    if (empty_len_array.length > 0) {
        for (let i = 0; i < empty_len_array.length; i++) {
            if (empty_len_array[i] === cell) {
                best_part_index = i;
                break;
            } else if (empty_len_array[i] > cell) {
                if (empty_len_array[i] < best_part_len) {
                    best_part_index = i;
                    best_part_len = empty_len_array[i];
                }
            }
        }
    } else {
        Swal.fire({
            title: "Not Enough Memory :(",
            icon: "error",
        });
    }

    // add to memory
    if (best_part_index !== -1) {
        let counter = 0
        for (let i = 0; i < cells; i++) {
            if (cell_array[i][0] === false) {
                if (counter === best_part_index) {
                    enough_space = true;
                } else {
                    while (true) {
                        if (cell_array[i][0] === true || i === cells - 1) {
                            break
                        }
                        i++;
                    }
                    counter++;
                }
                if (enough_space === true) {
                    for (let j = i; j < i + cell; j++) {
                        cell_array[j][0] = true;
                        cell_array[j][1] = p_counter;
                        cell_array[j][2] = calWaste(size);
                    }
                    addToTable(p_counter, size, i, i + cell);
                    i = i + cell;
                    last_add_index = i
                    p_counter++;
                    break;
                }
            }
        }

        if (enough_space === false) {
            Swal.fire({
                title: "Not Enough Memory :(",
                icon: "error",
            });
        }
    } else {
        Swal.fire({
            title: "Not Enough Memory :(",
            icon: "error",
        });
    }

    drawMemory();
}

//next fit !
function addMemoryNext() {
    enough_space = false;
    let size = $("#size").val();
    let cell = (size / 4);
    if (cell % 1 !== 0) {
        cell = ~~cell + 1;
    }

    //add after last
    for (let i = last_add_index; i < cells; i++) {
        if (cell_array[i][0] === false) {
            enough_space = true;
            for (let j = i; j < i + cell; j++) {
                if (j >= cells) {
                    enough_space = false;
                }
                else if (cell_array[j][0] === true) {
                    enough_space = false;
                }
                else if (i + cell > cells) {
                    enough_space = false;
                }
            }
            if (enough_space === true) {
                for (let j = i; j < i + cell; j++) {
                    cell_array[j][0] = true;
                    cell_array[j][1] = p_counter;
                    cell_array[j][2] = calWaste(size);
                }
                addToTable(p_counter, size, i, i + cell);
                i = i + cell;
                last_add_index = i
                p_counter++;
                break;
            }
        }
    }
    if (enough_space === false) {
        for (let i = 0; i < cells; i++) {
            if (cell_array[i][0] === false) {
                enough_space = true;
                for (let j = i; j < i + cell; j++) {
                    if (j >= cells) {
                        enough_space = false;
                    }
                    else if (cell_array[j][0] === true) {
                        enough_space = false;
                    }
                    else if (i + cell > cells) {
                        enough_space = false;
                    }
                }
                if (enough_space === true) {
                    for (let j = i; j < i + cell; j++) {
                        cell_array[j][0] = true;
                        cell_array[j][1] = p_counter;
                        cell_array[j][2] = calWaste(size);
                    }
                    addToTable(p_counter, size, i, i + cell);
                    i = i + cell;
                    last_add_index = i
                    p_counter++;
                    break;
                }
            }
        }
    }
    if (enough_space === false) {
        Swal.fire({
            title: "Not Enough Memory :(",
            icon: "error",
        });
    }

    drawMemory();
}

//worst fit !
function addToMemoryWorst() {
    enough_space = false;
    let empty_counter = 0;
    let empty_len_array = [];
    let index = 0;

    let size = $("#size").val();
    let cell = (size / 4);
    if (cell % 1 !== 0) {
        cell = ~~cell + 1;
    }

    // find all empty cells
    for (let i = 0; i < cells; i++) {
        if (cell_array[i][0] === false) {
            empty_counter++;
            if (i === cells - 1 && empty_counter != 0) {
                empty_len_array[index] = empty_counter;
                index += 1;
                empty_counter = 0;
            }
        } else if (empty_counter !== 0) {
            empty_len_array[index] = empty_counter;
            index += 1;
            empty_counter = 0;
        }
    }
    // find worst that fit cell
    let biggest_part_index = -1
    let biggest_part_len = 0
    if (empty_len_array.length > 0) {
        for (let i = 0; i < empty_len_array.length; i++) {
            if (empty_len_array[i] > biggest_part_len && empty_len_array[i] >= cell) {
                biggest_part_index = i;
                biggest_part_len = empty_len_array[i]
            }
        }
    } else {
        Swal.fire({
            title: "Not Enough Memory :(",
            icon: "error",
        });
    }
    // add to memory
    if (biggest_part_index !== -1) {
        let counter = 0
        for (let i = 0; i < cells; i++) {
            if (cell_array[i][0] === false) {
                if (counter === biggest_part_index) {
                    enough_space = true;
                } else {
                    while (true) {
                        if (cell_array[i][0] === true || i === cells - 1) {
                            break
                        }
                        i++;
                    }
                    counter++;
                }
                if (enough_space === true) {
                    for (let j = i; j < i + cell; j++) {
                        cell_array[j][0] = true;
                        cell_array[j][1] = p_counter;
                        cell_array[j][2] = calWaste(size);
                    }
                    addToTable(p_counter, size, i, i + cell);
                    i = i + cell;
                    last_add_index = i;
                    p_counter++;
                    break;
                }
            }
        }

        if (enough_space === false) {
            Swal.fire({
                title: "Not Enough Memory :(",
                icon: "error",
            });
        }
    } else {
        Swal.fire({
            title: "Not Enough Memory :(",
            icon: "error",
        });
    }

    drawMemory();
}

function removeFromMemory(para) {
    let Value = $(para).html(); //inner html p tag
    Value = parseInt(Value);
    for (let i = 0; i < cells; i++) {
        if (cell_array[i][1] === Value) {
            cell_array[i][0] = false;
            cell_array[i][1] = null;
            cell_array[i][2] = 0;
        }
    }
    let th = $(".program-number")[Value + 1];
    $(th).addClass('bg-danger-subtle').removeClass('bg-success');
    enough_space = false;
    fade = false;
    memorySize();
    drawMemory();
}

function addToTable(pNumber, pSize, startC, endC) {
    if (pSize > 0) {
        let waste = calWaste(pSize);
        $("#detail-table").append("<tr> <th class='program-number bg-success' ondblclick='removeFromMemory(this)'>" + pNumber + "</th> <th>" + pSize + "</th> <th>" + waste + "</th> <th>" + startC + "-" + endC + "</th> </tr>")
    }
    memorySize()
}

// calculate waste
function calWaste(pSize) {
    let waste = 0;
    if (pSize > 0) {
        let leftOver = pSize % unit_size
        if (leftOver !== 0) {
            waste = unit_size - leftOver
        }
    }
    return waste
}

function memorySize() {
    let full = 0;
    let empty = 0;
    let currentP;
    let waste = 0
    for (let i = 0; i < cells; i++) {
        if (cell_array[i][0] === true) {
            full += 4;
        } else {
            empty += 4;
        }
        if (currentP !== cell_array[i][1]) {
            waste += cell_array[i][2];
            currentP = cell_array[i][1];
        }
    }
    document.getElementById("status").innerHTML = empty + "k empty / " + full + "k full / " + waste + "k waste"
}


// need empty cells table and full cells table
function emptyMemory() {

}