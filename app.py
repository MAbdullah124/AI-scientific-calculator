import streamlit as st
import streamlit.components.v1 as components


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)


# ============================================================
# CALCULATOR
# ============================================================

calculator_html = r"""
<!DOCTYPE html>

<html>

<head>

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<style>

/* ============================================================
   PAGE
   ============================================================ */

* {
    box-sizing: border-box;
}

html,
body {

    margin: 0;
    padding: 0;

    width: 100%;

    overflow-x: hidden;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: white;
}


/* ============================================================
   CALCULATOR
   ============================================================ */

.calculator {

    width: 100%;

    max-width: 760px;

    margin: 0 auto;

    padding: 6px;

    overflow: hidden;
}


/* ============================================================
   DISPLAY
   ============================================================ */

.display {

    width: 100%;

    border: 1px solid #d1d5db;

    border-radius: 16px;

    padding: 8px 12px;

    margin-bottom: 7px;

    background: white;

    overflow: hidden;
}


.expression {

    width: 100%;

    height: 24px;

    line-height: 24px;

    text-align: right;

    color: #6b7280;

    font-size: 15px;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


.result {

    width: 100%;

    height: 40px;

    line-height: 40px;

    text-align: right;

    color: #111827;

    font-size: 30px;

    font-weight: 500;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;
}


/* ============================================================
   MODE / MEMORY ROW
   6 COLUMNS
   ============================================================ */

.mode-grid {

    display: grid;

    grid-template-columns:
        repeat(6, minmax(0, 1fr));

    gap: 4px;

    width: 100%;

    margin-bottom: 5px;
}


/* ============================================================
   MAIN KEYPAD
   7 COLUMNS
   ============================================================ */

.keypad {

    display: grid;

    grid-template-columns:
        repeat(7, minmax(0, 1fr));

    gap: 4px;

    width: 100%;
}


/* ============================================================
   BUTTON
   ============================================================ */

button {

    width: 100%;

    min-width: 0;

    height: 43px;

    border: none;

    border-radius: 22px;

    background: #f1f3f4;

    color: #111827;

    font-size: 12px;

    font-weight: 500;

    padding: 0;

    margin: 0;

    cursor: pointer;

    white-space: nowrap;

    overflow: hidden;

    text-overflow: ellipsis;

    -webkit-tap-highlight-color:
        transparent;
}


button:hover {

    background: #e5e7eb;
}


button:active {

    transform: scale(0.96);

    background: #dfe3e7;
}


/* ============================================================
   MODE BUTTONS
   ============================================================ */

.mode-grid button {

    height: 36px;

    border-radius: 18px;

    font-size: 10px;
}


/* ============================================================
   MORE FUNCTIONS
   ============================================================ */

.more-title {

    margin-top: 8px;

    margin-bottom: 5px;

    font-size: 12px;

    color: #4b5563;

    text-align: center;
}


.more-grid {

    display: grid;

    grid-template-columns:
        repeat(4, minmax(0, 1fr));

    gap: 4px;

    width: 100%;
}


.more-grid button {

    height: 36px;

    border-radius: 18px;

    font-size: 10px;
}


/* ============================================================
   HISTORY
   ============================================================ */

.history-title {

    margin-top: 8px;

    padding-top: 7px;

    border-top: 1px solid #e5e7eb;

    font-size: 12px;

    color: #4b5563;

    text-align: center;

    cursor: pointer;
}


.history {

    display: none;

    margin-top: 5px;

    border: 1px solid #e5e7eb;

    border-radius: 10px;

    padding: 7px;

    max-height: 150px;

    overflow-y: auto;

    font-size: 11px;

    color: #374151;
}


.history-item {

    padding: 5px 2px;

    border-bottom: 1px solid #f0f0f0;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 640px) {

    .calculator {

        width: 100%;

        padding: 3px;
    }


    .display {

        border-radius: 13px;

        padding: 5px 8px;

        margin-bottom: 5px;
    }


    .expression {

        height: 20px;

        line-height: 20px;

        font-size: 12px;
    }


    .result {

        height: 34px;

        line-height: 34px;

        font-size: 25px;
    }


    /*
       IMPORTANT:
       These are CSS GRID layouts.

       They NEVER stack into one column.
    */

    .mode-grid {

        grid-template-columns:
            repeat(6, minmax(0, 1fr));

        gap: 3px;

        margin-bottom: 4px;
    }


    .keypad {

        grid-template-columns:
            repeat(7, minmax(0, 1fr));

        gap: 3px;
    }


    .mode-grid button {

        height: 32px;

        border-radius: 16px;

        font-size: 8px;
    }


    .keypad button {

        height: 36px;

        border-radius: 18px;

        font-size: 9px;
    }


    .more-grid {

        grid-template-columns:
            repeat(4, minmax(0, 1fr));

        gap: 3px;
    }


    .more-grid button {

        height: 32px;

        border-radius: 16px;

        font-size: 9px;
    }

}


/* ============================================================
   VERY SMALL PHONE
   ============================================================ */

@media (max-width: 380px) {

    .calculator {

        padding: 2px;
    }


    .mode-grid {

        gap: 2px;
    }


    .keypad {

        gap: 2px;
    }


    .mode-grid button {

        height: 29px;

        font-size: 7px;
    }


    .keypad button {

        height: 33px;

        font-size: 8px;
    }


    .more-grid {

        gap: 2px;
    }


    .more-grid button {

        height: 29px;

        font-size: 8px;
    }

}

</style>

</head>


<body>


<div class="calculator">


    <!-- =====================================================
         DISPLAY
         ===================================================== -->

    <div class="display">

        <div
            class="expression"
            id="expression">
        </div>

        <div
            class="result"
            id="result">
            0
        </div>

    </div>


    <!-- =====================================================
         DEG / INV / MEMORY
         EXACTLY 6 COLUMNS
         ===================================================== -->

    <div class="mode-grid">

        <button onclick="toggleAngle()"
                id="angleButton">
            DEG
        </button>

        <button onclick="toggleInverse()"
                id="inverseButton">
            INV
        </button>

        <button onclick="memoryClear()">
            MC
        </button>

        <button onclick="memoryRecall()">
            MR
        </button>

        <button onclick="memoryAdd()">
            M+
        </button>

        <button onclick="memorySubtract()">
            M-
        </button>

    </div>


    <!-- =====================================================
         MAIN KEYPAD
         EXACTLY 7 COLUMNS
         ===================================================== -->

    <div class="keypad">


        <!-- ROW 1 -->

        <button onclick="factorial()">
            x!
        </button>

        <button onclick="add('(')">
            (
        </button>

        <button onclick="add(')')">
            )
        </button>

        <button onclick="add('%')">
            %
        </button>

        <button onclick="clearAll()">
            AC
        </button>

        <button onclick="backspace()">
            ⌫
        </button>

        <button onclick="add('/')">
            ÷
        </button>


        <!-- ROW 2 -->

        <button onclick="scientific('sin')">
            sin
        </button>

        <button onclick="scientific('ln')">
            ln
        </button>

        <button onclick="add('7')">
            7
        </button>

        <button onclick="add('8')">
            8
        </button>

        <button onclick="add('9')">
            9
        </button>

        <button onclick="add('*')">
            ×
        </button>

        <button onclick="scientific('sqrt')">
            √
        </button>


        <!-- ROW 3 -->

        <button onclick="scientific('cos')">
            cos
        </button>

        <button onclick="scientific('log')">
            log
        </button>

        <button onclick="add('4')">
            4
        </button>

        <button onclick="add('5')">
            5
        </button>

        <button onclick="add('6')">
            6
        </button>

        <button onclick="add('-')">
            −
        </button>

        <button onclick="add('pi')">
            π
        </button>


        <!-- ROW 4 -->

        <button onclick="scientific('tan')">
            tan
        </button>

        <button onclick="add('e')">
            e
        </button>

        <button onclick="add('1')">
            1
        </button>

        <button onclick="add('2')">
            2
        </button>

        <button onclick="add('3')">
            3
        </button>

        <button onclick="add('+')">
            +
        </button>

        <button onclick="add('Ans')">
            Ans
        </button>


        <!-- ROW 5 -->

        <button onclick="add('E')">
            EXP
        </button>

        <button onclick="add('^')">
            xʸ
        </button>

        <button onclick="add('0')">
            0
        </button>

        <button onclick="add('.')">
            .
        </button>

        <button onclick="calculate()">
            =
        </button>

        <button onclick="add('(')">
            (
        </button>

        <button onclick="add(')')">
            )
        </button>

    </div>


    <!-- =====================================================
         MORE FUNCTIONS
         ===================================================== -->

    <div
        class="more-title"
        onclick="toggleMore()">

        ⚙️ More Scientific Functions

    </div>


    <div
        class="more-grid"
        id="moreFunctions"
        style="display:none;">


        <button onclick="scientific('asin')">
            asin
        </button>

        <button onclick="scientific('acos')">
            acos
        </button>

        <button onclick="scientific('atan')">
            atan
        </button>

        <button onclick="scientific('sinh')">
            sinh
        </button>


        <button onclick="scientific('cosh')">
            cosh
        </button>

        <button onclick="scientific('tanh')">
            tanh
        </button>

        <button onclick="scientific('log2')">
            log₂
        </button>

        <button onclick="scientific('reciprocal')">
            1/x
        </button>


        <button onclick="scientific('square')">
            x²
        </button>

        <button onclick="scientific('cube')">
            x³
        </button>

        <button onclick="scientific('cuberoot')">
            ∛x
        </button>

        <button onclick="scientific('abs')">
            |x|
        </button>


        <button onclick="scientific('floor')">
            floor
        </button>

        <button onclick="scientific('ceil')">
            ceil
        </button>

    </div>


    <!-- =====================================================
         HISTORY
         ===================================================== -->

    <div
        class="history-title"
        onclick="toggleHistory()">

        🕘 History

    </div>


    <div
        class="history"
        id="history">
    </div>


</div>


<script>

/* ============================================================
   VARIABLES
   ============================================================ */

let expression = "";

let answer = 0;

let memory = 0;

let angleMode = "DEG";

let inverse = false;

let history = [];


/* ============================================================
   DISPLAY
   ============================================================ */

function updateDisplay() {

    document.getElementById(
        "expression"
    ).textContent = expression;

    document.getElementById(
        "result"
    ).textContent = answer;
}


/* ============================================================
   ADD
   ============================================================ */

function add(value) {

    expression += value;

    updateDisplay();
}


/* ============================================================
   CLEAR
   ============================================================ */

function clearAll() {

    expression = "";

    answer = 0;

    updateDisplay();
}


/* ============================================================
   BACKSPACE
   ============================================================ */

function backspace() {

    expression =
        expression.slice(
            0,
            -1
        );

    updateDisplay();
}


/* ============================================================
   ANGLE MODE
   ============================================================ */

function toggleAngle() {

    if (angleMode === "DEG") {

        angleMode = "RAD";

    } else {

        angleMode = "DEG";
    }


    document.getElementById(
        "angleButton"
    ).textContent = angleMode;
}


/* ============================================================
   INVERSE
   ============================================================ */

function toggleInverse() {

    inverse = !inverse;


    document.getElementById(
        "inverseButton"
    ).textContent =
        inverse
        ? "INV ✓"
        : "INV";
}


/* ============================================================
   FACTORIAL
   ============================================================ */

function factorial() {

    expression += "!";

    updateDisplay();
}


/* ============================================================
   FACTORIAL CALCULATION
   ============================================================ */

function factorialValue(n) {

    if (n < 0 ||
        !Number.isInteger(n)) {

        throw new Error(
            "Factorial requires a whole number"
        );
    }


    if (n > 170) {

        throw new Error(
            "Number too large"
        );
    }


    let result = 1;


    for (
        let i = 2;
        i <= n;
        i++
    ) {

        result *= i;
    }


    return result;
}


/* ============================================================
   TRIG FUNCTIONS
   ============================================================ */

function sin(x) {

    if (angleMode === "DEG") {

        return Math.sin(
            x * Math.PI / 180
        );
    }

    return Math.sin(x);
}


function cos(x) {

    if (angleMode === "DEG") {

        return Math.cos(
            x * Math.PI / 180
        );
    }

    return Math.cos(x);
}


function tan(x) {

    if (angleMode === "DEG") {

        return Math.tan(
            x * Math.PI / 180
        );
    }

    return Math.tan(x);
}


/* ============================================================
   INVERSE TRIG
   ============================================================ */

function asin(x) {

    let value = Math.asin(x);

    if (angleMode === "DEG") {

        value =
            value * 180 / Math.PI;
    }

    return value;
}


function acos(x) {

    let value = Math.acos(x);

    if (angleMode === "DEG") {

        value =
            value * 180 / Math.PI;
    }

    return value;
}


function atan(x) {

    let value = Math.atan(x);

    if (angleMode === "DEG") {

        value =
            value * 180 / Math.PI;
    }

    return value;
}


/* ============================================================
   SCIENTIFIC FUNCTION
   ============================================================ */

function scientific(type) {

    try {


        /* ----------------------------------------------------
           FUNCTIONS THAT ADD TO EXPRESSION
           ---------------------------------------------------- */

        if (
            type === "sin" ||
            type === "cos" ||
            type === "tan" ||
            type === "asin" ||
            type === "acos" ||
            type === "atan" ||
            type === "sinh" ||
            type === "cosh" ||
            type === "tanh"
        ) {

            let functionName = type;


            if (
                inverse &&
                type === "sin"
            ) {

                functionName = "asin";

            } else if (
                inverse &&
                type === "cos"
            ) {

                functionName = "acos";

            } else if (
                inverse &&
                type === "tan"
            ) {

                functionName = "atan";
            }


            expression +=
                functionName + "(";

            updateDisplay();

            return;
        }


        if (type === "ln") {

            expression += "ln(";

            updateDisplay();

            return;
        }


        if (type === "log") {

            expression += "log(";

            updateDisplay();

            return;
        }


        if (type === "log2") {

            expression += "log2(";

            updateDisplay();

            return;
        }


        if (type === "sqrt") {

            expression += "sqrt(";

            updateDisplay();

            return;
        }


        if (type === "cuberoot") {

            expression += "cbrt(";

            updateDisplay();

            return;
        }


        /* ----------------------------------------------------
           SQUARE
           ---------------------------------------------------- */

        if (type === "square") {

            expression =
                "(" +
                expression +
                ")^2";

            updateDisplay();

            return;
        }


        /* ----------------------------------------------------
           CUBE
           ---------------------------------------------------- */

        if (type === "cube") {

            expression =
                "(" +
                expression +
                ")^3";

            updateDisplay();

            return;
        }


        /* ----------------------------------------------------
           RECIPROCAL
           ---------------------------------------------------- */

        if (type === "reciprocal") {

            expression =
                "1/(" +
                expression +
                ")";

            updateDisplay();

            return;
        }


        /* ----------------------------------------------------
           ABS
           ---------------------------------------------------- */

        if (type === "abs") {

            expression =
                "abs(" +
                expression +
                ")";

            updateDisplay();

            return;
        }


        /* ----------------------------------------------------
           FLOOR
           ---------------------------------------------------- */

        if (type === "floor") {

            expression =
                "floor(" +
                expression +
                ")";

            updateDisplay();

            return;
        }


        /* ----------------------------------------------------
           CEIL
           ---------------------------------------------------- */

        if (type === "ceil") {

            expression =
                "ceil(" +
                expression +
                ")";

            updateDisplay();

            return;
        }

    }

    catch (error) {

        answer = "Error";

        updateDisplay();
    }
}


/* ============================================================
   EXPRESSION PREPARATION
   ============================================================ */

function prepareExpression(expr) {

    let result = expr;


    /* Ans */

    result =
        result.replace(
            /Ans/g,
            "(" + answer + ")"
        );


    /* Pi */

    result =
        result.replace(
            /pi/g,
            "Math.PI"
        );


    /* e */

    result =
        result.replace(
            /(?<![a-zA-Z])e(?![a-zA-Z])/g,
            "Math.E"
        );


    /* Percentage */

    result =
        result.replace(
            /(\d+(?:\.\d+)?)%/g,
            "($1/100)"
        );


    /* Factorial */

    result =
        result.replace(
            /(\d+(?:\.\d+)?)!/g,
            "factorialValue($1)"
        );


    /* Square root */

    result =
        result.replace(
            /sqrt\(/g,
            "Math.sqrt("
        );


    /* Cube root */

    result =
        result.replace(
            /cbrt\(/g,
            "Math.cbrt("
        );


    /* Natural log */

    result =
        result.replace(
            /ln\(/g,
            "Math.log("
        );


    /* Log base 10 */

    result =
        result.replace(
            /log\(/g,
            "Math.log10("
        );


    /* Log base 2 */

    result =
        result.replace(
            /log2\(/g,
            "Math.log2("
        );


    /* Absolute */

    result =
        result.replace(
            /abs\(/g,
            "Math.abs("
        );


    /* Floor */

    result =
        result.replace(
            /floor\(/g,
            "Math.floor("
        );


    /* Ceil */

    result =
        result.replace(
            /ceil\(/g,
            "Math.ceil("
        );


    /* Trigonometry */

    result =
        result.replace(
            /asin\(/g,
            "asin("
        );


    result =
        result.replace(
            /acos\(/g,
            "acos("
        );


    result =
        result.replace(
            /atan\(/g,
            "atan("
        );


    result =
        result.replace(
            /sin\(/g,
            "sin("
        );


    result =
        result.replace(
            /cos\(/g,
            "cos("
        );


    result =
        result.replace(
            /tan\(/g,
            "tan("
        );


    /* Hyperbolic */

    result =
        result.replace(
            /sinh\(/g,
            "Math.sinh("
        );


    result =
        result.replace(
            /cosh\(/g,
            "Math.cosh("
        );


    result =
        result.replace(
            /tanh\(/g,
            "Math.tanh("
        );


    /* Power */

    result =
        result.replace(
            /\^/g,
            "**"
        );


    return result;
}


/* ============================================================
   CALCULATE
   ============================================================ */

function calculate() {

    if (!expression) {

        return;
    }


    try {

        let original =
            expression;


        let prepared =
            prepareExpression(
                expression
            );


        let value =
            Function(
                "factorialValue",
                "sin",
                "cos",
                "tan",
                "asin",
                "acos",
                "atan",
                "return (" +
                prepared +
                ")"
            )(
                factorialValue,
                sin,
                cos,
                tan,
                asin,
                acos,
                atan
            );


        if (
            typeof value !== "number" ||
            !Number.isFinite(value)
        ) {

            throw new Error(
                "Invalid result"
            );
        }


        /* Clean tiny floating point errors */

        if (
            Math.abs(value) <
            1e-12
        ) {

            value = 0;
        }


        /* Round */

        value =
            Number(
                value.toPrecision(12)
            );


        answer =
            value;


        history.unshift({

            expression:
                original,

            result:
                value

        });


        if (history.length > 20) {

            history.pop();
        }


        updateHistory();

        updateDisplay();

    }

    catch (error) {

        answer = "Error";

        updateDisplay();
    }
}


/* ============================================================
   MEMORY
   ============================================================ */

function memoryClear() {

    memory = 0;
}


function memoryRecall() {

    expression +=
        String(memory);

    updateDisplay();
}


function memoryAdd() {

    try {

        calculate();

        if (
            typeof answer === "number"
        ) {

            memory += answer;
        }

    }

    catch (error) {

        // Ignore invalid memory operation
    }
}


function memorySubtract() {

    try {

        calculate();

        if (
            typeof answer === "number"
        ) {

            memory -= answer;
        }

    }

    catch (error) {

        // Ignore invalid memory operation
    }
}


/* ============================================================
   HISTORY
   ============================================================ */

function toggleHistory() {

    let historyBox =
        document.getElementById(
            "history"
        );


    if (
        historyBox.style.display ===
        "block"
    ) {

        historyBox.style.display =
            "none";

    } else {

        historyBox.style.display =
            "block";

        updateHistory();
    }
}


function updateHistory() {

    let historyBox =
        document.getElementById(
            "history"
        );


    if (history.length === 0) {

        historyBox.innerHTML =
            "No calculations yet.";

        return;
    }


    historyBox.innerHTML = "";


    history.forEach(
        function(item) {

            let div =
                document.createElement(
                    "div"
                );


            div.className =
                "history-item";


            div.textContent =
                item.expression +
                " = " +
                item.result;


            historyBox.appendChild(
                div
            );
        }
    );
}


/* ============================================================
   MORE FUNCTIONS
   ============================================================ */

function toggleMore() {

    let box =
        document.getElementById(
            "moreFunctions"
        );


    if (
        box.style.display ===
        "none"
    ) {

        box.style.display =
            "grid";

    } else {

        box.style.display =
            "none";
    }
}


/* ============================================================
   KEYBOARD SUPPORT
   ============================================================ */

document.addEventListener(
    "keydown",
    function(event) {

        let key =
            event.key;


        if (
            /^[0-9.]$/.test(key)
        ) {

            add(key);

            return;
        }


        if (
            ["+", "-", "*", "/", "(", ")", "^"]
            .includes(key)
        ) {

            add(key);

            return;
        }


        if (key === "Enter") {

            calculate();

            return;
        }


        if (key === "Backspace") {

            backspace();

            return;
        }


        if (key === "Escape") {

            clearAll();

            return;
        }

    }
);


/* ============================================================
   INITIAL DISPLAY
   ============================================================ */

updateDisplay();

</script>

</body>

</html>
"""


# ============================================================
# RENDER
# ============================================================

components.html(
    calculator_html,
    height=650,
    scrolling=False
)