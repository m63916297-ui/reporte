import os
from typing import List, Dict, Optional
from datetime import datetime
import random

ZEP_API_KEY = os.environ.get("ZEP_API_KEY", "")


class PredictionAgent:
    def __init__(self, name: str, specialty: str):
        self.name = name
        self.specialty = specialty
        self.model_version = "1.0"

    def predict(self, incident_history: List[Dict]) -> Dict:
        raise NotImplementedError

    def analyze(self, context: Dict) -> Dict:
        raise NotImplementedError


class HotspotPredictionAgent(PredictionAgent):
    def __init__(self):
        super().__init__("HotspotAgent", "Prediccion de zonas calientes")

    def predict(self, incident_history: List[Dict]) -> Dict:
        if not incident_history:
            return {"predictions": [], "confidence": 0.0, "method": "insufficient_data"}

        barrio_counts: Dict[str, int] = {}
        tipo_by_barrio: Dict[str, Dict[str, int]] = {}

        for inc in incident_history:
            barrio = inc.get("barrio", "unknown")
            tipo = inc.get("tipo", "unknown")

            barrio_counts[barrio] = barrio_counts.get(barrio, 0) + 1

            if barrio not in tipo_by_barrio:
                tipo_by_barrio[barrio] = {}
            tipo_by_barrio[barrio][tipo] = tipo_by_barrio[barrio].get(tipo, 0) + 1

        hotspots = sorted(barrio_counts.items(), key=lambda item: item[1], reverse=True)

        predictions = []
        for barrio, count in hotspots[:5]:
            tipos = tipo_by_barrio.get(barrio, {})
            most_common_tipo = (
                max(tipos.keys(), key=lambda k: tipos[k]) if tipos else "desconocido"
            )

            risk_score = min(count / 10.0, 1.0)

            predictions.append(
                {
                    "barrio": barrio,
                    "predicted_incidents": count + random.randint(1, 3),
                    "likely_type": most_common_tipo,
                    "risk_level": self._get_risk_level(risk_score),
                    "risk_score": round(risk_score * 100, 1),
                    "historical_count": count,
                }
            )

        return {
            "predictions": predictions,
            "confidence": min(len(incident_history) / 20.0, 1.0) * 100,
            "method": "frequency_analysis",
            "analysis_date": datetime.now().isoformat(),
        }

    def _get_risk_level(self, score: float) -> str:
        if score >= 0.8:
            return "critico"
        elif score >= 0.6:
            return "alto"
        elif score >= 0.4:
            return "medio"
        return "bajo"

    def analyze(self, context: Dict) -> Dict:
        predictions = self.predict(context.get("incidents", []))

        critical_zones = [
            p
            for p in predictions["predictions"]
            if p["risk_level"] in ["critico", "alto"]
        ]

        return {
            "agent": self.name,
            "summary": f"Se identificaron {len(critical_zones)} zonas de alto riesgo",
            "hotspots": predictions["predictions"][:3],
            "recommendations": self._generate_recommendations(critical_zones),
            "next_prediction_window": "24 horas",
        }

    def _generate_recommendations(self, critical_zones: List[Dict]) -> List[str]:
        recommendations = []
        for zone in critical_zones:
            recommendations.append(
                f"Incrementar vigilancia en {zone['barrio']} - tipo predominante: {zone['likely_type']}"
            )
        if not recommendations:
            recommendations.append("Mantener vigilancia regular en todas las zonas")
        return recommendations


class TemporalPatternAgent(PredictionAgent):
    def __init__(self):
        super().__init__("TemporalAgent", "Analisis de patrones temporales")

    def predict(self, incident_history: List[Dict]) -> Dict:
        hour_distribution: Dict[int, int] = {h: 0 for h in range(24)}
        day_distribution: Dict[str, int] = {}

        for inc in incident_history:
            fecha_str = inc.get("fecha", "")
            if fecha_str:
                try:
                    fecha = datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
                    hour_distribution[fecha.hour] += 1
                    day_name = fecha.strftime("%A")
                    day_distribution[day_name] = day_distribution.get(day_name, 0) + 1
                except Exception:
                    pass

        peak_hours = sorted(
            hour_distribution.items(), key=lambda x: x[1], reverse=True
        )[:3]
        peak_days = sorted(day_distribution.items(), key=lambda x: x[1], reverse=True)[
            :2
        ]

        return {
            "peak_hours": [{"hour": h, "count": c} for h, c in peak_hours],
            "peak_days": [{"day": d, "count": c} for d, c in peak_days],
            "confidence": min(len(incident_history) / 15.0, 1.0) * 100,
            "method": "temporal_analysis",
        }

    def analyze(self, context: Dict) -> Dict:
        predictions = self.predict(context.get("incidents", []))

        recommendations = []
        if predictions["peak_hours"]:
            top_hour = predictions["peak_hours"][0]["hour"]
            recommendations.append(
                f"Horario de mayor actividad: {top_hour}:00 - recomendar vigilancia reforzada"
            )

        return {
            "agent": self.name,
            "summary": f"Pico de incidentes esperado entre {predictions['peak_hours'][0]['hour'] if predictions['peak_hours'] else 'N/A'} horas",
            "patterns": predictions,
            "recommendations": recommendations,
        }


class RiskAssessmentAgent(PredictionAgent):
    def __init__(self):
        super().__init__("RiskAgent", "Evaluacion de riesgo")

    def predict(self, incident_history: List[Dict]) -> Dict:
        if not incident_history:
            return {"overall_risk": "bajo", "score": 0, "factors": {}}

        gravedad_weights = {"baja": 1, "media": 2, "alta": 3, "critica": 4}

        total_score = 0
        gravedad_counts: Dict[str, int] = {
            "baja": 0,
            "media": 0,
            "alta": 0,
            "critica": 0,
        }

        for inc in incident_history:
            gravedad = inc.get("gravedad", "baja")
            weight = gravedad_weights.get(gravedad, 1)
            total_score += weight
            if gravedad in gravedad_counts:
                gravedad_counts[gravedad] += 1

        avg_score = total_score / len(incident_history)
        risk_score = min(avg_score / 4.0, 1.0) * 100

        return {
            "overall_risk": self._classify_risk(risk_score),
            "score": round(risk_score, 1),
            "factors": gravedad_counts,
            "incident_count": len(incident_history),
            "method": "weighted_gravity_analysis",
        }

    def _classify_risk(self, score: float) -> str:
        if score >= 75:
            return "critico"
        elif score >= 50:
            return "alto"
        elif score >= 25:
            return "medio"
        return "bajo"

    def analyze(self, context: Dict) -> Dict:
        predictions = self.predict(context.get("incidents", []))

        risk_color = {
            "critico": "#FF6B6B",
            "alto": "#FF8C00",
            "medio": "#FFD700",
            "bajo": "#4CAF50",
        }

        return {
            "agent": self.name,
            "summary": f"Nivel de riesgo actual: {predictions['overall_risk'].upper()}",
            "risk_assessment": predictions,
            "color_code": risk_color.get(predictions["overall_risk"], "#888"),
            "recommendations": self._get_risk_recommendations(predictions),
        }

    def _get_risk_recommendations(self, predictions: Dict) -> List[str]:
        risk = predictions["overall_risk"]
        recommendations = {
            "critico": [
                "ACTIVAR protocolo de emergencia",
                "Notificar a autoridades inmediatamente",
                "Evacuar zonas de riesgo",
            ],
            "alto": [
                "Reforzar vigilancia en zonas afectadas",
                "Incrementar frecuencia de patrullaje",
                "Alertar a residentes del sector",
            ],
            "medio": [
                "Mantener monitoreo constante",
                "Revisar protocolo de respuesta",
                "Preparar recursos de respuesta",
            ],
            "bajo": [
                "Continuar vigilancia normal",
                "Mantenimiento preventivo",
                "Monitoreo regular",
            ],
        }
        return recommendations.get(risk, [])


class CorrelationAgent(PredictionAgent):
    def __init__(self):
        super().__init__("CorrelationAgent", "Correlacion de incidentes")

    def predict(self, incident_history: List[Dict]) -> Dict:
        correlations = []
        barrio_tipos: Dict[str, Dict[str, int]] = {}

        for inc in incident_history:
            barrio = inc.get("barrio", "unknown")
            tipo = inc.get("tipo", "unknown")

            if barrio not in barrio_tipos:
                barrio_tipos[barrio] = {}
            barrio_tipos[barrio][tipo] = barrio_tipos[barrio].get(tipo, 0) + 1

        for barrio, tipos in barrio_tipos.items():
            if len(tipos) > 1:
                correlations.append(
                    {
                        "barrio": barrio,
                        "incident_types": list(tipos.keys()),
                        "type_count": len(tipos),
                        "correlation_strength": self._calculate_correlation(tipos),
                    }
                )

        return {
            "correlations": correlations,
            "total_correlations": len(correlations),
            "method": "multi_type_analysis",
        }

    def _calculate_correlation(self, tipos: Dict[str, int]) -> float:
        total = sum(tipos.values())
        if total < 2:
            return 0.0
        max_count = max(tipos.values())
        return round((max_count / total) * 100, 1)

    def analyze(self, context: Dict) -> Dict:
        predictions = self.predict(context.get("incidents", []))

        return {
            "agent": self.name,
            "summary": f"Se encontraron {predictions['total_correlations']} correlaciones significativas",
            "correlations": predictions["correlations"],
            "recommendations": self._get_correlation_insights(predictions),
        }

    def _get_correlation_insights(self, predictions: Dict) -> List[str]:
        insights = []
        for corr in predictions["correlations"][:3]:
            insights.append(
                f"{corr['barrio']}: {corr['type_count']} tipos de incidentes correlacionados (fuerza: {corr['correlation_strength']}%)"
            )
        return insights


class AgentOrchestrator:
    def __init__(self):
        self.agents: List[PredictionAgent] = [
            HotspotPredictionAgent(),
            TemporalPatternAgent(),
            RiskAssessmentAgent(),
            CorrelationAgent(),
        ]
        self.api_key = ZEP_API_KEY

    def run_full_analysis(
        self, incident_history: List[Dict], user_context: Dict
    ) -> Dict:
        context = {
            "incidents": incident_history,
            "user": user_context,
            "timestamp": datetime.now().isoformat(),
        }

        agent_results: Dict = {}
        for agent in self.agents:
            try:
                agent_results[agent.name] = agent.analyze(context)
            except Exception as e:
                agent_results[agent.name] = {"error": str(e)}

        consolidated = self._consolidate_recommendations(agent_results)

        risk_level = "bajo"
        if "RiskAgent" in agent_results:
            risk_level = (
                agent_results["RiskAgent"]
                .get("risk_assessment", {})
                .get("overall_risk", "bajo")
            )

        confidence = 50.0
        if agent_results:
            total_confidence = sum(
                r.get("risk_assessment", r.get("predictions", {})).get("confidence", 50)
                for r in agent_results.values()
                if isinstance(r, dict)
            )
            confidence = total_confidence / len(agent_results)

        return {
            "analysis_timestamp": datetime.now().isoformat(),
            "agent_count": len(self.agents),
            "results": agent_results,
            "consolidated_recommendations": consolidated,
            "risk_level": risk_level,
            "confidence": confidence,
        }

    def _consolidate_recommendations(self, agent_results: Dict) -> List[Dict]:
        consolidated: List[Dict] = []
        seen: set = set()

        for agent_name, result in agent_results.items():
            recs = result.get("recommendations", [])
            for rec in recs:
                rec_lower = rec.lower()
                if rec_lower not in seen:
                    seen.add(rec_lower)
                    consolidated.append(
                        {
                            "text": rec,
                            "priority": self._get_priority(agent_name),
                            "source": agent_name,
                        }
                    )

        consolidated.sort(key=lambda x: x["priority"], reverse=True)
        return consolidated[:10]

    def _get_priority(self, agent_name: str) -> int:
        priority_map = {
            "RiskAgent": 3,
            "HotspotAgent": 2,
            "TemporalAgent": 1,
            "CorrelationAgent": 1,
        }
        return priority_map.get(agent_name, 1)


def create_agent_orchestrator() -> AgentOrchestrator:
    return AgentOrchestrator()
