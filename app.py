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

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background: #ffffff;
}

/* Main calculator */
.calculator {
    max-width: 720px;
    margin: auto;
}

/* Display */
.display-box {
    border: 1px solid #d1d5db;
    border-radius: 22px;
    padding: 10px 18px;
    margin-bottom: 8px;
    background: white;
}

.display-expression {
    text-align: right;
    font-size: 20px;
    min-height: 30px;
    color: #4b5563;
    overflow-x: auto;
    white-space: nowrap;
}

.display-result {
    text-align: right;
    font-size: 36px;
    min-height: 45px;
    color: #111827;
    overflow-x: auto;
    white-space: nowrap;
}

/* History button */
.history-icon {
    text-align: left;
    font-size: 22px;
    color: #4b5563;
}

/* Streamlit buttons */
.stButton > button {
    width: 100%;
    height: 48px;
    border-radius: 25px;
    border: none;
    font-size: 15px;
    background-color: #f1f3f4;
    color: #111827;
}

.stButton > button:hover {
    border: none;
    background-color: #e5e7eb;
}

/* Scientific buttons */
.scientific-btn .stButton > button {
    background-color: #e7eefc;
}

/* Equals button */
.equals-btn .stButton > button {
    background-color: #3478f6;
    color: white;
}

/* Operator buttons */
.operator-btn .stButton > button {
    background-color: #e7eefc;
}

/* Mode */
.mode-active .stButton > button {
    background-color: #3478f6;
    color: white;
}

/* History cards */
.history-card {
    padding: 10px 12px;
    border-bottom: 1px solid #eeeeee;
    cursor: pointer;
}

.history-expression {
    color: #6b7280;
    font-size: 13px;
}

.history-result {
    font-size: 18px;
    font-weight: 600;
}

/* More functions */
.more-box {
    margin-top: 10px;
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
    """Calculate factorial safely."""

    if value < 0:
        raise ValueError("Invalid factorial")

    if not float(value).is_integer():
        raise ValueError("Factorial requires a whole number")

    if value > 170:
        raise ValueError("Number is too large for factorial")

    return math.factorial(int(value))


def safe_float(value):
    """Convert result to a clean float."""

    value = float(value)

    if not math.isfinite(value):
        raise ValueError("Invalid mathematical result")

    return value


# ============================================================
# EXPRESSION PREPARATION
# ============================================================

def prepare_expression(expression):
    """
    Convert calculator symbols into SymPy-compatible syntax.
    """

    expr = expression

    # Multiplication symbol
    expr = expr.replace("×", "*")

    # Division symbol
    expr = expr.replace("÷", "/")

    # Power
    expr = expr.replace("^", "**")

    # Constants
    expr = re.sub(r"\bπ\b", "pi", expr)
    expr = re.sub(r"\be\b", "E", expr)

    # Ans
    expr = re.sub(r"\bAns\b", f"({st.session_state.ans})", expr)

    # Percentage
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
    """
    Safely calculate an expression using SymPy.
    """

    if not expression.strip():
        return "0"

    try:

        expr = prepare_expression(expression)

        # Replace factorial symbol
        factorial_pattern = r"(\d+(?:\.\d+)?)!"

        def factorial_replace(match):
            number = float(match.group(1))
            return str(factorial_value(number))

        expr = re.sub(
            factorial_pattern,
            factorial_replace,
            expr
        )

        # Allowed mathematical names
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
    "real_root": sp.real_root,
}
        # Degree mode conversion
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

        result = sp.sympify(
            expr,
            locals=allowed
        )

        result = sp.N(result)

        # Check invalid result
        if result.has(sp.zoo, sp.oo, -sp.oo, sp.nan):
            raise ValueError("Invalid mathematical result")

        result = float(result)

        if not math.isfinite(result):
            raise ValueError("Invalid mathematical result")

        # Remove unnecessary .0
        if result.is_integer():
            return str(int(result))

        return f"{result:.12g}"

    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")

    except ValueError as error:
        raise error

    except Exception:
        raise ValueError("Invalid expression")


# ============================================================
# ADD TO EXPRESSION
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
# DELETE LAST CHARACTER
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

        result = calculate_expression(expression)

        st.session_state.result = result

        try:
            st.session_state.ans = float(result)
        except:
            st.session_state.ans = 0

        # Add history
        st.session_state.history.insert(
            0,
            {
                "expression": expression,
                "result": result
            }
        )

        # Keep last 20 calculations
        st.session_state.history = (
            st.session_state.history[:20]
        )

        st.session_state.error = ""

    except ValueError as error:

        st.session_state.error = str(error)
        st.session_state.result = "Error"


# ============================================================
# SCIENTIFIC FUNCTION
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
        add_text(f"{function}(")

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
# HEADER
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

top_col1, top_col2 = st.columns([1, 5])

with top_col1:

    if st.button(
        "↶",
        key="history_toggle"
    ):
        st.session_state.show_history = (
            not st.session_state.show_history
        )

with top_col2:

    st.markdown(
        f"""
        <div style="text-align:right;color:#777;font-size:13px;">
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
# HISTORY PANEL
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

            st.info("No calculations yet.")


# ============================================================
# DEG / RAD + MEMORY
# ============================================================

mode_col, inv_col, mc_col, mr_col, mp_col, mm_col = st.columns(6)

with mode_col:

    if st.button(
        st.session_state.angle_mode,
        key="angle_mode"
    ):

        if st.session_state.angle_mode == "DEG":
            st.session_state.angle_mode = "RAD"
        else:
            st.session_state.angle_mode = "DEG"

        st.rerun()

with inv_col:

    if st.button(
        "INV" if not st.session_state.inverse
        else "INV✓",
        key="inverse"
    ):

        st.session_state.inverse = (
            not st.session_state.inverse
        )

        st.rerun()

with mc_col:

    if st.button("MC", key="mc"):
        st.session_state.memory = 0

with mr_col:

    if st.button("MR", key="mr"):
        add_text(str(st.session_state.memory))

with mp_col:

    if st.button("M+", key="mplus"):

        try:
            value = calculate_expression(
                st.session_state.expression
            )

            st.session_state.memory += float(value)

        except:
            pass

with mm_col:

    if st.button("M-", key="mminus"):

        try:
            value = calculate_expression(
                st.session_state.expression
            )

            st.session_state.memory -= float(value)

        except:
            pass


# ============================================================
# MAIN CALCULATOR BUTTONS
# ============================================================

buttons = [

    # Row 1
    [
        ("x!", "factorial"),
        ("(", "("),
        (")", ")"),
        ("%", "%"),
        ("AC", "AC"),
        ("⌫", "DEL"),
        ("÷", "÷"),
    ],

    # Row 2
    [
        ("sin", "sin"),
        ("ln", "ln"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("×", "×"),
        ("√", "sqrt"),
    ],

    # Row 3
    [
        ("cos", "cos"),
        ("log", "log"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("−", "-"),
        ("π", "π"),
    ],

    # Row 4
    [
        ("tan", "tan"),
        ("e", "e"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("+", "+"),
        ("Ans", "Ans"),
    ],

    # Row 5
    [
        ("EXP", "exp"),
        ("xʸ", "^"),
        ("0", "0"),
        (".", "."),
        ("=", "="),
        ("(", "("),
        (")", ")"),
    ],
]


for row_index, row in enumerate(buttons):

    columns = st.columns(7)

    for col_index, (label, action) in enumerate(row):

        with columns[col_index]:

            if action == "AC":

                if st.button(
                    label,
                    key=f"button_{row_index}_{col_index}"
                ):
                    clear_all()
                    st.rerun()

            elif action == "DEL":

                if st.button(
                    label,
                    key=f"button_{row_index}_{col_index}"
                ):
                    delete_last()
                    st.rerun()

            elif action == "=":

                if st.button(
                    label,
                    key=f"button_{row_index}_{col_index}"
                ):
                    calculate()
                    st.rerun()

            elif action == "Ans":

                if st.button(
                    label,
                    key=f"button_{row_index}_{col_index}"
                ):
                    add_text("Ans")
                    st.rerun()

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
                    key=f"button_{row_index}_{col_index}"
                ):

                    add_function(action)
                    st.rerun()

            else:

                if st.button(
                    label,
                    key=f"button_{row_index}_{col_index}"
                ):

                    add_text(action)
                    st.rerun()


# ============================================================
# MORE SCIENTIFIC FUNCTIONS
# ============================================================

st.markdown("---")

with st.expander("⚙️ More Scientific Functions"):

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

    more_columns = st.columns(4)

    for index, (label, action) in enumerate(more_buttons):

        with more_columns[index % 4]:

            if st.button(
                label,
                key=f"more_{index}"
            ):

                add_function(action)
                st.rerun()


# ============================================================
# KEYBOARD INFORMATION
# ============================================================

st.markdown("---")

st.caption(
    "⌨️ Keyboard: numbers, +, -, *, /, parentheses, "
    "Enter = calculate, Backspace = delete, Esc = clear"
)

st.caption(
    "🧮 Scientific Calculator • Python + Streamlit + SymPy"
)

st.markdown(
    "</div>",
    unsafe_allow_html=True
)
