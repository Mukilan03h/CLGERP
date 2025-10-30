from rest_framework.renderers import JSONRenderer

class StandardizedResponseMiddleware(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {
            'success': True,
            'message': 'Operation completed successfully.',
            'data': data
        }
        return super().render(response_data, accepted_media_type, renderer_context)
