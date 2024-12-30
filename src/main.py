from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from firebase_config import db  # Asegúrate de configurar firebase_config correctamente
from typing import Optional
from datetime import datetime

app = FastAPI()

# Modelo para filtrar por rango de fechas o por título
class ConsultaCortes(BaseModel):
    titulo: Optional[str] = None
    fecha_inicio: Optional[str] = None
    fecha_fin: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "API para consultas a la base de datos de Firebase"}

@app.get("/cortes")
def obtener_todos_los_cortes():
    try:
        cortes_ref = db.collection('cortes')
        cortes = cortes_ref.stream()
        resultado = []

        for corte in cortes:
            resultado.append({**corte.to_dict(), "id": corte.id})

        return {"cortes": resultado}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener los cortes: {e}")

@app.post("/cortes/filtrar")
def filtrar_cortes(consulta: ConsultaCortes):
    try:
        cortes_ref = db.collection('cortes')
        query = cortes_ref

        # Filtrar por título si está presente
        if consulta.titulo:
            query = query.where('titulo', '==', consulta.titulo)

        # Filtrar por rango de fechas si ambos límites están presentes
        if consulta.fecha_inicio and consulta.fecha_fin:
            fecha_inicio = datetime.strptime(consulta.fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(consulta.fecha_fin, '%Y-%m-%d')
            query = query.where('fecha', '>=', fecha_inicio).where('fecha', '<=', fecha_fin)

        cortes = query.stream()
        resultado = []

        for corte in cortes:
            resultado.append({**corte.to_dict(), "id": corte.id})

        if not resultado:
            return {"message": "No se encontraron cortes con los criterios especificados"}

        return {"cortes": resultado}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al filtrar los cortes: {e}")

@app.get("/cortes/{id}")
def obtener_corte_por_id(id: str):
    try:
        corte_ref = db.collection('cortes').document(id)
        corte = corte_ref.get()

        if not corte.exists:
            raise HTTPException(status_code=404, detail="Corte no encontrado")

        return {"id": id, **corte.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener el corte: {e}")
