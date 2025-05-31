import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    from taller_utils.helpers import calculate_age
    from taller_utils.visuals import plot_distribution
    from taller_utils.analysis import explorar_relacion_con_target

    df = pd.read_csv("data/processed/encuesta_codificada.csv")
    df.head
    # Definir columna target
    target_col = "¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    return calculate_age, df, explorar_relacion_con_target


@app.cell
def _(calculate_age, df):
    df["edad"] = df["Fecha de nacimiento"].apply(calculate_age)
    df["edad"].describe()

    return


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="¿Cuántas horas te dedicarías en una semana a estudiar para una asignatura si no tuvieras una evaluación pronto?",
        target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    )
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="¿Cuánto tiempo dedicas en una semana a estudiar para una asignatura en la que pronto tendrás una evaluación?",
        target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    )
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="Si sientes que estás preparad(a/o) para una evaluación ¿Dedicarías horas a estudiar de todas formas?",
        target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    )
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="Cuando estudias algo relacionado con Matemática...¿Cuántos ejercicios resuelves en una sesión de estudio?",
        target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    )
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="¿Sientes que tienes tiempo suficiente para estudiar?",
        target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    )
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="¿Cuántas horas dedicas diariamente a dormir?",
        target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?"
    )
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(
        df,
        pregunta="¿Cuántas horas dedicas diariamente a dormir?",
        target="¿Cuál o cuáles de los siguientes métodos utilizas para estudiar?"
    )
    return


if __name__ == "__main__":
    app.run()
