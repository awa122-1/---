from backend.live2d.parameters import EMOTION_PARAMETERS

class Live2DController:
    def expression_event(self, emotion):
        return {"emotion": emotion,
                "parameters": EMOTION_PARAMETERS.get(
                    emotion, EMOTION_PARAMETERS["neutral"])}
