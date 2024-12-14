import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from openai import OpenAI
import json

ai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def chatbot_response(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data['message']
            messages = [
                {"role": "system", "content": "Vous êtes un assistant IA utile et amical."},
                {"role": "user", "content": user_message},
            ]
            chat_completion = ai_client.chat.completions.create(
                messages=messages,
                model="gpt-4o",
                temperature=0.7,
                max_tokens=150
            )
            bot_response = chat_completion.choices[0].message.content
            return JsonResponse({'message': bot_response})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)