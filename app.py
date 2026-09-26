import streamlit as st
import sympy as sp
import math
import re


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Scientific Calculator",
    page_icon="🧮",
    layout="centered"
)


# ============================================================
# CSS
# IMPORTANT:
# NO GRID/FLEX LAYOUT CHANGES
# ============================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}


/* Main page */

.block-container {
    max-width: 760px !important;
    padding-top: 8px !important;
    padding-bottom: 15px !important;
    padding-left: 5px !important;
    padding-right: 5px !important;

    overflow-x: hidden !important;
}


/* Prevent horizontal scrolling */

html,
body,
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    overflow-x: hidden !important;
}


/* Streamlit columns */

[data-testid="column"] {
    padding-left: 2px !important;
    padding-right: 2px !important;
    min-width: 0 !important;
}


/* Buttons */

.stButton {
    width: 100% !important;
    padding: 0 !important;
    margin: 0 !important;
}

.stButton > button {
    width: 100% !important;
    min-width: 0 !important;

    height: 43px !important;
    min-height: 43px !important;

    padding: 0 !important;
    margin: 0 !important;

    border-radius: 21px !important;

    font-size: 12px !important;
    font-weight: 500 !important;

    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;

    box-sizing: border-box !important;
}


/* Display */

.display-box {
    border: 1px solid #d1d5db;
    border-radius: 15px;

    padding: 7px 10px;
    margin-bottom: 6px;

    background: white;

    overflow: hidden;
}

.display-expression {
    text-align: right;

    font-size: 15px;
    line-height: 23px;
    height: 23px;

    color: #6b7280;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.display-result {
    text-align: right;

    font-size: 29px;
    line-height: 38px;
    height: 38px;

    color: #111827;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}


/* Small gap between every native Streamlit row */

div[data-testid="stHorizontalBlock"] {
    margin-bottom: 4px !important;
}


/* Mobile */

@media (max-width: 640px) {

    .block-container {
        padding-left: 2px !important;
        padding-right: 2px !important;
    }

    [data-testid="column"] {
        padding-left: 1px !important;
        padding-right: 1px !important;
    }

    .stButton > button {
        height: 37px !important;
        min-height: 37px !important;

        border-radius: 19px !important;

        font-size: 10px !important;
    }

    .display-box {
        padding: 5px 8px;
        margin-bottom: 5px;
    }

    .display-expression {
        font-size: 13px;
        line-height: 20px;
        height: 20px;
    }

    .display-result {
        font-size: 25px;
        line-height: 34px;
        height: 34px;
    }
}


/* Very small phones */

@media (max-width: 380px) {

    .stButton > button {
        height: 34px !important;
        min-height: 34px !important;

        font-size: 9px !important;
    }

    .display-result {
        font-size: 23px;
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
    "error": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# FACTORIAL
# ============================================================

def factorial_value(value):

    if value < 0:
        raise ValueError("Invalid factorial")

    if not float(value).is_integer():
        raise ValueError("Factorial requires a whole number")

    if value > 170:
        raise ValueError("Number is too large for factorial")

    return math.factorial(int(value))


# ============================================================
# PREPARE EXPRESSION
# ============================================================

def prepare_expression(expression):

    expr = expression

    expr = expr.replace("×", "*")
    expr = expr.replace("÷", "/")
    expr = expr.replace("−", "-")
    expr = expr.replace("^", "**")

    expr = expr.replace("π", "pi")

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
# CALCULATE
# ============================================================

def calculate_expression(expression):

    if not expression.strip():
        return "0"

    try:

        expr = prepare_expression(expression)

        # Factorial
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

        # Allowed functions
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

            "log2": lambda x: sp.log(x, 2),

            "Abs": sp.Abs,

            "floor": sp.floor,
            "ceiling": sp.ceiling,

            "real_root": sp.real_root
        }

        # DEG mode
        if st.session_state.angle_mode == "DEG":

            allowed["sin"] = lambda x: sp.sin(
                sp.pi * x / 180
            )

            allowed["cos"] = lambda x: sp.cos(
                sp.pi * x / 180
            )

            allowed["tan"] = lambda x: sp.tan(
                sp.pi * x / 180
            )

            allowed["asin"] = lambda x: (
                sp.asin(x) * 180 / sp.pi
            )

            allowed["acos"] = lambda x: (
                sp.acos(x) * 180 / sp.pi
            )

            allowed["atan"] = lambda x: (
                sp.atan(x) * 180 / sp.pi
            )

        # Evaluate
        result = sp.sympify(
            expr,
            locals=allowed
        )

        result = sp.N(result)

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

        if numeric_result.is_integer():
            return str(int(numeric_result))

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
# BASIC ACTIONS
# ============================================================

def add_text(text):

    st.session_state.expression += text
    st.session_state.error = ""


def clear_all():

    st.session_state.expression = ""
    st.session_state.result = "0"
    st.session_state.error = ""


def delete_last():

    st.session_state.expression = (
        st.session_state.expression[:-1]
    )

    st.session_state.error = ""


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
            st.session_state.ans = float(result)
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
# DISPLAY
# NO HTML WRAPPER AROUND STREAMLIT WIDGETS
# ============================================================

display_col1, display_col2 = st.columns(
    [1, 8],
    gap="small"
)

with display_col1:

    if st.button(
        "↶",
        key="history_toggle"
    ):

        st.session_state.show_history = (
            not st.session_state.show_history
        )

        st.rerun()


with display_col2:

    st.markdown(
        f"""
        <div class="display-box">
            <div class="display-expression">
                {st.session_state.expression or ""}
            </div>

            <div class="display-result">
                {st.session_state.error or st.session_state.result}
            </div>
        </div>
        """,
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
# DEG / INV / MEMORY
# EXACTLY 6 COLUMNS
# ============================================================

mode_columns = st.columns(
    6,
    gap="small"
)


# DEG / RAD
with mode_columns[0]:

    if st.button(
        st.session_state.angle_mode,
        key="angle_mode_btn"
    ):

        if st.session_state.angle_mode == "DEG":
            st.session_state.angle_mode = "RAD"
        else:
            st.session_state.angle_mode = "DEG"

        st.rerun()


# INV
with mode_columns[1]:

    inv_text = (
        "INV ✓"
        if st.session_state.inverse
        else "INV"
    )

    if st.button(
        inv_text,
        key="inverse_btn"
    ):

        st.session_state.inverse = (
            not st.session_state.inverse
        )

        st.rerun()


# MC
with mode_columns[2]:

    if st.button(
        "MC",
        key="MC"
    ):

        st.session_state.memory = 0


# MR
with mode_columns[3]:

    if st.button(
        "MR",
        key="MR"
    ):

        add_text(
            str(st.session_state.memory)
        )

        st.rerun()


# M+
with mode_columns[4]:

    if st.button(
        "M+",
        key="Mplus"
    ):

        try:

            value = calculate_expression(
                st.session_state.expression
            )

            st.session_state.memory += float(value)

        except Exception:
            pass


# M-
with mode_columns[5]:

    if st.button(
        "M-",
        key="Mminus"
    ):

        try:

            value = calculate_expression(
                st.session_state.expression
            )

            st.session_state.memory -= float(value)

        except Exception:
            pass


# ============================================================
# FUNCTION TO CREATE 7-BUTTON ROW
# ============================================================

def button_row(row_number, buttons):

    # THIS IS A REAL STREAMLIT ROW
    columns = st.columns(
        7,
        gap="small"
    )

    for index, (label, action) in enumerate(buttons):

        with columns[index]:

            key = f"row_{row_number}_button_{index}"

            # AC
            if action == "AC":

                if st.button(
                    label,
                    key=key
                ):

                    clear_all()
                    st.rerun()

            # BACKSPACE
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

            # SCIENTIFIC FUNCTIONS
            elif action in [
                "factorial",
                "sin",
                "cos",
                "tan",
                "sqrt",
                "ln",
                "log",
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
# ROW 1
# ============================================================

button_row(
    1,
    [
        ("x!", "factorial"),
        ("(", "("),
        (")", ")"),
        ("%", "%"),
        ("AC", "AC"),
        ("⌫", "DEL"),
        ("÷", "÷")
    ]
)


# ============================================================
# ROW 2
# ============================================================

button_row(
    2,
    [
        ("sin", "sin"),
        ("ln", "ln"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("×", "×"),
        ("√", "sqrt")
    ]
)


# ============================================================
# ROW 3
# ============================================================

button_row(
    3,
    [
        ("cos", "cos"),
        ("log", "log"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("−", "−"),
        ("π", "π")
    ]
)


# ============================================================
# ROW 4
# ============================================================

button_row(
    4,
    [
        ("tan", "tan"),
        ("e", "e"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("+", "+"),
        ("Ans", "Ans")
    ]
)


# ============================================================
# ROW 5
# ============================================================

button_row(
    5,
    [
        ("EXP", "exp"),
        ("xʸ", "^"),
        ("0", "0"),
        (".", "."),
        ("=", "="),
        ("(", "("),
        (")", ")")
    ]
)


# ============================================================
# MORE FUNCTIONS
# 4 COLUMNS
# ============================================================

st.divider()

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
        ("ceil", "ceil")
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


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "⌨️ Keyboard: numbers, +, -, *, /, "
    "parentheses, Enter = calculate, "
    "Backspace = delete"
)

st.caption(
    "🧮 Scientific Calculator • "
    "Python + Streamlit + SymPy"
)
