import os
from typing import List, Dict, Optional
from zep_cloud.client import Zep

ZEP_API_KEY = os.environ.get("ZEP_API_KEY", "")


class GraphRAGService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ZEP_API_KEY
        self.client: Optional[Zep] = None
        if self.api_key:
            self.client = Zep(api_key=self.api_key)

    def is_available(self) -> bool:
        return self.client is not None

    def add_incident_context(self, user_id: str, incident_data: Dict) -> bool:
        if not self.client:
            return False

        try:
            collection_name = "incidentes_medellin"
            incident_text = f"""
            Tipo: {incident_data.get("tipo", "N/A")}
            Descripcion: {incident_data.get("descripcion", "N/A")}
            Ubicacion: {incident_data.get("ubicacion", "N/A")}
            Barrio: {incident_data.get("barrio", "N/A")}
            Gravedad: {incident_data.get("gravedad", "N/A")}
            Fecha: {incident_data.get("fecha", "N/A")}
            """.strip()

            self.client.document.add(
                collection_name=collection_name,
                documents=[
                    {
                        "document_id": str(incident_data.get("id", "")),
                        "content": incident_text,
                        "metadata": {
                            "user_id": user_id,
                            "tipo": str(incident_data.get("tipo", "")),
                            "gravedad": str(incident_data.get("gravedad", "")),
                            "barrio": str(incident_data.get("barrio", "")),
                            "ciudad": "Medellin",
                        },
                    }
                ],
            )
            return True
        except Exception as e:
            print(f"Error adding incident to Zep: {e}")
            return False

    def search_incidents(self, query: str, limit: int = 10) -> List[Dict]:
        if not self.client:
            return []

        try:
            results = self.client.search.search(
                query=query, collection_name="incidentes_medellin", limit=limit
            )
            return [
                {"content": r.content, "score": r.score, "metadata": r.metadata or {}}
                for r in results
            ]
        except Exception as e:
            print(f"Error searching in Zep: {e}")
            return []

    def get_user_incident_history(self, user_id: str) -> List[Dict]:
        if not self.client:
            return []

        return self.search_incidents(query=f"user_id:{user_id}", limit=50)

    def analyze_incident_patterns(self, user_id: str) -> Dict:
        if not self.client:
            return {"patterns": [], "recommendations": []}

        history = self.get_user_incident_history(user_id)

        tipos: Dict[str, int] = {}
        barrios: Dict[str, int] = {}

        for item in history:
            metadata = item.get("metadata", {})
            tipo = str(metadata.get("tipo", "unknown"))
            barrio = str(metadata.get("barrio", "unknown"))

            tipos[tipo] = tipos.get(tipo, 0) + 1
            barrios[barrio] = barrios.get(barrio, 0) + 1

        recommendations: List[str] = []
        if tipos:
            most_common_type = max(tipos, key=lambda k: tipos[k])
            recommendations.append(
                f"Basado en tu historial, el tipo de incidente mas frecuente es: {most_common_type}"
            )

        if barrios:
            most_affected = max(barrios, key=lambda k: barrios[k])
            recommendations.append(f"Tu zona mas afectada es: {most_affected}")

        return {
            "incident_types": tipos,
            "affected_areas": barrios,
            "recommendations": recommendations,
            "total_incidents": len(history),
        }


def create_graphrag_service(api_key: Optional[str] = None) -> GraphRAGService:
    return GraphRAGService(api_key)
