import os
from typing import List, Dict, Optional

ZEP_API_KEY = os.environ.get("ZEP_API_KEY", "")


def create_graphrag_service(api_key: Optional[str] = None) -> "GraphRAGService":
    return GraphRAGService(api_key)


class GraphRAGService:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or ZEP_API_KEY
        self.client = None
        self._initialized = False

        if self.api_key:
            try:
                from zep_cloud.client import Zep

                self.client = Zep(api_key=self.api_key)
                self._initialized = True
            except ImportError:
                print("Zep Cloud no instalado. Use: pip install zep-cloud")
            except Exception as e:
                print(f"Error inicializando Zep: {e}")

    def is_available(self) -> bool:
        return self.client is not None and self._initialized

    def add_incident_context(self, user_id: str, incident_data: Dict) -> bool:
        if not self.is_available():
            return False

        try:
            incident_text = f"""
            Tipo: {incident_data.get("tipo", "N/A")}
            Descripcion: {incident_data.get("descripcion", "N/A")}
            Ubicacion: {incident_data.get("ubicacion", "N/A")}
            Barrio: {incident_data.get("barrio", "N/A")}
            Gravedad: {incident_data.get("gravedad", "N/A")}
            Fecha: {incident_data.get("fecha", "N/A")}
            Ciudad: Medellin
            """.strip()

            self.client.document.add(
                collection_name="incidentes_medellin",
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
            print(f"Error agregando incidente: {e}")
            return False

    def create_incident_graph(self, user_id: str, incident_data: Dict) -> bool:
        if not self.is_available():
            return False

        try:
            incident_text = f"""
            INCIDENTE
            Tipo: {incident_data.get("tipo", "N/A")}
            Barrio: {incident_data.get("barrio", "N/A")}
            Ubicacion: {incident_data.get("ubicacion", "N/A")}
            Gravedad: {incident_data.get("gravedad", "N/A")}
            Descripcion: {incident_data.get("descripcion", "N/A")}
            """.strip()

            self.client.document.add(
                collection_name="incidentes_medellin_graph",
                documents=[
                    {
                        "document_id": str(incident_data.get("id", "")),
                        "content": incident_text,
                        "metadata": {
                            "user_id": user_id,
                            "tipo": str(incident_data.get("tipo", "")),
                            "gravedad": str(incident_data.get("gravedad", "")),
                            "barrio": str(incident_data.get("barrio", "")),
                            "ubicacion": str(incident_data.get("ubicacion", "")),
                            "ciudad": "Medellin",
                        },
                    }
                ],
            )
            return True
        except Exception as e:
            print(f"Error creando grafo: {e}")
            return False

    def search_incidents(self, query: str, limit: int = 10) -> List[Dict]:
        if not self.is_available():
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
            print(f"Error buscando: {e}")
            return []

    def build_incident_graph(self, user_id: str) -> Dict:
        if not self.is_available():
            return {"nodes": [], "edges": [], "clusters": {}}

        try:
            results = self.client.search.search(
                query=f"user_id:{user_id}",
                collection_name="incidentes_medellin_graph",
                limit=50,
            )

            nodes = []
            edges = []
            barrio_clusters = {}
            tipo_clusters = {}

            for i, r in enumerate(results):
                metadata = r.metadata or {}
                node_id = f"node_{i}"

                nodes.append(
                    {
                        "id": node_id,
                        "tipo": metadata.get("tipo", "unknown"),
                        "barrio": metadata.get("barrio", "unknown"),
                        "gravedad": metadata.get("gravedad", "baja"),
                        "score": r.score,
                        "content": r.content[:100] if r.content else "",
                    }
                )

                barrio = metadata.get("barrio", "unknown")
                if barrio not in barrio_clusters:
                    barrio_clusters[barrio] = []
                barrio_clusters[barrio].append(node_id)

                tipo = metadata.get("tipo", "unknown")
                if tipo not in tipo_clusters:
                    tipo_clusters[tipo] = []
                tipo_clusters[tipo].append(node_id)

            for i in range(len(nodes)):
                for j in range(i + 1, len(nodes)):
                    if nodes[i]["barrio"] == nodes[j]["barrio"]:
                        edges.append(
                            {
                                "source": nodes[i]["id"],
                                "target": nodes[j]["id"],
                                "type": "mismo_barrio",
                            }
                        )
                    if nodes[i]["tipo"] == nodes[j]["tipo"]:
                        edges.append(
                            {
                                "source": nodes[i]["id"],
                                "target": nodes[j]["id"],
                                "type": "mismo_tipo",
                            }
                        )

            return {
                "nodes": nodes,
                "edges": edges,
                "clusters": {"por_barrio": barrio_clusters, "por_tipo": tipo_clusters},
            }
        except Exception as e:
            print(f"Error construyendo grafo: {e}")
            return {"nodes": [], "edges": [], "clusters": {}}

    def get_hotspots(self, top_n: int = 10) -> List[Dict]:
        if not self.is_available():
            return []

        try:
            results = self.client.search.search(
                query="gravedad:alta OR gravedad:critica",
                collection_name="incidentes_medellin_graph",
                limit=100,
            )

            barrio_counts = {}
            for r in results:
                barrio = (
                    r.metadata.get("barrio", "unknown") if r.metadata else "unknown"
                )
                if barrio not in barrio_counts:
                    barrio_counts[barrio] = {"count": 0, "incidents": []}
                barrio_counts[barrio]["count"] += 1
                if r.metadata:
                    barrio_counts[barrio]["incidents"].append(
                        {
                            "tipo": r.metadata.get("tipo", ""),
                            "gravedad": r.metadata.get("gravedad", ""),
                        }
                    )

            hotspots = sorted(
                [{"barrio": b, **data} for b, data in barrio_counts.items()],
                key=lambda x: x["count"],
                reverse=True,
            )[:top_n]

            return hotspots
        except Exception as e:
            print(f"Error obteniendo hotspots: {e}")
            return []

    def get_user_incident_history(self, user_id: str) -> List[Dict]:
        if not self.is_available():
            return []
        return self.search_incidents(query=f"user_id:{user_id}", limit=50)

    def analyze_incident_patterns(self, user_id: str) -> Dict:
        if not self.is_available():
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
            most_common = max(tipos, key=lambda k: tipos[k])
            recommendations.append(f"Tu tipo de incidente mas frecuente: {most_common}")

        if barrios:
            most_affected = max(barrios, key=lambda k: barrios[k])
            recommendations.append(f"Tu zona mas afectada: {most_affected}")

        return {
            "incident_types": tipos,
            "affected_areas": barrios,
            "recommendations": recommendations,
            "total_incidents": len(history),
        }
