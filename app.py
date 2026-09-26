import streamlit as st
import sympy as sp
import math
import re


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   HIDE STREAMLIT DEFAULT UI
   ========================================================== */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* ==========================================================
   APP
   ========================================================== */

.stApp {
    background: #ffffff;
}

.block-container {
    max-width: 760px !important;
    padding-top: 10px !important;
    padding-bottom: 20px !important;
    padding-left: 8px !important;
    padding-right: 8px !important;
}


/* ==========================================================
   CALCULATOR
   ========================================================== */

.calculator {
    width: 100%;
    max-width: 760px;
    margin: auto;
}


/* ==========================================================
   DISPLAY
   ========================================================== */

.display-box {
    width: 100%;
    box-sizing: border-box;

    border: 1px solid #d1d5db;
    border-radius: 18px;

    padding: 8px 14px;
    margin-bottom: 7px;

    background: white;

    overflow: hidden;
}

.display-expression {
    width: 100%;

    text-align: right;

    font-size: 18px;
    min-height: 26px;
    line-height: 26px;

    color: #4b5563;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}

.display-result {
    width: 100%;

    text-align: right;

    font-size: 32px;
    min-height: 42px;
    line-height: 42px;

    color: #111827;

    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
}


/* ==========================================================
   NORMAL STREAMLIT COLUMNS
   ========================================================== */

/*
   IMPORTANT:
   We DO NOT change stHorizontalBlock to grid.
   Streamlit columns are used normally.
*/

[data-testid="column"] {
    padding: 0 !important;
    min-width: 0 !important;
}


/* ==========================================================
   BUTTONS
   ========================================================== */

.stButton {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
}

.stButton > button {
    width: 100% !important;
    min-width: 0 !important;

    height: 44px !important;
    min-height: 44px !important;

    padding: 0 !important;
    margin: 0 !important;

    border-radius: 22px;
    border: none;

    background-color: #f1f3f4;
    color: #111827;

    font-size: 13px;
    font-weight: 500;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;

    box-sizing: border-box !important;
}

.stButton > button:hover {
    background-color: #e5e7eb;
    border: none;
}


/* ==========================================================
   BUTTON ROW SPACING
   ========================================================== */

.keypad-row {
    margin-bottom: 5px;
}


/* ==========================================================
   MODE / MEMORY BUTTONS
   ========================================================== */

.mode-row {
    margin-top: 2px;
    margin-bottom: 6px;
}

.mode-row .stButton > button {
    height: 37px !important;
    min-height: 37px !important;

    border-radius: 19px;

    font-size: 11px;
}


/* ==========================================================
   MORE FUNCTIONS
   ========================================================== */

.more-box .stButton > button {
    height: 38px !important;
    min-height: 38px !important;

    border-radius: 19px;

    font-size: 11px;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {
    margin: 7px 0 !important;
}


/* ==========================================================
   MOBILE
   ========================================================== */

@media (max-width: 640px) {

    .block-container {
        width: 100% !important;

        padding-left: 4px !important;
        padding-right: 4px !important;
    }

    .calculator {
        width: 100% !important;
    }


    /* Display */

    .display-box {
        border-radius: 16px;
        padding: 6px 9px;
        margin-bottom: 5px;
    }

    .display-expression {
        font-size: 14px;
        min-height: 22px;
        line-height: 22px;
    }

    .display-result {
        font-size: 27px;
        min-height: 35px;
        line-height: 35px;
    }


    /* Mode buttons */

    .mode-row .stButton > button {
        height: 33px !important;
        min-height: 33px !important;

        border-radius: 17px;

        font-size: 9px !important;
    }


    /* Calculator buttons */

    .keypad-row {
        margin-bottom: 3px;
    }

    .keypad-row .stButton > button {
        height: 39px !important;
        min-height: 39px !important;

        border-radius: 20px;

        font-size: 11px !important;
    }


    /* More functions */

    .more-box .stButton > button {
        height: 34px !important;
        min-height: 34px !important;

        border-radius: 17px;

        font-size: 10px !important;
    }
}


/* ==========================================================
   VERY SMALL PHONES
   ========================================================== */

@media (max-width: 380px) {

    .block-container {
        padding-left: 2px !important;
        padding-right: 2px !important;
    }

    .display-result {
        font-size: 24px;
    }

    .mode-row .stButton > button {
        height: 30px !important;
        min-height: 30px !important;

        font-size: 8px !important;
    }

    .keypad-row {
        margin-bottom: 2px;
    }

    .keypad-row .stButton > button {
        height: 35px !important;
        min-height: 35px !important;

        border-radius: 18px;

        font-size: 9px !important;
    }

    .more-box .stButton > button {
        height: 31px !important;
        min-height: 31px !important;

        font-size: 9px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "expression": "",
    "result": "0",
    "angle_mode": "DEG",
    "inverse": False,
    "memory": 0,
    "ans": 0,
    "history": [],
    "show_history": False,
    "error": "",
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# MATHEMATICAL FUNCTIONS
# ============================================================

def factorial_value(value):

    if value < 0:
        raise ValueError("Invalid factorial")

    if not float(value).is_integer():
        raise ValueError(
            "Factorial requires a whole number"
        )

    if value > 170:
        raise ValueError(
            "Number is too large for factorial"
        )

    return math.factorial(int(value))


def safe_float(value):

    value = float(value)

    if not math.isfinite(value):
        raise ValueError(
            "Invalid mathematical result"
        )

    return value


# ============================================================
# EXPRESSION PREPARATION
# ============================================================

def prepare_expression(expression):

    expr = expression

    expr = expr.replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace("^", "**")

    expr = re.sub(
        r"\bπ\b",
        "pi",
        expr
    )

    expr = re.sub(
        r"\be\b",
        "E",
        expr
    )

    expr = re.sub(
        r"\bAns\b",
        f"({st.session_state.ans})",
        expr
    )

    expr = re.sub(
        r"(\d+(?:\.\d+)?)%",
        r"(\1/100)",
        expr
    )

    return expr


# ============================================================
# CALCULATE EXPRESSION
# ============================================================

def calculate_expression(expression):

    if not expression.strip():
        return "0"

    try:

        expr = prepare_expression(expression)


        # FACTORIAL

        factorial_pattern = r"(\d+(?:\.\d+)?)!"

        def factorial_replace(match):

            number = float(match.group(1))

            return str(
                factorial_value(number)
            )

        expr = re.sub(
            factorial_pattern,
            factorial_replace,
            expr
        )


        # ALLOWED FUNCTIONS

        allowed = {

            "pi": sp.pi,
            "E": sp.E,

            "sqrt": sp.sqrt,

            "sin": sp.sin,
            "cos": sp.cos,
            "tan": sp.tan,

            "asin": sp.asin,
            "acos": sp.acos,
            "atan": sp.atan,

            "sinh": sp.sinh,
            "cosh": sp.cosh,
            "tanh": sp.tanh,

            "log": sp.log,
            "log10": sp.log,

            "log2": lambda x:
                sp.log(x, 2),

            "Abs": sp.Abs,

            "floor": sp.floor,
            "ceiling": sp.ceiling,

            "real_root": sp.real_root,
        }


        # DEGREE MODE

        if st.session_state.angle_mode == "DEG":

            allowed["sin"] = lambda x: (
                sp.sin(
                    sp.pi * x / 180
                )
            )

            allowed["cos"] = lambda x: (
                sp.cos(
                    sp.pi * x / 180
                )
            )

            allowed["tan"] = lambda x: (
                sp.tan(
                    sp.pi * x / 180
                )
            )

            allowed["asin"] = lambda x: (
                sp.asin(x)
                * 180
                / sp.pi
            )

            allowed["acos"] = lambda x: (
                sp.acos(x)
                * 180
                / sp.pi
            )

            allowed["atan"] = lambda x: (
                sp.atan(x)
                * 180
                / sp.pi
            )


        # SYMPIFY

        result = sp.sympify(
            expr,
            locals=allowed
        )

        result = sp.N(result)


        # INVALID RESULTS

        if result.has(
            sp.zoo,
            sp.oo,
            -sp.oo,
            sp.nan
        ):

            raise ValueError(
                "Invalid mathematical result"
            )


        numeric_result = float(result)


        if not math.isfinite(numeric_result):

            raise ValueError(
                "Invalid mathematical result"
            )


        # CLEAN RESULT

        if numeric_result.is_integer():

            return str(
                int(numeric_result)
            )

        return f"{numeric_result:.12g}"


    except ZeroDivisionError:

        raise ValueError(
            "Cannot divide by zero"
        )


    except ValueError as error:

        raise error


    except Exception:

        raise ValueError(
            "Invalid expression"
        )


# ============================================================
# ADD TEXT
# ============================================================

def add_text(text):

    st.session_state.expression += text

    st.session_state.error = ""


# ============================================================
# CLEAR
# ============================================================

def clear_all():

    st.session_state.expression = ""

    st.session_state.result = "0"

    st.session_state.error = ""


# ============================================================
# DELETE
# ============================================================

def delete_last():

    st.session_state.expression = (
        st.session_state.expression[:-1]
    )

    st.session_state.error = ""


# ============================================================
# CALCULATE
# ============================================================

def calculate():

    expression = st.session_state.expression

    if not expression:
        return

    try:

        result = calculate_expression(
            expression
        )

        st.session_state.result = result

        try:

            st.session_state.ans = float(
                result
            )

        except Exception:

            st.session_state.ans = 0


        st.session_state.history.insert(
            0,
            {
                "expression": expression,
                "result": result
            }
        )

        st.session_state.history = (
            st.session_state.history[:20]
        )

        st.session_state.error = ""


    except ValueError as error:

        st.session_state.error = str(error)

        st.session_state.result = "Error"


# ============================================================
# SCIENTIFIC FUNCTIONS
# ============================================================

def add_function(function):

    if st.session_state.inverse:

        inverse_functions = {

            "sin": "asin",
            "cos": "acos",
            "tan": "atan"
        }

        function = inverse_functions.get(
            function,
            function
        )


    if function == "sqrt":

        add_text("sqrt(")


    elif function == "ln":

        add_text("log(")


    elif function == "log":

        add_text("log10(")


    elif function == "log2":

        add_text("log2(")


    elif function in [

        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sinh",
        "cosh",
        "tanh"

    ]:

        add_text(
            f"{function}("
        )


    elif function == "abs":

        add_text("Abs(")


    elif function == "square":

        if st.session_state.expression:

            st.session_state.expression += "^2"


    elif function == "cube":

        if st.session_state.expression:

            st.session_state.expression += "^3"


    elif function == "reciprocal":

        if st.session_state.expression:

            st.session_state.expression = (
                f"1/({st.session_state.expression})"
            )


    elif function == "cuberoot":

        add_text("real_root(")


    elif function == "floor":

        add_text("floor(")


    elif function == "ceil":

        add_text("ceiling(")


    elif function == "factorial":

        if st.session_state.expression:

            st.session_state.expression += "!"


    elif function == "exp":

        add_text("E")


    st.session_state.error = ""


# ============================================================
# START CALCULATOR
# ============================================================

st.markdown(
    "<div class='calculator'>",
    unsafe_allow_html=True
)


# ============================================================
# DISPLAY
# ============================================================

st.markdown(
    "<div class='display-box'>",
    unsafe_allow_html=True
)


top_col1, top_col2 = st.columns(
    [1, 5],
    gap="small"
)


with top_col1:

    if st.button(
        "↶",
        key="history_toggle"
    ):

        st.session_state.show_history = (
            not st.session_state.show_history
        )

        st.rerun()


with top_col2:

    st.markdown(
        f"""
        <div style="
            text-align:right;
            color:#777;
            font-size:12px;
            padding-top:4px;
        ">
            {st.session_state.angle_mode}
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown(
    f"""
    <div class="display-expression">
        {st.session_state.expression or ""}
    </div>

    <div class="display-result">
        {st.session_state.error or st.session_state.result}
    </div>
    """,
    unsafe_allow_html=True
)


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# HISTORY
# ============================================================

if st.session_state.show_history:

    with st.expander(
        "🕘 Calculation History",
        expanded=True
    ):

        if st.session_state.history:

            if st.button(
                "Clear History",
                key="clear_history"
            ):

                st.session_state.history = []

                st.rerun()


            for index, item in enumerate(
                st.session_state.history
            ):

                st.write(
                    f"**{item['expression']}** = "
                    f"**{item['result']}**"
                )

                if st.button(
                    "Use",
                    key=f"use_history_{index}"
                ):

                    st.session_state.expression = (
                        item["result"]
                    )

                    st.session_state.result = (
                        item["result"]
                    )

                    st.rerun()

        else:

            st.info(
                "No calculations yet."
            )


# ============================================================
# DEG / RAD + MEMORY
# ============================================================

st.markdown(
    '<div class="mode-row">',
    unsafe_allow_html=True
)

mode_col, inv_col, mc_col, mr_col, mp_col, mm_col = (
    st.columns(
        6,
        gap="small"
    )
)


with mode_col:

    if st.button(
        st.session_state.angle_mode,
        key="angle_mode_button"
    ):

        if st.session_state.angle_mode == "DEG":

            st.session_state.angle_mode = "RAD"

        else:

            st.session_state.angle_mode = "DEG"

        st.rerun()


with inv_col:

    inv_label = (
        "INV"
        if not st.session_state.inverse
        else "INV ✓"
    )

    if st.button(
        inv_label,
        key="inverse_button"
    ):

        st.session_state.inverse = (
            not st.session_state.inverse
        )

        st.rerun()


with mc_col:

    if st.button(
        "MC",
        key="memory_clear_button"
    ):

        st.session_state.memory = 0


with mr_col:

    if st.button(
        "MR",
        key="memory_recall_button"
    ):

        add_text(
            str(
                st.session_state.memory
            )
        )

        st.rerun()


with mp_col:

    if st.button(
        "M+",
        key="memory_add_button"
    ):

        try:

            value = calculate_expression(
                st.session_state.expression
            )

            st.session_state.memory += (
                float(value)
            )

        except Exception:

            pass


with mm_col:

    if st.button(
        "M-",
        key="memory_subtract_button"
    ):

        try:

            value = calculate_expression(
                st.session_state.expression
            )

            st.session_state.memory -= (
                float(value)
            )

        except Exception:

            pass


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# FUNCTION TO CREATE ONE REAL ROW
# ============================================================

def create_button_row(row_number, buttons):

    """
    Creates ONE separate Streamlit row.

    Every row has exactly 7 columns.
    """

    columns = st.columns(
        7,
        gap="small"
    )


    for column_index, (label, action) in enumerate(
        buttons
    ):

        with columns[column_index]:

            key = (
                f"calc_{row_number}_{column_index}"
            )


            # AC

            if action == "AC":

                if st.button(
                    label,
                    key=key
                ):

                    clear_all()

                    st.rerun()


            # DELETE

            elif action == "DEL":

                if st.button(
                    label,
                    key=key
                ):

                    delete_last()

                    st.rerun()


            # EQUALS

            elif action == "=":

                if st.button(
                    label,
                    key=key
                ):

                    calculate()

                    st.rerun()


            # ANSWER

            elif action == "Ans":

                if st.button(
                    label,
                    key=key
                ):

                    add_text("Ans")

                    st.rerun()


            # SCIENTIFIC FUNCTIONS

            elif action in [

                "sin",
                "cos",
                "tan",
                "sqrt",
                "ln",
                "log",
                "factorial",
                "exp"

            ]:

                if st.button(
                    label,
                    key=key
                ):

                    add_function(action)

                    st.rerun()


            # NORMAL BUTTON

            else:

                if st.button(
                    label,
                    key=key
                ):

                    add_text(action)

                    st.rerun()


# ============================================================
# MAIN SCIENTIFIC CALCULATOR
# ============================================================


# ------------------------------------------------------------
# ROW 1
# ------------------------------------------------------------

create_button_row(
    1,
    [
        ("x!", "factorial"),
        ("(", "("),
        (")", ")"),
        ("%", "%"),
        ("AC", "AC"),
        ("⌫", "DEL"),
        ("÷", "÷"),
    ]
)


# ------------------------------------------------------------
# ROW 2
# ------------------------------------------------------------

create_button_row(
    2,
    [
        ("sin", "sin"),
        ("ln", "ln"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("×", "×"),
        ("√", "sqrt"),
    ]
)


# ------------------------------------------------------------
# ROW 3
# ------------------------------------------------------------

create_button_row(
    3,
    [
        ("cos", "cos"),
        ("log", "log"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("−", "-"),
        ("π", "π"),
    ]
)


# ------------------------------------------------------------
# ROW 4
# ------------------------------------------------------------

create_button_row(
    4,
    [
        ("tan", "tan"),
        ("e", "e"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("+", "+"),
        ("Ans", "Ans"),
    ]
)


# ------------------------------------------------------------
# ROW 5
# ------------------------------------------------------------

create_button_row(
    5,
    [
        ("EXP", "exp"),
        ("xʸ", "^"),
        ("0", "0"),
        (".", "."),
        ("=", "="),
        ("(", "("),
        (")", ")"),
    ]
)


# ============================================================
# MORE SCIENTIFIC FUNCTIONS
# ============================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)

st.markdown(
    '<div class="more-box">',
    unsafe_allow_html=True
)

with st.expander(
    "⚙️ More Scientific Functions"
):

    more_buttons = [

        ("asin", "asin"),
        ("acos", "acos"),
        ("atan", "atan"),
        ("sinh", "sinh"),

        ("cosh", "cosh"),
        ("tanh", "tanh"),
        ("log₂", "log2"),
        ("1/x", "reciprocal"),

        ("x²", "square"),
        ("x³", "cube"),
        ("∛x", "cuberoot"),
        ("|x|", "abs"),

        ("floor", "floor"),
        ("ceil", "ceil"),
    ]


    more_columns = st.columns(
        4,
        gap="small"
    )


    for index, (label, action) in enumerate(
        more_buttons
    ):

        with more_columns[index % 4]:

            if st.button(
                label,
                key=f"more_{index}"
            ):

                add_function(action)

                st.rerun()


st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# INFORMATION
# ============================================================

st.markdown(
    "<hr>",
    unsafe_allow_html=True
)

st.caption(
    "⌨️ Keyboard: numbers, +, -, *, /, "
    "parentheses, Enter = calculate, "
    "Backspace = delete, Esc = clear"
)

st.caption(
    "🧮 Scientific Calculator • "
    "Python + Streamlit + SymPy"
)


# ============================================================
# CLOSE CALCULATOR
# ============================================================

st.markdown(
    "</div>",
    unsafe_allow_html=True
)