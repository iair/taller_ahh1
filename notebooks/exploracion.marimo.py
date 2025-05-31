import marimo

__generated_with = "0.13.15"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    from taller_utils.analysis import explorar_relacion_con_target
    return explorar_relacion_con_target, pd


@app.cell
def _(pd):
    df = pd.read_csv("data/processed/encuesta_codificada.csv")
    return (df,)


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Qué tanto te gusta estudiar?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Cuántas horas te dedicarías en una semana a estudiar para una asignatura si no tuvieras una evaluación pronto?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Cuánto tiempo dedicas en una semana a estudiar para una asignatura en la que pronto tendrás una evaluación?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="Si sientes que estás preparad(a/o) para una evaluación ¿Dedicarías horas a estudiar de todas formas?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="Cuando estudias algo relacionado con Matemática...¿Cuántos ejercicios resuelves en una sesión de estudio?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Cuál o cuáles de los siguientes métodos utilizas para estudiar?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿En qué horario prefieres estudiar?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Qué lugar(es) utilizas para estudiar?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Qué factores consideras que dificultan tus estudios?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Sientes que tienes tiempo suficiente para estudiar?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Cuántas horas dedicas diariamente a dormir?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Cuántas horas dedicas diariamente a descansar?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Estudias sol(a/o) o acompañad(a/o)?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="¿Si no sabes resolver un problema a quién acudes?", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _(df, explorar_relacion_con_target):
    explorar_relacion_con_target(df, pregunta="Por favor describe brevemente por qué estás estudiando esta carrera", target="¿Has tenido la idea de retirarte o cambiarte a otra carrera?")
    return


@app.cell
def _():
    import marimo as mo
    return


if __name__ == "__main__":
    app.run()
