"""Genera el corpus SINTÉTICO de reseñas odontológicas para la Actividad 4.

120 reseñas escritas para esta práctica, 40 por polaridad y 4 por tema.
No son datos extraídos de pacientes ni representan resultados clínicos reales.
No requiere bibliotecas externas. Reproducible (seed=42).
"""
from __future__ import annotations
import csv
import random
from collections import Counter
from pathlib import Path

# Cada registro: (tema, texto). Etiquetas POS/NEU/NEG definidas manualmente.
CORPUS = {
    "POS": [
        ("atencion", "Me atendieron con paciencia y me sentí escuchada durante toda la consulta."),
        ("atencion", "El personal fue muy amable y resolvió mis dudas sin apresurarme."),
        ("atencion", "Aunque estaba nervioso, el trato del equipo me hizo sentir tranquilo."),
        ("atencion", "Agradecí que respetaran mis preguntas y me explicaran cada paso con calma."),
        ("tiempos", "La consulta comenzó puntual y aun así tuvieron tiempo para revisarme con cuidado."),
        ("tiempos", "Mi tratamiento terminó dentro del horario estimado, lo cual me facilitó el día."),
        ("tiempos", "Hubo una pequeña espera, pero el proceso fue ágil y la atención valió la pena."),
        ("tiempos", "La revisión fue rápida sin sentirse apresurada; salí muy satisfecho."),
        ("resultados", "Me gustó el aspecto natural de las restauraciones y cómo se integraron a mi sonrisa."),
        ("resultados", "Estoy contenta con el cambio en mis dientes; se ven como esperaba."),
        ("resultados", "El acabado del tratamiento superó mis expectativas sin verse artificial."),
        ("resultados", "A pesar de mis dudas al inicio, terminé satisfecho con el resultado estético."),
        ("explicaciones", "Me mostraron las opciones de tratamiento de forma clara y pude decidir con confianza."),
        ("explicaciones", "Entendí los cuidados posteriores gracias a las indicaciones sencillas que recibí."),
        ("explicaciones", "Antes de comenzar me explicaron los beneficios y limitaciones del procedimiento."),
        ("explicaciones", "Respondieron incluso mis preguntas más básicas y nunca sentí presión para aceptar."),
        ("costos", "Me entregaron un presupuesto claro y el cobro coincidió con lo acordado."),
        ("costos", "Los precios se explicaron desde el inicio y eso me dio mucha tranquilidad."),
        ("costos", "Aunque invertí más de lo planeado, me pareció justo por la atención recibida."),
        ("costos", "Aprecié que me presentaran alternativas antes de elegir el tratamiento."),
        ("instalaciones", "El consultorio estaba limpio, ordenado y me transmitió confianza."),
        ("instalaciones", "Las instalaciones son cómodas y el equipo se veía bien cuidado."),
        ("instalaciones", "Me gustó que mantuvieran una buena higiene durante toda la visita."),
        ("instalaciones", "El ambiente fue tranquilo y todo estaba organizado para atenderme."),
        ("citas", "Pude elegir un horario conveniente y recibí la confirmación de mi cita sin problemas."),
        ("citas", "Reprogramé mi valoración fácilmente y me ofrecieron varias opciones."),
        ("citas", "La reserva fue sencilla; me enviaron la información necesaria con anticipación."),
        ("citas", "Conseguí cita para la misma semana y el proceso de agenda fue excelente."),
        ("molestias", "Tuve muy pocas molestias y me explicaron qué sensaciones podían ser normales."),
        ("molestias", "Me ayudaron a estar más cómoda durante la limpieza y la experiencia fue buena."),
        ("molestias", "Estaba preocupado por el dolor, pero el procedimiento fue mucho más llevadero de lo esperado."),
        ("molestias", "Cuando necesité una pausa durante la atención, la respetaron de inmediato."),
        ("seguimiento", "Después del procedimiento me dieron seguimiento y respondieron mis preguntas."),
        ("seguimiento", "Recibí indicaciones por escrito y me sentí acompañada en la recuperación."),
        ("seguimiento", "En la revisión posterior escucharon mis comentarios y ajustaron un detalle sin problema."),
        ("seguimiento", "Me recordaron los cuidados de mantenimiento de una manera útil y amable."),
        ("pagos", "Pude pagar con tarjeta y me explicaron las condiciones antes de realizar el cargo."),
        ("pagos", "La recepción me ofreció opciones de pago claras y sin complicaciones."),
        ("pagos", "El comprobante llegó enseguida y el monto fue exactamente el presupuestado."),
        ("pagos", "Me resultó muy cómodo dividir el pago conforme a las condiciones acordadas."),
    ],
    "NEU": [
        ("atencion", "Acudí a una valoración dental y el odontólogo revisó mis dientes."),
        ("atencion", "En recepción registraron mi llegada antes de pasar al consultorio."),
        ("atencion", "La consulta incluyó una entrevista inicial y una exploración bucal."),
        ("atencion", "Durante la visita hablé con el odontólogo y con una persona de recepción."),
        ("tiempos", "Mi cita estaba programada para la mañana y terminó antes del mediodía."),
        ("tiempos", "La limpieza duró aproximadamente cuarenta minutos."),
        ("tiempos", "La revisión y la explicación del plan se realizaron en la misma consulta."),
        ("tiempos", "El procedimiento se dividió en dos citas de diferente duración."),
        ("resultados", "Hoy se colocó una restauración y tengo una revisión programada."),
        ("resultados", "Me tomaron fotografías para comparar el estado de mis dientes en la próxima visita."),
        ("resultados", "Durante la cita se verificó la forma de las piezas restauradas."),
        ("resultados", "El odontólogo revisó el ajuste de la restauración al cerrar la boca."),
        ("explicaciones", "Me entregaron una hoja con las indicaciones para después del tratamiento."),
        ("explicaciones", "La consulta incluyó información sobre limpieza, restauraciones y controles."),
        ("explicaciones", "Recibí una explicación de las etapas previstas para mi tratamiento."),
        ("explicaciones", "Me indicaron qué estudios se requieren antes de iniciar la siguiente fase."),
        ("costos", "Solicité una cotización de tratamiento para valorar distintas opciones."),
        ("costos", "El presupuesto incluye un desglose de los procedimientos propuestos."),
        ("costos", "Me informaron el precio de la revisión y el de una posible restauración."),
        ("costos", "Antes de continuar, pregunté por el costo del mantenimiento semestral."),
        ("instalaciones", "La recepción se encuentra junto al área de espera."),
        ("instalaciones", "En el consultorio hay una unidad dental y equipo para tomar fotografías."),
        ("instalaciones", "Pasé primero a la sala de espera y después al área clínica."),
        ("instalaciones", "Durante el tratamiento utilizaron instrumental y una lámpara de trabajo."),
        ("citas", "Programé una cita para el jueves por la tarde."),
        ("citas", "La próxima revisión quedó anotada para dentro de seis meses."),
        ("citas", "Me enviaron por mensaje la fecha y la hora de la consulta."),
        ("citas", "La cita de control fue agendada al terminar el tratamiento."),
        ("molestias", "Antes del procedimiento me preguntaron si tenía sensibilidad dental."),
        ("molestias", "El odontólogo me preguntó cómo me sentía al terminar la sesión."),
        ("molestias", "Durante la revisión me solicitaron señalar las zonas que sentía sensibles."),
        ("molestias", "En la consulta hablamos sobre los cuidados que debo seguir durante los próximos días."),
        ("seguimiento", "Me dieron una fecha para revisar el estado de la restauración."),
        ("seguimiento", "Recibí un mensaje con las indicaciones para mi próxima visita."),
        ("seguimiento", "La revisión de control incluyó fotografías y preguntas sobre los cuidados."),
        ("seguimiento", "Después del tratamiento me proporcionaron un número para dudas administrativas."),
        ("pagos", "Realicé el pago de la consulta mediante transferencia."),
        ("pagos", "En recepción me explicaron los métodos de pago disponibles."),
        ("pagos", "Solicité la factura y entregué mis datos fiscales."),
        ("pagos", "El comprobante de pago se envió por correo electrónico."),
    ],
    "NEG": [
        ("atencion", "Sentí que mis preguntas incomodaban al personal y no recibí respuestas claras."),
        ("atencion", "La consulta fue apresurada y apenas pude comentar mis preocupaciones."),
        ("atencion", "Aunque el procedimiento terminó, no me gustó la manera en que me trataron."),
        ("atencion", "En recepción respondieron de forma poco amable cuando pedí información."),
        ("tiempos", "Esperé demasiado para pasar y nadie me explicó el motivo del retraso."),
        ("tiempos", "La cita comenzó mucho después de la hora acordada y perdí toda la mañana."),
        ("tiempos", "El procedimiento se prolongó más de lo anunciado sin aviso previo."),
        ("tiempos", "Me hicieron regresar otro día porque la atención se interrumpió antes de terminar."),
        ("resultados", "No me convenció el aspecto de la restauración y sigo esperando una revisión."),
        ("resultados", "El resultado estético no se parece a lo que habíamos conversado."),
        ("resultados", "Quedé inconforme con la forma de mis dientes después del procedimiento."),
        ("resultados", "La restauración se siente incómoda al morder y no han resuelto mi inquietud."),
        ("explicaciones", "No me explicaron bien las opciones y terminé con más dudas que al llegar."),
        ("explicaciones", "Recibí instrucciones contradictorias sobre los cuidados posteriores."),
        ("explicaciones", "Me propusieron un tratamiento sin aclarar sus limitaciones ni otras alternativas."),
        ("explicaciones", "Pregunté por los pasos del procedimiento, pero la respuesta fue confusa."),
        ("costos", "El cobro final fue mayor al presupuesto y no entendí el cambio."),
        ("costos", "Me hablaron de cargos adicionales cuando el tratamiento ya había comenzado."),
        ("costos", "No recibí un desglose de los precios y terminé insatisfecho con la información."),
        ("costos", "La cotización era poco clara y me sentí presionada para decidir de inmediato."),
        ("instalaciones", "La sala de espera estaba descuidada y me resultó incómoda."),
        ("instalaciones", "El ruido y la falta de privacidad hicieron desagradable mi consulta."),
        ("instalaciones", "El área de recepción se veía desordenada y eso me generó desconfianza."),
        ("instalaciones", "No me agradaron las condiciones del espacio donde tuve que esperar."),
        ("citas", "Cancelaron mi cita con muy poca anticipación y no ofrecieron una solución útil."),
        ("citas", "Confirmé mi horario, pero al llegar mi reserva no aparecía en el sistema."),
        ("citas", "Intenté cambiar la cita varias veces y nadie respondió mis mensajes."),
        ("citas", "Me asignaron un horario distinto al que había solicitado y fue difícil corregirlo."),
        ("molestias", "Tuve molestias importantes y sentí que no tomaron en serio mis comentarios."),
        ("molestias", "Pedí una pausa por incomodidad, pero tardaron en atender mi solicitud."),
        ("molestias", "La sesión me resultó más dolorosa de lo previsto y no recibí suficiente orientación."),
        ("molestias", "Salí preocupado por una sensación extraña y no conseguí que me explicaran qué hacer."),
        ("seguimiento", "Escribí por una duda después del tratamiento y pasaron días sin respuesta."),
        ("seguimiento", "Me prometieron una revisión de seguimiento, pero nunca me contactaron."),
        ("seguimiento", "Las indicaciones posteriores fueron insuficientes y tuve que buscar aclaraciones."),
        ("seguimiento", "Aunque la primera consulta fue buena, el seguimiento posterior me decepcionó."),
        ("pagos", "Me aplicaron un cargo que no esperaba y tardaron en darme una explicación."),
        ("pagos", "El proceso de pago fue confuso y no recibí el comprobante solicitado."),
        ("pagos", "La terminal rechazó el cobro, pero no supieron orientarme sobre la operación."),
        ("pagos", "Me ofrecieron una modalidad de pago que al final no estaba disponible."),
    ],
}


def generar(destino: Path) -> None:
    registros = []
    for clase, ejemplos in CORPUS.items():
        for tema, texto in ejemplos:
            registros.append({"texto": texto, "etiqueta": clase, "tema": tema, "origen": "simulado"})
    assert len(registros) == 120, f"Se esperaban 120 reseñas, hay {len(registros)}"
    assert Counter(r["etiqueta"] for r in registros) == {"POS": 40, "NEU": 40, "NEG": 40}
    assert len({r["texto"].strip().casefold() for r in registros}) == 120, "Textos duplicados"
    for tema in {r["tema"] for r in registros}:
        assert Counter(r["etiqueta"] for r in registros if r["tema"] == tema) == {
            "POS": 4, "NEU": 4, "NEG": 4
        }, f"Distribución por tema incorrecta: {tema}"
    random.Random(42).shuffle(registros)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8-sig") as f:
        wr = csv.DictWriter(f, fieldnames=["id", "texto", "etiqueta", "tema", "origen"])
        wr.writeheader()
        for i, r in enumerate(registros, start=1):
            wr.writerow({"id": f"R{i:03}", **r})
    print(f"Dataset guardado: {destino} ({len(registros)} registros)")
    print("Distribución por clase:", dict(Counter(r["etiqueta"] for r in registros)))


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    generar(root / "resenas_dentales_simuladas.csv")
